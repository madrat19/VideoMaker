import requests
import httplib2
import time
import random
from apiclient.errors import HttpError


def resumable_request(
    type, url, auth={}, data={}, headers={}, params={}, right_code=200
):
    httplib2.RETRIES = 1
    MAX_RETRIES = 4
    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
    status_code = 0
    error = None
    retry = 0
    while status_code != right_code:
        try:

            if type == "get":
                responce = requests.get(
                    url, auth=auth, data=data, headers=headers, params=params
                )
                status_code = responce.status_code
            elif type == "post":
                responce = requests.post(
                    url, auth=auth, data=data, headers=headers, params=params
                )
                status_code = responce.status_code

            if status_code == right_code:
                return responce
            else:
                print("The request failed with an unexpected code: %s" % status_code)

        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (
                    e.resp.status,
                    e.content,
                )
            else:
                raise

        except Exception as e:

            error = "A retriable error occurred: %s" % e

        if error is not None or status_code != right_code:
            if error is not None:
                print(error)
            retry += 1
            if retry > MAX_RETRIES:
                return False

            max_sleep = 2**retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)
