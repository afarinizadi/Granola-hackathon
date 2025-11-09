"""
Simple test to verify HeyGen API connectivity and SSL handling.
"""

import os
import sys
import ssl
import requests
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Load environment variables
def load_env():
    env_file = current_dir.parent.parent.parent / ".env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

def test_heygen_connection():
    """Test basic connection to HeyGen API."""
    api_key = os.getenv("HEYGEN_API_KEY")
    if not api_key:
        print("❌ No API key found")
        return False
    
    print(f"🔑 Testing with API key: {api_key[:10]}...")
    
    # Test with requests library (more reliable SSL handling)
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        # Test getting avatars (simpler endpoint)
        print("🔍 Testing HeyGen API connection...")
        response = requests.get(
            "https://api.heygen.com/v2/avatars",
            headers=headers,
            timeout=30,
            verify=True  # Try with SSL verification first
        )
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connection successful!")
            print(f"📊 Available avatars: {len(data.get('data', {}).get('avatars', []))}")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed - check your API key")
            return False
        else:
            print(f"⚠️  API returned status {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.SSLError as e:
        print(f"🔒 SSL Error: {e}")
        print("🔧 Trying with SSL verification disabled...")
        
        try:
            # Fallback: disable SSL verification
            response = requests.get(
                "https://api.heygen.com/v2/avatars",
                headers=headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                print("✅ Connection successful (SSL verification disabled)")
                return True
            else:
                print(f"❌ Still failed: {response.status_code}")
                return False
                
        except Exception as e2:
            print(f"❌ Complete failure: {e2}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_simple_video_request():
    """Test a simple video generation request."""
    api_key = os.getenv("HEYGEN_API_KEY")
    if not api_key:
        return False
    
    print("\n🎬 Testing video generation request...")
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    # Simple test payload
    payload = {
        "video_inputs": [{
            "character": {
                "type": "avatar",
                "avatar_id": "default_avatar",  # Use a basic avatar
                "scale": 1.0
            },
            "voice": {
                "type": "text",
                "input_text": "Hello, this is a test video for the text to video feature.",
                "voice_id": "en_US_female_1"  # Basic voice
            }
        }],
        "title": "Test Video"
    }
    
    try:
        response = requests.post(
            "https://api.heygen.com/v2/video/generate",
            headers=headers,
            json=payload,
            timeout=30,
            verify=False  # Use the working SSL setting from previous test
        )
        
        print(f"📡 Video request status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            video_id = data.get("data", {}).get("video_id")
            print(f"✅ Video generation started!")
            print(f"🎥 Video ID: {video_id}")
            return True
        else:
            print(f"❌ Video request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Video request error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 HeyGen API Connection Test")
    print("=" * 40)
    
    # Test basic connection
    if test_heygen_connection():
        print("\n" + "=" * 40)
        # If connection works, test video generation
        test_simple_video_request()
    
    print("\n✅ Test complete!")