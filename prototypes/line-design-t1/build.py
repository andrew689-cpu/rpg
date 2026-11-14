#!/usr/bin/env python3
"""PROTOTYPE, throwaway. Trial of the line-design method (ticket 28) on Starter trio T1.

Run:  python3 prototypes/line-design-t1/build.py

It writes content-shaped drafts (content/lines, content/species, content/traits,
strings/en.csv) next to this file, appends a rendered summary to each design sheet
(what `tools/line_sheet` would do), and runs a mini-lint of the method's rules.
Moves are SLOTS (`<type>.<tier>.<category>`, `<type>.support.N`, `<type>.all_foes`,
`bond_only.<type>.N`, `signature.<line>`), because the move records don't exist yet.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- method tables (ticket 28)
SHARES = {  # % of the 6-stat total: hp, power, guard, focus, will, speed
    "bruiser":    [22, 22, 16, 10, 14, 16],
    "bulwark":    [18, 13, 22, 13, 22, 12],
    "caster":     [15, 10, 14, 25, 18, 18],
    "skirmisher": [14, 22, 13, 13, 13, 25],
    "balanced":   [17, 17, 17, 17, 16, 16],
    "warden":     [18, 10, 17, 15, 24, 16],
}
ENERGY_FINAL = {"bruiser": 80, "bulwark": 100, "caster": 130, "skirmisher": 100, "balanced": 100, "warden": 130}
STAGE_TOTAL = {"base": 300, "middle": 400, "final": 500}
STAGE_ENERGY = {"base": 0.8, "middle": 0.9, "final": 1.0}
CATCH_BAND = {"base": 12, "middle": 25, "final": 12}  # starter line: wild-starter band for the base form
TRAIT_BANDS = {
    "type_damage": [10, 15, 20], "category_damage": [8, 12, 15], "resist_type": [15, 20, 25],
    "status_chance": [5, 8, 10], "energy_regen": [5, 8, 10], "low_hp_boost": [15, 20, 25],
    "turn_heal": [3, 4, 6], "retaliate": [3, 4, 5],
}
TIER_LEVEL = {"weak": 1, "mid": 12, "strong": 25, "finisher": 36}
TIER_RANK = {"weak": 1, "mid": 2, "strong": 3, "finisher": 4, "signature": 5}
STATS = ["hp", "power", "guard", "focus", "will", "speed"]


def stats(archetype, stage):
    total = STAGE_TOTAL[stage]
    s = [round(total * p / 100) for p in SHARES[archetype]]
    e = int(5 * round(ENERGY_FINAL[archetype] * STAGE_ENERGY[stage] / 5))
    return dict(zip(STATS, s)), e


def L(*pairs):
    return [{"level": lv, "move": m} for lv, m in pairs]


def B(*pairs):
    return [{"rank": r, "move": m} for r, m in pairs]


# ---------------------------------------------------------------- the three drafts
LINES = [
  {
    "line": {
      "id": "brockle", "trio": "t1", "habitat": "meadow", "times": ["day", "evening"],
      "species": ["brockle", "sootbrock", "forgeback", "smokesage"],
      "trait_slots": [
        {"slot": "rain", "condition": {"weather": ["rain"]}},
        {"slot": "dusk", "condition": {"time": ["evening"]}},
        {"slot": "default"},
      ],
      "level_up": L((1, "flame.weak.power"), (5, "flame.weak.focus"), (9, "stone.weak.power"),
                    (13, "flame.mid.focus"), (20, "flame.support.1"), (26, "flame.strong.power"),
                    (30, "wild.mid.focus"), (37, "flame.finisher.power"), (44, "flame.strong.focus"),
                    (52, "flame.all_foes")),
      "spawns": [{"area": "route_3", "stages": [1, 2, 3], "form": "brockle", "tier": "rare",
                  "levels": [12, 15], "habitat": "meadow", "times": ["day", "evening"]}],
    },
    "species": [
      dict(id="brockle", stage="base", types=["flame"], archetype="bruiser", behaviour="wander",
           extra_moves=L((11, "stone.support.1")),
           traits={"rain": "damp_proof", "dusk": "ember_dusk", "default": "stoked"},
           evolution={"level": 16, "into": "sootbrock"},
           bond_moves=B((1, "stone.weak.focus"), (2, "gale.mid.power"))),
      dict(id="sootbrock", stage="middle", types=["flame"], archetype="bruiser", behaviour="wander",
           extra_moves=L((18, "flame.mid.power")),
           traits={"rain": "damp_proof", "dusk": "ember_dusk", "default": "stoked"},
           evolution={"level": 34, "branch": {"axis": "style", "ends": ["power", "focus"],
                                              "into": ["forgeback", "smokesage"]}},
           bond_moves=B((1, "wild.weak.focus"), (2, "stone.mid.power"), (3, "bond_only.flame.1"))),
      dict(id="forgeback", stage="final", types=["flame", "stone"], archetype="bruiser", behaviour="wander",
           extra_moves=L((36, "wild.strong.power")),
           traits={"rain": "damp_proof", "dusk": "ember_dusk", "default": "stoked"},
           bond_moves=B((2, "wild.mid.power"), (3, "bond_only.stone.1"), (4, "wild.finisher.power"),
                        (5, "signature.brockle"))),
      dict(id="smokesage", stage="final", types=["flame", "lumen"], archetype="caster", behaviour="wander",
           extra_moves=L((36, "flame.finisher.focus"), (38, "lumen.mid.focus")),
           traits={"rain": "damp_proof", "dusk": "ember_dusk", "default": "smoulder_mind"},
           bond_moves=B((2, "shade.mid.focus"), (3, "bond_only.lumen.1"), (4, "shade.finisher.focus"),
                        (5, "signature.brockle"))),
    ],
  },
  {
    "line": {
      "id": "hazelpip", "trio": "t1", "habitat": "woodland", "times": ["evening", "night"],
      "species": ["hazelpip", "hedgemote", "rootdelve", "frostdoze"],
      "trait_slots": [
        {"slot": "cold", "condition": {"weather": ["fog", "snow"]}},
        {"slot": "night", "condition": {"time": ["night"]}},
        {"slot": "default"},
      ],
      "level_up": L((1, "grove.weak.focus"), (5, "grove.weak.power"), (9, "stone.weak.focus"),
                    (13, "grove.mid.focus"), (20, "grove.support.1"), (26, "grove.strong.focus"),
                    (30, "frost.mid.focus"), (37, "grove.finisher.focus"), (44, "grove.strong.power"),
                    (52, "grove.all_foes")),
      "spawns": [{"area": "route_4", "stages": [1, 2, 3], "form": "hazelpip", "tier": "rare",
                  "levels": [12, 15], "habitat": "woodland", "times": ["evening", "night"]}],
    },
    "species": [
      dict(id="hazelpip", stage="base", types=["grove"], archetype="balanced", behaviour="shy",
           extra_moves=L((3, "grove.support.2")),
           traits={"cold": "snug_burrow", "night": "night_forager", "default": "hedge_coat"},
           evolution={"level": 16, "into": "hedgemote"},
           bond_moves=B((1, "stone.weak.power"), (2, "grove.mid.power"))),
      dict(id="hedgemote", stage="middle", types=["grove"], archetype="warden", behaviour="shy",
           extra_moves=L((17, "frost.weak.focus")),
           traits={"cold": "snug_burrow", "night": "night_forager", "default": "hedge_coat"},
           evolution={"level": 34, "branch": {"axis": "type", "ends": ["stone", "frost"],
                                              "into": ["rootdelve", "frostdoze"]}},
           bond_moves=B((1, "frost.weak.power"), (2, "stone.mid.focus"), (3, "bond_only.grove.1"))),
      dict(id="rootdelve", stage="final", types=["grove", "stone"], archetype="bulwark", behaviour="shy",
           extra_moves=L((36, "stone.strong.power")),
           traits={"cold": "snug_burrow", "night": "night_forager", "default": "hedge_coat"},
           bond_moves=B((2, "stone.mid.power"), (3, "bond_only.stone.2"), (4, "stone.finisher.power"),
                        (5, "signature.hazelpip"))),
      dict(id="frostdoze", stage="final", types=["grove", "frost"], archetype="warden", behaviour="shy",
           extra_moves=L((36, "frost.strong.focus")),
           traits={"cold": "snug_burrow", "night": "night_forager", "default": "hedge_coat"},
           bond_moves=B((2, "frost.mid.power"), (3, "bond_only.frost.1"), (4, "frost.finisher.focus"),
                        (5, "signature.hazelpip"))),
    ],
  },
  {
    "line": {
      "id": "lodgekit", "trio": "t1", "habitat": "wetland", "times": ["morning", "evening"],
      "species": ["lodgekit", "dambrook", "mossdam", "spraytail"],
      "trait_slots": [
        {"slot": "rain", "condition": {"weather": ["rain"]}},
        {"slot": "dusk", "condition": {"time": ["evening"]}},
        {"slot": "default"},
      ],
      "level_up": L((1, "tide.weak.power"), (5, "tide.weak.focus"), (9, "grove.weak.power"),
                    (13, "tide.mid.power"), (20, "tide.support.1"), (26, "tide.strong.power"),
                    (30, "gale.mid.power"), (37, "tide.finisher.power"), (44, "tide.strong.focus"),
                    (52, "tide.all_foes")),
      "spawns": [{"area": "route_3", "stages": [1, 2, 3], "form": "lodgekit", "tier": "rare",
                  "levels": [11, 15], "habitat": "wetland", "times": ["morning", "evening"]}],
    },
    "species": [
      dict(id="lodgekit", stage="base", types=["tide"], archetype="bulwark", behaviour="curious",
           extra_moves=L((11, "tide.support.2")),
           traits={"rain": "rain_swell", "dusk": "tail_slap", "default": "dam_builder"},
           evolution={"level": 16, "into": "dambrook"},
           bond_moves=B((1, "grove.weak.focus"), (2, "tide.mid.focus"))),
      dict(id="dambrook", stage="middle", types=["tide"], archetype="bulwark", behaviour="curious",
           extra_moves=L((22, "grove.mid.focus")),
           traits={"rain": "rain_swell", "dusk": "tail_slap", "default": "dam_builder"},
           evolution={"level": 34, "branch": {"axis": "habitat", "ends": ["wetland", "coast"],
                                              "into": ["mossdam", "spraytail"]}},
           bond_moves=B((1, "gale.weak.power"), (2, "stone.mid.power"), (3, "bond_only.tide.1"))),
      dict(id="mossdam", stage="final", types=["tide", "grove"], archetype="bulwark", behaviour="curious",
           extra_moves=L((36, "grove.strong.focus")),
           traits={"rain": "rain_swell", "dusk": "tail_slap", "default": "dam_builder"},
           bond_moves=B((2, "grove.mid.power"), (3, "bond_only.grove.2"), (4, "grove.finisher.focus"),
                        (5, "signature.lodgekit"))),
      dict(id="spraytail", stage="final", types=["tide", "gale"], archetype="skirmisher", behaviour="curious",
           habitat="coast",
           extra_moves=L((36, "gale.strong.power")),
           traits={"rain": "rain_swell", "dusk": "tail_slap", "default": "sea_legs"},
           bond_moves=B((2, "gale.mid.focus"), (3, "bond_only.gale.1"), (4, "gale.finisher.power"),
                        (5, "signature.lodgekit"))),
    ],
  },
]

TRAITS = {
  "stoked":        {"kind": "category_damage", "category": "power", "magnitude": [8, 12, 15]},
  "smoulder_mind": {"kind": "category_damage", "category": "focus", "magnitude": [8, 12, 15]},
  "ember_dusk":    {"kind": "low_hp_boost", "threshold": "1/3", "magnitude": [15, 20, 25]},
  "damp_proof":    {"kind": "resist_type", "type": "tide", "magnitude": [15, 20, 25]},
  "hedge_coat":    {"kind": "resist_type", "type": "flame", "magnitude": [15, 20, 25]},
  "night_forager": {"kind": "energy_regen", "magnitude": [5, 8, 10]},
  "snug_burrow":   {"kind": "turn_heal", "magnitude": [3, 4, 6]},
  "dam_builder":   {"kind": "start_stage", "stat": "guard", "stages": 1},
  "sea_legs":      {"kind": "start_stage", "stat": "speed", "stages": 1},
  "tail_slap":     {"kind": "retaliate", "category": "power", "magnitude": [3, 4, 5]},
  "rain_swell":    {"kind": "type_damage", "type": "tide", "magnitude": [15, 22, 30],
                    "when": {"weather": ["rain"]}},
}

STRINGS = {
  "species.brockle.name": "Brockle", "species.sootbrock.name": "Sootbrock",
  "species.forgeback.name": "Forgeback", "species.smokesage.name": "Smokesage",
  "species.hazelpip.name": "Hazelpip", "species.hedgemote.name": "Hedgemote",
  "species.rootdelve.name": "Rootdelve", "species.frostdoze.name": "Frostdoze",
  "species.lodgekit.name": "Lodgekit", "species.dambrook.name": "Dambrook",
  "species.mossdam.name": "Mossdam", "species.spraytail.name": "Spraytail",
  "species.brockle.log": "A badger cub whose white stripe glows like a banked coal. It digs warm dens in meadow banks and naps in them through the heat of the day.",
  "species.sootbrock.log": "It tunnels through old charcoal pits, coming up grey with soot. The embers along its back flare when it is cross.",
  "species.forgeback.log": "Its claws are hammered hard by digging through hot stone. Folk once followed its trails to find good iron.",
  "species.smokesage.log": "It sits very still by its den and reads the smoke. The stripe on its face burns pale, like a lantern turned low.",
  "species.hazelpip.log": "A dormouse no bigger than a hazelnut, which it often hugs. It is gone at the first loud footstep.",
  "species.hedgemote.log": "It weaves a hedge of briars round its nest each autumn. Bramble seeds caught in its fur sprout where it sleeps.",
  "species.rootdelve.log": "It burrows down among old roots and wakes with stones grown into its coat. Its dens hold the soil of a whole hillside in place.",
  "species.frostdoze.log": "It sleeps through the cold with frost on its whiskers, and the frost does not melt when it wakes. Its breath leaves rime on the leaves.",
  "species.lodgekit.log": "A beaver kit that stacks twigs wherever it goes, whether or not there is any water to dam. It is very proud of each pile.",
  "species.dambrook.log": "One night's work by a Dambrook can turn a trickle into a pond. Reedwood's marsh is said to be its handiwork.",
  "species.mossdam.log": "Moss and reeds grow over its back until it looks like part of the dam it sleeps in. Marsh life gathers wherever it settles.",
  "species.spraytail.log": "It left the rivers for the sea and swims through surf with a tail like a rudder. It slaps the waves to call its kin.",
  "trait.stoked.name": "Stoked", "trait.smoulder_mind.name": "Smoulder", "trait.ember_dusk.name": "Dusk Ember",
  "trait.damp_proof.name": "Damp-proof", "trait.hedge_coat.name": "Hedge Coat", "trait.night_forager.name": "Night Forager",
  "trait.snug_burrow.name": "Snug Burrow", "trait.dam_builder.name": "Dam Builder", "trait.sea_legs.name": "Sea Legs",
  "trait.tail_slap.name": "Tail Slap", "trait.rain_swell.name": "Rain Swell",
}

# ---------------------------------------------------------------- build
def build():
    out = {}
    log_no = 1
    for entry in LINES:
        line = entry["line"]
        for sp in entry["species"]:
            st, en = stats(sp["archetype"], sp["stage"])
            rec = {"id": sp["id"], "line": line["id"], "log_no": log_no, "stage": sp["stage"],
                   "types": sp["types"], "archetype": sp["archetype"], "stats": st, "energy": en,
                   "catch_pct": CATCH_BAND[sp["stage"]], "behaviour": sp["behaviour"]}
            if "habitat" in sp:
                rec["habitat"] = sp["habitat"]
            rec.update({"extra_moves": sp["extra_moves"], "traits": sp["traits"]})
            if "evolution" in sp:
                rec["evolution"] = sp["evolution"]
            rec["bond_moves"] = sp["bond_moves"]
            log_no += 1
            out[f"content/species/{sp['id']}.json"] = rec
        out[f"content/lines/{line['id']}.json"] = line
    for tid, eff in TRAITS.items():
        out[f"content/traits/{tid}.json"] = {"id": tid, "effect": eff}
    for path, rec in out.items():
        full = os.path.join(HERE, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            json.dump(rec, f, indent=2)
            f.write("\n")
    os.makedirs(os.path.join(HERE, "strings"), exist_ok=True)
    with open(os.path.join(HERE, "strings/en.csv"), "w") as f:
        f.write("keys,en\n")
        for k, v in STRINGS.items():
            f.write(f'{k},"{v}"\n')
    return out


# ---------------------------------------------------------------- mini-lint (method rules only)
def slot_parts(m):
    p = m.split(".")
    if p[0] == "signature":
        return {"type": None, "tier": "signature", "cat": "best"}
    if p[0] == "bond_only":
        return {"type": p[1], "tier": None, "cat": None}
    if p[1] in TIER_LEVEL:
        return {"type": p[0], "tier": p[1], "cat": p[2]}
    return {"type": p[0], "tier": None, "cat": None}


def lint(out):
    errs, warns = [], []
    species = {r["id"]: r for p, r in out.items() if p.startswith("content/species/")}
    traits = {r["id"]: r for p, r in out.items() if p.startswith("content/traits/")}
    names = {k.split(".")[1]: v for k, v in STRINGS.items() if k.endswith(".name") and k.startswith("species.")}
    for entry in LINES:
        line = entry["line"]
        lid = line["id"]
        forms = [species[s] for s in line["species"]]
        # stats
        for f in forms:
            tot = sum(f["stats"].values())
            want = STAGE_TOTAL[f["stage"]]
            if abs(tot - want) > want * 0.05:
                errs.append(f"{f['id']}: stat total {tot} not within 5% of {want}")
            for s, share in zip(STATS, SHARES[f["archetype"]]):
                got = 100 * f["stats"][s] / tot
                if abs(got - share) > 3:
                    errs.append(f"{f['id']}: {s} share {got:.1f}% off archetype {share}%")
            n = names[f["id"]]
            if not (4 <= len(n) <= 9 and n.isalpha()):
                errs.append(f"{f['id']}: name '{n}' not 4-9 letters")
        finals = [f for f in forms if f["stage"] == "final"]
        if len({sum(f["stats"].values()) for f in finals}) > 1:
            errs.append(f"{lid}: branch forms' totals differ")
        # level-up tier floors, Power+Focus before first evolution, 2 extra Types by final
        first_evo = forms[0]["evolution"]["level"]
        own = forms[0]["types"][0]
        for e in line["level_up"] + [m for f in forms for m in f["extra_moves"]]:
            t = slot_parts(e["move"])["tier"]
            if t in TIER_LEVEL and e["level"] < TIER_LEVEL[t]:
                errs.append(f"{lid}: {e['move']} at level {e['level']} below tier floor {TIER_LEVEL[t]}")
        early = [slot_parts(e["move"])["cat"] for e in line["level_up"] + forms[0]["extra_moves"]
                 if e["level"] < first_evo]
        if "power" not in early or "focus" not in early:
            errs.append(f"{lid}: no Power and Focus move before level {first_evo}")
        for fin in finals:
            ts = {slot_parts(e["move"])["type"] for e in line["level_up"] + fin["extra_moves"]} - {own, None}
            if len(ts) < 2:
                errs.append(f"{fin['id']}: only {len(ts)} extra move Types")
        # bond moves
        for f in forms:
            bm = f["bond_moves"]
            if not 2 <= len(bm) <= 4:
                errs.append(f"{f['id']}: {len(bm)} Bond moves")
            if len({b["move"] for b in bm}) != len(bm):
                errs.append(f"{f['id']}: duplicate Bond move")
            for b in bm:
                t = slot_parts(b["move"])["tier"]
                if t in TIER_RANK and b["rank"] < TIER_RANK[t]:
                    errs.append(f"{f['id']}: {b['move']} at rank {b['rank']} below floor {TIER_RANK[t]}")
                if b["move"].startswith("signature.") and b["rank"] != 5:
                    errs.append(f"{f['id']}: signature not at rank 5")
        # branch axis checks
        mid = forms[1]
        br = mid["evolution"]["branch"]
        lvl = mid["evolution"]["level"]
        if br["axis"] == "type":
            learnable = {slot_parts(e["move"])["type"] for e in line["level_up"] + forms[0]["extra_moves"]
                         + mid["extra_moves"] if e["level"] < lvl}
            learnable |= {slot_parts(b["move"])["type"] for f in forms[:2] for b in f["bond_moves"]}
            for end in br["ends"]:
                if end not in learnable:
                    errs.append(f"{lid}: Type end {end} not learnable before {lvl}")
        if br["axis"] == "style":  # ticket 28 Q4 (round 3): balanced before the branch, as an error
            pre = [e["move"] for e in line["level_up"] + forms[0]["extra_moves"] + mid["extra_moves"] if e["level"] < lvl]
            pre += [b["move"] for f in forms[:2] for b in f["bond_moves"]]
            cats = [slot_parts(m)["cat"] for m in pre]
            p, fo = cats.count("power"), cats.count("focus")
            if abs(p - fo) > 1:
                errs.append(f"{lid}: Style line learns {p} Power / {fo} Focus moves before {lvl} (max gap 1)")
        if line.get("trio"):  # ticket 28 Q2 (round 3): starter lines put no morning in a Trait condition
            for s in line["trait_slots"]:
                if "morning" in s.get("condition", {}).get("time", []):
                    errs.append(f"{lid}: starter line has a morning Trait condition")
        seen = set()  # ticket 28 Q5 (round 3): fresh Bond lists per form (warning)
        for f in forms:
            seen |= {e["move"] for e in line["level_up"] + f["extra_moves"]}
        for f in forms:
            for b in f["bond_moves"]:
                earlier = [g for g in forms[:forms.index(f)] if g["stage"] != f["stage"]]
                if any(b["move"] in {x["move"] for x in g["bond_moves"] + g["extra_moves"]} for g in earlier) \
                        or b["move"] in {e["move"] for e in line["level_up"]}:
                    warns.append(f"{f['id']}: Bond move {b['move']} repeats a move an earlier form can learn")
        # traits
        slots = [s["slot"] for s in line["trait_slots"]]
        if slots[-1] != "default":
            errs.append(f"{lid}: default slot must be last")
        for f in forms:
            if set(f["traits"]) != set(slots):
                errs.append(f"{f['id']}: Trait slots don't match the line")
            stage_i = ["base", "middle", "final"].index(f["stage"])
            for tid in f["traits"].values():
                eff = traits[tid]["effect"]
                band = TRAIT_BANDS.get(eff["kind"])
                if band and "magnitude" in eff:
                    want = band[stage_i] * (1.5 if "when" in eff else 1)
                    got = eff["magnitude"][stage_i]
                    if abs(got - want) > want * 0.2:
                        errs.append(f"{f['id']}: Trait {tid} magnitude {got} vs band {want}")
        # spawns: wild starter base forms Rare, below first evolution level
        for sp in line["spawns"]:
            if sp["levels"][1] >= first_evo:
                errs.append(f"{lid}: wild {sp['form']} up to level {sp['levels'][1]}, at or past evolution {first_evo}")
            if sp["habitat"] != species[sp["form"]].get("habitat", line["habitat"]):
                errs.append(f"{lid}: spawn Habitat off the form's home Habitat")
    return errs, warns


# ---------------------------------------------------------------- render (what tools/line_sheet would do)
def render(entry, out):
    line = entry["line"]
    sp = {s: out[f"content/species/{s}.json"] for s in line["species"]}
    r = ["<!-- line_sheet: generated by build.py, do not edit below -->", "", "## Generated summary", ""]
    r += ["| Form | Types | Archetype | HP | Pow | Grd | Foc | Will | Spd | Total | Energy | Catch % | Evolves |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in sp.values():
        ev = s.get("evolution", {})
        evs = ""
        if "into" in ev:
            evs = f"Lv {ev['level']} → {ev['into']}"
        elif "branch" in ev:
            b = ev["branch"]
            evs = f"Lv {ev['level']}, {b['axis']}: {b['ends'][0]} → {b['into'][0]}, {b['ends'][1]} → {b['into'][1]}"
        st = s["stats"]
        r.append(f"| {STRINGS['species.'+s['id']+'.name']} (`{s['id']}`) | {' / '.join(s['types'])} | {s['archetype']} | "
                 + " | ".join(str(st[k]) for k in STATS) + f" | {sum(st.values())} | {s['energy']} | {s['catch_pct']} | {evs} |")
    r += ["", f"Home Habitat **{line['habitat']}**, times **{', '.join(line['times'])}**"
          + "".join(f"; {STRINGS['species.'+s['id']+'.name']} overrides Habitat to **{s['habitat']}**"
                    for s in sp.values() if "habitat" in s) + ".", ""]
    r += ["### Level-up moves", "", "| Level | Move slot | Learned by |", "|---|---|---|"]
    rows = [(e["level"], e["move"], "line") for e in line["level_up"]]
    for s in sp.values():
        rows += [(e["level"], e["move"], STRINGS["species." + s["id"] + ".name"] + " only") for e in s["extra_moves"]]
    for lv, m, who in sorted(rows):
        r.append(f"| {lv} | `{m}` | {who} |")
    r += ["", "### Bond moves", "", "| Form | Rank 1 | Rank 2 | Rank 3 | Rank 4 | Rank 5 |", "|---|---|---|---|---|---|"]
    for s in sp.values():
        by = {b["rank"]: f"`{b['move']}`" for b in s["bond_moves"]}
        r.append(f"| {STRINGS['species.'+s['id']+'.name']} | " + " | ".join(by.get(i, "–") for i in range(1, 6)) + " |")
    r += ["", "### Traits (first matching slot wins)", "", "| Slot | Caught when | " +
          " | ".join(STRINGS["species." + s + ".name"] for s in sp) + " |", "|---|---|" + "---|" * len(sp)]
    for slot in line["trait_slots"]:
        cond = slot.get("condition")
        cs = "otherwise" if not cond else ", ".join(f"{k}: {'/'.join(v)}" for k, v in cond.items())
        cells = []
        stage_of = {"base": 0, "middle": 1, "final": 2}
        for s in sp.values():
            tid = s["traits"][slot["slot"]]
            eff = TRAITS[tid]
            mag = eff.get("magnitude")
            what = eff["kind"] + (f" {eff.get('type', eff.get('category', eff.get('stat', '')))}")
            what += f" {mag[stage_of[s['stage']]]}" if mag else f" +{eff.get('stages', '')}"
            if "when" in eff:
                what += " in " + "/".join(eff["when"]["weather"])
            cells.append(f"{STRINGS['trait.'+tid+'.name']}: {what}")
        r.append(f"| {slot['slot']} | {cs} | " + " | ".join(cells) + " |")
    r += ["", "### Wild spawns", "", "| Area | Stages | Form | Tier | Levels | Habitat | Times |", "|---|---|---|---|---|---|---|"]
    for w in line["spawns"]:
        r.append(f"| `{w['area']}` | {', '.join(map(str, w['stages']))} | {w['form']} | {w['tier']} | "
                 f"{w['levels'][0]}–{w['levels'][1]} | {w['habitat']} | {', '.join(w['times'])} |")
    r += ["", "### Collection log", ""]
    for s in sp.values():
        r.append(f"- **{STRINGS['species.'+s['id']+'.name']}:** {STRINGS['species.'+s['id']+'.log']}")
    return "\n".join(r) + "\n"


if __name__ == "__main__":
    out = build()
    for entry in LINES:
        path = os.path.join(HERE, "content/lines", entry["line"]["id"] + ".md")
        text = open(path).read() if os.path.exists(path) else f"# {entry['line']['id']}\n"
        text = re.split(r"<!-- line_sheet:", text)[0].rstrip() + "\n\n"
        with open(path, "w") as f:
            f.write(text + render(entry, out))
    errs, warns = lint(out)
    for w in warns:
        print("WARN ", w)
    for e in errs:
        print("ERROR", e)
    print(f"{len(out)} records, {len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)
