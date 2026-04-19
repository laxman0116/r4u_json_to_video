# Python JSON to Video Microservice

A Flask-based microservice that converts JSON data into videos with images, text, and audio.

## 📋 Prerequisites

- Python 3.8+
- `uv` package manager (lightweight & fast)
- FFmpeg (for video processing)

## 🚀 Quick Setup with UV Virtual Environment

### If `python` is not in PATH

Use the full path and PowerShell call operator:

```powershell
& "C:\Program Files\Python314\python.exe" -m pip install uv
& "C:\Program Files\Python314\python.exe" -m uv venv
.venv\Scripts\activate
pip install -r requirements.txt
```

If you need to use `python` directly later, keep using the quoted path:

```powershell
& "C:\Program Files\Python314\python.exe" --version
& "C:\Program Files\Python314\python.exe" -m pip install -r requirements.txt
```

### Step 1: Install UV
```bash
python -m pip install uv
```

### Step 2: Create UV Virtual Environment
```bash
cd c:\1026\javaGitHub\pythonDev\r4u_json_to_video
python -m uv venv
```

### Step 3: Activate Virtual Environment
```bash
.venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### Verify Installation
```bash
python --version
pip list
```

You should see all packages listed below.

## 📦 Dependencies (requirements.txt)

```
flask==2.3.3
flask-cors==4.0.0
pillow==10.0.0
moviepy==1.0.3
google-cloud-text-to-speech==2.14.1
google-auth-oauthlib==1.1.0
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

## 🎬 Running the Application

### Terminal 1: Start Microservice
```bash
.venv\Scripts\activate
python microservice_api.py
```

### Terminal 2: Run Demo
```bash
.venv\Scripts\activate
python demo_client.py
```

## 📁 Project Structure

```
r4u_json_to_video/
├── .venv/                      # Virtual environment (created by uv)
├── microservice_api.py         # Main Flask API
├── demo_client.py              # Demo client script
├── demo_sample.json            # Sample JSON data
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── MICROSERVICE_GUIDE.md       # Detailed documentation
└── video_outputs/              # Generated videos (auto-created)
```

## 🔌 API Endpoints

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Create Video
```bash
curl -X POST http://localhost:5000/api/video/create \
  -H "Content-Type: application/json" \
  -d @demo_sample.json
```

### 3. List Videos
```bash
curl http://localhost:5000/api/video/list
```

### 4. Check Status
```bash
curl http://localhost:5000/api/video/status/learning_demo_2024
```

### 5. Download Video
```bash
curl http://localhost:5000/api/video/download/learning_demo_2024 -o video.mp4
```

## 📝 Example: Create Video Programmatically

```python
import requests

url = "http://localhost:5000/api/video/create"

payload = {
    "project_name": "my_project",
    "items": [
        {"text": "Slide 1 - Welcome"},
        {"text": "Slide 2 - Content"},
        {"text": "Slide 3 - Thank You"}
    ],
    "duration_per_image": 3,
    "resolution": [1280, 720],
    "fps": 24
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Status: {result['status']}")
print(f"Video Path: {result['video_path']}")
```

## 🛠️ Troubleshooting

### Virtual Environment Not Activating
```bash
# Windows - If .venv\Scripts\activate doesn't work
.venv\Scripts\activate.bat

# Or use PowerShell
.venv\Scripts\Activate.ps1
```

### Permission Denied (PowerShell)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Dependencies Installation Issues
```bash
# Clear pip cache and reinstall
pip cache purge
uv pip install --upgrade -r requirements.txt
```

### FFmpeg Not Found
**Windows:**
```bash
# Using chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

## 🧹 Cleanup

```bash
deactivate
rmdir /s .venv
rmdir /s video_outputs
```

## 📊 Performance Tips

- **UV is faster** than pip (5-10x faster installation)
- Use `uv pip install` instead of `pip install` when venv is active
- UV caches packages locally for quick reinstalls

## 🚢 Production Deployment

```bash
# Install with production settings
uv pip install gunicorn

# Run with Gunicorn (Windows)
gunicorn -w 4 -b 0.0.0.0:5000 microservice_api:app

# For production, use proper WSGI server
```

## 📚 Additional Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MoviePy Documentation](https://zulko.github.io/moviepy/)
- [Pillow Documentation](https://python-pillow.org/)

## 📄 License

MIT License

## ❓ Support

For issues or questions, check the MICROSERVICE_GUIDE.md file.

---

**Last Updated:** April 19, 2026
