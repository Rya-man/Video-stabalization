import os
import cv2
from moviepy.editor import VideoFileClip

def extract_audio(video_path, output_folder):
    video = VideoFileClip(video_path)
    audio_path = os.path.join(output_folder, "audio.mp3")
    video.audio.write_audiofile(audio_path)
    return audio_path

def extract_frames(video_path, frames_folder):
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error opening video file: {video_path}")
        return
    frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
    count = 0
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break
        timestamp = count / frame_rate
        timestamp_str = f"{timestamp:.2f}".replace(".", "_")
        frame_filename = f"frame_{timestamp_str}.png"
        frame_path = os.path.join(frames_folder, frame_filename)
        cv2.imwrite(frame_path, frame)
        count += 1
    video_capture.release()
    cv2.destroyAllWindows()

def process_video(video_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = os.path.join(os.getcwd(), video_name)
    os.makedirs(output_folder, exist_ok=True)
    extract_audio(video_path, output_folder)
    frames_folder = os.path.join(output_folder, "frames")
    os.makedirs(frames_folder, exist_ok=True)
    extract_frames(video_path, frames_folder)
    return frames_folder

if __name__ == "__main__":
    video_path = "sample.mp4"
    process_video(video_path)
