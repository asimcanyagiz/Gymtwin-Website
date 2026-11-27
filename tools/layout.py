"""The shared page frame (head, navbar, footer) for generated and hand-written pages."""
import html, json

e = html.escape
SITE = "https://gymtwins.com/"
NAV = [("#features", "Features", None), ("exercises/", "Exercises", "exercises"), ("programs/", "Programs", "programs"), ("contact.html", "Support", "support")]


def head(title, desc, canon, depth, ld=None, og_type="article", image="Assets/og-image.png"):
    up = "../" * depth
    lds = "".join(f'\n    <script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#FFFFFF">
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}">
    <link rel="canonical" href="{SITE}{canon}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="Gym Twins">
    <meta property="og:url" content="{SITE}{canon}">
    <meta property="og:title" content="{e(title)}">
    <meta property="og:description" content="{e(desc)}">
    <meta property="og:image" content="{SITE}{image}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" type="image/png" href="{up}Assets/favicon.png">
    <link rel="apple-touch-icon" href="{up}Assets/apple-touch-icon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{up}css/style.css">{lds}
</head>
'''


def navbar(depth, active=None):
    up = "../" * depth
    links = "\n".join(
        f'                <a href="{up}{href}" class="navbar-link{" active" if key and key == active else ""}"{" aria-current=\"page\"" if key and key == active else ""}>{label}</a>'
        for href, label, key in NAV
    )
    return f'''<body>
    <a href="#main" class="skip-link">Skip to content</a>
    <nav class="navbar" aria-label="Main">
        <div class="container navbar-container">
            <a href="{up or './'}" class="navbar-brand" aria-label="Gym Twins home">
                <img src="{up}Assets/icon.png" alt="" class="navbar-logo" width="38" height="38">
                <span class="navbar-name">Gym Twins</span>
            </a>
            <div class="navbar-menu" id="navbarMenu">
{links}
                <a href="{up}#get" class="navbar-cta">Coming soon</a>
            </div>
            <button class="navbar-toggle" id="navbarToggle" aria-label="Open menu" aria-expanded="false" aria-controls="navbarMenu">
                <span class="navbar-toggle-icon"></span>
            </button>
        </div>
    </nav>

    <main id="main">
'''


def footer(depth):
    up = "../" * depth
    return f'''    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <img src="{up}Assets/icon.png" alt="" class="footer-logo" width="44" height="44">
                    <div>
                        <span class="footer-name">Gym Twins</span>
                        <span class="footer-tag">Gym streak tracker for iPhone</span>
                    </div>
                </div>
                <nav class="footer-links" aria-label="Footer">
                    <a href="{up}exercises/">Exercises</a>
                    <a href="{up}programs/">Programs</a>
                    <a href="{up}workout-streak-tracker/">Workout streak tracker</a>
                    <a href="{up}contact.html">Support</a>
                    <a href="{up}privacy.html">Privacy Policy</a>
                    <a href="{up}consumer-health-data.html">Consumer Health Data Privacy Policy</a>
                    <a href="{up}terms.html">Terms of Use</a>
                </nav>
            </div>
            <p class="footer-copyright">&copy; 2026 Asım Can Yağız. All rights reserved.</p>
        </div>
    </footer>

    <script src="{up}js/main.js"></script>
</body>
</html>
'''


def store_badge(depth):
    up = "../" * depth
    return (f'<a class="store-badge" data-store-badge><img src="{up}Assets/icon.png" alt="" class="store-badge__icon" width="40" height="40">'
            f'<span class="store-badge__text"><small>Coming soon</small><strong>on the App Store</strong></span></a>')


def breadcrumbs(items):
    """items: [(name, absolute url or None)] -> BreadcrumbList JSON-LD."""
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, **({"item": u} if u else {})} for i, (n, u) in enumerate(items)]}
