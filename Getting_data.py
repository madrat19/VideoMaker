import datetime
from Resumable_request import resumable_request


def get_post(subreddit, order_on_page, headers, max_branches, min_branches, shorts):

    posts_limit = str(order_on_page + 1)

    url = "https://oauth.reddit.com/r/{}/top".format(subreddit)
    posts = resumable_request(
        type="get",
        url=url,
        headers=headers,
        params={"limit": posts_limit},
        right_code=200,
    )
    if posts == False:
        exit("failed to get posts")

    article_id = posts.json()["data"]["children"][order_on_page]["data"]["name"]

    post_date = posts.json()["data"]["children"][order_on_page]["data"]["created"]
    date = datetime.datetime.fromtimestamp(post_date)
    date = datetime.datetime.now() - date
    date = (datetime.datetime.min + date).time()
    if date.hour > 0:
        time_ago = str(date.hour) + " hr. ago"
    else:
        time_ago = str(date.minute) + " min. ago"

    url = "https://oauth.reddit.com/r/{}/comments/{}".format(subreddit, article_id[3:])
    comm = resumable_request(
        type="get",
        url=url,
        headers=headers,
        params={"depth": "10", "sort": "top"},
        right_code=200,
    )
    if comm == False:
        exit("failed to get coments")

    url = "https://oauth.reddit.com/r/{}/about".format(subreddit)
    sub = resumable_request(type="get", url=url, headers=headers, right_code=200)
    if sub == False:
        exit("failed to get subreddit")

    sub_logo_url = sub.json()["data"]["community_icon"]
    sub_logo_url = sub_logo_url[: sub_logo_url.find("png") + 3]

    title = posts.json()["data"]["children"][order_on_page]["data"]["title"]
    selftext = posts.json()["data"]["children"][order_on_page]["data"]["selftext"]
    if selftext == "":
        selftext = False
    ups = posts.json()["data"]["children"][order_on_page]["data"]["ups"]
    author = posts.json()["data"]["children"][order_on_page]["data"]["author"]
    num_comments = posts.json()["data"]["children"][order_on_page]["data"][
        "num_comments"
    ]

    if subreddit == "AmItheAsshole":  # comment branch logic
        branch_ups_threshold = ups * 0.025
    if subreddit == "AskReddit":
        branch_ups_threshold = ups * 0.025

    comments = []

    if subreddit == "AmItheAsshole":  # Первой коммент - закреп
        nomber_on_page = 1
    if subreddit == "AskReddit":  # Первый комент норм
        nomber_on_page = 0

    for n in range(nomber_on_page, max_branches):
        comment = comm.json()[1]["data"]["children"][n]["data"]
        if comment["author"] == "[deleted]":
            continue
        elif comment["ups"] < branch_ups_threshold and n > min_branches:
            break

        depth_ups_threshold = comment["ups"] * 0.05  # comment depth logic
        comments_tree = get_comments_branch(
            comment=comment,
            headers=headers,
            depth_ups_threshold=depth_ups_threshold,
            shorts=shorts,
        )
        comments.append(comments_tree)

    post = {}
    post["author"] = author
    post["title"] = title
    post["time_ago"] = time_ago
    post["title_audio_file"] = ""
    post["title_audio_file_lenght"] = ""
    post["ups"] = str(ups)
    post["subreddit_name"] = "r/" + subreddit
    post["subreddit_logo_file"] = ""
    post["num_comments"] = str(num_comments)
    post["sub_logo_url"] = sub_logo_url
    post["selftext"] = selftext
    post["comments"] = comments

    return post


def get_comments_branch(comment, headers, depth_ups_threshold, shorts):
    c_author = comment["author"]

    comment_date = comment["created"]
    date = datetime.datetime.fromtimestamp(comment_date)
    date = datetime.datetime.now() - date
    date = (datetime.datetime.min + date).time()
    if date.hour > 0:
        time_ago = str(date.hour) + " hr. ago"
    else:
        time_ago = str(date.minute) + " min. ago"

    url = "https://oauth.reddit.com/user/{}/about".format(c_author)
    c_user_info = resumable_request(
        type="get", url=url, headers=headers, right_code=200
    )
    if c_user_info == False:
        exit("failed to get c_user_info")

    c_user_info = c_user_info.json()["data"]
    if "snoovatar_img" in c_user_info:
        c_avatar_url = c_user_info["snoovatar_img"]
        if c_avatar_url == "":
            c_avatar_url = c_user_info["icon_img"]
            if "styles" in c_avatar_url:
                if "png" in c_avatar_url:
                    c_avatar_url = c_avatar_url[: c_avatar_url.find("png") + 3]
                elif "jpg" in c_avatar_url:
                    c_avatar_url = c_avatar_url[: c_avatar_url.find("jpg") + 3]
                else:
                    c_avatar_url = "https://i.redd.it/snoovatar/avatars/6b275ae2-35b8-4516-b69a-adf6b73ccd40.png"
    else:
        c_avatar_url = "https://i.redd.it/snoovatar/avatars/6b275ae2-35b8-4516-b69a-adf6b73ccd40.png"

    c_ups = comment["ups"]
    body = comment["body"]

    comment_data = {
        "author": c_author,
        "time_ago": time_ago,
        "avatar_url": c_avatar_url,
        "avatar_file": "",
        "ups": str(c_ups),
        "body": body,
    }
    if not shorts:
        if comment["replies"] != "":
            reply = comment["replies"]["data"]["children"][0]["data"]
            if "author" in reply and reply["author"] != "[deleted]":
                if reply["ups"] > depth_ups_threshold:
                    comment_data["comments"] = get_comments_branch(
                        reply, headers, depth_ups_threshold, shorts
                    )

    return comment_data
