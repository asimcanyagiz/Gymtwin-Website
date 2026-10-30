# Gymtwin, landing site

Marketing and legal website for **Gymtwin**, a gym streak tracker for iPhone. Log a workout or a
rest-day check-in every day and your pixel-art gym twin grows through five levels, from Beginner to
Beast Mode.

- **Live site (GitHub Pages):** https://asimcanyagiz.github.io/Gymtwin-Website/
- **Privacy policy:** https://asimcanyagiz.github.io/Gymtwin-Website/privacy.html
- **Terms of use:** https://asimcanyagiz.github.io/Gymtwin-Website/terms.html
- **Support:** https://asimcanyagiz.github.io/Gymtwin-Website/contact.html
- **App Store:** not live yet (the pages show a "coming soon" badge)

## Stack

Pure HTML5, CSS3 and vanilla JavaScript. No frameworks, no build step, no custom domain (no CNAME).

- `index.html`: landing page (hero with a playable twin demo, five levels, streak rules, features including Spot, Food, programs, friends, Hardmode and Gym Dash, privacy summary, final call to action)
- `contact.html`: support page (FAQ and a contact form)
- `privacy.html` / `terms.html`: legal pages. They must match what the app does with data and what the subscription offers (weekly with a 3-day free trial, yearly, monthly offer). Update them in the same change whenever the app's data flows or plans change; the app links to both (`LegalLinks.swift` in the Gymtwin repo)
- `css/style.css`: single stylesheet, the app's Duolingo-style design tokens (orange `#FF9600`, Nunito)
- `js/main.js`: navigation, scroll reveals, store badge swap, hero twin demo
- `js/web3forms.js`: contact form handler (opens the visitor's email app, same approach as the MoneyPot site)
- `Assets/`: icon, social image, and pixel sprite sheets copied from the app (`Assets/sprites/`)

## Going live on the App Store

Set `APP_STORE_URL` at the top of `js/main.js`. Every element with `data-store-badge` then turns into
Apple's official "Download on the App Store" badge linking to the app.

## Notes

- All links and asset paths are relative, because the site is served from the `/Gymtwin-Website/` subpath.
- Push to `main` to deploy.
