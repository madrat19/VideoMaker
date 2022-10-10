import json
import os

from Thumbnail import create_thumbnail
from Resumable_request import resumable_request
from Title_reduction import title_reduction

import Audio
import Authorization
import Getting_data
import Images
import Secrets

client_id = Secrets.client_id
secret_key = Secrets.secret_key
username = Secrets.username
password = Secrets.password
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{Data is hidden}"
headers = Authorization.authorization(client_id, secret_key, username, password)


def check_repeats(subreddit, headers, shorts, mrReddit):
    if mrReddit:
        file_name = "data/mrReddit_used_id.json"
    else:
        file_name = "data/used_id.json"

    url = "https://oauth.reddit.com/r/{}/top".format(subreddit)
    posts = resumable_request(
        type="get", url=url, headers=headers, params={"limit": 50}, right_code=200
    )

    if posts == False:
        exit("failed to get posts here")

    if shorts:
        max_symbol = 1150
    else:
        max_symbol = 10000000

    with open(file_name, "r") as f:
        s = f.read()
        used_id = json.loads(s)

    for order_on_page in range(50):
        article_id = posts.json()["data"]["children"][order_on_page]["data"]["name"]
        symbol_q = len(
            posts.json()["data"]["children"][order_on_page]["data"]["selftext"]
        )
        if article_id not in used_id and symbol_q < max_symbol:

            if mrReddit:
                path = "YouTube/MrReddit/data/article_id.txt"
            else:
                if shorts:
                    path = "YouTube/{}Shorts/data/article_id.txt".format(subreddit)
                else:
                    path = "YouTube/{}/data/article_id.txt".format(subreddit)

            with open(path, "w") as f:
                f.write(article_id)

            if mrReddit:
                path = "YouTube/MrReddit/data/post_link.txt"
            else:
                if shorts:
                    path = "YouTube/{}Shorts/data/post_link.txt".format(subreddit)
                else:
                    path = "YouTube/{}/data/post_link.txt".format(subreddit)

            with open(path, "w") as f:
                f.write(
                    "https://www.reddit.com/r/{}/comments/{}/".format(
                        subreddit, article_id[3:]
                    )
                )

            return order_on_page


def main(subreddit, headers, shorts=False):
    folder = subreddit
    if subreddit == "MrReddit":
        subreddit = "AskReddit"
        mrReddit = True
    else:
        mrReddit = False

    order_on_page = check_repeats(
        subreddit=subreddit, headers=headers, shorts=shorts, mrReddit=mrReddit
    )

    if shorts:
        if subreddit == "AmItheAsshole":
            max_branches = 0
            min_branches = 0
        elif subreddit == "AskReddit":
            max_branches = 10
            min_branches = 10
    else:
        max_branches = 20
        min_branches = 15

    post = Getting_data.get_post(
        subreddit=subreddit,
        order_on_page=order_on_page,
        max_branches=max_branches,
        min_branches=min_branches,
        headers=headers,
        shorts=shorts,
    )

    if shorts:
        path = "youtube/{}Shorts/data/title.txt".format(subreddit)
        if folder == "MrReddit":
            path = "youtube/MrReddit/data/title.txt"
    else:
        path = "youtube/{}/data/title.txt".format(subreddit)
    with open(path, "w") as f:
        title = post["title"]
        title = title_reduction(title, subreddit, "title")
        f.write(title)

    if not shorts:
        text = post["title"]
        text = title_reduction(text, subreddit, "thumbnail")

        create_thumbnail(
            title=text,
            path_to_overlay="Thumbnails/{}_Thumbnail_Overlay.png".format(subreddit),
            output_path="YouTube/{}/data/thumbnail.png".format(subreddit),
        )

    Images.add_images(post, shorts)
    Audio.add_audiofiles(post, shorts)

    if shorts:
        path = "shorts/public/post.json"
    else:
        path = "renderer/data/post.json"

    with open(path, "w") as f:
        json.dump(post, f)


subreddit = sys.argv[1]
shorts = sys.argv[2]
# subreddit = "AskReddit"
# shorts = "false"
if shorts == "true":
    shorts = True
else:
    shorts = False
main(subreddit=subreddit, headers=headers, shorts=shorts)

print("Done!")
