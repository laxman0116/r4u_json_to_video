import os
import json
import cv2
import numpy as np
from gtts import gTTS
import soundfile as sf
import av

# -----------------------
# Paths & Config
# -----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "slides.json")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "microservices_overview.mp4")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
IMAGE_WIDTH = 750
TEXT_WIDTH = VIDEO_WIDTH - IMAGE_WIDTH
FPS = 10
DURATION_PER_SLIDE = 5  # seconds per slide

# -----------------------
# Helpers
# -----------------------
def create_bullet_text(explanation_list):
    return "\n".join([f"- {line}" for line in explanation_list]) if explanation_list else ""

def put_multiline_text(frame, text, x, y, line_height=40, font_scale=1, color=(255,255,255)):
    # Slightly more padding and spacing for readability
    PANEL_MARGIN = 20
    BULLET_SPACING = 40  # fixed spacing between bullets

    for j, bullet in enumerate(explanation):
        y_pos = PANEL_MARGIN + j * BULLET_SPACING
        cv2.putText(panel, f"- {bullet}", (20, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
    #for i, line in enumerate(text.split("\n")):
    #    y_pos = y + i * line_height
    #    cv2.putText(frame, line, (x, y_pos), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2, cv2.LINE_AA)

def put_bullet_text(frame, text_list, x, y, max_width, line_height=35, font_scale=1, color=(255,255,255)):
    """
    Draws bullet points on the frame with automatic word wrap.
    frame      : the image panel (numpy array)
    text_list  : list of bullet strings
    x, y       : top-left corner
    max_width  : max pixel width for text
    """
    for i, bullet in enumerate(text_list):
        words = bullet.split()
        line = ""
        y_pos = y + i * line_height
        for word in words:
            test_line = f"{line} {word}".strip()
            (w, h), _ = cv2.getTextSize(test_line, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
            if w > max_width - 20:  # wrap line
                cv2.putText(frame, line, (x, y_pos), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2, cv2.LINE_AA)
                line = word
                y_pos += line_height
            else:
                line = test_line
        cv2.putText(frame, line, (x, y_pos), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2, cv2.LINE_AA)

def put_bullet_text_scaled(frame, text_list, x, y, max_width, panel_height, font_scale=1, color=(255,255,255)):
    """
    Draw bullet points with dynamic spacing to fit the panel height.
    """
    n = len(text_list)
    if n == 0:
        return
    
    # Compute line height
    line_height = min(35, panel_height // n)  # max 35 px, else shrink
    for i, bullet in enumerate(text_list):
        words = bullet.split()
        line = ""
        y_pos = y + i * line_height
        for word in words:
            test_line = f"{line} {word}".strip()
            (w, h), _ = cv2.getTextSize(test_line, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
            if w > max_width - 20:  # wrap line
                cv2.putText(frame, line, (x, y_pos), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2, cv2.LINE_AA)
                line = word
                y_pos += line_height
            else:
                line = test_line
        cv2.putText(frame, line, (x, y_pos), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2, cv2.LINE_AA)        
# -----------------------
# Load slides
# -----------------------
with open(DATA_FILE, "r", encoding="utf-8") as f:
    slides = json.load(f).get("slides", [])

all_frames = []
all_audio = []

# -----------------------
# Generate frames & audio
# -----------------------
for i, slide in enumerate(slides):
    text = slide.get("text", "")
    images = slide.get("images", [])
    explanation = slide.get("explanation", [])

    if not text or not images:
        continue

    # --- TTS ---
    mp3_file = os.path.join(AUDIO_DIR, f"tmp_audio_{i}.mp3")
    tts = gTTS(text=text, lang="en", tld="co.uk")
    tts.save(mp3_file)

    # Load audio and make mono
    audio_data, sr = sf.read(mp3_file, dtype='float32')
    if audio_data.ndim > 1:
        audio_data = audio_data.mean(axis=1)

    # Stretch/trim audio to slide duration
    expected_samples = int(DURATION_PER_SLIDE * sr)
    if len(audio_data) < expected_samples:
        audio_data = np.pad(audio_data, (0, expected_samples - len(audio_data)))
    else:
        audio_data = audio_data[:expected_samples]

    all_audio.append((audio_data, sr))

    # --- Video frames ---
    frames_per_image = max(1, int(FPS * DURATION_PER_SLIDE / len(images)))
    for img_name in images:
        img_path = os.path.join(IMAGE_DIR, img_name)
        if not os.path.exists(img_path):
            continue

        img = cv2.imread(img_path)
        img = cv2.resize(img, (IMAGE_WIDTH, VIDEO_HEIGHT))

        for f in range(frames_per_image):
            factor = 1 + 0.03 * (f / FPS)
            zoomed = cv2.resize(img, None, fx=factor, fy=factor)
            h, w, _ = zoomed.shape
            start_x = (w - IMAGE_WIDTH)//2
            start_y = (h - VIDEO_HEIGHT)//2
            frame = zoomed[start_y:start_y+VIDEO_HEIGHT, start_x:start_x+IMAGE_WIDTH]

            panel = np.full((VIDEO_HEIGHT, TEXT_WIDTH, 3), 30, dtype=np.uint8)
            bullet_text = create_bullet_text(explanation)
            put_multiline_text(panel, bullet_text, 20, 40)
            combined = np.hstack([frame, panel])
            all_frames.append(combined)

# -----------------------
# Write MP4 using PyAV
# -----------------------
container = av.open(OUTPUT_VIDEO, mode='w')

video_stream = container.add_stream('libx264', rate=FPS)
video_stream.width = VIDEO_WIDTH
video_stream.height = VIDEO_HEIGHT
video_stream.pix_fmt = 'yuv420p'

sr = all_audio[0][1]
audio_stream = container.add_stream('aac', rate=sr)
audio_stream.layout = 'mono'

print("Writing video and audio to MP4...")

# --- Encode video frames ---
for frame in all_frames:
    video_frame = av.VideoFrame.from_ndarray(frame, format='bgr24')
    for packet in video_stream.encode(video_frame):
        container.mux(packet)

# --- Encode audio properly (split into small chunks per video frame) ---
samples_per_frame = int(sr / FPS)
for audio_data, sr in all_audio:
    for start in range(0, len(audio_data), samples_per_frame):
        chunk = audio_data[start:start+samples_per_frame]
        if len(chunk) < samples_per_frame:
            chunk = np.pad(chunk, (0, samples_per_frame - len(chunk)))

        # Must be 2D: (channels, samples)
        audio_frame_int16 = (chunk * 32767).astype(np.int16).reshape(1, -1)
        audio_frame = av.AudioFrame.from_ndarray(audio_frame_int16, format='s16', layout='mono')
        audio_frame.sample_rate = sr
        for packet in audio_stream.encode(audio_frame):
            container.mux(packet)

# Flush remaining packets
for packet in video_stream.encode():
    container.mux(packet)
for packet in audio_stream.encode():
    container.mux(packet)

container.close()
print("MP4 created successfully at:", OUTPUT_VIDEO)