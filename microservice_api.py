"""
Flask Microservice for JSON to Video Conversion
This service provides REST API endpoints for video generation
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime
import logging
from com.r4u.stt.to.video.image_generator import ImageGenerator
from com.r4u.stt.to.video.video_creator import VideoCreator
from gtts import gTTS

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create output directories
OUTPUT_BASE_DIR = 'video_outputs'
TEMP_DIR = os.path.join(OUTPUT_BASE_DIR, 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

class VideoConversionService:
    """Service to handle JSON to Video conversion"""
    
    def __init__(self, output_base_dir=OUTPUT_BASE_DIR):
        self.output_base_dir = output_base_dir
        self.temp_dir = os.path.join(output_base_dir, 'temp')
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def process_json_to_video(self, json_data, project_name=None):
        """
        Convert JSON data to video
        
        Args:
            json_data: Dictionary containing video configuration
            project_name: Name of the project (optional)
            
        Returns:
            Dictionary with status and video path
        """
        try:
            # Create unique session ID
            session_id = project_name or f"project_{uuid.uuid4().hex[:8]}"
            session_dir = os.path.join(self.output_base_dir, session_id)
            images_dir = os.path.join(session_dir, 'images')
            audio_dir = os.path.join(session_dir, 'audio')
            
            os.makedirs(images_dir, exist_ok=True)
            os.makedirs(audio_dir, exist_ok=True)
            
            logger.info(f"Processing project: {session_id}")
            
            # Extract configuration
            items = json_data.get('items', [])
            fps = json_data.get('fps', 24)
            resolution = tuple(json_data.get('resolution', [1280, 720]))
            duration_per_image = json_data.get('duration_per_image', 2)
            add_text = json_data.get('add_text', True)
            background_color = tuple(json_data.get('background_color', [255, 255, 255]))
            text_color = tuple(json_data.get('text_color', [0, 0, 0]))
            
            # Generate images and audio
            image_generator = ImageGenerator(output_dir=images_dir, 
                                           width=resolution[0], 
                                           height=resolution[1])
            image_paths = []
            audio_paths = []
            
            for idx, item in enumerate(items):
                text = item.get('text', f'Slide {idx + 1}')
                bg_color = tuple(item.get('background_color', background_color))
                txt_color = tuple(item.get('text_color', text_color))
                
                # Generate image
                image_name = f'slide_{idx:03d}.png'
                if add_text:
                    image_path = image_generator.create_gradient_image(
                        text,
                        image_name=image_name,
                        color1=(50, 50, 150),
                        color2=(200, 100, 255),
                        text_color=(255, 255, 255),
                        font_size=80
                    )
                else:
                    image_path = image_generator.create_text_image(
                        text,
                        image_name=image_name,
                        bg_color=bg_color,
                        text_color=txt_color,
                        font_size=70
                    )
                
                image_paths.append(image_path)
                
                # Generate audio
                audio_name = f'audio_{idx:03d}.mp3'
                audio_path = os.path.join(audio_dir, audio_name)
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(audio_path)
                audio_paths.append(audio_path)
                
                logger.info(f"Generated slide {idx + 1}/{len(items)}")
            
            # Create video from images
            video_creator = VideoCreator(fps=fps, resolution=resolution)
            video_output = os.path.join(session_dir, f'{session_id}_video.mp4')
            
            # Create image-duration pairs
            image_duration_pairs = [
                (img_path, duration_per_image) for img_path in image_paths
            ]
            
            logger.info("Creating video from images...")
            video_creator.create_video_with_timing(image_duration_pairs, video_output)
            
            result = {
                'status': 'success',
                'session_id': session_id,
                'message': f'Video created successfully with {len(items)} slides',
                'video_path': video_output,
                'images_count': len(image_paths),
                'fps': fps,
                'resolution': resolution,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Video created successfully: {video_output}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}", exc_info=True)
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Initialize service
service = VideoConversionService()

# Routes
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'JSON to Video Microservice',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/video/create', methods=['POST'])
def create_video():
    """
    Create video from JSON data
    
    Expected JSON format:
    {
        "project_name": "my_project",
        "items": [
            {"text": "Welcome to Learning"},
            {"text": "Slide 2 content"},
            ...
        ],
        "fps": 24,
        "resolution": [1280, 720],
        "duration_per_image": 2,
        "add_text": true,
        "background_color": [255, 255, 255],
        "text_color": [0, 0, 0]
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400
        
        if 'items' not in data or not data['items']:
            return jsonify({'status': 'error', 'message': 'Items array is required and cannot be empty'}), 400
        
        result = service.process_json_to_video(data)
        
        if result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in /api/video/create: {str(e)}", exc_info=True)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/video/download/<session_id>', methods=['GET'])
def download_video(session_id):
    """Download generated video"""
    try:
        video_path = os.path.join(OUTPUT_BASE_DIR, session_id, f'{session_id}_video.mp4')
        
        if not os.path.exists(video_path):
            return jsonify({'status': 'error', 'message': 'Video not found'}), 404
        
        return send_file(video_path, mimetype='video/mp4', as_attachment=True, 
                        download_name=f'{session_id}.mp4')
        
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}", exc_info=True)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/video/list', methods=['GET'])
def list_videos():
    """List all generated videos"""
    try:
        videos = []
        
        if os.path.exists(OUTPUT_BASE_DIR):
            for project_dir in os.listdir(OUTPUT_BASE_DIR):
                project_path = os.path.join(OUTPUT_BASE_DIR, project_dir)
                if os.path.isdir(project_path) and project_dir != 'temp':
                    video_file = os.path.join(project_path, f'{project_dir}_video.mp4')
                    if os.path.exists(video_file):
                        videos.append({
                            'session_id': project_dir,
                            'created': datetime.fromtimestamp(os.path.getctime(video_file)).isoformat(),
                            'size_mb': os.path.getsize(video_file) / (1024 * 1024)
                        })
        
        return jsonify({
            'status': 'success',
            'count': len(videos),
            'videos': videos
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing videos: {str(e)}", exc_info=True)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/video/status/<session_id>', methods=['GET'])
def video_status(session_id):
    """Get status of a video project"""
    try:
        project_path = os.path.join(OUTPUT_BASE_DIR, session_id)
        
        if not os.path.exists(project_path):
            return jsonify({'status': 'error', 'message': 'Project not found'}), 404
        
        video_file = os.path.join(project_path, f'{session_id}_video.mp4')
        
        if os.path.exists(video_file):
            return jsonify({
                'status': 'success',
                'project_id': session_id,
                'video_ready': True,
                'size_mb': os.path.getsize(video_file) / (1024 * 1024),
                'created': datetime.fromtimestamp(os.path.getctime(video_file)).isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'success',
                'project_id': session_id,
                'video_ready': False,
                'message': 'Project exists but video is not ready'
            }), 200
            
    except Exception as e:
        logger.error(f"Error getting video status: {str(e)}", exc_info=True)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting JSON to Video Microservice...")
    app.run(debug=True, host='0.0.0.0', port=5000)
