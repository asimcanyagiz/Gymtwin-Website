"""The hand-written use-case pages. The copy lives here so every page shares one frame (tools/layout.py)
and its FAQ JSON-LD is built from the same questions the page shows.

Every fact about the app on these pages is also on the home page or the support page; change them together.
"""
import re
from layout import e, head, navbar, footer, store_badge, breadcrumbs, SITE

TWIN = '<div class="sprite" role="img" aria-label="{label}" style="background-image: url(\'../Assets/sprites/{sheet}.png\'); --frames: {frames};"></div>'


def faq_ld(faq):
    strip = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]}


PAGES = [
    {
        "slug": "workout-streak-tracker",
        "title": "Workout Streak Tracker That Counts Rest Days | Gym Twins",
        "desc": "Gym Twins is a workout streak tracker for iPhone where planned rest days keep your streak. Log gym days, check in on rest days, and grow a pixel twin.",
        "kicker": "Workout streak tracker",
        "h1": "A workout streak tracker that doesn't punish rest days",
        "twin": ("twin-lv4-flex", 8, "A level 4 twin flexing"),
        "answer": "Most streak apps want a workout every single day, so the first rest day breaks the chain. Gym Twins counts days you <strong>keep</strong> instead: on a gym day you log a workout of 10 minutes or more, and on a rest day a quick check-in keeps the streak alive. Your plan decides which day is which, so resting on schedule never costs you the streak.",
        "sections": [
            ("How the streak works", "<ul><li><strong>Gym days:</strong> pick the weekdays you train. On those days, log a workout of 10 minutes or more.</li><li><strong>Rest days:</strong> every other day, one tap on Rest check-in keeps the day. A workout counts too.</li><li><strong>Late sessions:</strong> your day ends at 3:00 AM, not midnight, and a workout counts for the day it started.</li></ul>"),
            ("What happens when you miss a day", "<p>The streak resets and your pixel twin gets tired. You then have 3 days: log a workout of 10 minutes or more and your twin recovers at the same level. If you don't, it shrinks back one level. A Level 1 twin can't shrink further.</p><p>Gems you earn from workouts buy a streak freeze or a level shield in the Shop, for the weeks life gets in the way.</p>"),
            ("Why a twin instead of a number", "<p>A streak counter is easy to ignore once it resets. In Gym Twins the streak feeds a pixel-art twin that grows through five levels, from Beginner to Beast Mode, as you earn XP from the minutes you train. Seeing it tired is a nudge that a plain number never gives you.</p>"),
            ("Keep it in view", "<p>A streak widget on your Lock Screen, a heat map of your training on the Home Screen, and a Live Activity with your rest timer while you work out. Invite a friend with a link and you can keep a shared streak together.</p>"),
        ],
        "faq": [
            ("Does a rest day break my workout streak?", "No. Days that aren't in your plan are rest days, and a rest check-in keeps them. Only a gym day without a workout of 10 minutes or more breaks the streak."),
            ("When does my day end?", "At 3:00 AM in your time zone. A workout that starts at 11:30 PM still counts for that day."),
            ("Can I change my gym days?", "Yes, in Settings. The new plan starts the next day."),
        ],
        "links": [("rest-day-streak/", "Do rest days break your streak?"), ("gym-consistency/", "How to stay consistent at the gym"), ("programs/", "Free workout plans")],
    },
    {
        "slug": "gym-consistency",
        "title": "How to Stay Consistent at the Gym: 7 Habits That Work",
        "desc": "How to stay consistent at the gym: set a weekly plan you can keep, make rest days count, use a 10-minute minimum, and bounce back fast after a missed day.",
        "kicker": "Guide",
        "h1": "How to stay consistent at the gym",
        "twin": ("twin-lv3-flex", 6, "A level 3 twin flexing"),
        "answer": "Consistency comes from a plan you can actually keep, not from motivation. Choose a realistic number of gym days, put them on fixed weekdays, treat rest days as part of the plan, set a small minimum for bad days, and decide in advance how fast you return after a miss. Then track it, so every kept day is visible.",
        "sections": [
            ("1. Pick fewer days than you think", "<p>Three days a week you keep beat five days you drop after two weeks. Start with the number you could manage in your busiest week, and add a day once that feels easy.</p>"),
            ("2. Give every gym day a weekday", "<p>“Three times a week” leaves the decision open every day. “Monday, Wednesday, Friday” makes it a routine. A <a href=\"../programs/\">ready-made plan</a> answers the other question, what to do once you're there.</p>"),
            ("3. Plan your rest days too", "<p>Rest days are part of training, not a failure to train. If your tracker treats them as gaps, you'll feel behind on days you're doing exactly what the plan says. Count a planned rest day as a kept day.</p>"),
            ("4. Set a minimum for bad days", "<p>Tired, busy or traveling? Decide on a short minimum session ahead of time, such as 10 minutes. A short session keeps the habit alive and is easier to start than a full workout.</p>"),
            ("5. Decide how fast you come back", "<p>Everyone misses a day. The damage comes from the second and third day off. Set a rule, such as training again within 3 days, so one miss doesn't turn into a month.</p>"),
            ("6. Make progress visible", "<p>A streak, a calendar heat map or a character that grows all turn invisible effort into something you can see. Log every session, even the short ones.</p>"),
            ("7. Train with someone", "<p>A friend who sees whether you kept the day adds a little accountability without needing to meet at the gym.</p>"),
            ("How Gym Twins builds these in", "<p>Gym Twins is built around these habits: you set your gym days, rest days keep your streak with a check-in, a 10-minute workout keeps a gym day, and after a miss you have 3 days to bounce back before your pixel twin shrinks a level. Friends can keep a shared streak with you.</p>"),
        ],
        "faq": [
            ("How many days a week should I go to the gym to stay consistent?", "Pick the number you could keep in your busiest week. For many people that is two or three days, and you can add more once it feels easy."),
            ("What should I do after missing a gym day?", "Go back within a few days, even for a short session. The second and third missed days do more harm to the habit than the first."),
            ("Is a short workout worth it?", "For the habit, yes. A short session on a bad day keeps the routine going and is easier to start than a full workout."),
        ],
        "links": [("workout-streak-tracker/", "A workout streak tracker that counts rest days"), ("rest-day-streak/", "Do rest days break your streak?"), ("programs/", "Free workout plans")],
    },
    {
        "slug": "rest-day-streak",
        "title": "Do Rest Days Break Your Workout Streak? | Gym Twins",
        "desc": "Do rest days break your workout streak? Not in Gym Twins: planned rest days keep it with a quick check-in. How rest days, missed days and the 3 AM day end work.",
        "kicker": "Rest days",
        "h1": "Do rest days break your workout streak?",
        "twin": ("twin-lv2-idle", 7, "A level 2 twin resting"),
        "answer": "In many streak apps, yes: they count only days with a workout, so every rest day resets you. In Gym Twins, no. Any day that isn't in your training plan is a rest day, and one tap on Rest check-in keeps the streak alive. A workout on a rest day counts too.",
        "sections": [
            ("Gym days and rest days", "<p>You choose your gym days once, for example Monday, Wednesday and Friday. On those days the streak needs a workout of 10 minutes or more. Every other day is a rest day, and a check-in is all it needs. A check-in alone doesn't keep a gym day, which is why the app offers it only on rest days.</p>"),
            ("Late workouts and the 3 AM day end", "<p>Your day ends at 3:00 AM in your time zone, not at midnight. A session that starts at 11:30 PM and ends after midnight still counts for the day it started.</p>"),
            ("What if you skip a gym day?", "<p>Then the streak resets and your pixel twin gets tired. Log a workout of 10 minutes or more within the next 3 days and it recovers at the same level. If not, it shrinks back one level.</p><p>Need a break you didn't plan? A streak freeze from the Shop, bought with gems you earn by training, covers a missed day.</p>"),
            ("Why rest days should count", "<p>Recovery is part of training. A tracker that treats rest as failure pushes you toward skipping recovery or quitting the streak. Counting planned rest keeps the streak honest: it measures whether you followed your plan.</p>"),
        ],
        "faq": [
            ("What counts as a rest day in Gym Twins?", "Any day that isn't in your training plan. You can change the plan in Settings and the new plan starts the next day."),
            ("Can I work out on a rest day?", "Yes. A workout on a rest day keeps the day too."),
            ("Does a rest check-in keep a gym day?", "No. A gym day needs a workout of 10 minutes or more."),
        ],
        "links": [("workout-streak-tracker/", "A workout streak tracker that counts rest days"), ("gym-consistency/", "How to stay consistent at the gym"), ("contact.html", "Support and FAQ")],
    },
    {
        "slug": "workout-log-app",
        "title": "Simple Workout Log for iPhone: Sets, Reps, Weight",
        "desc": "Gym Twins is a simple workout log for iPhone: log sets, reps and weight with a rest timer, or log a whole session in about 10 seconds. Keep a gym streak.",
        "kicker": "Workout log",
        "h1": "A simple workout log for iPhone",
        "twin": ("twin-lv5-flex", 6, "A level 5 twin flexing"),
        "answer": "Gym Twins logs a workout two ways. A quick log takes about 10 seconds: pick the body regions you trained, set the time and say how it felt. A live workout tracks every set, rep and weight as you go, with a rest timer between sets. Either one keeps your daily gym streak.",
        "sections": [
            ("Live workouts", "<p>Start a session from a <a href=\"../programs/\">plan</a> or from scratch and log sets, weight and reps as you lift. A rest timer runs between sets and shows on your Lock Screen and Dynamic Island as a Live Activity. If the app closes mid-workout, you pick up where you left off.</p>"),
            ("Quick logs", "<p>Trained somewhere you don't want to tap through every set? Log the session in about 10 seconds: body regions, minutes and how hard it felt.</p>"),
            ("An exercise library that works offline", "<p>More than 90 exercises with step-by-step form guides, sorted by body region and equipment. The same guides are on this site in the <a href=\"../exercises/\">exercise library</a>.</p>"),
            ("A log that keeps you coming back", "<p>Every workout feeds your streak and your pixel twin, which grows through five levels as you earn XP from the minutes you train. A Home Screen heat map shows the weeks you trained.</p>"),
        ],
        "faq": [
            ("Can I log sets, reps and weight?", "Yes. A live workout logs each set's weight and reps, with a rest timer between sets."),
            ("How fast is logging a workout?", "A quick log takes about 10 seconds: body regions, time and how it felt."),
            ("Does the exercise library need an account or internet?", "No. It works offline."),
        ],
        "links": [("exercises/", "Exercise library"), ("programs/", "Free workout plans"), ("workout-streak-tracker/", "A workout streak tracker that counts rest days")],
    },
]


def page(p):
    sheet, frames, label = p["twin"]
    sections = "".join(f'<section class="ex-block card"><h2>{e(h)}</h2>{body}</section>' for h, body in p["sections"])
    faq = "".join(f'<details class="card"><summary>{e(q)}</summary><div class="faq-answer"><p>{e(a)}</p></div></details>' for q, a in p["faq"])
    more = "".join(f'<li><a href="../{href}">{e(label_)}</a></li>' for href, label_ in p["links"])
    ld = [faq_ld(p["faq"]), breadcrumbs([("Home", SITE), (p["kicker"], None)])]
    body = f'''    <article class="ex">
      <div class="container ex-wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a></nav>
        <header class="ex-head">
          <div class="ex-art card guide-twin">{TWIN.format(label=label, sheet=sheet, frames=frames)}</div>
          <div>
            <span class="section-kicker">{e(p["kicker"])}</span>
            <h1>{e(p["h1"])}</h1>
            <p class="ex-answer">{p["answer"]}</p>
          </div>
        </header>
        {sections}
        <aside class="ex-cta card"><div><h2>Try it in Gym Twins</h2><p>Plan your gym days, keep the streak and watch your pixel twin grow, from Beginner to Beast Mode.</p></div>{store_badge(1)}</aside>
        <section class="faq guide-faq"><h2>Questions</h2>{faq}</section>
        <section class="ex-related"><h2>Read next</h2><ul class="guide-links">{more}</ul></section>
      </div>
    </article>
'''
    return head(p["title"], p["desc"], f'{p["slug"]}/', 1, ld) + navbar(1) + body + footer(1)


def generate(root):
    for p in PAGES:
        (root / p["slug"]).mkdir(exist_ok=True)
        (root / p["slug"] / "index.html").write_text(page(p), encoding="utf-8")
    return len(PAGES)
