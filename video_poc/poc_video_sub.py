import os
import json
import cv2
import numpy as np
from gtts import gTTS
import tempfile

# -----------------------
# Paths & Config
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "slides.json")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "demo_video.avi")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
IMAGE_WIDTH = 750
TEXT_WIDTH = VIDEO_WIDTH - IMAGE_WIDTH
FPS = 10
DURATION_PER_SLIDE = 5  # seconds

# -----------------------
# Helper Functions
# -----------------------
def create_bullet_text(explanation_list):
    return "\n".join([f"- {line}" for line in explanation_list]) if explanation_list else ""

def put_multiline_text(frame, text, x, y, line_height=40, font_scale=1, color=(255,255,255)):
    for i, line in enumerate(text.split("\n")):
        y_pos = y + i * line_height
        cv2.putText(frame, line, (x, y_pos), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2, cv2.LINE_AA)

# -----------------------
# Load slides
# -----------------------
with open(DATA_FILE, "r", encoding="utf-8") as f:
    slides = json.load(f).get("slides", [])

all_frames = []

# -----------------------
# Process slides
# -----------------------
for i, slide in enumerate(slides):
    text = slide.get("text", "")
    images = slide.get("images", [])
    explanation = slide.get("explanation", [])

    if not text or not images:
        print(f"Skipping slide {i+1}, missing text or images.")
        continue

    frames_per_image = int(FPS * DURATION_PER_SLIDE / len(images))

    for img_name in images:
        img_path = os.path.join(IMAGE_DIR, img_name)
        if not os.path.exists(img_path):
            print(f"Image missing: {img_path}")
            continue

        img = cv2.imread(img_path)
        img = cv2.resize(img, (IMAGE_WIDTH, VIDEO_HEIGHT))

        for f in range(frames_per_image):
            # Zoom effect
            factor = 1 + 0.03 * (f / FPS)
            zoomed = cv2.resize(img, None, fx=factor, fy=factor)
            h, w, _ = zoomed.shape
            start_x = (w - IMAGE_WIDTH)//2
            start_y = (h - VIDEO_HEIGHT)//2
            frame = zoomed[start_y:start_y+VIDEO_HEIGHT, start_x:start_x+IMAGE_WIDTH]

            # Explanation panel
            panel = np.full((VIDEO_HEIGHT, TEXT_WIDTH, 3), 30, dtype=np.uint8)
            bullet_text = create_bullet_text(explanation)
            put_multiline_text(panel, bullet_text, 20, 40)

            combined = np.hstack([frame, panel])
            all_frames.append(combined)

# -----------------------
# Save video using OpenCV (AVI)
# -----------------------
out = cv2.VideoWriter(OUTPUT_VIDEO, cv2.VideoWriter_fourcc(*'XVID'), FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))
for frame in all_frames:
    out.write(frame)
out.release()
print("Video created at:", OUTPUT_VIDEO)