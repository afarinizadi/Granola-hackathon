"""
Codebase Processor
Processes and formats repository data for Claude API analysis
"""
from typing import Dict, List
import json


class CodebaseProcessor:
    """Processes repository data and prepares it for AI analysis"""

    def __init__(self):
        """Initialize the codebase processor"""
        pass

    def format_file_tree(self, tree: Dict, prefix: str = "", is_last: bool = True) -> str:
        """
        Format file tree into a readable string representation

        Args:
            tree: File tree dictionary from GitHub client
            prefix: Prefix for tree structure (for recursion)
            is_last: Whether this is the last item in current level

        Returns:
            Formatted string representation of file tree
        """
        output = []

        # Format directories
        dirs = list(tree.get('dirs', {}).items())
        files = tree.get('files', [])

        all_items = [(d[0], 'dir', d[1]) for d in dirs] + [(f['name'], 'file', f) for f in files]

        for idx, (name, item_type, data) in enumerate(all_items):
            is_last_item = idx == len(all_items) - 1
            connector = "└── " if is_last_item else "├── "

            if item_type == 'dir':
                output.append(f"{prefix}{connector}{name}/")
                extension = "    " if is_last_item else "│   "
                subtree_output = self.format_file_tree(data, prefix + extension, is_last_item)
                if subtree_output:
                    output.append(subtree_output)
            else:
                size_kb = data.get('size', 0) / 1024
                output.append(f"{prefix}{connector}{name} ({size_kb:.1f} KB)")

        return "\n".join(output)

    def extract_dependencies(self, files: List[Dict]) -> Dict[str, List[str]]:
        """
        Extract dependencies from common dependency files

        Args:
            files: List of file dictionaries with content

        Returns:
            Dictionary mapping file types to extracted dependencies
        """
        dependencies = {}

        for file in files:
            filename = file['name']
            content = file.get('content', '')

            if filename == 'package.json':
                dependencies['npm'] = self._extract_npm_deps(content)
            elif filename == 'requirements.txt':
                dependencies['pip'] = self._extract_pip_deps(content)
            elif filename == 'pyproject.toml':
                dependencies['python'] = self._extract_pyproject_deps(content)
            elif filename == 'Cargo.toml':
                dependencies['rust'] = self._extract_cargo_deps(content)
            elif filename == 'go.mod':
                dependencies['go'] = self._extract_go_deps(content)
            elif filename == 'pom.xml':
                dependencies['maven'] = ['See pom.xml for Java dependencies']
            elif filename == 'build.gradle':
                dependencies['gradle'] = ['See build.gradle for Java dependencies']

        return dependencies

    def _extract_npm_deps(self, content: str) -> List[str]:
        """Extract NPM dependencies from package.json"""
        try:
            package_json = json.loads(content)
            deps = []
            if 'dependencies' in package_json:
                deps.extend(list(package_json['dependencies'].keys()))
            if 'devDependencies' in package_json:
                deps.extend([f"{dep} (dev)" for dep in package_json['devDependencies'].keys()])
            return deps
        except json.JSONDecodeError:
            return []

    def _extract_pip_deps(self, content: str) -> List[str]:
        """Extract pip dependencies from requirements.txt"""
        deps = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Remove version specifiers
                dep = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0]
                deps.append(dep.strip())
        return deps

    def _extract_pyproject_deps(self, content: str) -> List[str]:
        """Extract dependencies from pyproject.toml"""
        deps = []
        in_dependencies = False
        for line in content.split('\n'):
            if '[tool.poetry.dependencies]' in line or '[project.dependencies]' in line:
                in_dependencies = True
                continue
            if in_dependencies:
                if line.startswith('['):
                    break
                if '=' in line:
                    dep = line.split('=')[0].strip().strip('"')
                    if dep and dep != 'python':
                        deps.append(dep)
        return deps

    def _extract_cargo_deps(self, content: str) -> List[str]:
        """Extract Rust dependencies from Cargo.toml"""
        deps = []
        in_dependencies = False
        for line in content.split('\n'):
            if '[dependencies]' in line:
                in_dependencies = True
                continue
            if in_dependencies:
                if line.startswith('['):
                    break
                if '=' in line:
                    dep = line.split('=')[0].strip()
                    if dep:
                        deps.append(dep)
        return deps

    def _extract_go_deps(self, content: str) -> List[str]:
        """Extract Go dependencies from go.mod"""
        deps = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('require'):
                continue
            if line and not line.startswith('//') and '/' in line:
                parts = line.split()
                if parts:
                    deps.append(parts[0])
        return deps

    def build_context_summary(self, repo_data: Dict) -> str:
        """
        Build a comprehensive summary of the repository for Claude API

        Args:
            repo_data: Repository data from GitHub client

        Returns:
            Formatted string summary of the codebase
        """
        summary_parts = []

        # Repository metadata
        summary_parts.append("# Repository Information")
        summary_parts.append(f"**Name:** {repo_data.get('full_name', 'Unknown')}")
        summary_parts.append(f"**Description:** {repo_data.get('description', 'No description')}")
        summary_parts.append(f"**Primary Language:** {repo_data.get('language', 'Unknown')}")
        summary_parts.append(f"**Stars:** {repo_data.get('stars', 0)}")
        summary_parts.append(f"**License:** {repo_data.get('license', 'Not specified')}")

        topics = repo_data.get('topics', [])
        if topics:
            summary_parts.append(f"**Topics:** {', '.join(topics)}")

        summary_parts.append("")

        # File structure
        summary_parts.append("# File Structure")
        file_tree = repo_data.get('file_tree', {})
        if file_tree:
            tree_str = self.format_file_tree(file_tree)
            summary_parts.append("```")
            summary_parts.append(tree_str)
            summary_parts.append("```")
        summary_parts.append("")

        # Dependencies
        files = repo_data.get('files', [])
        dependencies = self.extract_dependencies(files)
        if dependencies:
            summary_parts.append("# Dependencies")
            for dep_type, deps in dependencies.items():
                summary_parts.append(f"## {dep_type.upper()}")
                for dep in deps[:20]:  # Limit to first 20 dependencies
                    summary_parts.append(f"- {dep}")
                if len(deps) > 20:
                    summary_parts.append(f"... and {len(deps) - 20} more")
            summary_parts.append("")

        # Important files content
        summary_parts.append("# Key Files")
        for file in files:
            if file['name'] in ['README.md', 'README.rst', 'README.txt']:
                summary_parts.append(f"## {file['name']}")
                summary_parts.append("```")
                # Limit README content to first 100 lines
                content_lines = file.get('content', '').split('\n')[:100]
                summary_parts.append('\n'.join(content_lines))
                if len(file.get('content', '').split('\n')) > 100:
                    summary_parts.append("\n... (truncated)")
                summary_parts.append("```")
                summary_parts.append("")

        return "\n".join(summary_parts)

    def calculate_codebase_stats(self, repo_data: Dict) -> Dict:
        """
        Calculate statistics about the codebase

        Args:
            repo_data: Repository data from GitHub client

        Returns:
            Dictionary of codebase statistics
        """
        stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size_kb': 0,
        }

        def count_tree(tree):
            file_count = len(tree.get('files', []))
            dir_count = len(tree.get('dirs', {}))
            size = sum(f.get('size', 0) for f in tree.get('files', []))

            for subdir in tree.get('dirs', {}).values():
                sub_counts = count_tree(subdir)
                file_count += sub_counts[0]
                dir_count += sub_counts[1]
                size += sub_counts[2]

            return file_count, dir_count, size

        file_tree = repo_data.get('file_tree', {})
        if file_tree:
            files, dirs, size = count_tree(file_tree)
            stats['total_files'] = files
            stats['total_dirs'] = dirs
            stats['total_size_kb'] = round(size / 1024, 2)

        return stats
