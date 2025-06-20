from PIL import Image # type: ignore
import os

def compress_image(input_path, output_path, quality=70):
    with Image.open(input_path) as img:
        img.save(output_path, optimize=True, quality=quality)
