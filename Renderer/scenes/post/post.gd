class_name Post
extends PanelContainer

signal finished

@onready var data = Data.data

var default_picture := preload('res://icons/default_picture.png')

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
  var avatar_picture = load("res://data/" + data["subreddit_logo_file"] + ".png")
  if avatar_picture:
    %avatar.texture = avatar_picture
  else:
    %avatar.texture = default_picture

  if data["selftext"]:
    for part in data["selftext"]:
      if part["text"] == "!!":
        %content.text += "\n\n"
      else:
        %content.text += part["text"] + " "
  else: %content.queue_free()

func main() -> void:
  play_title_audio(data["title_audio_file"])
  await get_tree().create_timer(data["title_audio_file_lenght"].to_float()).timeout
#  await get_tree().create_timer(0.5).timeout

  var fake_post := get_tree().get_nodes_in_group("fake_post")[0] as PostDynamic

  var target: float = get_parent().position.y

  if data["selftext"]:
    for part in data["selftext"]:
      if fake_post.get_parent().get_rect().end.y + 64 >= get_viewport_rect().size.y:
        print(fake_post.get_parent().get_rect().end.y)
        print(get_viewport_rect().size.y)
        var tween := create_tween()
        var fake_tween := create_tween()
        target -= fake_post.get_parent().get_rect().end.y + 300 - get_viewport_rect().size.y
        tween.tween_property(get_parent(), "position:y", float(target), 0.5).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_BACK)
        fake_tween.tween_property(fake_post.get_parent(), "position:y", float(target), 0.5).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_BACK)

      if part["text"] == "!!":
        %content.visible_characters += 2
        continue
      %content.visible_characters += part["text"].length() + 1
      play_audio(part["audio"])
#      await get_tree().create_timer(0.5).timeout
      await get_tree().create_timer(part["length"].to_float()).timeout

  finish()

func play_title_audio(path: String) -> void:
  play_audio(path)

func load_image(path: String):
  var image = Image.new()
  print(path)
  image.load(path)
  print(image)
  var texture = ImageTexture.new()
  texture.create_from_image(image)
  return texture

func load_mp3(path: String):
  var file := File.new()
  file.open(path, File.READ)
  var sound := AudioStreamMP3.new()
  sound.data = file.get_buffer(file.get_length())
  file.close()
  return sound

func play_audio(path: String):
  var player := AudioStreamPlayer.new()
  player.stream = load_mp3("res://data/" + path)
  player.autoplay = true
  add_child(player)

func finish() -> void:
  var tween := create_tween()
  var fake_tween := create_tween()
  var fake_post := get_tree().get_nodes_in_group("fake_post")[0] as PostDynamic
  tween.tween_property(get_parent(), "position:x", -2000.0, 0.5).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_BACK)
  fake_tween.tween_property(fake_post.get_parent(), "position:x", -2000.0, 0.5).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_BACK)
  emit_signal("finished")
