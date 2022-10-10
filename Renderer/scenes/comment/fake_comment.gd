class_name FakeComment
extends MarginContainer

signal fake_comment_finished

@onready var comments = Data.data["comments"]
var comment: Dictionary
var index: int
var slide: int

var comment_handle

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
  %avatar.texture = load("res://data/" + comment["avatar_file"])
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
  if get_parent().get_rect().end.y + 64 >= get_viewport_rect().size.y:
    update_minimum_size()
    get_parent().get_parent().target.y -= get_parent().get_rect().end.y + 300 - get_viewport_rect().size.y

  if !get_viewport_rect().size.x == 1080:
    get_parent().get_parent().target.x = -slide * 128 + 64
  var tween = create_tween()
  if get_parent() != null:
    tween.tween_property(get_parent(), "position", get_parent().get_parent().target, 0.5).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_BACK)
  comment_handle = get_tree().get_nodes_in_group("comment_handle")[0]
  if comment_handle != null and not comment_handle.is_finished:
    var main_tween = create_tween()
    main_tween.tween_property(comment_handle, "position", get_parent().get_parent().target, 0.5).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_BACK)

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
    reposition()
#    await get_tree().create_timer(0.5).timeout
    await get_tree().create_timer(part["length"].to_float()).timeout

  if !"comments" in comment or get_viewport_rect().size.x == 1080:
    finish()

func finish() -> void:
  get_parent().is_finished = true
  var pos: float = get_parent().position.x - 2000
  var tween = create_tween()
  tween.tween_property(get_parent(), "position:x", pos, 0.5).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_BACK)
  emit_signal("fake_comment_finished")
