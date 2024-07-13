import os
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, AudioFileClip

def get_fps_from_video(video_path):
    with VideoFileClip(video_path) as video:
        return video.fps
        
def combine_frames_and_audio(frames_folder, video_path, audio_path=None):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    folder_name = os.path.dirname(frames_folder)
    frames_folder = os.path.join(folder_name, "frames_extended")
    if audio_path:
        audio_clip = AudioFileClip(audio_path)
    else:
        audio_clip = None

    output_video_path = os.path.join(folder_name, f"{video_name}_proc.mp4")
    fps = get_fps_from_video(video_path)
    frames = sorted(
        [os.path.join(frames_folder, f) for f in os.listdir(frames_folder) if f.endswith('.png')],
        key=lambda x: float(os.path.splitext(os.path.basename(x))[0].split('_')[1] + '.' + os.path.splitext(os.path.basename(x))[0].split('_')[2])
    )
    frame_clips = [ImageClip(m).set_duration(1.0 / fps) for m in frames]
    video_clip = concatenate_videoclips(frame_clips, method="compose")
    if audio_clip:
        video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_video_path, fps=fps)
    return output_video_path

if __name__ == "__main__":
    folder_name = "./sample"
    combine_frames_and_audio(folder_name)
