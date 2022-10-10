from PIL import Image, ImageFont, ImageDraw, ImageFilter
import os, random


def create_thumbnail(
    title: str,
    path_to_overlay: str = "{Data is hidden}",
    output_path: str = "kekw.png",
):
    font_size = 140
    shadow_offset = 8
    blur_strength = 8
    title = add_new_lines(title, 6)
    dirname = os.path.dirname(__file__)
    path_to_stickers = os.path.join(dirname, "./Stickers")
    path_to_sticker = os.path.join(
        path_to_stickers, (random.choice(os.listdir(path_to_stickers)))
    )
    path_to_font = os.path.join(dirname, "./VERDANAB.TTF")

    background = Image.new("RGBA", (1280, 720), "white")

    with Image.open(path_to_sticker) as sticker:
        sticker = sticker.resize((700, 700), Image.Resampling.LANCZOS)
        sticker = sticker.filter(ImageFilter.GaussianBlur(blur_strength))
        background.paste(
            sticker, (680 - shadow_offset, 60 + shadow_offset), mask=sticker
        )

    with Image.open(path_to_sticker) as sticker:
        sticker = sticker.resize((700, 700), Image.Resampling.LANCZOS)
        background.paste(sticker, (680, 60), mask=sticker)

    blurred = Image.new("RGBA", background.size)

    fnt = ImageFont.truetype(path_to_font, font_size)
    d = ImageDraw.Draw(blurred)

    text_height = 360 - font_size * (calculate_newlines(title) + 1) * 0.5
    d.multiline_text(
        (30 - shadow_offset, text_height + shadow_offset),
        title,
        font=fnt,
        fill=(200, 200, 200),
    )

    blurred = blurred.filter(ImageFilter.GaussianBlur(blur_strength))

    background = Image.alpha_composite(background, blurred)

    draw = ImageDraw.Draw(background)
    draw.multiline_text((30, text_height), title, font=fnt, fill=(0, 0, 0))

    overlay_png = Image.open(path_to_overlay)
    background.paste(overlay_png, (0, 0), mask=overlay_png)

    background.save(output_path, "PNG")


def add_new_lines(input: str, max: int) -> str:
    current = 0
    lines = 0
    buffer = ""
    output = ""

    for char in input:
        current += 1
        if not char.isspace():
            buffer += char
        else:
            if current > max:
                if lines >= 4:
                    return output + "..."
                output += "\n"
                lines += 1
                current = 0
            else:
                if output != "":
                    output += " "
            output += buffer
            buffer = ""

    if buffer != "":
        if current >= max:
            output += "\n"
        else:
            output += " "
        output += buffer

    return output


def calculate_newlines(input: str) -> int:
    return input.count("\n")


def main():
    create_thumbnail('"Be a man little boy"')


if __name__ == "__main__":
    main()
