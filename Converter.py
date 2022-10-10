# pip install Pillow

from PIL import Image


def convert_image(path: str, path_to_overlay: str):
    # file is not a png
    if not path.endswith(".png"):
        return

    # open image in png format
    img_png = Image.open(path)
    img_png = img_png.resize((1280, 720))
    overlay_png = Image.open(path_to_overlay)

    img_png.paste(overlay_png, (0, 0), mask=overlay_png)
    img_png.save(path[0:-3] + "jpg", "JPEG", quality=80)
