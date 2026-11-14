# Compares the YATI-imported scene against the Tiled .tmj it came from.
extends SceneTree

const FH := 0x80000000
const FV := 0x40000000
const FD := 0x20000000

func _init() -> void:
	var tmj: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://maps/check_area.tmj"))
	var sets := []  # [{firstgid, columns, name, tilecount}]
	for ts in tmj.tilesets:
		var tsj: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://maps/" + ts.source))
		sets.append({"firstgid": int(ts.firstgid), "columns": int(tsj.columns), "name": tsj.name, "w": int(tsj.imagewidth), "h": int(tsj.imageheight)})
	var scene: PackedScene = load("res://maps/check_area.tmj")
	var root: Node = scene.instantiate()
	var problems := 0
	var checked_cells := 0
	var flipped_cells := 0
	for layer in tmj.layers:
		var node := root.get_node_or_null(NodePath(layer.name))
		if node == null:
			print("MISSING node for layer ", layer.name); problems += 1; continue
		if layer.type == "tilelayer":
			var tml := node as TileMapLayer
			if tml.visible != layer.visible: print("visible mismatch ", layer.name); problems += 1
			if not is_equal_approx(tml.modulate.a, float(layer.opacity)): print("opacity mismatch ", layer.name); problems += 1
			var expected_used := 0
			for i in layer.data.size():
				var raw := int(layer.data[i])
				var cell := Vector2i(i % int(tmj.width), i / int(tmj.width))
				if raw == 0:
					if tml.get_cell_source_id(cell) != -1: print("extra cell ", layer.name, cell); problems += 1
					continue
				expected_used += 1
				var gid := raw & 0x1FFFFFFF
				var si := -1
				for k in sets.size():
					if gid >= sets[k].firstgid: si = k
				var local: int = gid - sets[si].firstgid
				var want_coords := Vector2i(local % sets[si].columns, local / sets[si].columns)
				var src_id := tml.get_cell_source_id(cell)
				var coords := tml.get_cell_atlas_coords(cell)
				var alt := tml.get_cell_alternative_tile(cell)
				var src := tml.tile_set.get_source(src_id) as TileSetAtlasSource if src_id >= 0 else null
				if src == null:
					print("no source ", layer.name, cell); problems += 1; continue
				var tex_size := src.texture.get_size()
				if Vector2i(tex_size) != Vector2i(sets[si].w, sets[si].h) or coords != want_coords:
					print("tile mismatch ", layer.name, cell, " want ", sets[si].name, want_coords, " got src ", src_id, " ", tex_size, coords); problems += 1
				var td := src.get_tile_data(coords, alt)
				var want_h := (raw & FH) != 0; var want_v := (raw & FV) != 0; var want_d := (raw & FD) != 0
				if want_h or want_v or want_d: flipped_cells += 1
				if td.flip_h != want_h or td.flip_v != want_v or td.transpose != want_d:
					print("flip mismatch ", layer.name, cell, " want h/v/d ", want_h, want_v, want_d, " got ", td.flip_h, td.flip_v, td.transpose); problems += 1
				if sets[si].name == "logic":
					var kinds := ["wall", "patch_meadow", "patch_wetland", "ledge"]
					if td.get_custom_data("kind") != kinds[local]: print("custom data mismatch ", cell); problems += 1
				checked_cells += 1
			if tml.get_used_cells().size() != expected_used:
				print("used-cell count mismatch ", layer.name, " ", tml.get_used_cells().size(), " vs ", expected_used); problems += 1
		elif layer.type == "objectgroup":
			for o in layer.objects:
				var n: Node2D = node.get_node_or_null(NodePath(o.name))
				if n == null: n = node.get_node_or_null(NodePath(o.name + " (SB)"))
				if n == null:
					print("MISSING marker ", o.name); problems += 1; continue
				var want_pos := Vector2(o.x, o.y)
				if n.position != want_pos: print("position mismatch ", o.name, " ", n.position, " vs ", want_pos); problems += 1
				if n.get_meta("class", "") != o.type: print("class mismatch ", o.name); problems += 1
				if int(n.get_meta("id", -1)) != int(o.id): print("id mismatch ", o.name); problems += 1
				for p in o.get("properties", []):
					var got = n.get_meta(p.name, null)
					var same: bool = (int(got) == int(p.value) and typeof(got) == TYPE_INT) if p.type == "int" else (got == p.value)
					if not same: print("property mismatch ", o.name, ".", p.name, " ", got, " vs ", p.value); problems += 1
				print("  marker ", o.name, " -> ", n.get_class(), " at ", n.position, " meta ", _meta(n))
	print("checked cells: ", checked_cells, " (", flipped_cells, " flipped), problems: ", problems)
	root.free()
	quit(1 if problems > 0 else 0)

func _meta(n: Node) -> Dictionary:
	var d := {}
	for k in n.get_meta_list(): d[k] = n.get_meta(k)
	return d
