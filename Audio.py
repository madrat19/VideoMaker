from google.cloud import texttospeech
import re
from mutagen.mp3 import MP3
import nltk
from text_redactor import text_redactor


def expressions_analysis(text):
    edited = text

    # Абб-ры:
    edited = re.sub(r"\bOP\b", "Original poster", edited)
    edited = re.sub(r"\bNAH\b", "No assholes here", edited)
    edited = re.sub(r"\bAH\b", "Asshole", edited)
    edited = re.sub(r"\bAITA\b", "Am i the asshole", edited)
    edited = re.sub(r"\bWIBTA\b", "Would i be the asshole", edited)
    edited = re.sub(r"\bNTA\b", "Not the asshole", edited)
    edited = re.sub(r"\bYTA\b", "You are the Asshole", edited)
    edited = re.sub(r"\bESH\b", "Everyone sucks here", edited)
    edited = re.sub(r"\bINFO\b", "Not Enough Information", edited)
    edited = re.sub(r"\bidk\b", "i dont know", edited, flags=re.IGNORECASE)
    edited = re.sub(r"\bbf\b", "boyfriend", edited, flags=re.IGNORECASE)
    edited = re.sub(r"\bgf\b", "girlfriend", edited, flags=re.IGNORECASE)
    edited = re.sub(r"\wtf\b", "what a fuck", edited, flags=re.IGNORECASE)

    # Возраст/пол:
    expression = re.compile(
        r"(?:\b(?:m|f)\d+\b)|(?:\b\d+(?:f|m)\b)", flags=re.IGNORECASE
    )
    examples = re.findall(expression, edited)
    for ex in examples:
        if ex[0].lower() == "m":
            edited = edited.replace(ex, "male " + ex[1:])
        elif ex[0].lower() == "f":
            edited = edited.replace(ex, "female " + ex[1:])
        elif ex[-1].lower() == "m":
            edited = edited.replace(ex, ex[:-1] + " male")
        elif ex[-1].lower() == "f":
            edited = edited.replace(ex, ex[:-1] + " female")

    # Не букв. символы:
    pattern = re.compile("[*!~]")
    edited = re.sub(pattern, " ", edited)
    edited = edited.replace("...", " ")

    # Сcылки:
    edited = re.sub(r"\bhttp[^ ]+\b", " ", edited)

    return edited


def add_audiofiles(post, shorts):
    speaking_rate = 1.2
    if shorts:
        speaking_rate = 1.2
        path = "shorts/public/media/title_audio_file.mp3"
    else:
        path = "renderer/data/media/title_audio_file.mp3"

    make_audio(post["title"], path, speaking_rate)
    post["title_audio_file"] = "media/title_audio_file.mp3"
    lenght = MP3(path).info.length
    post["title_audio_file_lenght"] = str(round(lenght, 1))

    if post["selftext"]:
        sentences = split_text(post["selftext"])
        post["selftext"] = []
        for n in range(len(sentences)):
            if shorts:
                path = "shorts/public/media/selftext_audio_file_{}.mp3".format(n)
            else:
                path = "renderer/data/media/selftext_audio_file_{}.mp3".format(n)
            make_audio(sentences[n], path, speaking_rate)
            post["selftext"].append({})
            post["selftext"][n]["text"] = sentences[n]
            post["selftext"][n]["audio"] = "media/selftext_audio_file_{}.mp3".format(n)
            length = MP3(path).info.length
            post["selftext"][n]["length"] = str(round(length, 1))

    for n in range(len(post["comments"])):
        add_audiofiles_to_branch(post["comments"][n], n, 0, shorts)


def split_text(text: str):
    text = text_redactor(text)
    text = text.replace("\n", "[#&*^]")
    pst = nltk.PunktSentenceTokenizer()
    sentences = pst.tokenize(text)
    for i in range(len(sentences)):
        sentences[i] = sentences[i].replace("[#&*^]", "\n")
    return sentences


def add_audiofiles_to_branch(branch, n, m, shorts):
    speaking_rate = 1.2
    if shorts:
        speaking_rate = 1.2

    sentences = split_text(branch["body"])
    branch["body"] = []
    for i in range(len(sentences)):
        if shorts:
            path = "shorts/public/media/comment_audio_file_{}_{}_{}.mp3".format(n, m, i)
        else:
            path = "renderer/data/media/comment_audio_file_{}_{}_{}.mp3".format(n, m, i)
        make_audio(sentences[i], path, speaking_rate)
        branch["body"].append({})
        branch["body"][i]["text"] = sentences[i]
        branch["body"][i]["audio"] = "media/comment_audio_file_{}_{}_{}.mp3".format(
            n, m, i
        )
        length = MP3(path).info.length
        branch["body"][i]["length"] = str(round(length, 1))

    if "comments" in branch:
        add_audiofiles_to_branch(branch["comments"], n, m + 1, shorts)


def make_audio(text, file_name, speaking_rate):
    edited_text = expressions_analysis(text)
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=edited_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Wavenet-I"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speaking_rate
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(file_name, "wb") as out:
        out.write(response.audio_content)
