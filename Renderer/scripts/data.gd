extends Node

var data_path := 'res://data/post.json'
var data: Dictionary

func _ready() -> void:
  load_data()

func load_data() -> void:
  var file := File.new()
  file.open(data_path, File.READ)
  var json := JSON.new()
  var _parse_err = json.parse(file.get_as_text())
  file.close()
  data = json.get_data()
