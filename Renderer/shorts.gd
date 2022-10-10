extends Control

@onready var handle := $handle
@onready var fake_handle := $handle2
var comment_handle
var fake_comment_handle
var another_handle
var fake_another_handle
var is_another := false

var post_scene := preload('res://scenes/post/post.tscn')
var post_dynamic_scene := preload('res://scenes/post/post_dynamic.tscn')

#var comment_handle_scene := preload('res://scenes/comment/short_comment_handle.tscn')
#var fake_comment_handle_scene := preload('res://scenes/comment/short_comment_handle2.tscn')

var comment_handle_scene := preload('res://scenes/comment/comment_handle.tscn')
var fake_comment_handle_scene := preload('res://scenes/comment/comment_handle2.tscn')

var comment_scene := preload('res://scenes/comment/comment.tscn')
var fake_comment_scene := preload('res://scenes/comment/fake_comment.tscn')

var farewell_scene := preload('res://scenes/farewell/farewell.tscn')

var index := 0
var fake_index :=0
var target := Vector2(64, 64)

var background_music: AudioStreamPlayer

var frame := 0

func _ready() -> void:
  if get_viewport_rect().size.x == 1080:
    target = Vector2(64, 660)
#  print(get_viewport_rect().size)
  background_music = play_audio('res://audio/Smokey\'s Lounge - TrackTribe.mp3', -16.0, true)
  spawn_post()
#  on_comment_finished()
#  spawn_farewell()
  pass

func _process(delta: float) -> void:
  frame += 1
  if frame >= 3540:
    quit()

func quit():
  get_tree().quit()

func spawn_post() -> void:
  var post_dyn_instance := post_dynamic_scene.instantiate() as PostDynamic
  fake_handle.add_child(post_dyn_instance)

  var post_instance := post_scene.instantiate() as Post
  post_instance.finished.connect(on_post_finished)
  handle.add_child(post_instance)

func spawn_farewell() -> void:
  var farewell_instance := farewell_scene.instantiate()
  add_child(farewell_instance)
  farewell_instance.position = Vector2(1080, 0)
  var tween = get_tree().create_tween()
  tween.tween_property(farewell_instance, "position:x", 0.0, 0.5).set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_BACK)
  var tween_sound = get_tree().create_tween()
  tween_sound.tween_property(background_music, "volume_db", -64.0, 5).set_trans(Tween.TRANS_EXPO)
  await get_tree().create_timer(5).timeout
  quit()

func spawn_comment_handles():
  if not is_another:
    fake_comment_handle = fake_comment_handle_scene.instantiate()
    fake_comment_handle.position = Vector2(1080, 660)
    add_child(fake_comment_handle)
    comment_handle = comment_handle_scene.instantiate()
    comment_handle.position = Vector2(1080, 660)
    add_child(comment_handle)
  else:
    fake_another_handle = fake_comment_handle_scene.instantiate()
    fake_another_handle.position = Vector2(1080, 660)
    add_child(fake_another_handle)
    another_handle = comment_handle_scene.instantiate()
    another_handle.position = Vector2(1080, 660)
    add_child(another_handle)

func spawn_comment(comment: Dictionary, slide: int) -> void:
  var comment_instance := comment_scene.instantiate() as Comment
  comment_instance.index = index
  comment_instance.comment = comment
  comment_instance.slide = slide
  comment_instance.add_theme_constant_override("margin_left", 128 * slide)
  comment_instance.finished.connect(on_comment_finished)
  if not is_another:
    comment_handle.add_child(comment_instance)
  else:
    another_handle.add_child(comment_instance)

  var fake_comment_instance := fake_comment_scene.instantiate() as FakeComment
  fake_comment_instance.index = fake_index
  fake_comment_instance.comment = comment
  fake_comment_instance.slide = slide
  fake_comment_instance.add_theme_constant_override("margin_left", 128 * slide)
  if not is_another:
    fake_comment_handle.add_child(fake_comment_instance)
  else:
    fake_another_handle.add_child(fake_comment_instance)

func on_post_finished() -> void:
  play_audio('res://audio/short_swoosh.mp3', -12.0)
  spawn_comment_handles()
  spawn_comment(Data.data["comments"][index], 0)
  await get_tree().create_timer(0.5).timeout
  handle.queue_free()
  fake_handle.queue_free()

func on_comment_finished() -> void:
  is_another = !is_another
  target = Vector2(64, 660)
  play_audio('res://audio/short_swoosh.mp3', -12.0)
  spawn_comment_handles()
  index += 1
  if Data.data["comments"].size() > index:
    spawn_comment(Data.data["comments"][index], 0)
  else:
    spawn_farewell()
  await get_tree().create_timer(0.5).timeout
  print(comment_handle)
  print(another_handle)
  if is_another:
    comment_handle.queue_free()
    fake_comment_handle.queue_free()
  else:
    another_handle.queue_free()
    fake_another_handle.queue_free()

func load_mp3(path: String, loop: bool):
  var file := File.new()
  file.open(path, File.READ)
  var sound := AudioStreamMP3.new()
  sound.data = file.get_buffer(file.get_length())
  file.close()
  sound.loop = loop
  return sound

func play_audio(path: String, volume := 0.0, loop := false):
  var player := AudioStreamPlayer.new()
  if path.begins_with("res://"):
    player.stream = load_mp3(path, loop)
  else:
    player.stream = load_mp3("res://data/" + path, loop)
  player.volume_db = volume
  player.autoplay = true
  add_child(player)
  return player
