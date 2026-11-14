# Renders the imported scene at stage 0 and stage 2 and diffs it against tmxrasterizer output.
extends SceneTree

var vp: SubViewport
var area: Node
var frame := 0
var out_dir: String

func _init() -> void:
	out_dir = OS.get_cmdline_user_args()[0]
	vp = SubViewport.new()
	vp.size = Vector2i(320, 288)
	vp.transparent_bg = true
	vp.canvas_item_default_texture_filter = Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	area = (load("res://maps/check_area.tmj") as PackedScene).instantiate()
	area.get_node("logic").visible = false
	area.get_node("markers").visible = false
	vp.add_child(area)

func _process(_d: float) -> bool:
	frame += 1
	if frame == 5:
		_compare("stage0", "tiled_stage0.png")
		area.get_node("restore_1").visible = true
		area.get_node("restore_2").visible = true
	elif frame == 10:
		_compare("stage2", "tiled_stage2.png")
		quit()
	return false

func _compare(tag: String, ref_name: String) -> void:
	var got := vp.get_texture().get_image()
	got.convert(Image.FORMAT_RGBA8)
	got.save_png(out_dir + "/godot_" + tag + ".png")
	var ref := Image.load_from_file(out_dir + "/" + ref_name)
	ref.convert(Image.FORMAT_RGBA8)
	var diff := 0
	var first := Vector2i(-1, -1)
	for y in ref.get_height():
		for x in ref.get_width():
			if not got.get_pixel(x, y).is_equal_approx(ref.get_pixel(x, y)):
				diff += 1
				if first.x < 0: first = Vector2i(x, y)
	print(tag, ": ", got.get_size(), " vs ", ref.get_size(), " differing pixels: ", diff, " first at ", first)
