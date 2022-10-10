class_name PostDynamic
extends PanelContainer

signal finished

@onready var data = Data.data

func _ready() -> void:
  if get_viewport_rect().size.x == 1080:
    %content.custom_minimum_size.x = 800
  fill_text()
  main()

func fill_text() -> void:
  %sub.text = data["subreddit_name"]
  %author.text = 'Posted by u/' + data["author"]
  %title.text = data["title"]
  %ups.text = data["ups"]
  %comments.text = data["num_comments"] + " comments"
  %content.text = ""
  %time.text = data["time_ago"]
  %avatar.texture = load("res://data/" + data["subreddit_logo_file"] + ".png")

  if data["selftext"]:
    for part in data["selftext"]:
      if part["text"] == "!!":
        %content.text += "\n\n"
      else:
        %content.text += part["text"] + " "
  else: %content.queue_free()

func main() -> void:
  await get_tree().create_timer(data["title_audio_file_lenght"].to_float()).timeout
#  await get_tree().create_timer(0.5).timeout

  if data["selftext"]:
    for part in data["selftext"]:
      if part["text"] == "!!":
        %content.visible_characters += 2
        continue
      %content.visible_characters += part["text"].length() + 1
      await get_tree().create_timer(part["length"].to_float()).timeout
#      await get_tree().create_timer(0.5).timeout
