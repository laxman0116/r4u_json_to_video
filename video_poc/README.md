# Video PoC Demo

This repository contains a small Python proof-of-concept for generating video content using MoviePy, OpenCV, and gTTS.

## Project files

- `video_poc.py`: Main project script that reads `data/slides.json`, generates spoken narration with `gTTS`, and builds a video from slide images.
- `animation_demo.py`: Simple MoviePy animation demo that creates a text animation video.
- `main_video_test.py`: OpenCV demo that generates a basic AVI video with overlaid text.
- `poc_mp4.py`: Additional video proof-of-concept script.
- `poc_video_sub.py`: Additional video/subtitle proof-of-concept script.
- `data/slides.json`: Slide definitions used by `video_poc.py`.
- `images/`: Source images for slides.
- `output/`: Generated video output directory.
- `audio/`: Generated TTS audio files.

## Python setup

Recommended Python version: `3.10` or newer.

1. Open PowerShell and change directory to the repository:

   ```powershell
   Set-Location D:\mypycode\video_poc
   ```

2. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Activate the virtual environment:

   ```powershell
   .\.venv\Scripts\Activate
   ```

4. Install dependencies:

   ```powershell
   pip install --upgrade pip
   pip install -r ..\requirements.txt
   ```

   If you want to install only the project dependencies inside `video_poc`, run:

   ```powershell
   pip install moviepy==2.0.0 gTTS==2.3.0 numpy==1.27.0
   ```

## How to run

### 1. Run the main video generator

This creates `output/CAPwithPACELC.mp4` using the JSON slide data and images.

```powershell
python .\video_poc.py
```

Output:
- `output/CAPwithPACELC.mp4`
- `audio/audio_0.mp3`, `audio/audio_1.mp3`, ...

### 2. Run the animation demo

```powershell
python .\animation_demo.py
```

Output:
- `animation.mp4`

### 3. Run the OpenCV video test

```powershell
python .\main_video_test.py
```

Output:
- `output_video.avi`

## Demo description

- `video_poc.py` uses `data/slides.json` to build a slideshow video.
- Each slide includes one or more images from `images/` and text narration.
- The script generates voice audio with `gTTS`, combines it with image clips, and renders subtitles.
- `main_video_test.py` shows a minimal OpenCV video creation workflow.
- `animation_demo.py` shows how to generate a simple text animation using MoviePy.

## Notes

- `gTTS` requires internet access to generate audio.
- Ensure the referenced image files exist in the `images/` folder.
- If `video_poc.py` prints `⚠ Image missing:`, verify the image path names in `data/slides.json`.

## Quick start demo

1. Activate the environment.
2. Run `python .\video_poc.py`.
3. Open `output\CAPwithPACELC.mp4` to view the generated video.

Enjoy exploring the video proof of concept!