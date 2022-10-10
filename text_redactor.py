import demoji
from html import unescape


def text_redactor(text):
    text = demoji.replace(text, "")
    text = text.replace("&#x200B", " ")
    text = unescape(text)

    return text
