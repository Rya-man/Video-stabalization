import sys
import os
from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename

# Ensure the modules directory is in the Python path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(project_path)

# Import the previously defined functions
from modules.frame_extraction.split import process_video
from modules.frame_extraction.compile import combine_frames_and_audio
from modules.frame_outpainting.extend_frame import extend_frames
from modules.stabilisation.stabiliser import stablize_full, stablize_normal

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

# Create the folders if they do not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def extend_video(video_path):
    frames_folder, audio_path = process_video(video_path)
    if frames_folder is None:
        return None
    extend_frames(frames_folder)
    output_video_path = combine_frames_and_audio(frames_folder, video_path, audio_path)
    if audio_path:
        stabilize_path = stablize_full(output_video_path)
        return stabilize_path
    else:
        stabilize_path2 = stablize_normal(output_video_path)
        return stabilize_path2


@app.route('/')
def upload_form():
    return render_template('mainpage.html')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Process the video
        processed_video_path = extend_video(file_path)
        if processed_video_path is None:
            return "Processing the video failed. Ensure the video file has an audio stream and is properly formatted."
        
        return send_file(processed_video_path, as_attachment=True, download_name='processed_video.mp4')

if __name__ == "__main__":
    app.run(debug=True)
