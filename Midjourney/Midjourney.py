import random
import time
import datetime

import Secrets
from Resumable_request import resumable_request


def make_picture(text, auth):
    url = "https://canary.discord.com/api/v9/interactions"
    nonce = str(random.randint(0, 1012477082447380480))
    payload_json = "{Data is hidden}"
    data = {"payload_json": payload_json}
    headers = {"authorization": auth}
    succeed = resumable_request(
        type="post", url=url, data=data, headers=headers, right_code=204
    )
    if succeed == False:
        return False
    date = datetime.datetime.now()
    return date


def upscale_last_picture(auth, last_date):
    url = "https://canary.discord.com/api/v9/channels/{Data is hidden}/messages"
    headers = {"authorization": auth}

    for _ in range(6):
        responce = resumable_request(
            type="get", url=url, headers=headers, right_code=200
        )

        timestamp = responce.json()[0]["timestamp"]
        date = timestamp.replace("T", " ")
        date = date[: date.find("+")]
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        date = date + datetime.timedelta(hours=3)

        if date > last_date:

            message_id = responce.json()[0]["id"]

            nonce = str(random.randint(0, 1012477082447380480))
            payload_json = "{Data is hidden}"
            data = {"payload_json": payload_json}
            url = "https://canary.discord.com/api/v9/interactions"
            responce = resumable_request(
                type="post", url=url, headers=headers, data=data, right_code=204
            )
            if responce == False:
                return False
            date = datetime.datetime.now()
            return date

        else:
            print("No picture to upscale")
            print("Sleeping 30 seconds and check again")
            time.sleep(30)

    print("Couldnt find picture to upscale")
    print("Making new picture")
    return False


def go_fast(auth):
    url = "https://canary.discord.com/api/v9/interactions"
    headers = {"authorization": auth}

    nonce = str(random.randint(0, 1012477082447380480))
    payload_json = "{Data is hidden}"

    data = {"payload_json": payload_json}
    responce = resumable_request(
        type="post", url=url, data=data, headers=headers, right_code=204
    )

    if responce == False:
        return False
    date = datetime.datetime.now()
    return date


def go_relax(auth):
    url = "https://canary.discord.com/api/v9/interactions"
    headers = {"authorization": auth}

    nonce = str(random.randint(0, 1012477082447380480))
    payload_json = "{Data is hidden}"

    data = {"payload_json": payload_json}
    responce = resumable_request(
        type="post", url=url, data=data, headers=headers, right_code=204
    )

    if responce == False:
        return False
    date = datetime.datetime.now()
    return date


def upscale_to_max(auth, last_date):
    url = "https://canary.discord.com/api/v9/channels/{Data is hidden}/messages"
    headers = {"authorization": auth}

    for _ in range(6):
        responce = resumable_request(
            type="get", url=url, headers=headers, right_code=200
        )

        timestamp = responce.json()[0]["timestamp"]
        date = timestamp.replace("T", " ")
        date = date[: date.find("+")]
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        date = date + datetime.timedelta(hours=3)

        if date > last_date:

            message_id = responce.json()[0]["id"]

            nonce = str(random.randint(0, 1012477082447380480))
            payload_json = "{Data is hidden}"
            data = {"payload_json": payload_json}
            url = "https://canary.discord.com/api/v9/interactions"
            responce = resumable_request(
                type="post", url=url, headers=headers, data=data, right_code=204
            )
            if responce == False:
                return False
            date = datetime.datetime.now()
            return date

        else:
            print("No picture to upscale")
            print("Sleeping 30 seconds and check again")
            time.sleep(30)

    print("Couldnt find picture to upscale")
    print("Making new picture")
    return False


def get_last_picture_url(auth, last_date):
    url = "https://canary.discord.com/api/v9/channels/{Data is hidden}/messages"
    headers = {"authorization": auth}
    for _ in range(6):
        responce = resumable_request(
            type="get", url=url, headers=headers, right_code=200
        )
        timestamp = responce.json()[0]["timestamp"]
        date = timestamp.replace("T", " ")
        date = date[: date.find("+")]
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        date = date + datetime.timedelta(hours=3)

        if date > last_date:
            if (
                "attachments" in responce.json()[0]
                and len(responce.json()[0]["attachments"]) != 0
            ):
                if "url" in responce.json()[0]["attachments"][0]:
                    pic_url = responce.json()[0]["attachments"][0]["url"]
                    return pic_url
                else:
                    return False
            else:
                return False

        else:
            print("Failed to find upscaled picture")
            print("Sleeping 30 seconds and check again")
            time.sleep(30)

    print("Failed to find upscaled picture")
    print("Making new picture")
    return False


def get_picture(text, file, auth, max_upscale):
    for _ in range(5):
        date = make_picture(text, auth)
        if date == False:
            print("Failed to make picture")
            print("Making new picture...")
            continue
        print("Making picture...")
        time.sleep(120)
        date = upscale_last_picture(auth, date)
        if date == False:
            continue
        print("Upscaling picture...")
        time.sleep(120)
        if max_upscale:
            go_fast(auth)
            time.sleep(5)
            date = upscale_to_max(auth, date)
            if date == False:
                continue
            print("Upscaling to max...")
            time.sleep(120)

        url = get_last_picture_url(auth, date)
        if url == False:
            continue
        else:
            image = resumable_request(
                type="get", url=url, data={}, headers={}, right_code=200
            )
            with open(file, "wb") as f:
                f.write(image.content)
            print("Picture made successfully!")
            go_relax(auth)
            time.sleep(2)
            return True

    return False


def main(text, file, ar, max_upscale, stile):

    midjourney_request = "{} {} --ar {}".format(text, stile, ar)

    succeed = get_picture(
        midjourney_request,
        file,
        Secrets.discord_auth,
        max_upscale,
    )

    if succeed == False:
        exit("Midjourney seems dead :(")
