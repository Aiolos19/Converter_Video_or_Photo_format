import os
import cv2
import numpy as np
from tqdm import tqdm

input_directory = r'D:\Converter'

def unblur_frame_gpu(frame):
    # Upload frame to GPU
    gpu_frame = cv2.cuda_GpuMat()
    gpu_frame.upload(frame)

    # Create kernel on GPU
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]], dtype=np.float32)
    gpu_kernel = cv2.cuda_GpuMat()
    gpu_kernel.upload(kernel)

    # Apply filter on GPU
    gpu_result = cv2.cuda.filter2D(gpu_frame, -1, gpu_kernel)

    # Download result from GPU
    result = gpu_result.download()
    return result

def process_video(input_video_file, output_video_file):
    try:
        cap = cv2.VideoCapture(input_video_file)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file: {input_video_file}")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        out = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))

        for _ in tqdm(range(total_frames), desc=f"Processing {os.path.basename(input_video_file)}"):
            ret, frame = cap.read()
            if not ret:
                break
            unblurred_frame = unblur_frame_gpu(frame)
            out.write(unblurred_frame)

    except Exception as e:
        print(f"Error processing {input_video_file}: {str(e)}")
    finally:
        if 'cap' in locals():
            cap.release()
        if 'out' in locals():
            out.release()

def batch_unblur_videos(directory):
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return

    video_files = [f for f in os.listdir(directory) if f.lower().endswith(('.mp4', '.avi', '.mov'))]

    if not video_files:
        print(f"No video files found in {directory}")
        return

    for filename in video_files:
        input_video_file = os.path.join(directory, filename)
        output_video_file = os.path.join(directory, f'unblurred_{filename}')
        process_video(input_video_file, output_video_file)
        print(f"Process completed: {input_video_file} -> {output_video_file}")

if __name__ == "__main__":
    # Check if CUDA is available
    if cv2.cuda.getCudaEnabledDeviceCount() == 0:
        print("No CUDA-capable GPU found. Exiting.")
    else:
        print(f"Found {cv2.cuda.getCudaEnabledDeviceCount()} CUDA-capable GPU(s).")
        batch_unblur_videos(input_directory)