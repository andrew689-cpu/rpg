// Draws one small check Area through Tiled's scripting API and saves it as .tmj + .tsj.
const root = "__ROOT__";
tiled.log("map formats: " + tiled.mapFormats.join(", "));
tiled.log("tileset formats: " + tiled.tilesetFormats.join(", "));

function makeTileset(name, png) {
  const ts = new Tileset(name);
  ts.tileWidth = 16; ts.tileHeight = 16;
  ts.image = root + "/tiles/" + png;
  return ts;
}
const tsFmt = tiled.tilesetFormat("json");
const sets = {
  floor: makeTileset("TilesetFloor", "TilesetFloor.png"),
  water: makeTileset("TilesetWater", "TilesetWater.png"),
  nature: makeTileset("TilesetNature", "TilesetNature.png"),
  logic: makeTileset("logic", "logic.png"),
};
const kinds = ["wall", "patch_meadow", "patch_wetland", "ledge"];
for (let i = 0; i < 4; i++) sets.logic.tile(i).setProperty("data_kind", kinds[i]);
for (const k in sets) {
  const path = root + "/tiles/" + sets[k].name + ".tsj";
  const err = tsFmt.write(sets[k], path);
  if (err) tiled.error("tileset write " + path + ": " + err);
  sets[k] = tsFmt.read(path);
  tiled.log(k + " tileCount=" + sets[k].tileCount + " columns=" + sets[k].columns + " file=" + sets[k].fileName);
}

const W = 20, H = 18;
const map = new TileMap();
map.setSize(W, H); map.setTileSize(16, 16);
map.orientation = TileMap.Orthogonal;
map.layerDataFormat = TileMap.CSV;
for (const k of ["floor", "water", "nature", "logic"]) map.addTileset(sets[k]);

function layer(name) { const l = new TileLayer(name); l.width = W; l.height = H; map.addLayer(l); return l; }
const ground = layer("ground");
const r1 = layer("restore_1"), r2 = layer("restore_2");
const detail = layer("detail"), logic = layer("logic");
logic.opacity = 0.5;
r1.visible = false; r2.visible = false;

const F = sets.floor, Wt = sets.water, N = sets.nature, L = sets.logic;
const g = ground.edit(), d = detail.edit(), lg = logic.edit(), e1 = r1.edit(), e2 = r2.edit();
const focal = {x: 10, y: 9};
const pond = (x, y) => x >= 13 && x <= 17 && y >= 3 && y <= 6;
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
  const path = (x === 9 || x === 10);
  if (pond(x, y)) { g.setTile(x, y, Wt.tile(29)); lg.setTile(x, y, L.tile(0)); }
  else g.setTile(x, y, F.tile(path ? 188 : 264));
  // stage 1: lush grass within 4 tiles of the focal point (not path, not pond)
  const dist = Math.abs(x - focal.x) + Math.abs(y - focal.y);
  if (!path && !pond(x, y) && dist <= 4) e1.setTile(x, y, F.tile(275));
  // stage 2: lush grass everywhere else that isn't path or pond
  if (!path && !pond(x, y) && dist > 4) e2.setTile(x, y, F.tile(275));
}
// 2x2 trees down the left edge, walls under them
for (let ty = 0; ty < H - 1; ty += 2) {
  d.setTile(0, ty, N.tile(0)); d.setTile(1, ty, N.tile(1));
  d.setTile(0, ty + 1, N.tile(24)); d.setTile(1, ty + 1, N.tile(25));
  for (const [x, y] of [[0, ty], [1, ty], [0, ty + 1], [1, ty + 1]]) lg.setTile(x, y, L.tile(0));
}
// mirrored trees down the right edge: exercises Tiled's flip bits
for (let ty = 0; ty < H - 1; ty += 2) {
  d.setTile(19, ty, N.tile(0), Tile.FlippedHorizontally); d.setTile(18, ty, N.tile(1), Tile.FlippedHorizontally);
  d.setTile(19, ty + 1, N.tile(24), Tile.FlippedHorizontally); d.setTile(18, ty + 1, N.tile(25), Tile.FlippedHorizontally);
  for (const [x, y] of [[18, ty], [19, ty], [18, ty + 1], [19, ty + 1]]) lg.setTile(x, y, L.tile(0));
}
// one vertically flipped and one rotated detail tile
d.setTile(5, 15, N.tile(196), Tile.FlippedVertically);
d.setTile(6, 15, N.tile(196), Tile.FlippedAntiDiagonally | Tile.FlippedHorizontally);
// meadow patch cells and wetland ring logic
for (let y = 10; y <= 13; y++) for (let x = 3; x <= 6; x++) lg.setTile(x, y, L.tile(1));
for (let x = 12; x <= 17; x++) lg.setTile(x, 7, L.tile(2));
lg.setTile(12, 14, L.tile(3));
for (const ed of [g, d, lg, e1, e2]) ed.apply();

// markers
const mk = map.addLayer(new ObjectGroup("markers")) || null;
const markers = map.layers[map.layerCount - 1];
function point(name, cls, cx, cy, props) {
  const o = new MapObject(name); o.shape = MapObject.Point; o.className = cls;
  o.x = cx * 16 + 8; o.y = cy * 16 + 8;
  for (const k in props) o.setProperty(k, props[k]);
  markers.addObject(o); return o;
}
function rect(name, cls, cx, cy, w, h, props) {
  const o = new MapObject(name); o.shape = MapObject.Rectangle; o.className = cls;
  o.x = cx * 16; o.y = cy * 16; o.width = w * 16; o.height = h * 16;
  for (const k in props) o.setProperty(k, props[k]);
  markers.addObject(o); return o;
}
point("focal", "focal_point", focal.x, focal.y, {marker_id: "check_area.focal"});
point("rest", "rest_point", 7, 8, {marker_id: "check_area.rest"});
point("trainer_a", "trainer", 12, 11, {marker_id: "check_area.trainer_a", trainer_id: "hiker_amel", facing: "left", sight_tiles: 4});
point("trainer_b", "trainer", 4, 4, {marker_id: "check_area.trainer_b", trainer_id: "kid_tomo"}); // facing, sight_tiles left at class default
point("item", "item_spot", 16, 14, {marker_id: "check_area.item_1", item_id: "lure_basic", count: 2, hidden: true});
point("exit_n", "area_exit", 9, 0, {marker_id: "check_area.exit_n", to_area: "route_2", to_exit: "route_2.exit_s"});
point("exit_s", "area_exit", 10, 17, {marker_id: "check_area.exit_s", to_area: "town_1", to_exit: "town_1.exit_n"});
rect("barrier", "blight_barrier", 9, 1, 2, 1, {marker_id: "check_area.barrier_n", clear_flag: "chapter_2_open", clears_at_stage: 1});
rect("patch_meadow", "habitat_patch", 3, 10, 4, 4, {marker_id: "check_area.patch_1", habitat: tiled.propertyValue("Habitat", "meadow"), stage_from: 0});
rect("patch_wetland", "habitat_patch", 12, 7, 6, 1, {marker_id: "check_area.patch_2", habitat: tiled.propertyValue("Habitat", "wetland"), stage_from: 2});

const out = root + "/maps/check_area.tmj";
const err = tiled.mapFormat("json").write(map, out);
if (err) tiled.error("map write: " + err); else tiled.log("wrote " + out);
