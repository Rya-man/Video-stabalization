from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('mainpage.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Call the API to process the video file
        processed_filename = process_video(filepath)
        
        # Redirect to the external site to display the processed video
        external_site_url = f"https://external-site.com/display?video={processed_filename}"
        return redirect(external_site_url)
    return redirect(request.url)

def process_video(filepath):
    api_url = 'https://your-api-endpoint.com/process'  # Replace with your API endpoint
    files = {'file': open(filepath, 'rb')}
    response = requests.post(api_url, files=files)
    
    # Save the processed file to the PROCESSED_FOLDER
    processed_filename = os.path.basename(filepath)
    processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
    
    with open(processed_filepath, 'wb') as f:
        f.write(response.content)
    
    return processed_filename

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
