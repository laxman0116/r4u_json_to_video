"""
Demo Client for JSON to Video Microservice
This script demonstrates how to use the microservice API
"""

import requests
import json
import time
import os
from pathlib import Path

# Configuration
API_BASE_URL = 'http://localhost:5000'
DEMO_JSON_FILE = 'demo_sample.json'

class VideoServiceClient:
    """Client for interacting with the JSON to Video microservice"""
    
    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}
    
    def health_check(self):
        """Check if the service is running"""
        try:
            response = requests.get(f'{self.base_url}/health')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            print("❌ Error: Cannot connect to the service. Is it running on port 5000?")
            return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def create_video(self, json_data, project_name=None):
        """
        Create a video from JSON data
        
        Args:
            json_data: Dictionary with video configuration
            project_name: Name of the project (optional)
            
        Returns:
            Response data
        """
        try:
            if project_name:
                json_data['project_name'] = project_name
            
            print("\n📤 Sending request to create video...")
            response = requests.post(
                f'{self.base_url}/api/video/create',
                headers=self.headers,
                json=json_data,
                timeout=300  # 5 minutes timeout for video generation
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print("❌ Error: Request timed out. Video generation took too long.")
            return {'status': 'error', 'message': 'Request timed out'}
        except requests.exceptions.ConnectionError:
            print("❌ Error: Cannot connect to the service.")
            return {'status': 'error', 'message': 'Connection failed'}
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def get_video_status(self, session_id):
        """Get status of a video project"""
        try:
            response = requests.get(f'{self.base_url}/api/video/status/{session_id}')
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def list_videos(self):
        """List all generated videos"""
        try:
            response = requests.get(f'{self.base_url}/api/video/list')
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None
    
    def download_video(self, session_id, output_file=None):
        """Download a generated video"""
        try:
            if output_file is None:
                output_file = f'{session_id}.mp4'
            
            response = requests.get(
                f'{self.base_url}/api/video/download/{session_id}',
                stream=True
            )
            response.raise_for_status()
            
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Video downloaded to: {output_file}")
            return output_file
        except Exception as e:
            print(f"❌ Error downloading video: {str(e)}")
            return None

def print_separator(title=""):
    """Print a formatted separator"""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}")
    else:
        print(f"\n{'-'*70}")

def run_demo():
    """Run the complete demo"""
    
    print_separator("JSON to Video Microservice - Demo")
    
    # Initialize client
    client = VideoServiceClient()
    
    # Step 1: Health Check
    print("\n🔍 Step 1: Checking service health...")
    health = client.health_check()
    if health:
        print(f"✅ Service is running!")
        print(f"   Service: {health.get('service')}")
        print(f"   Status: {health.get('status')}")
    else:
        print("\n⚠️  Please start the microservice first!")
        print("   Run: python microservice_api.py")
        return
    
    # Step 2: Load demo data
    print_separator("Step 2: Loading Demo Data")
    if not os.path.exists(DEMO_JSON_FILE):
        print(f"❌ Demo file not found: {DEMO_JSON_FILE}")
        return
    
    with open(DEMO_JSON_FILE, 'r') as f:
        demo_data = json.load(f)
    
    print(f"✅ Demo data loaded successfully")
    print(f"   Items: {len(demo_data['items'])}")
    print(f"   Project: {demo_data['project_name']}")
    print(f"   Resolution: {demo_data['resolution']}")
    print(f"   Duration per image: {demo_data['duration_per_image']} seconds")
    print("\n   Slides:")
    for idx, item in enumerate(demo_data['items'], 1):
        print(f"     {idx}. {item['text']}")
    
    # Step 3: Create video
    print_separator("Step 3: Creating Video")
    print("\n⏳ This may take a minute or two...")
    print("   - Generating images")
    print("   - Generating audio")
    print("   - Creating video file")
    
    start_time = time.time()
    result = client.create_video(demo_data)
    elapsed_time = time.time() - start_time
    
    if result.get('status') == 'success':
        print(f"\n✅ Video created successfully in {elapsed_time:.1f} seconds!")
        session_id = result.get('session_id')
        video_path = result.get('video_path')
        
        print(f"   Session ID: {session_id}")
        print(f"   Video path: {video_path}")
        print(f"   Images: {result.get('images_count')}")
        print(f"   FPS: {result.get('fps')}")
        print(f"   Resolution: {result.get('resolution')}")
        
        # Step 4: Verify video was created
        print_separator("Step 4: Verifying Video")
        if os.path.exists(video_path):
            file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
            print(f"✅ Video file exists")
            print(f"   File size: {file_size_mb:.2f} MB")
            print(f"   Path: {video_path}")
        
        # Step 5: List all videos
        print_separator("Step 5: Listing All Generated Videos")
        videos = client.list_videos()
        if videos and videos.get('status') == 'success':
            print(f"✅ Total videos generated: {videos.get('count')}")
            for video in videos.get('videos', []):
                print(f"   - {video['session_id']} ({video['size_mb']:.2f} MB)")
        
        # Step 6: Get video status
        print_separator("Step 6: Checking Video Status")
        status = client.get_video_status(session_id)
        if status:
            print(f"✅ Video status: {status}")
        
        # Final Summary
        print_separator("Demo Complete! 🎉")
        print(f"\n✅ Your video has been created and saved to:")
        print(f"   {video_path}")
        print(f"\n💡 To use the microservice:")
        print(f"   1. Send a POST request to: {API_BASE_URL}/api/video/create")
        print(f"   2. Include your JSON data with 'items' array")
        print(f"   3. Get the video from the response or download using session_id")
        print(f"\n📚 Available endpoints:")
        print(f"   GET  /health")
        print(f"   POST /api/video/create")
        print(f"   GET  /api/video/list")
        print(f"   GET  /api/video/status/<session_id>")
        print(f"   GET  /api/video/download/<session_id>")
        
    else:
        print(f"\n❌ Error creating video:")
        print(f"   {result.get('message')}")

if __name__ == '__main__':
    run_demo()
