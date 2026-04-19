# JSON to Video Microservice - Complete Guide

## Overview

This microservice converts JSON data containing text content into video files. It automatically:
- Generates images from text
- Creates audio from text using Google Text-to-Speech (gTTS)
- Combines them into a video file

## Architecture

```
┌─────────────────────┐
│   Client/Demo       │
│  (demo_client.py)   │
└──────────┬──────────┘
           │ HTTP REST
           ▼
┌─────────────────────────────────────────┐
│      Flask Microservice API             │
│      (microservice_api.py)              │
├─────────────────────────────────────────┤
│  ✓ /health                              │
│  ✓ /api/video/create                    │
│  ✓ /api/video/list                      │
│  ✓ /api/video/status/<id>               │
│  ✓ /api/video/download/<id>             │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│    Core Processing Modules              │
├─────────────────────────────────────────┤
│  • ImageGenerator (PIL)                 │
│  • gTTS (Text-to-Speech)                │
│  • VideoCreator (MoviePy)               │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│    Output Video Files                   │
│    (video_outputs/ directory)           │
└─────────────────────────────────────────┘
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- FFmpeg (required by moviepy)

### Step 1: Install FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

### Step 2: Install Python Dependencies

```bash
# Navigate to the project directory
cd r4u_json_to_video

# Install required packages
pip install -r requirements.txt
```

## Running the Microservice

### Start the Service

```bash
python microservice_api.py
```

You should see output like:
```
Starting JSON to Video Microservice...
WARNING in app.run()
 * Running on http://0.0.0.0:5000
 * Press CTRL+C to quit
```

The service is now running on `http://localhost:5000`

### Verify Service is Running

Open a new terminal and run:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "JSON to Video Microservice",
  "timestamp": "2024-04-19T10:30:00.123456"
}
```

## Running the Demo

Open a new terminal and run:

```bash
python demo_client.py
```

This will:
1. ✅ Check service health
2. 📤 Load demo JSON data
3. 🎬 Create a sample video with 5 slides
4. 📊 Display generation statistics
5. ✅ Verify the video file
6. 📚 Show available API endpoints

Expected output:
```
======================================================================
  JSON to Video Microservice - Demo
======================================================================

🔍 Step 1: Checking service health...
✅ Service is running!
   Service: JSON to Video Microservice
   Status: healthy

...

✅ Video created successfully in 45.3 seconds!
   Session ID: learning_demo_2024
   Video path: video_outputs/learning_demo_2024/learning_demo_2024_video.mp4
   Images: 5
   FPS: 24
   Resolution: [1280, 720]

...
```

## API Endpoints

### 1. Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "service": "JSON to Video Microservice",
  "timestamp": "2024-04-19T10:30:00.123456"
}
```

### 2. Create Video
```
POST /api/video/create

Request Body:
{
  "project_name": "my_project",
  "items": [
    {"text": "Slide 1 content"},
    {"text": "Slide 2 content"},
    {"text": "Slide 3 content"}
  ],
  "fps": 24,
  "resolution": [1280, 720],
  "duration_per_image": 3,
  "add_text": true,
  "background_color": [255, 255, 255],
  "text_color": [0, 0, 0]
}

Response:
{
  "status": "success",
  "session_id": "my_project",
  "message": "Video created successfully with 3 slides",
  "video_path": "video_outputs/my_project/my_project_video.mp4",
  "images_count": 3,
  "fps": 24,
  "resolution": [1280, 720],
  "timestamp": "2024-04-19T10:30:00.123456"
}
```

### 3. List All Videos
```
GET /api/video/list

Response:
{
  "status": "success",
  "count": 2,
  "videos": [
    {
      "session_id": "learning_demo_2024",
      "created": "2024-04-19T10:30:00.123456",
      "size_mb": 15.5
    },
    {
      "session_id": "my_project",
      "created": "2024-04-19T10:35:00.123456",
      "size_mb": 12.3
    }
  ]
}
```

### 4. Get Video Status
```
GET /api/video/status/<session_id>

Response:
{
  "status": "success",
  "project_id": "learning_demo_2024",
  "video_ready": true,
  "size_mb": 15.5,
  "created": "2024-04-19T10:30:00.123456"
}
```

### 5. Download Video
```
GET /api/video/download/<session_id>

Response: Binary video file (mp4)
```

## JSON Input Format

### Complete Example
```json
{
  "project_name": "educational_video",
  "items": [
    {
      "text": "Introduction to Python"
    },
    {
      "text": "Variables and Data Types"
    },
    {
      "text": "Functions and Modules"
    },
    {
      "text": "Object Oriented Programming"
    },
    {
      "text": "Thank you!"
    }
  ],
  "fps": 24,
  "resolution": [1280, 720],
  "duration_per_image": 3,
  "add_text": true,
  "background_color": [255, 255, 255],
  "text_color": [0, 0, 0]
}
```

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| project_name | string | auto-generated | Unique identifier for the project |
| items | array | required | Array of slide objects with "text" property |
| fps | integer | 24 | Frames per second for the video |
| resolution | array | [1280, 720] | Video resolution [width, height] |
| duration_per_image | integer | 2 | Duration each slide appears (seconds) |
| add_text | boolean | true | Add text with gradient background or plain background |
| background_color | array | [255, 255, 255] | RGB color for slide background |
| text_color | array | [0, 0, 0] | RGB color for text |

## Example Usage with cURL

```bash
# Create a video
curl -X POST http://localhost:5000/api/video/create \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "my_video",
    "items": [
      {"text": "Hello World"},
      {"text": "Slide 2"},
      {"text": "The End"}
    ],
    "duration_per_image": 2
  }'

# List all videos
curl http://localhost:5000/api/video/list

# Get video status
curl http://localhost:5000/api/video/status/my_video

# Download video
curl http://localhost:5000/api/video/download/my_video -o my_video.mp4
```

## Example Usage with Python

```python
import requests
import json

# Create video
response = requests.post('http://localhost:5000/api/video/create', json={
    'project_name': 'python_demo',
    'items': [
        {'text': 'Welcome to Python'},
        {'text': 'Learning Microservices'},
        {'text': 'The End'}
    ],
    'duration_per_image': 3
})

result = response.json()
print(f"Video created: {result['video_path']}")
print(f"Session ID: {result['session_id']}")

# Download video
session_id = result['session_id']
response = requests.get(f'http://localhost:5000/api/video/download/{session_id}')
with open(f'{session_id}.mp4', 'wb') as f:
    f.write(response.content)
```

## Output Structure

Generated videos are stored in `video_outputs/` directory:

```
video_outputs/
├── learning_demo_2024/
│   ├── images/
│   │   ├── slide_000.png
│   │   ├── slide_001.png
│   │   └── ...
│   ├── audio/
│   │   ├── audio_000.mp3
│   │   ├── audio_001.mp3
│   │   └── ...
│   └── learning_demo_2024_video.mp4
├── my_project/
│   ├── images/
│   ├── audio/
│   └── my_project_video.mp4
└── temp/
    └── (temporary files)
```

## Performance Notes

- **Video generation time**: ~2-3 seconds per slide
- **Output file size**: ~3-5 MB per minute of video
- **Memory usage**: ~500 MB - 1 GB during processing
- **CPU usage**: Scales with resolution and frame rate

## Troubleshooting

### Issue: "Cannot connect to the service"
**Solution**: Make sure `microservice_api.py` is running in another terminal

### Issue: FFmpeg not found
**Solution**: Install FFmpeg (see Installation section above)

### Issue: "ModuleNotFoundError"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: Video file is corrupted or won't play
**Solution**: 
- Check the console for error messages
- Verify FFmpeg is properly installed
- Try with a smaller resolution first

### Issue: Service running very slow
**Solution**:
- Reduce video resolution
- Reduce number of slides
- Use fewer FPS
- Close other applications

## Performance Optimization Tips

1. **Reduce resolution** for faster processing:
   ```json
   "resolution": [854, 480]
   ```

2. **Reduce duration per image**:
   ```json
   "duration_per_image": 1
   ```

3. **Use plain text** instead of gradient:
   ```json
   "add_text": false
   ```

## Scaling Considerations

For production use:
- Run multiple instances behind a load balancer
- Use a job queue (Celery + Redis) for video processing
- Store videos in cloud storage (S3, Azure Blob)
- Implement video caching
- Add authentication/authorization
- Use docker containers

## API Testing Tools

### Postman
1. Import the following request:
```
POST http://localhost:5000/api/video/create
Content-Type: application/json

{
  "project_name": "test",
  "items": [{"text": "Test"}],
  "duration_per_image": 2
}
```

### Swagger/OpenAPI (Optional)
Can be added for interactive API documentation.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in the console
3. Check the API response status and message fields

## License

See LICENSE file in the project root.
