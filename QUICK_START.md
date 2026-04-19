# Quick Start Guide - JSON to Video Microservice

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Microservice
```bash
python microservice_api.py
```
Wait for the message: `* Running on http://0.0.0.0:5000`

### Step 3: Run Demo (in a new terminal)
```bash
python demo_client.py
```

That's it! Your first video will be created in ~1-2 minutes.

---

## 📋 What Happens in the Demo

The demo will:
1. ✅ Connect to the microservice
2. 📄 Load demo JSON with 5 slides
3. 🎨 Generate colorful images with text
4. 🔊 Generate audio from text using Google TTS
5. 🎬 Create a video combining images and audio
6. 💾 Save to `video_outputs/learning_demo_2024/learning_demo_2024_video.mp4`

---

## 🎯 Create Your Own Video

Edit `demo_sample.json` and change the items:

```json
{
  "project_name": "my_awesome_video",
  "items": [
    {"text": "Slide 1 text here"},
    {"text": "Slide 2 text here"},
    {"text": "Slide 3 text here"}
  ],
  "duration_per_image": 2,
  "fps": 24
}
```

Then run:
```bash
python demo_client.py
```

---

## 🔌 API Usage (Advanced)

### Using cURL:
```bash
curl -X POST http://localhost:5000/api/video/create \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "test_video",
    "items": [
      {"text": "Hello"},
      {"text": "World"},
      {"text": "Done"}
    ],
    "duration_per_image": 2
  }'
```

### Using Python:
```python
import requests

response = requests.post('http://localhost:5000/api/video/create', json={
    'project_name': 'my_video',
    'items': [
        {'text': 'Slide 1'},
        {'text': 'Slide 2'},
        {'text': 'Slide 3'}
    ]
})

print(response.json())
```

---

## 📁 Output Location

Videos are saved to:
```
video_outputs/
├── learning_demo_2024/
│   └── learning_demo_2024_video.mp4
├── my_video/
│   └── my_video_video.mp4
└── ...
```

---

## ⚡ API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check if service is running |
| `/api/video/create` | POST | Create a video from JSON |
| `/api/video/list` | GET | List all videos |
| `/api/video/status/<id>` | GET | Check video status |
| `/api/video/download/<id>` | GET | Download video |

---

## 🛠️ Troubleshooting

**Q: "ModuleNotFoundError"**
- Run: `pip install -r requirements.txt`

**Q: "FFmpeg not found"**
- Install FFmpeg from: https://ffmpeg.org/download.html

**Q: "Connection refused"**
- Make sure `microservice_api.py` is running in another terminal

**Q: "Video takes too long"**
- Reduce resolution: `"resolution": [854, 480]`
- Reduce duration: `"duration_per_image": 1`

---

## 📚 Documentation

See `MICROSERVICE_GUIDE.md` for complete documentation.

---

## 💡 Example JSON Configurations

### Short & Fast
```json
{
  "project_name": "quick_demo",
  "items": [
    {"text": "Intro"},
    {"text": "Content"},
    {"text": "End"}
  ],
  "resolution": [854, 480],
  "duration_per_image": 1,
  "fps": 24
}
```

### Long & High Quality
```json
{
  "project_name": "premium_video",
  "items": [
    {"text": "Welcome"},
    {"text": "Section 1"},
    {"text": "Section 2"},
    {"text": "Section 3"},
    {"text": "Conclusion"},
    {"text": "Thank You"}
  ],
  "resolution": [1920, 1080],
  "duration_per_image": 3,
  "fps": 30
}
```

---

## 🎓 How It Works

```
1. JSON Input
   ↓
2. Text Processing
   ├─ Generate images from text
   └─ Generate audio from text
   ↓
3. Media Combination
   ├─ Arrange images in sequence
   └─ Combine with audio
   ↓
4. Video Encoding
   └─ Create MP4 video file
   ↓
5. Output Video
```

---

Happy video creating! 🎉
