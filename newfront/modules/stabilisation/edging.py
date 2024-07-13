import numpy as np
import cv2
from moviepy.editor import VideoFileClip, ImageSequenceClip

def add_reflection_padding(frame, padding_size):
    return cv2.copyMakeBorder(
        frame, padding_size, padding_size, padding_size, padding_size, cv2.BORDER_REFLECT
    )

def remove_padding(frame, padding_size):
    height, width = frame.shape[:2]
    return frame[padding_size:height-padding_size, padding_size:width-padding_size]

def stabilize_frame(prev_frame, curr_frame, prev_transform, padding_size):
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_RGB2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)

    prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30, blockSize=3)
    curr_pts, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None)

    good_old = prev_pts[status == 1]
    good_new = curr_pts[status == 1]

    transform_matrix, _ = cv2.estimateAffinePartial2D(good_old, good_new)

    if transform_matrix is not None:
        prev_transform = np.vstack([transform_matrix, [0, 0, 1]])

    padded_frame = add_reflection_padding(curr_frame, padding_size)
    stabilized_frame = cv2.warpAffine(
        padded_frame, prev_transform[:2], (padded_frame.shape[1], padded_frame.shape[0])
    )

    return remove_padding(stabilized_frame, padding_size), prev_transform

def fill_edge_data(stabilized_frame, background_frame, transform_matrix, padding_size):
    inv_transform_matrix = np.linalg.inv(transform_matrix)

    height, width = stabilized_frame.shape[:2]
    aligned_background = cv2.warpAffine(
        background_frame, inv_transform_matrix[:2], (width, height)
    )

    stabilized_mask = cv2.cvtColor(stabilized_frame, cv2.COLOR_RGB2GRAY) > 0

    filled_frame = stabilized_frame.copy()
    filled_frame[~stabilized_mask] = aligned_background[~stabilized_mask]

    return filled_frame

def detect_background_change(prev_frame, curr_frame, threshold=30):
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_RGB2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)
    frame_diff = cv2.absdiff(prev_gray, curr_gray)
    non_zero_count = np.count_nonzero(frame_diff > threshold)
    change_ratio = non_zero_count / float(prev_gray.size)
    return change_ratio > 0.05  # Adjust this ratio as needed

def stabilize_video(input_video_path, output_video_path, padding_size=50):
    clip = VideoFileClip(input_video_path)

    # Use the first frame as the background model
    first_frame = next(clip.iter_frames())
    background_frame = add_reflection_padding(first_frame, padding_size)

    prev_transform = np.eye(3)
    prev_frame = first_frame
    stabilized_frames = [first_frame]
    change_frames = []

    for i, frame in enumerate(clip.iter_frames()):
        if i == 0:
            continue  # Skip the first frame (already processed)

        stabilized_frame, prev_transform = stabilize_frame(prev_frame, frame, prev_transform, padding_size)
        filled_frame = fill_edge_data(stabilized_frame, background_frame, prev_transform, padding_size)
        stabilized_frames.append(filled_frame)

        # Detect background change
        if detect_background_change(prev_frame, frame):
            change_frames.append(i)

        prev_frame = frame

    # Create a new video clip from the stabilized frames
    fps = clip.fps
    stabilized_clip = ImageSequenceClip(stabilized_frames, fps=fps)
    stabilized_clip.write_videofile(output_video_path, codec='libx264')

    print("Frames where background changed significantly:", change_frames)

# Define the input and output video paths
input_video_path = 'test.mp4'
output_video_path = 'filler5.mp4'

# Stabilize the video
stabilize_video(input_video_path, output_video_path)
