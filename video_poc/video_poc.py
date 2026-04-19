import json
import os
from moviepy import (
    ImageClip,
    concatenate_videoclips,
    AudioFileClip,
    TextClip,
    CompositeVideoClip
)
from gtts import gTTS

# -----------------------
# Paths
# -----------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "data", "slides.json")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "CAPwithPACELC.mp4")

print("Loading slides from:", DATA_FILE)

# -----------------------
# Load JSON
# -----------------------

with open(DATA_FILE, "r", encoding="utf-8") as f:
    slides = json.load(f)["slides"]

clips = []

# -----------------------
# Process Slides
# -----------------------

for i, slide in enumerate(slides):

    text = slide["text"]

    # support image or images
    image_list = slide.get("images") or [slide.get("image")]

    audio_file = os.path.join(AUDIO_DIR, f"audio_{i}.mp3")

    print(f"Generating narration for slide {i+1}")

    # TTS
    tts = gTTS(text=text, lang="en", tld="co.in")
    tts.save(audio_file)

    audio_clip = AudioFileClip(audio_file)
    duration = audio_clip.duration

    image_clips = []

    img_duration = duration / len(image_list)

    for img in image_list:

        # support both formats
        if img.startswith("images"):
            image_path = os.path.join(BASE_DIR, img)
        else:
            image_path = os.path.join(IMAGE_DIR, img)

        if not os.path.exists(image_path):
            print("⚠ Image missing:", image_path)
            continue

        print("Loading image:", image_path)

        clip = (
            ImageClip(image_path)
            .with_duration(img_duration)
            .resized(height=720)
        )

        # zoom animation
        clip = clip.resized(lambda t: 1 + 0.001 * t)

        image_clips.append(clip)

    if not image_clips:
        print("No images found for slide:", i + 1)
        continue

    slide_video = concatenate_videoclips(image_clips)

    # subtitles
    subtitle = (
    TextClip(
        text=text,
        font_size=38,
        color="white",
        method="caption",
        size=(1000, None)
    )
    .with_position(("center", "bottom"))
    .with_duration(duration)
)

    video = CompositeVideoClip([slide_video, subtitle])
    video = video.with_audio(audio_clip)

    clips.append(video)

# -----------------------
# Combine All Slides
# -----------------------

print("Combining slides...")

final_video = concatenate_videoclips(clips, method="compose")

# -----------------------
# Export Video
# -----------------------

print("Rendering video...")

final_video.write_videofile(
    OUTPUT_VIDEO,
    fps=24,
    codec="libx264",
    preset="ultrafast",
    threads=4
)

print("✅ Video created successfully!")
print("Output:", OUTPUT_VIDEO)