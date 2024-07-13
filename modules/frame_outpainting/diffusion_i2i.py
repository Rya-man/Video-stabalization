import torch
import requests
from PIL import Image
from diffusers import StableDiffusionDepth2ImgPipeline
import os

def extend_frame_i2i(image_path,pipe):
    
    img = Image.open(image_path)
    prompt = "Extend the edges of the frame to increase the frame size while maintaining the original style and content. Generate new areas around the edges that seamlessly blend with the existing image, preserving the overall composition and visual elements."
    negative_prompt = "Do not alter or change anything inside the current boundaries of the image. Avoid modifying the central content and existing features. Only generate and extend the areas beyond the current edges."
        
    img=pipe(prompt=prompt, image=img, negative_prompt=negative_prompt, strength=0.7).images[0]
    return img

def extend_frames_i2i(source_path):
    
    pipe = StableDiffusionDepth2ImgPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-depth",
        torch_dtype=torch.float16,
    ).to("cuda")

    dir_name=os.path.dirname(source_path)
    destination_path =  os.path.join(dir_name,'frames_extended')
    os.makedirs(destination_path, exist_ok=True)

    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    for filename in os.listdir(source_path):
        if any(filename.lower().endswith(ext) for ext in supported_extensions):
            file_path = os.path.join(source_path, filename)
            extended_image = extend_frame_i2i(file_path, pipe)
            save_path=os.path.join(destination_path, filename)
            extended_image.save(save_path)
    return destination_path

if __name__ == "__main__":
    video_path=r"testy.mp4"
    extend_frames_i2i(video_path)
