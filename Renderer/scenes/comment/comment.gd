class_name Comment
extends MarginContainer

signal finished

@onready var comments = Data.data["comments"]

var default_picture := preload('res://icons/default_picture.png')

var comment: Dictionary
var index: int
var slide: int

func _ready() -> void:
  if get_viewport_rect().size.x == 1080:
    %content.custom_minimum_size.x = 800
    size_flags_horizontal = 4
    size_flags_vertical = 4
  fill_text()
  reposition()
  main()

func fill_text() -> void:
  %author.text = comment["author"]
  %ups.text = comment["ups"]
  %content.text = ""
  var avatar_picture = load("res://data/" + comment["avatar_file"])
  if avatar_picture:
    %avatar.texture = avatar_picture
  else:
    %avatar.texture = default_picture
  %time.text = comment["time_ago"]

  var is_first = true
  for part in comment["body"]:
    if part["text"] == "!!":
      %content.text += "\n\n"
    else:
      %content.text += part["text"] + " "
    if is_first:
      %content.visible_characters += part["text"].length() + 1
      is_first = false


func reposition():
  var tween = create_tween()
  tween.tween_property(get_parent(), "position", get_parent().get_parent().target, 0.5).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_BACK)

func main() -> void:
  await get_tree().create_timer(0.5).timeout
#  var fake_post := get_tree().get_nodes_in_group("fake_post")[0] as PostDynamic

#  var target := 0
  var is_first = true
  for part in comment["body"]:
#    if fake_post.get_parent().get_rect().end.y + 128 >= get_viewport_rect().size.y:
#      var tween := create_tween()
#      var fake_tween := create_tween()
#      target -= fake_post.get_parent().get_rect().end.y + 256 - get_viewport_rect().size.y
#      tween.tween_property(get_parent(), "position:y", float(target), 0.5)
#      fake_tween.tween_property(fake_post.get_parent(), "position:y", float(target), 0.5)

    if part["text"] == "!!":
      %content.visible_characters += 2
      continue
    if is_first:
      is_first = false
    else:
      %content.visible_characters += part["text"].length() + 1
#
#    var tween = create_tween()
#    tween.tween_property(get_parent().get_parent(), "global_position", get_parent().get_parent().get_parent().target, 0.1)
    play_audio(part["audio"])
    await get_tree().create_timer(part["length"].to_float()).timeout
#    await get_tree().create_timer(0.5).timeout

  if "comments" in comment and !get_viewport_rect().size.x == 1080:
    get_parent().get_parent().target.y -= 150
    get_parent().get_parent().spawn_comment(comment["comments"], slide + 1)
  else:
    finish()

func load_image(path: String):
  var image := Image.new()
  image.load(path)
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
  get_parent().is_finished = true
  var pos: float = get_parent().position.x - 2000
  var tween = create_tween()
  tween.tween_property(get_parent(), "position:x", pos, 0.5).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_BACK)
  print("finish: ", get_parent())
  emit_signal("finished")
