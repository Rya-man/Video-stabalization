from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim

def compare_frame(image_path1, image_path2):
    img1 = Image.open(image_path1).convert('L')
    img2 = Image.open(image_path2).convert('L')
    
    img_array1 = np.array(img1)
    img_array2 = np.array(img2)
    
    if img_array1.shape != img_array2.shape:
        raise ValueError("Images must have the same dimensions for comparison")
    
    similarity_score, _ = ssim(img_array1, img_array2, full=True)
    
    return similarity_score

if __name__ == "__main__":
# Example usage
    image_path1 = '/kaggle/input/frames/frames/frame_1_57.png'
    image_path2 = '/kaggle/input/frames/frames/frame_1_60.png'

    try:
        similarity = compare_frame(image_path1, image_path2)
        print(f"Similarity score: {similarity}")
    except ValueError as e:
        print(f"Error: {e}")
