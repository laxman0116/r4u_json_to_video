import json
import cv2
import numpy as np
import os
from gtts import gTTS
from moviepy.editor import ImageSequenceClip

class JsonToVideo:
    def __init__(self, json_file, output_path):
        self.json_file = json_file
        self.output_path = output_path
        self.images = []
        self.audios = []

    def process_json(self):
        with open(self.json_file, 'r') as f:
            data = json.load(f)
            for item in data['items']:
                image_path = item['image']
                text = item['text']
                self.generate_audio(text)
                self.images.append(image_path)

    def generate_audio(self, text):
        tts = gTTS(text=text, lang='en')
        audio_file = os.path.join(self.output_path, 'audio.mp3')
        tts.save(audio_file)
        self.audios.append(audio_file)

    def create_video(self):
        clips = []
        for img in self.images:
            clips.append(cv2.imread(img))
        clip = ImageSequenceClip(clips, fps=24)
        video_file = os.path.join(self.output_path, 'output_video.mp4')
        clip.write_videofile(video_file, codec='libx264')

if __name__ == '__main__':
    json_processing = JsonToVideo('input.json', 'output_directory')
    json_processing.process_json()
    json_processing.create_video()