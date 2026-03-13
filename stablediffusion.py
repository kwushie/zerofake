import torch
from PIL import Image
from io import BytesIO
import json
import os

from diffusers import StableDiffusionImg2ImgPipeline
from accelerate import PartialState

prompt_img_dir = "/srv/scratch/z5419665/coco/coco_small/"
generated_img_dir = "/srv/scratch/z5419665/coco/coco_small_stable_diffusion"

# device = "cuda"
# pipe = StableDiffusionImg2ImgPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16).to(
#     device
# )
pipe = StableDiffusionImg2ImgPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float16)
distributed_state = PartialState()
pipe.to(distributed_state.device)

with open('coco_small_annotations.json', 'r') as file:
    data = json.load(file)
    for (img_name, annotations) in data.items():
        with Image.open(os.path.join(prompt_img_dir, img_name)) as prompt_image:
            with distributed_state.split_between_processes(annotations) as prompt:
                generated_images = pipe(prompt=prompt, image=prompt_image, strength=0.5, guidance_scale=7.5).images
                for i, image in enumerate(generated_images):
                    generated_image_name = os.path.join(generated_img_dir, img_name.split('.')[0] + '_' + str(i) + '.jpg')
                    image.save(generated_image_name, 'JPEG')
