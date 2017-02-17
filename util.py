from PIL import Image


def to_hex(rgb):
    """Convert RGB to hex."""
    return '#%02x%02x%02x' % rgb


def get_image(path):
    """Reads the image from the path provided. Converts to RGB."""
    im = Image.open(path)
    return im.convert('RGB')
