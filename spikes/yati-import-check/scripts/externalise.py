import json, sys
src, dst = sys.argv[1], sys.argv[2]
m = json.load(open(src))
m["tilesets"] = [{"firstgid": t["firstgid"], "source": "../tiles/" + t["name"] + ".tsj"} for t in m["tilesets"]]
json.dump(m, open(dst, "w"))
