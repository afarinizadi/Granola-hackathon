"""
Tutorial Generator

Converts text summaries into structured video scripts optimized for HeyGen tutorials.
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TutorialType(Enum):
    """Types of tutorials that can be generated"""
    OVERVIEW = "overview"
    DEEP_DIVE = "deep_dive"
    WALKTHROUGH = "walkthrough"
    EXPLANATION = "explanation"
    QUICK_START = "quick_start"


@dataclass
class TutorialSection:
    """A section within a tutorial"""
    title: str
    content: str
    duration_estimate: int  # in seconds
    emphasis_level: int = 1  # 1-3, where 3 is most important


@dataclass
class TutorialScript:
    """Complete tutorial script ready for video generation"""
    title: str
    introduction: str
    sections: List[TutorialSection]
    conclusion: str
    total_duration: int
    metadata: Dict[str, str]


class TutorialGenerator:
    """
    Generates structured tutorial scripts from text summaries.
    Optimized for HeyGen video generation.
    """
    
    # Maximum recommended duration for different tutorial types (in seconds)
    DURATION_LIMITS = {
        TutorialType.OVERVIEW: 180,      # 3 minutes
        TutorialType.DEEP_DIVE: 600,     # 10 minutes
        TutorialType.WALKTHROUGH: 480,   # 8 minutes
        TutorialType.EXPLANATION: 300,   # 5 minutes
        TutorialType.QUICK_START: 120    # 2 minutes
    }
    
    def __init__(self):
        self.speaking_rate = 150  # words per minute (average)
    
    def generate_tutorial(
        self, 
        text_summary: str, 
        tutorial_type: TutorialType = TutorialType.OVERVIEW,
        title: Optional[str] = None,
        target_audience: str = "developers",
        include_code_examples: bool = True
    ) -> TutorialScript:
        """
        Generate a tutorial script from text summary.
        
        Args:
            text_summary: The summarized text from code analysis
            tutorial_type: Type of tutorial to generate
            title: Optional custom title
            target_audience: Target audience for the tutorial
            include_code_examples: Whether to include code examples
            
        Returns:
            Complete tutorial script ready for video generation
        """
        # Clean and prepare the input text
        cleaned_text = self._clean_text(text_summary)
        
        # Generate title if not provided
        if not title:
            title = self._generate_title(cleaned_text, tutorial_type)
        
        # Break down content into sections
        sections = self._create_sections(cleaned_text, tutorial_type, include_code_examples)
        
        # Generate introduction and conclusion
        introduction = self._generate_introduction(title, tutorial_type, target_audience)
        conclusion = self._generate_conclusion(tutorial_type)
        
        # Calculate total duration
        total_duration = self._calculate_duration([introduction] + [s.content for s in sections] + [conclusion])
        
        # Optimize for duration if needed
        if total_duration > self.DURATION_LIMITS[tutorial_type]:
            sections = self._optimize_for_duration(sections, tutorial_type)
            total_duration = self._calculate_duration([introduction] + [s.content for s in sections] + [conclusion])
        
        return TutorialScript(
            title=title,
            introduction=introduction,
            sections=sections,
            conclusion=conclusion,
            total_duration=total_duration,
            metadata={
                "tutorial_type": tutorial_type.value,
                "target_audience": target_audience,
                "word_count": str(len(cleaned_text.split())),
                "sections_count": str(len(sections))
            }
        )
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize input text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove markdown formatting that doesn't translate well to speech
        text = re.sub(r'`([^`]+)`', r'\1', text)  # Remove backticks
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Remove italic
        
        # Fix common abbreviations for speech
        replacements = {
            'API': 'A P I',
            'JSON': 'JSON',
            'HTTP': 'H T T P',
            'URL': 'U R L',
            'HTML': 'H T M L',
            'CSS': 'C S S',
            'JS': 'JavaScript',
            'DB': 'database',
            'CLI': 'command line interface'
        }
        
        for abbrev, full in replacements.items():
            text = re.sub(r'\b' + abbrev + r'\b', full, text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _generate_title(self, text: str, tutorial_type: TutorialType) -> str:
        """Generate an appropriate title based on content and type."""
        # Extract potential project or main concept from text
        words = text.lower().split()
        
        # Look for key technical terms
        key_terms = []
        tech_keywords = [
            'application', 'system', 'service', 'library', 'framework',
            'module', 'component', 'function', 'class', 'method',
            'api', 'database', 'server', 'client', 'interface'
        ]
        
        for keyword in tech_keywords:
            if keyword in words:
                key_terms.append(keyword.title())
        
        # Generate title based on type
        type_prefixes = {
            TutorialType.OVERVIEW: "Understanding",
            TutorialType.DEEP_DIVE: "Deep Dive into",
            TutorialType.WALKTHROUGH: "Walkthrough of",
            TutorialType.EXPLANATION: "How",
            TutorialType.QUICK_START: "Quick Start with"
        }
        
        prefix = type_prefixes.get(tutorial_type, "Introduction to")
        
        if key_terms:
            main_term = key_terms[0]
            return f"{prefix} {main_term}"
        else:
            return f"{prefix} This Codebase"
    
    def _create_sections(
        self, 
        text: str, 
        tutorial_type: TutorialType, 
        include_code_examples: bool
    ) -> List[TutorialSection]:
        """Break down content into logical sections."""
        
        # Split text into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        sections = []
        
        if tutorial_type == TutorialType.OVERVIEW:
            sections = self._create_overview_sections(paragraphs)
        elif tutorial_type == TutorialType.DEEP_DIVE:
            sections = self._create_deep_dive_sections(paragraphs, include_code_examples)
        elif tutorial_type == TutorialType.WALKTHROUGH:
            sections = self._create_walkthrough_sections(paragraphs)
        elif tutorial_type == TutorialType.EXPLANATION:
            sections = self._create_explanation_sections(paragraphs)
        elif tutorial_type == TutorialType.QUICK_START:
            sections = self._create_quick_start_sections(paragraphs)
        
        return sections
    
    def _create_overview_sections(self, paragraphs: List[str]) -> List[TutorialSection]:
        """Create sections for overview tutorial."""
        sections = []
        
        # Group paragraphs into logical sections
        if len(paragraphs) >= 3:
            # Structure
            sections.append(TutorialSection(
                title="Project Structure",
                content=paragraphs[0],
                duration_estimate=30,
                emphasis_level=2
            ))
            
            # Main functionality
            sections.append(TutorialSection(
                title="Key Components",
                content=". ".join(paragraphs[1:-1]),
                duration_estimate=60,
                emphasis_level=3
            ))
            
            # Purpose and usage
            sections.append(TutorialSection(
                title="Purpose and Usage",
                content=paragraphs[-1],
                duration_estimate=30,
                emphasis_level=2
            ))
        else:
            # Single section for short content
            sections.append(TutorialSection(
                title="Overview",
                content=". ".join(paragraphs),
                duration_estimate=60,
                emphasis_level=3
            ))
        
        return sections
    
    def _create_deep_dive_sections(self, paragraphs: List[str], include_code: bool) -> List[TutorialSection]:
        """Create sections for deep dive tutorial."""
        sections = []
        
        for i, paragraph in enumerate(paragraphs):
            title = f"Component {i + 1}" if len(paragraphs) > 3 else ["Architecture", "Implementation", "Details"][i % 3]
            
            sections.append(TutorialSection(
                title=title,
                content=paragraph,
                duration_estimate=90,
                emphasis_level=2 if i % 2 == 0 else 3
            ))
        
        return sections
    
    def _create_walkthrough_sections(self, paragraphs: List[str]) -> List[TutorialSection]:
        """Create sections for walkthrough tutorial."""
        sections = []
        
        for i, paragraph in enumerate(paragraphs):
            sections.append(TutorialSection(
                title=f"Step {i + 1}",
                content=f"Let's examine {paragraph}",
                duration_estimate=60,
                emphasis_level=2
            ))
        
        return sections
    
    def _create_explanation_sections(self, paragraphs: List[str]) -> List[TutorialSection]:
        """Create sections for explanation tutorial."""
        sections = []
        
        sections.append(TutorialSection(
            title="What it does",
            content=paragraphs[0] if paragraphs else "This code performs specific functionality.",
            duration_estimate=45,
            emphasis_level=3
        ))
        
        if len(paragraphs) > 1:
            sections.append(TutorialSection(
                title="How it works",
                content=". ".join(paragraphs[1:]),
                duration_estimate=75,
                emphasis_level=2
            ))
        
        return sections
    
    def _create_quick_start_sections(self, paragraphs: List[str]) -> List[TutorialSection]:
        """Create sections for quick start tutorial."""
        sections = []
        
        sections.append(TutorialSection(
            title="Getting Started",
            content=f"Here's what you need to know: {paragraphs[0] if paragraphs else 'This is a quick overview.'}",
            duration_estimate=60,
            emphasis_level=3
        ))
        
        return sections
    
    def _generate_introduction(self, title: str, tutorial_type: TutorialType, audience: str) -> str:
        """Generate tutorial introduction."""
        intros = {
            TutorialType.OVERVIEW: f"Welcome to this overview of {title.lower()}. In this tutorial, we'll explore the key components and understand how everything works together.",
            TutorialType.DEEP_DIVE: f"In this deep dive, we'll thoroughly examine {title.lower()} and understand its implementation details.",
            TutorialType.WALKTHROUGH: f"Let's walk through {title.lower()} step by step and see how each part contributes to the whole.",
            TutorialType.EXPLANATION: f"Today I'll explain {title.lower()} and help you understand exactly how it works.",
            TutorialType.QUICK_START: f"This is a quick start guide to {title.lower()}. Let's get you up to speed quickly."
        }
        
        return intros.get(tutorial_type, f"Welcome to this tutorial about {title.lower()}.")
    
    def _generate_conclusion(self, tutorial_type: TutorialType) -> str:
        """Generate tutorial conclusion."""
        conclusions = {
            TutorialType.OVERVIEW: "That's our overview! You now have a solid understanding of the main components and how they work together.",
            TutorialType.DEEP_DIVE: "We've covered the implementation details thoroughly. You should now have a deep understanding of how this code works.",
            TutorialType.WALKTHROUGH: "We've walked through each step. You should now be familiar with the entire process.",
            TutorialType.EXPLANATION: "I hope this explanation helped clarify how everything works. The key points should now be clear.",
            TutorialType.QUICK_START: "That's your quick start guide! You're now ready to work with this code."
        }
        
        return conclusions.get(tutorial_type, "Thanks for watching this tutorial!")
    
    def _calculate_duration(self, text_segments: List[str]) -> int:
        """Calculate estimated duration in seconds."""
        total_words = sum(len(segment.split()) for segment in text_segments)
        return int((total_words / self.speaking_rate) * 60)
    
    def _optimize_for_duration(self, sections: List[TutorialSection], tutorial_type: TutorialType) -> List[TutorialSection]:
        """Optimize sections to fit within duration limit."""
        target_duration = self.DURATION_LIMITS[tutorial_type]
        current_duration = sum(section.duration_estimate for section in sections)
        
        if current_duration <= target_duration:
            return sections
        
        # Prioritize sections by emphasis level and reduce content
        sections.sort(key=lambda x: x.emphasis_level, reverse=True)
        
        # Keep most important sections, truncate or remove others
        optimized_sections = []
        remaining_duration = target_duration - 60  # Reserve time for intro/conclusion
        
        for section in sections:
            if remaining_duration >= 30:  # Minimum section duration
                if section.duration_estimate <= remaining_duration:
                    optimized_sections.append(section)
                    remaining_duration -= section.duration_estimate
                else:
                    # Truncate content to fit
                    words = section.content.split()
                    target_words = int(len(words) * (remaining_duration / section.duration_estimate))
                    truncated_content = " ".join(words[:target_words])
                    
                    optimized_sections.append(TutorialSection(
                        title=section.title,
                        content=truncated_content,
                        duration_estimate=remaining_duration,
                        emphasis_level=section.emphasis_level
                    ))
                    break
        
        return optimized_sections
    
    def format_for_heygen(self, script: TutorialScript) -> str:
        """Format the tutorial script for HeyGen video generation."""
        # Combine all sections into a single script
        full_script = []
        
        # Add introduction
        full_script.append(script.introduction)
        
        # Add sections with transitions
        for i, section in enumerate(script.sections):
            if i > 0:
                full_script.append("Now, let's move on to the next part.")
            
            # Add section content with natural speech patterns
            content = section.content
            
            # Add pauses for better speech flow
            content = content.replace('. ', '. ... ')
            content = content.replace('? ', '? ... ')
            content = content.replace('! ', '! ... ')
            
            full_script.append(content)
        
        # Add conclusion
        full_script.append(script.conclusion)
        
        return " ".join(full_script)