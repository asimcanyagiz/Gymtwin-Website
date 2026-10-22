/**
 * Gymtwin - Main JavaScript
 * Navigation, scroll reveals, smooth scrolling, the store badge swap,
 * and the "try it" twin demo in the hero. Vanilla JS, no dependencies.
 */

/* ---------------------------------------------------------------
   App Store link
   Gymtwin is not on the App Store yet. Leave this empty until launch;
   when the app is live, paste its URL here (for example
   'https://apps.apple.com/app/id0000000000') and every
   [data-store-badge] element turns into Apple's official badge.
--------------------------------------------------------------- */
const APP_STORE_URL = '';

const APPLE_BADGE_SRC =
    'https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/en-us';

function initStoreBadges() {
    if (!APP_STORE_URL) return; // still "coming soon": keep the placeholder pill

    document.querySelectorAll('[data-store-badge]').forEach((badge) => {
        badge.setAttribute('href', APP_STORE_URL);
        badge.setAttribute('aria-label', 'Download Gymtwin on the App Store');
        badge.classList.add('is-live');
        const img = document.createElement('img');
        img.src = APPLE_BADGE_SRC;
        img.alt = 'Download on the App Store';
        img.width = 160;
        img.height = 54;
        badge.replaceChildren(img);
    });
}

/* ---------------------------------------------------------------
   TikTok in-app browser workaround (same as the other landing sites)
   TikTok's WebView blocks App Store links, so we nudge visitors to
   open the page in their real browser. Only useful once there is an
   App Store link, so it does nothing before launch.
--------------------------------------------------------------- */
function initTikTokWorkaround() {
    if (!APP_STORE_URL) return;

    const userAgent = navigator.userAgent || navigator.vendor || window.opera;
    const isTikTokBrowser = /musical_ly|BytedanceWebview|TikTok/i.test(userAgent);
    const fromTikTok = new URLSearchParams(window.location.search).get('from') === 'tiktok';

    if (isTikTokBrowser) {
        // Tag the URL so, if reopened in Safari, we can send them on to the App Store
        if (!fromTikTok) {
            const newUrl = new URL(window.location.href);
            newUrl.searchParams.set('from', 'tiktok');
            window.history.replaceState({}, '', newUrl);
        }
    } else if (fromTikTok) {
        window.location.href = APP_STORE_URL;
    }
}

/* ---------------------------------------------------------------
   Navigation bar: border on scroll + mobile drawer toggle
--------------------------------------------------------------- */
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const toggle = document.getElementById('navbarToggle');
    const menu = document.getElementById('navbarMenu');
    if (!navbar) return;

    // Hairline under the bar once the page scrolls
    const onScroll = () => navbar.classList.toggle('scrolled', window.scrollY > 10);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    if (!toggle || !menu) return;

    const closeMenu = () => {
        toggle.classList.remove('active');
        menu.classList.remove('active');
        toggle.setAttribute('aria-expanded', 'false');
    };

    toggle.addEventListener('click', () => {
        const open = menu.classList.toggle('active');
        toggle.classList.toggle('active', open);
        toggle.setAttribute('aria-expanded', String(open));
    });

    // Close after picking a link
    menu.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));

    // Close when clicking outside the bar
    document.addEventListener('click', (e) => {
        if (menu.classList.contains('active') && !navbar.contains(e.target)) closeMenu();
    });

    // Close on Escape and hand focus back to the toggle
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && menu.classList.contains('active')) {
            closeMenu();
            toggle.focus();
        }
    });
}

/* ---------------------------------------------------------------
   Scroll reveal: fade elements in as they enter the viewport
--------------------------------------------------------------- */
function initScrollReveal() {
    const targets = document.querySelectorAll(
        '.section-head, .ladder-item, .rule, .miss, .feature, .privacy-band, .final-cta, ' +
        '.legal-body > section, .faq details, .contact-card'
    );
    targets.forEach((el) => el.classList.add('reveal'));

    // No IntersectionObserver (or reduced motion): just show everything
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!('IntersectionObserver' in window) || reduceMotion) {
        targets.forEach((el) => el.classList.add('active'));
        return;
    }

    const observer = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    obs.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    targets.forEach((el) => observer.observe(el));
}

/* ---------------------------------------------------------------
   Smooth scroll for same-page anchors (offset for the sticky bar)
--------------------------------------------------------------- */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((link) => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (!target) return;
            e.preventDefault();
            const navbar = document.querySelector('.navbar');
            const offset = navbar ? navbar.offsetHeight : 68;
            const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top, behavior: 'smooth' });
        });
    });
}

/* ---------------------------------------------------------------
   Twin demo (hero)
   A simplified copy of the app's streak rules:
   - Gym days need a workout; rest days need a check-in (or a workout).
   - Each kept day adds 1 to the streak. Workouts also add XP.
   - Fill the XP bar and the twin evolves to the next level.
   - Missing a day with a streak makes the twin tired. A workout within
     3 days brings it back; otherwise it shrinks one level (never below Lv 1).
   The demo uses 2 workouts per level so visitors can see an evolution
   quickly. Real XP comes from the minutes you train.
--------------------------------------------------------------- */
const LEVEL_NAMES = ['Beginner', 'Starter Pump', 'Consistent Grinder', 'Iron Mode', 'Beast Mode'];
// Frames per sheet, read from the PNG widths (64px per frame)
const SHEET_FRAMES = { idle: [6, 7, 6, 8, 6], flex: [7, 8, 5, 9, 8] };
const WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const GYM_DAYS = [true, false, true, false, true, true, false]; // Mon, Wed, Fri, Sat
const XP_PER_WORKOUT = 50;     // percent of the bar
const RECOVERY_DAYS = 3;

function initTwinDemo() {
    const root = document.getElementById('twinDemo');
    if (!root) return;

    // Elements the demo writes to
    const el = {
        stage: root.querySelector('.stage'),
        sprite: root.querySelector('.stage-twin .sprite'),
        level: root.querySelector('[data-demo="level"]'),
        streak: root.querySelector('[data-demo="streak"]'),
        tired: root.querySelector('[data-demo="tired"]'),
        xpLabel: root.querySelector('[data-demo="xp-label"]'),
        xpFill: root.querySelector('.xp-fill'),
        xpBar: root.querySelector('.xp-bar'),
        week: root.querySelectorAll('.week li'),
        day: root.querySelector('[data-demo="day"]'),
        status: root.querySelector('[data-demo="status"]'),
        btnWorkout: root.querySelector('[data-action="workout"]'),
        btnCheckin: root.querySelector('[data-action="checkin"]'),
        btnSkip: root.querySelector('[data-action="skip"]'),
    };
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // The whole demo state
    const state = {
        level: 1,          // 1..5
        xp: 0,             // 0..100 (% of the current level's bar)
        streak: 0,
        tired: false,
        daysLeft: 0,       // days left to recover while tired
        day: 0,            // index into WEEK_DAYS
        marks: Array(7).fill(null), // 'done' | 'rested' | 'missed' per weekday
    };
    let flexTimer = null;
    let sheetKind = 'idle'; // which sheet is on screen

    /* Show a sheet ('idle' or 'flex') for the current level */
    function showSheet(kind) {
        sheetKind = kind;
        const lv = state.level;
        el.sprite.style.backgroundImage = "url('Assets/sprites/twin-lv" + lv + '-' + kind + ".png')";
        el.sprite.style.setProperty('--frames', SHEET_FRAMES[kind][lv - 1]);
        el.sprite.setAttribute('aria-label', 'Your twin at level ' + lv + ', ' + LEVEL_NAMES[lv - 1] +
            (state.tired ? ', looking tired' : ''));
    }

    /* Play the flex animation for a moment, then go back to idle */
    function celebrate() {
        clearTimeout(flexTimer);
        showSheet('flex');
        flexTimer = setTimeout(() => showSheet('idle'), 1800);
    }

    /* Re-run a one-shot CSS effect class on the stage */
    function playEffect(className, ms) {
        if (reduceMotion) return;
        el.stage.classList.remove(className);
        void el.stage.offsetWidth; // restart the animation
        el.stage.classList.add(className);
        setTimeout(() => el.stage.classList.remove(className), ms);
    }

    /* Draw everything from state */
    function render() {
        const isGymDay = GYM_DAYS[state.day];
        el.level.textContent = 'Lv ' + state.level + ' · ' + LEVEL_NAMES[state.level - 1];
        el.streak.textContent = '🔥 ' + state.streak;
        el.streak.setAttribute('aria-label', 'Streak: ' + state.streak + (state.streak === 1 ? ' day' : ' days'));
        el.tired.hidden = !state.tired;
        el.tired.textContent = '💤 Tired · ' + state.daysLeft + (state.daysLeft === 1 ? ' day left' : ' days left');
        el.stage.classList.toggle('is-tired', state.tired);

        const maxed = state.level === 5;
        el.xpFill.style.width = (maxed ? 100 : state.xp) + '%';
        el.xpBar.setAttribute('aria-valuenow', String(maxed ? 100 : state.xp));
        el.xpLabel.textContent = maxed ? 'Max level' : 'Next: ' + LEVEL_NAMES[state.level];

        // Week strip: plan icon, result of past days, ring on today
        el.week.forEach((li, i) => {
            const mark = state.marks[i];
            const dot = li.querySelector('.dot');
            li.className = '';
            if (mark === 'done') { li.classList.add('is-done'); dot.textContent = '🔥'; }
            else if (mark === 'rested') { li.classList.add('is-rested'); dot.textContent = '🌙'; }
            else if (mark === 'missed') { li.classList.add('is-missed'); dot.textContent = '✕'; }
            else { li.classList.add(GYM_DAYS[i] ? 'is-plan' : 'is-rest'); dot.textContent = GYM_DAYS[i] ? '💪' : '🌙'; }
            if (i === state.day) li.classList.add('is-today');
        });

        // Gym day: Log workout is the main action. Rest day: check-in is.
        const dayName = document.createElement('strong');
        dayName.textContent = WEEK_DAYS[state.day];
        el.day.replaceChildren('Today: ', dayName, ' · ' + (isGymDay ? 'gym day' : 'rest day'));
        el.btnCheckin.hidden = isGymDay;
        el.btnWorkout.classList.toggle('btn--primary', isGymDay);
        el.btnWorkout.classList.toggle('btn--block', isGymDay);
        el.btnWorkout.classList.toggle('btn--secondary', !isGymDay);
        // Keep the primary button on top: on rest days Log workout moves into the row
        if (isGymDay) el.btnCheckin.after(el.btnWorkout);
        else el.btnSkip.before(el.btnWorkout);
    }

    /* Move to the next day (a new week clears the strip) */
    function nextDay() {
        state.day = (state.day + 1) % 7;
        if (state.day === 0) state.marks = Array(7).fill(null);
    }

    /* A day closed without a workout while tired counts down; at 0 the twin shrinks */
    function countDownTired() {
        state.daysLeft -= 1;
        if (state.daysLeft > 0) return null;
        state.tired = false;
        if (state.level === 1) {
            return 'Three days without a workout. Your twin is already a Beginner, so it can\'t shrink further.';
        }
        state.level -= 1;
        state.xp = 0;
        playEffect('is-shrinking', 1000);
        return 'Three days without a workout. Your twin shrank to Lv ' + state.level + ' ' + LEVEL_NAMES[state.level - 1] + '.';
    }

    function logWorkout() {
        let msg;
        const recovered = state.tired; // a workout is the only cure for tiredness
        state.marks[state.day] = 'done';
        state.streak += 1;
        state.tired = false;
        if (recovered) {
            msg = 'Workout logged. Your twin recovered and kept its level. Streak: ' + state.streak + '.';
        } else {
            msg = 'Workout logged. +XP, and your streak is ' + state.streak + '.';
        }

        if (state.level < 5) {
            state.xp += XP_PER_WORKOUT;
            if (state.xp >= 100) {
                state.level += 1;
                state.xp = 0;
                // Keep the recovery news when both happen on the same workout
                msg = (recovered ? 'Recovered and evolved! ' : 'Evolution! ') +
                    'Your twin is now Lv ' + state.level + ' ' + LEVEL_NAMES[state.level - 1] + '.';
                playEffect('is-evolving', 1400);
            }
        }
        celebrate();
        return msg;
    }

    function restCheckIn() {
        state.marks[state.day] = 'rested';
        state.streak += 1;
        const msg = 'Rest day checked in. Streak: ' + state.streak + '.';
        if (state.tired) {
            // A check-in keeps the day, but only a workout cures tiredness
            return countDownTired() || msg + ' Still tired: only a workout brings it back.';
        }
        return msg;
    }

    function skipDay() {
        state.marks[state.day] = 'missed';
        if (state.tired) {
            state.streak = 0;
            return countDownTired() || 'Another missed day. Log a workout within ' + state.daysLeft +
                (state.daysLeft === 1 ? ' day' : ' days') + ' or your twin shrinks.';
        }
        if (state.streak >= 1) {
            state.streak = 0;
            state.tired = true;
            state.daysLeft = RECOVERY_DAYS;
            showSheet('idle');
            return 'Streak broken. Your twin is tired. A workout in the next 3 days brings it back.';
        }
        return 'Nothing to lose yet. Start a streak with your next workout or check-in.';
    }

    // Wire the buttons: run the action, move to the next day, redraw
    const actions = { workout: logWorkout, checkin: restCheckIn, skip: skipDay };
    root.querySelectorAll('[data-action]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const message = actions[btn.dataset.action]();
            nextDay();
            render();
            showSheet(sheetKind); // redraw for a level change or the tired label
            el.status.textContent = message;
        });
    });

    showSheet('idle');
    render();
}

/* ---------------------------------------------------------------
   Boot
--------------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
    initStoreBadges();
    initTikTokWorkaround();
    initNavbar();
    initScrollReveal();
    initSmoothScroll();
    initTwinDemo();
});
