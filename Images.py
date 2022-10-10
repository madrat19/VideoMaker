from Resumable_request import resumable_request


def add_images(post, shorts):

    url = post["sub_logo_url"]
    subreddit_logo = resumable_request(type="get", url=url, right_code=200)
    if subreddit_logo == False:
        exit("failed to get subreddit logo")

    if shorts:
        path = "shorts/public/media/subreddit_logo.png"
    else:
        path = "renderer/data/media/subreddit_logo.png"
    with open(path, "wb") as f:
        f.write(subreddit_logo.content)
    post["subreddit_logo_file"] = "media/subreddit_logo"
    post.pop("sub_logo_url")

    for n in range(len(post["comments"])):
        add_images_to_branch(post["comments"][n], n, 0, shorts)


def add_images_to_branch(branch, n, m, shorts):

    url = branch["avatar_url"]
    c_author_avatar = resumable_request(type="get", url=url, right_code=200)
    if c_author_avatar == False:
        print("failed to get c_author_avatar_{}_{}".format(n, m))
    else:
        img_format = "png"

        if "png" in branch["avatar_url"]:
            img_format = "png"
        elif "jpg" in branch["avatar_url"]:
            img_format = "jpg"

        if shorts:
            path = "shorts/public/media/commentator_avatar_{}_{}.{}".format(
                n, m, img_format
            )
        else:
            path = "renderer/data/media/commentator_avatar_{}_{}.{}".format(
                n, m, img_format
            )
        with open(path, "wb") as f:
            f.write(c_author_avatar.content)
        branch["avatar_file"] = "media/commentator_avatar_{}_{}.{}".format(
            n, m, img_format
        )
        branch.pop("avatar_url")

    if "comments" in branch:
        add_images_to_branch(branch["comments"], n, m + 1, shorts)
