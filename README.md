# Gym Twin, landing site

Marketing and legal website for **Gym Twin**, a gym streak tracker for iPhone. Log a workout or a
rest-day check-in every day and your pixel-art gym twin grows through five levels, from Beginner to
Beast Mode.

- **Live site (GitHub Pages, custom domain):** https://gymtwins.com/
- **Privacy policy:** https://gymtwins.com/privacy.html
- **Consumer health data privacy policy:** https://gymtwins.com/consumer-health-data.html
- **Terms of use:** https://gymtwins.com/terms.html
- **Support:** https://gymtwins.com/contact.html
- **App Store:** not live yet (the pages show a "coming soon" badge)

## Stack

Pure HTML5, CSS3 and vanilla JavaScript. No frameworks, no build step. The custom domain `gymtwins.com` is set by the `CNAME` file (DNS at Namecheap: four GitHub Pages A records on `@` and a `www` CNAME to `asimcanyagiz.github.io`).

- `index.html`: landing page (hero with a playable twin demo, five levels, streak rules, features including Spot, Food, programs, friends, Hardmode and Gym Dash, privacy summary, final call to action)
- `contact.html`: support page (FAQ and a contact form)
- `privacy.html` / `consumer-health-data.html` / `terms.html`: legal pages. `consumer-health-data.html` is the Consumer Health Data Privacy Policy that Washington's My Health My Data Act requires (linked from the home page footer and privacy.html). They must match what the app does with data and what the subscription offers (weekly with a 3-day free trial, yearly, monthly offer). Update them in the same change whenever the app's data flows or plans change; the app links to both (`LegalLinks.swift` in the Gym Twin repo)
- `css/style.css`: single stylesheet, the app's Duolingo-style design tokens (orange `#FF9600`, Nunito)
- `js/main.js`: navigation, scroll reveals, store badge swap, hero twin demo
- `js/web3forms.js`: contact form handler (opens the visitor's email app, same approach as the MoneyPot site)
- `Assets/`: icon, social image, and pixel sprite sheets copied from the app (`Assets/sprites/`)

## Going live on the App Store

Set `APP_STORE_URL` at the top of `js/main.js`. Every element with `data-store-badge` then turns into
Apple's official "Download on the App Store" badge linking to the app.

## Notes

- Keep links and asset paths relative. The site is served from the root of `gymtwins.com`; the old `asimcanyagiz.github.io/Gymtwin-Website/` URLs redirect there.
- Push to `main` to deploy.
