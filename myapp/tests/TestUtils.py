import io
import uuid

from PIL import Image


def scramble_uploaded_filename(instance, filename):
    # This method scrambles the filename passed to it and returns a unique string
    extension = filename.split(".")[-1]
    return "uploads/{}.{}".format(uuid.uuid4(), extension)


def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file