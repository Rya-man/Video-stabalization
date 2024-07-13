import cv2
import numpy as np

def interpolate_frames(frame1, frame2, input_fps, desired_fps):
    fps_ratio = desired_fps / input_fps
    num_interpolations = int(np.ceil(fps_ratio)) - 1

    interpolated_frames = []
    for i in range(1, num_interpolations + 1):
        alpha = i / (num_interpolations + 1)
        interpolated_frame = cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0)
        interpolated_frames.append(interpolated_frame)
    
    return interpolated_frames

def increase_frame_rate(input_file, output_file, desired_fps):
    cap = cv2.VideoCapture(input_file)

    input_fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Input FPS: {input_fps}")
    print(f"Desired Output FPS: {desired_fps}")

    if desired_fps <= 0:
        print("Desired FPS should be greater than 0. Setting it to default value of 30.0")
        desired_fps = 30.0

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, desired_fps, (width, height))
    
    if not out.isOpened():
        print(f"Error: Failed to open output VideoWriter for FPS {desired_fps}")
        return

    prev_frame = None
    total_frames_written = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        out.write(frame)
        total_frames_written += 1
        
        if prev_frame is not None:
            interpolated_frames = interpolate_frames(prev_frame, frame, input_fps, desired_fps)
            for interp_frame in interpolated_frames:
                out.write(interp_frame)
                total_frames_written += 1
        
        prev_frame = frame.copy()

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    if total_frames_written > 0:
        duration_seconds = total_frames_written / desired_fps
        output_fps = total_frames_written / duration_seconds
        print(f"Output FPS: {output_fps}")

input_file = 'input_video.mp4'
output_file = 'output_video.mp4'
desired_fps = 60.0  # Desired output frame rate

increase_frame_rate(input_file, output_file, desired_fps)
