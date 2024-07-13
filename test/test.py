import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_path)

from modules.frame_extraction.split import process_video
from modules.frame_extraction.compile import combine_frames_and_audio
from modules.frame_outpainting.extend_frame import extend_frames
from modules.stabilisation.stabiliser import stablize_full,stablize_normal
from modules.frame_outpainting.diffusion_i2i import extend_frames_i2i

def extend_video(video_path):
    frames_folder=process_video(video_path)
    #extend_frames(frames_folder)
    extend_frames_i2i(frames_folder)
    output_video_path=combine_frames_and_audio(frames_folder,video_path)
    stablize_full(output_video_path)

if __name__ == "__main__":
    video_path=r"test\aa.mp4"
    extend_video(video_path)
    stablize_normal(video_path)