import requests
import time
import certifi


# === 1️⃣ CONFIG ===
HEYGEN_API_KEY = "sk_V2_hgu_kfBHVYRDOpI_iyjgSDFNyw4p9GcD63krhShUd8UjGwWj"
AVATAR_ID = "Annie_Office_Sitting_Side_2_public"  
TALKING_PHOTO_ID = "cf504ecbbae14903845795ac099e5e12"
VOICE_ID = "f8c69e517f424cafaecde32dde57096b"  # any valid HeyGen voice


# url = "https://api.heygen.com/v2/avatars"

# headers = {
#     "accept": "application/json",
#     "x-api-key": HEYGEN_API_KEY
# }

# response = requests.get(url, headers=headers, verify=False)

# print(response.text)

# === 2️⃣ CREATE VIDEO ===
def create_video(text, avatar_id):
    url = "https://api.heygen.com/v2/video/generate"

    payload = {
        "caption": False,
        "dimension": {"width": 1280, "height": 720},
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar_id,
                    # "talking_photo_id": TALKING_PHOTO_ID,
                    "scale": 1,
                    "avatar_style": "normal",
                    "talking_style": "stable",
                    "expression": "default",
                    "super_resolution": True,
                    "matting": True,
                },
                "voice": {
                    "type": "text",
                    "voice_id": VOICE_ID,
                    "input_text": text,
                    "speed": 1.0,
                    "pitch": 1.0,
                    "emotion": "Excited",
                    # "locale": "en_US",
                },
                "background": {
                    "type": "color",
                    "value": "#FFFFFF",  # white background
                },
            }
        ],
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": HEYGEN_API_KEY,
    }

    print("🎬 Creating video...")
    response = requests.post(url, json=payload, headers=headers, verify=False)
    print("Status:", response.status_code)
    print("Response:", response.text)

    try:
        data = response.json()
    except Exception:
        print("❌ Could not parse JSON response.")
        return None

    if not data.get("data") or not data["data"].get("video_id"):
        print("❌ Could not find video_id in response:", data)
        return None

    return data["data"]["video_id"]

# === 3️⃣ CHECK STATUS ===
def check_video_status(video_id):
    url = f"https://api.heygen.com/v2/video/status/{video_id}"
    headers = {"x-api-key": HEYGEN_API_KEY}

    while True:
        try:
            resp = requests.get(url, headers=headers, verify=False)
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Request error: {e}")
            time.sleep(10)
            continue

        # Sometimes the API returns no JSON (HTML or empty)
        try:
            data = resp.json()
        except ValueError:
            print(f"⚠️ Non-JSON response (status {resp.status_code}): {resp.text[:200]}")
            time.sleep(10)
            continue

        if not data.get("data"):
            print(f"⚠️ Unexpected response: {data}")
            time.sleep(10)
            continue

        status = data["data"].get("status")

        if status == "completed":
            video_url = data["data"].get("video_url")
            print(f"✅ Video ready: {video_url}")
            break
        elif status == "failed":
            print("❌ Video generation failed:", data)
            break
        else:
            print(f"⏳ Status: {status}... waiting 10s")
            time.sleep(10)


# === 4️⃣ RUN ===
if __name__ == "__main__":
    # Example script text for testing
    SCRIPT_TEXT = """
    Hello everyone! This is a demo video generated using HeyGen's v2 API.
    It's created entirely from text using Python. Enjoy the automation!
    """
    
    video_id = create_video(SCRIPT_TEXT, AVATAR_ID)
    if video_id:
        check_video_status(video_id)
