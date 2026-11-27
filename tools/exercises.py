"""The exercise library (exercises/) and the program pages (programs/), generated from the Gym Twins app's own data.

Sources, all in <app>/Gymtwin/Resources: exercise-catalog.json (names, region, equipment), exercise-guides.json (the 96
owner-signed-off guides), exercise-regions.json (what each muscle does), exercise-equipment.json (what each exercise needs),
program-templates.json (the 8 plans) and ExerciseArt.xcassets (the drawings). Display names come from the app's Swift
sources (LearnNames.swift, GymEquipment+Text.swift) so the site says what the app says.
"""
import hashlib, json, re, shutil
from layout import e, head, navbar, footer, store_badge, breadcrumbs, SITE

REGION = {"chest": "Chest", "back": "Back", "shoulders": "Shoulders", "arms": "Arms", "legs": "Legs", "core": "Core",
          "cardio": "Cardio", "fullBody": "Full Body"}
LEVEL = {"beginner": "Beginner", "intermediate": "Intermediate", "allLevels": "All levels"}
LEVEL_PHRASE = {"beginner": "beginner", "intermediate": "intermediate", "allLevels": "all-levels"}
NOTE = ('<p class="ex-note">General guidance, not medical advice. Stop if something hurts, and ask a professional if you '
        'have an injury or a health condition.</p>')


def words(xs):
    xs = list(xs)
    if len(xs) == 1:
        return xs[0]
    return ", ".join(xs[:-1]) + ("," if len(xs) > 2 else "") + " and " + xs[-1]


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def article(name):
    return "an" if name[0].lower() in "aeiou" else "a"


def rest(sec):
    return f"{sec // 60}:{sec % 60:02d}" if sec >= 60 else f"{sec} s"


def load(app):
    r = app / "Gym Twins" / "Resources"
    j = lambda n: json.loads((r / n).read_text(encoding="utf-8"))
    swift = lambda p: dict(re.findall(r'case \.(\w+): String\(localized: "([^"]+)"\)', (app / p).read_text(encoding="utf-8")))
    guides_raw = (r / "exercise-guides.json").read_bytes()
    signoff = j("exercise-guides-signoff.json")
    if hashlib.sha256(guides_raw).hexdigest() != signoff["guidesSha256"]:
        raise SystemExit("exercise-guides.json does not match the owner's sign-off; publish only signed-off guides")
    return {
        "res": r,
        "catalog": j("exercise-catalog.json"),
        "guides": {g["id"]: g for g in json.loads(guides_raw)["guides"]},
        "muscle_line": {m["id"]: m["line"] for m in j("exercise-regions.json")["muscles"]},
        "needs": j("exercise-equipment.json")["requirements"],
        "templates": j("program-templates.json")["templates"],
        "muscle": swift("Gymtwin/Features/Learn/LearnNames.swift"),
        "equipment": swift("Gymtwin/Features/Gyms/Shared/GymEquipment+Text.swift"),
        "signoff": signoff,
    }


def equipment_text(d, ex_id):
    opts = d["needs"].get(ex_id, [])
    if not opts:
        return "No equipment, just your body weight."
    return "You need " + ", or ".join(words(d["equipment"][p].lower() for p in o) for o in opts) + "."


def tile(href, img, label, extra=""):
    return (f'<li><a class="ex-tile card" href="{href}"><img src="{img}" alt="" width="96" height="96" loading="lazy">'
            f'<span>{e(label)}</span>{extra}</a></li>')


def exercise_page(d, x, by_region, used_in):
    i, n = x["id"], x["name"]
    g = d["guides"][i]
    mus = d["muscle"]
    prim = [mus[m].lower() for m in g["primaryMuscles"]]
    sec = [mus[m].lower() for m in g["secondaryMuscles"]]
    region = REGION[x["primaryRegion"]]
    answer = f"The {n.lower()} mainly works your {words(prim)}" + (f", with help from your {words(sec)}" if sec else "") + "."
    answer += f" {g['steps'][0]} {g['steps'][-1]}" if len(g["steps"]) > 1 else f" {g['steps'][0]}"
    title = f"How to Do {article(n).capitalize()} {n}: Form, Steps and Muscles"
    if len(title) > 65:
        title = f"How to Do {article(n).capitalize()} {n}: Form Guide"
    if len(title) > 65:
        title = f"{n}: Form Guide"
    desc = (f"How to do {article(n)} {n.lower()} with good form, in {len(g['steps'])} steps. Works your {words(prim)}. "
            "Form tips and the equipment you need.")
    if len(desc) > 160:
        desc = f"How to do {article(n)} {n.lower()} with good form: {len(g['steps'])} steps, form tips, muscles worked and equipment."
    url = f"{SITE}exercises/{i}/"
    opts = d["needs"].get(i, [])
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": f"How to do {article(n)} {n.lower()}",
             "image": f"{SITE}exercises/img/{i}.png", "url": url,
             "step": [{"@type": "HowToStep", "position": k + 1, "text": s} for k, s in enumerate(g["steps"])]}
    if opts:
        howto["tool"] = [{"@type": "HowToTool", "name": d["equipment"][p]} for p in opts[0]]
    crumbs = breadcrumbs([("Home", SITE), ("Exercises", f"{SITE}exercises/"), (region, f"{SITE}exercises/#{x['primaryRegion']}"), (n, None)])
    gear = ", ".join(d["equipment"][p] for p in opts[0]) if opts else "Bodyweight"
    chips = "".join(f'<li class="chip chip--level">{e(mus[m])}</li>' for m in g["primaryMuscles"])
    chips += "".join(f'<li class="chip">{e(mus[m])}</li>' for m in g["secondaryMuscles"])
    muscles = "".join(f'<dt>{e(mus[m])} <span>main</span></dt><dd>{e(d["muscle_line"][m])}</dd>' for m in g["primaryMuscles"])
    muscles += "".join(f'<dt>{e(mus[m])}</dt><dd>{e(d["muscle_line"][m])}</dd>' for m in g["secondaryMuscles"])
    related = [y for y in by_region[x["primaryRegion"]] if y["id"] != i][:6]
    plans = ""
    if used_in.get(i):
        links = ", ".join(f'<a href="../../programs/{slug(t["name"])}/">{e(t["name"])}</a>' for t in used_in[i])
        plans = f'<section class="ex-block card"><h2>Plans with this exercise</h2><p>{links}</p></section>'
    body = f'''    <article class="ex">
      <div class="container ex-wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="../../">Home</a> › <a href="../">Exercises</a> › <a href="../#{x["primaryRegion"]}">{region}</a></nav>
        <header class="ex-head">
          <div class="ex-art card"><img src="../img/{i}.png" alt="{e(n)}, drawn in the Gym Twins style" width="256" height="256"></div>
          <div>
            <span class="section-kicker">{region} · {e(gear)}</span>
            <h1>How to do {article(n)} {e(n.lower())}</h1>
            <p class="ex-answer">{e(answer)}</p>
            <ul class="ex-tags" aria-label="Muscles worked">{chips}</ul>
          </div>
        </header>
        <section class="ex-block card"><h2>Step by step</h2><ol class="ex-steps">{"".join(f"<li>{e(s)}</li>" for s in g["steps"])}</ol></section>
        <section class="ex-block card"><h2>Form tips</h2><ul class="ex-tips">{"".join(f"<li>{e(s)}</li>" for s in g["tips"])}</ul></section>
        <section class="ex-block card"><h2>Muscles worked</h2><dl class="ex-muscles">{muscles}</dl></section>
        <section class="ex-block card"><h2>Equipment</h2><p>{e(equipment_text(d, i))}</p></section>
        {plans}
        <aside class="ex-cta card"><div><h2>Log your {e(n.lower())} in Gym Twins</h2><p>Track sets, reps and weight, keep a daily gym streak, and watch your pixel twin grow. This guide is in the app too, and works offline.</p></div>{store_badge(2)}</aside>
        <section class="ex-related"><h2>More {region.lower()} exercises</h2><ul class="ex-grid">{"".join(tile(f"../{y['id']}/", f"../img/{y['id']}.png", y["name"]) for y in related)}</ul></section>
        {NOTE}
      </div>
    </article>
'''
    return head(title, desc, f"exercises/{i}/", 2, [howto, crumbs], image=f"exercises/img/{i}.png") + navbar(2, "exercises") + body + footer(2)


def exercises_hub(d, by_region):
    n = len(d["catalog"])
    secs = "".join(
        f'<section class="ex-related" id="{r}"><h2>{REGION[r]} exercises</h2><ul class="ex-grid">'
        + "".join(tile(f"{y['id']}/", f"img/{y['id']}.png", y["name"]) for y in by_region[r]) + "</ul></section>"
        for r in REGION if r in by_region)
    jump = " · ".join(f'<a href="#{r}">{REGION[r]}</a>' for r in REGION if r in by_region)
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Exercise library", "url": f"{SITE}exercises/",
           "hasPart": [{"@type": "HowTo", "name": f"How to do {article(x['name'])} {x['name'].lower()}", "url": f"{SITE}exercises/{x['id']}/"} for x in d["catalog"]]},
          breadcrumbs([("Home", SITE), ("Exercises", None)])]
    body = f'''    <section class="page-hero"><div class="container"><h1>Exercise <span class="highlight">library</span></h1>
      <p>{n} gym and home exercises, each with a step-by-step form guide, form tips and the muscles it works.</p>
      <p class="ex-jump">{jump}</p></div></section>
    <div class="container ex-wrap">{secs}
      <aside class="ex-cta card"><div><h2>Put them in a plan</h2><p>See the <a href="../programs/">workout plans</a> built from these exercises, or log any of them in Gym Twins and keep your gym streak going.</p></div>{store_badge(1)}</aside>
      {NOTE}
    </div>
'''
    return (head(f"Exercise Library: {n} Exercises with Form Guides | Gym Twins",
                 f"Step-by-step form guides for {n} gym and home exercises: chest, back, shoulders, arms, legs and core, with muscles worked and form tips.",
                 "exercises/", 1, ld, og_type="website") + navbar(1, "exercises") + body + footer(1))


def plan_gear(d, t):
    need = []
    for day in t["days"]:
        for ex in day["exercises"]:
            for p in (d["needs"].get(ex["exerciseId"]) or [[]])[0]:
                if d["equipment"][p] not in need:
                    need.append(d["equipment"][p])
    return need


def program_page(d, t, names):
    s, n, days = slug(t["name"]), t["name"], t["days"]
    gear = plan_gear(d, t)
    lv = LEVEL_PHRASE[t["level"]]
    answer = (f"{n} is {article(lv)} {lv} plan with {len(days)} workout days of about {t['minutes']} minutes each. "
              + " ".join(f"Day {k + 1}, {day['title']}: {words(names[x['exerciseId']] for x in day['exercises'])}." for k, day in enumerate(days)))
    title = f"{n} Workout Plan: {len(days)} Days, Sets and Reps"
    desc = f"A {len(days)}-day {n.lower()} workout plan ({LEVEL[t['level']].lower()}, about {t['minutes']} minutes a session) with sets, reps, rest times and exercise swaps."
    rows = []
    for k, day in enumerate(days):
        items = []
        for x in day["exercises"]:
            i = x["exerciseId"]
            swap = ", ".join(f'<a href="../../exercises/{a}/">{e(names[a])}</a>' for a in x["alternates"])
            items.append(f'''<li class="pl-ex"><img src="../../exercises/img/{i}.png" alt="" width="64" height="64" loading="lazy">
              <div><a class="pl-name" href="../../exercises/{i}/">{e(names[i])}</a>
              <span class="pl-dose">{x["sets"]} sets × {x["repsLow"]}-{x["repsHigh"]} reps · rest {rest(x["restSeconds"])}</span>
              {f'<span class="pl-swap">Swap: {swap}</span>' if swap else ""}</div></li>''')
        regions = ", ".join(REGION[r] for r in day["regions"])
        rows.append(f'<section class="ex-block card" id="day-{k + 1}"><h2>Day {k + 1}: {e(day["title"])}</h2><p class="pl-regions">{e(regions)}</p><ol class="pl-list">{"".join(items)}</ol></section>')
    gear_html = f"You need {words(g.lower() for g in gear)}." if gear else "No equipment, just your body weight."
    ld = [{"@context": "https://schema.org", "@type": "ExercisePlan", "name": f"{n} workout plan", "url": f"{SITE}programs/{s}/",
           "exerciseType": "Strength training", "activityDuration": f"PT{t['minutes']}M", "activityFrequency": f"{len(days)} days per week",
           "workload": answer},
          breadcrumbs([("Home", SITE), ("Programs", f"{SITE}programs/"), (n, None)])]
    body = f'''    <article class="ex">
      <div class="container ex-wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="../../">Home</a> › <a href="../">Programs</a></nav>
        <header class="pl-head">
          <span class="section-kicker">{LEVEL[t["level"]]} · {len(days)} days · about {t["minutes"]} min</span>
          <h1>{e(n)} workout plan</h1>
          <p class="ex-answer">{e(answer)}</p>
        </header>
        {"".join(rows)}
        <section class="ex-block card"><h2>Equipment</h2><p>{e(gear_html)} Each exercise lists a swap if your gym doesn't have the main one.</p></section>
        <aside class="ex-cta card"><div><h2>Run this plan in Gym Twins</h2><p>{e(n)} is built into the app. Pick your training days, start a day as a live workout with a rest timer, and keep your gym streak going.</p></div>{store_badge(2)}</aside>
        {NOTE}
      </div>
    </article>
'''
    return head(title, desc, f"programs/{s}/", 2, ld) + navbar(2, "programs") + body + footer(2)


def programs_hub(d):
    cards = "".join(
        f'<li><a class="pl-card card" href="{slug(t["name"])}/"><span class="section-kicker">{LEVEL[t["level"]]}</span>'
        f'<strong>{e(t["name"])}</strong><span>{len(t["days"])} days · about {t["minutes"]} min</span></a></li>' for t in d["templates"])
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Workout plans", "url": f"{SITE}programs/"},
          breadcrumbs([("Home", SITE), ("Programs", None)])]
    body = f'''    <section class="page-hero"><div class="container"><h1>Workout <span class="highlight">plans</span></h1>
      <p>{len(d["templates"])} free workout plans with sets, reps and rest times: full body, dumbbell only, bodyweight, push pull legs and more.</p></div></section>
    <div class="container ex-wrap">
      <ul class="pl-grid">{cards}</ul>
      <aside class="ex-cta card"><div><h2>Every plan is in the app</h2><p>Gym Twins fits each plan to the equipment your gym has, and turns your training days into a daily streak.</p></div>{store_badge(1)}</aside>
      {NOTE}
    </div>
'''
    return (head("Free Workout Plans: Full Body, PPL, Upper Lower | Gym Twins",
                 f"{len(d['templates'])} free workout plans with sets, reps and rest: full body, machines, dumbbell only, bodyweight, push pull legs and upper lower.",
                 "programs/", 1, ld, og_type="website") + navbar(1, "programs") + body + footer(1))


def generate(app, root):
    d = load(app)
    names = {x["id"]: x["name"] for x in d["catalog"]}
    by_region, used_in = {}, {}
    for x in d["catalog"]:
        by_region.setdefault(x["primaryRegion"], []).append(x)
    for t in d["templates"]:
        for day in t["days"]:
            for x in day["exercises"]:
                if t not in used_in.setdefault(x["exerciseId"], []):
                    used_in[x["exerciseId"]].append(t)
    for sub in ("exercises", "programs"):
        if (root / sub).exists():
            shutil.rmtree(root / sub)
    (root / "exercises" / "img").mkdir(parents=True)
    for x in d["catalog"]:
        i = x["id"]
        shutil.copyfile(d["res"] / "ExerciseArt.xcassets" / f"exercise_{i}.imageset" / f"exercise_{i}.png", root / "exercises" / "img" / f"{i}.png")
        (root / "exercises" / i).mkdir()
        (root / "exercises" / i / "index.html").write_text(exercise_page(d, x, by_region, used_in), encoding="utf-8")
    (root / "exercises" / "index.html").write_text(exercises_hub(d, by_region), encoding="utf-8")
    for t in d["templates"]:
        (root / "programs" / slug(t["name"])).mkdir(parents=True)
        (root / "programs" / slug(t["name"]) / "index.html").write_text(program_page(d, t, names), encoding="utf-8")
    (root / "programs" / "index.html").write_text(programs_hub(d), encoding="utf-8")
    (root / "exercises" / "source.json").write_text(json.dumps({"guidesSha256": d["signoff"]["guidesSha256"], "signedOff": d["signoff"]["reviewedOn"]}, indent=2) + "\n", encoding="utf-8")
    return len(d["catalog"]) + len(d["templates"]) + 2
