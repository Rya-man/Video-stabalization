import torch
import requests
from PIL import Image
from diffusers import StableDiffusionDepth2ImgPipeline

pipe = StableDiffusionDepth2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-depth",
    torch_dtype=torch.float16,
).to("cuda")

img = Image.open("test_img.jpg")

prompt = "Extend the edges of the frame to increase the frame size while maintaining the original style and content. Generate new areas around the edges that seamlessly blend with the existing image, preserving the overall composition and visual elements."
negative_prompt = "Do not alter or change anything inside the current boundaries of the image. Avoid modifying the central content and existing features. Only generate and extend the areas beyond the current edges."

img_extd=pipe(prompt=prompt, image=img, negative_prompt=negative_prompt, strength=0.7).images[0]

img_extd.save("ext.jpg")