import io
import random
import uuid

from PIL import Image


def generate_photo_file():
    file = io.BytesIO()
    for x in range(3):
        red = random.randrange(0, 255, 10)
        green = random.randrange(0, 255, 10)
        blue = random.randrange(0, 255, 10)
    image = Image.new('RGBA', size=(100, 100), color=(red, green, blue))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file