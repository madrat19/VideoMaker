import requests
from Resumable_request import resumable_request


def authorization(client_id, secret_key, username, password):
    client_auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
    post_data = {"grant_type": "password", "username": username, "password": password}
    headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}

    url = "https://www.reddit.com/api/v1/access_token"
    response = resumable_request(
        type="post",
        url=url,
        auth=client_auth,
        data=post_data,
        headers=headers,
        right_code=200,
    )
    if response == False:
        exit("failed to get reddit token")

    token = response.json()["access_token"]
    headers["Authorization"] = f"bearer {token}"

    url = "https://oauth.reddit.com/api/v1/me"
    response = resumable_request(type="get", url=url, headers=headers, right_code=200)

    if response == False:
        exit("not authorized!")

    if response.status_code == 200:
        print("authorized!")
    else:
        print("something wrong with authorization!")

    return headers
