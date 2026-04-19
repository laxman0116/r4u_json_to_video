import cv2
import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
import numpy as np

class VideoCreator:
    def __init__(self, fps=24, resolution=(1280, 720)):
        self.fps = fps
        self.resolution = resolution

    def create_video_from_images(self, image_paths, output_path='output.mp4', duration_per_image=2):
        """
        Create a video from a list of image paths
        
        Args:
            image_paths: List of image file paths
            output_path: Path to save the output video
            duration_per_image: Duration each image appears in seconds
        """
        clips = []
        
        for img_path in image_paths:
            # Create a clip from the image
            clip = ImageClip(img_path)
            clip = clip.set_duration(duration_per_image)
            clip = clip.resize(height=self.resolution[1])
            clips.append(clip)
        
        # Concatenate all clips
        final_clip = concatenate_videoclips(clips)
        
        # Write video file
        final_clip.write_videofile(output_path, fps=self.fps, verbose=False, logger=None)
        final_clip.close()
        
        return output_path

    def add_audio_to_video(self, video_path, audio_path, output_path='output_with_audio.mp4'):
        """
        Add audio to an existing video
        
        Args:
            video_path: Path to the video file
            audio_path: Path to the audio file
            output_path: Path to save the final output
        """
        from moviepy.editor import VideoFileClip
        
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        # Set the audio to the video
        final_video = video.set_audio(audio)
        
        # Write the final video
        final_video.write_videofile(output_path, fps=self.fps, verbose=False, logger=None)
        
        video.close()
        audio.close()
        final_video.close()
        
        return output_path

    def create_video_with_timing(self, image_duration_pairs, output_path='output_timed.mp4'):
        """
        Create a video where each image has its own duration
        
        Args:
            image_duration_pairs: List of tuples (image_path, duration_in_seconds)
            output_path: Path to save the output video
        """
        clips = []
        
        for img_path, duration in image_duration_pairs:
            clip = ImageClip(img_path)
            clip = clip.set_duration(duration)
            clip = clip.resize(height=self.resolution[1])
            clips.append(clip)
        
        # Concatenate all clips
        final_clip = concatenate_videoclips(clips)
        
        # Write video file
        final_clip.write_videofile(output_path, fps=self.fps, verbose=False, logger=None)
        final_clip.close()
        
        return output_path

if __name__ == '__main__':
    creator = VideoCreator()
    # Example usage
    # images = ['image1.png', 'image2.png', 'image3.png']
    # creator.create_video_from_images(images)
    # creator.add_audio_to_video('output.mp4', 'audio.mp3')