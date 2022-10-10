import httplib2
import os
import random
import sys
import time
import json

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow


httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(client_secret_file):
    flow = flow_from_clientsecrets(
        client_secret_file,
        scope=YOUTUBE_UPLOAD_SCOPE,
        message="MISSING_CLIENT_SECRETS_MESSAGE",
    )

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()),
    )


def initialize_upload(youtube, options):

    body = dict(
        snippet=dict(
            title=options["title"],
            description=options["description"],
            tags=options["keywords"],
            categoryId=options["category"],
        ),
        status=dict(privacyStatus=options["privacyStatus"]),
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options["file"], chunksize=-1, resumable=True),
    )

    video_id = resumable_upload(insert_request)
    return video_id


def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if "id" in response:
                    print("Video id '%s' was successfully uploaded." % response["id"])
                    return response["id"]
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (
                    e.resp.status,
                    e.content,
                )
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2**retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)


def upload_video(youtube, options):
    try:
        video_id = initialize_upload(youtube, options)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

    return video_id


def set_thumbnail(video_id, thumbnail_file, youtube):
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_file),
    )
    response = request.execute()

    if "items" in response:
        print("thumbnail set successfully")


def build_params():
    params = {}
    with open(
        "youtube/AmItheAssholeShorts/data/permanent_params.json", "r"
    ) as permanent_params:
        params.update(json.load(permanent_params))
    with open("youtube/AmItheAssholeShorts/data/title.txt", "r") as f:
        params["title"] = f.readline() + " #Shorts #AITA"
    with open("youtube/AmItheAssholeShorts/data/post_link.txt", "r") as f:
        link = f.readline()
        params["description"] += "\nOriginal post: {}".format(link)

    return params


def main(client_secret_file):
    params = build_params()
    youtube = get_authenticated_service(client_secret_file)
    video_id = upload_video(youtube, params)

    used_id = {}
    with open("data/used_id.json", "r") as f:
        with open("YouTube/AmItheAssholeShorts/data/article_id.txt", "r") as a:
            article_id = a.read()
            s = f.read()
            used_id = json.loads(s)
            used_id[article_id] = True
    with open("data/used_id.json", "w") as f:
        json.dump(used_id, f)


client_secret_file = "YouTube/AmItheAssholeShorts/data/aitaShortsKey.json"
main(client_secret_file)
