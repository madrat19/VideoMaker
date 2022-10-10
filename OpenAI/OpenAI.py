import Secrets
import openai

openai.api_key = Secrets.openAI_key


def build_promt(text, subreddit, place):
    if subreddit == "AmItheAsshole":
        if place == "thumbnail":
            from AITAThumbnailPromt import promt

            promt = promt + "text: {" + text + "}\ncaption:"
        if place == "title":
            from AITATitlePromt import promt

            promt = promt + "text: {" + text + "}\ncaption:"

    if subreddit == "AskReddit":
        if place == "thumbnail":
            from AskThumbnailPromt import promt

            promt = promt + "text: {" + text + "}\ncaption:"
        if place == "title":
            from AskTitlePromt import promt

            promt = promt + "text: {" + text + "}\ncaption:"

    return promt


def capturing(text, subreddit, place):
    promt = build_promt(text, subreddit, place)

    responce = openai.Completion.create(
        model="text-davinci-002",
        prompt=promt,
        max_tokens=20,
        temperature=0.7,
    )

    ans = responce["choices"][0]["text"]
    ans = ans.replace("{", "")
    ans = ans.replace("}", "")

    if "\n" in ans:
        ans = ans[: ans.find("\n")]
    return ans[1:]
