import OpenAI


def title_reduction(title: str, subreddit, place):
    if subreddit == "AmItheAsshole":
        if title.startswith("AITA for") or title.startswith("AITA For"):
            title = title[9:]
        elif title.startswith("AITA"):
            title = title[5:]
        elif title.startswith("WIBTA for") or title.startswith("WIBTA For"):
            title = title[10:]
        elif title.startswith("WIBTA if") or title.startswith("WIBTA If"):
            title = title[9:]
        elif title.startswith("WIBTA"):
            title = title[6:]

    title = OpenAI.capturing(title, subreddit, place)

    return title
