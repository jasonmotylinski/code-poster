import config
from PIL import Image


def to_hex(rgb):
    """Convert RGB to hex."""
    return '#%02x%02x%02x' % rgb


def get_image(path):
    """Reads the image from the path provided. Converts to RGB."""
    conf = config.get()
    im = Image.open(path)
    (width, height) = im.size
    newwidth = int(round(width + (width * conf["svg"]["ratio"]), 0))
    im = im.resize((newwidth, height))
    return im.convert('RGB')
