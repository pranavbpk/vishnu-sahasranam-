# Brief for another AI (Gemini) working on Sahasranama Guru

Paste this whole file at the start of the chat, then say what you want done.
Owner: Pranav. Plain, simple wording please, short answers, bullet points.

## 1. What the app is
A free web app (PWA, works offline, installed to the iPhone Home Screen) for learning
Vishnu Sahasranamam the guru way: listen, repeat line by line, record yourself, read the meaning.
One new verse a day, revision after 1, 3 and 7 days. Telugu / Hindi interface.
Extras: Swadhyayam (guru's class recordings, notes, links), My slokas (add any audio + words and
practise it), Satsang dates, Learn (meanings, stories, how to read).

- Repo: https://github.com/pranavbpk/vishnu-sahasranam-  (branch `main`, GitHub Pages)
- Live:  https://pranavbpk.github.io/vishnu-sahasranam-/
- Test:  https://pranavbpk.github.io/vishnu-sahasranam-/index-proto.html
- Dev:   https://pranavbpk.github.io/vishnu-sahasranam-/index-dev.html
- Full technical notes: `HANDOFF.md` in the repo. Read it before changing code.

## 2. The three copies (very important)
One code file, three copies. They differ ONLY in one line `var ENV='dev'|'test'|'prod'`
(top of the first `<script>`), the title, the manifest and the version label.

| Copy | File | Who |
|---|---|---|
| Dev  | `index-dev.html`   | All new work goes here first |
| Test | `index-proto.html` | Owner + testers |
| Live | `index.html`       | Everyone. Only when the owner says "go live" |

- Change `index-dev.html` only. Bump `var APPV=<n>` by 1 on every change.
- Copy Dev to Test: `python3 tools/promote.py dev test`
- Go live (only when the owner says so): `python3 tools/promote.py test prod`, commit, `git tag vNNN`.
- Check: `python3 tools/promote.py check`
- Never hand-edit `index-proto.html` or `index.html`.
- Dev and Test keep their own phone storage (prefix `dev_` / `test_`), so they can't touch live data.

## 3. How the code works (short)
- One HTML file: HTML + CSS + plain JavaScript. No framework, no build step.
- State: object `S`, saved with `sv()`. `render()` redraws `#app` from HTML strings; `render(1)` redraws fully.
- Clicks: one listener reads `data-act` and `data-v` on buttons. Owner areas use the `OWNA` object.
- Views: `view` = 'home' | 'verse'. Home tabs `HT` = today | prac | sat | lib | me.
- Practice ("Repeat after me"): `RP` state, `rpStart()`, old screen `rpSheet()`, new screen `rpSheet2()`, finish screens `g2Done()`.
- Verses: array `V` (n, sa = Devanagari, te = Telugu, pr = English read-aloud with dashes, en).
  Meanings `M`. Telugu/Devanagari dash lines `DASH`.
- Swadhyayam: list `LEC`, player `swOpen()`, page `swPage()`. OneDrive sign-in `msLogin()` (expires every 24 h, by Microsoft).
- My slokas: list `SLK`, setup screen `myT2Page()`, help page `help/my-slokas.html` (English / Telugu / Hindi).
- Audio files: `audio/vNNN.m4a` (owner's voice), `audio/cuts.json` (pause between line 1 and 2).

## 4. Rules (learned the hard way)
1. iPhone: never use Web Audio (AudioContext) for playback. `play()` must run inside the user's tap.
2. Never put anything on `body::before` or `body::after`: they paint the Vishnu picture behind the verse screens.
   (A DEV/TEST tag there once made the practice screen see-through.)
3. Before every push: check the script for syntax errors:
   extract the `<script>` blocks and run `node --check`. Test at phone size 393 x 852.
4. If you can, run `python3 tools/smoke.py index-dev.html` (needs Playwright) and fix any error it prints.
5. Anything with sound: Dev/Test first, the owner checks on his iPhone.
6. Never name books, institutes or commercial recordings in the app. Guide audio = owner's own voice.
7. Meanings, Telugu/Hindi wording and pronunciation are drafts for the guru's review.
8. Owner-only areas (Swadhyayam, My slokas, `OWN` checks): don't change who can see them.
9. Plain wording in the app: short sentences, no jargon.

## 5. Where things stand (9 Nov 2026)
- Live = Version 106. Dev and Test = build 303.
- Being tested in Test, owner deciding:
  - Today layout D with 4 header styles (Big / Circle / Portrait / Arch).
  - Soft echo at line ends (pra-bhu^hu), with a setting in You → Look.
  - Verse 1 meaning picture (A soft / B colourful).
- Coming next (owner's own work): recording Dhyanam, Poorvangam, Phala-shruti.
- Ideas not built yet: save Swadhyayam classes on the phone (to avoid the daily sign-in);
  Swadhyayam for the whole class (weekly lessons, notes, quizzes, doubts to Swamy);
  satsang booking on Azure.

## 6. How to ask for work
- "Change X in Dev": build in `index-dev.html`, bump APPV, push.
- "Move to Test": `promote.py dev test`, push.
- "Go live": `promote.py test prod`, tag, push.
- Always say what you changed in 2 to 4 bullet points, and which build number.
