# Sahasranama Guru: handoff for another developer or AI

Owner: Pranav. Repo: https://github.com/pranavbpk/vishnu-sahasranam-
Live site (GitHub Pages): https://pranavbpk.github.io/vishnu-sahasranam-/
Updated: 8 Nov 2026 (live = Version 106, Guru Test = build 277).

## What the app is
A free web app (PWA) for learning Vishnu Sahasranamam the guru-shishya way:
listen, repeat each line after the guide, say the whole verse, record yourself,
then read the meaning. One new verse a day, revision after 1, 3 and 7 days.
Extras: Swadhyayam (guru's class recordings, owner and students only),
My slokas (owner only: add any audio + words and practise it), Satsang dates,
Learn (meanings, stories, how to read), Telugu/Hindi interface.

## Files
- `index.html`: the LIVE app. One file: HTML + CSS + vanilla JS. No framework, no build step.
- `index-proto.html`: "Guru Test", the test copy. ALL new work goes here first.
- `sw-proto.js`: service worker (offline cache) for both pages.
- `manifest.webmanifest` (live) and `manifest-test.webmanifest` (Guru Test).
- `audio/vNNN.m4a`: guide audio for verses 1-108 (owner's voice).
  `audio/cuts.json` = pause between line 1 and line 2 (seconds) per verse.
  `audio/trim.json` = [speech start, speech end] per verse.
  `audio/all108.m4a` + `audio/all108.json` = all 108 verses in one file.
  `audio/ex/*.m4a` = example words for the "How to read" table.
- `content/*.json`: Guru explains, stories, Dhyanam, why-we-chant, arrangement, students list.
- `img/story/*.jpg`, `img/mean/*.jpg`: pictures (AI made, owner chosen).
- `satsang.json`: satsang dates and links.
- `preview-future.html`: static, clickable preview of future screens (not part of the app).
- Old versions live on the `backups` branch (backups/index-vNN.html), not on main.

## How the code is organised (inside index-proto.html)
- State: one object `S`, saved to localStorage key `sp2` with `sv()`.
  Recordings in IndexedDB `sp_rec`; owner data (My slokas etc.) in its own IndexedDB stores (`oPut`).
- Verse data: array `V` (n, sa = Devanagari lines, te = Telugu lines, pr = dash read-aloud lines, en, tip).
  Meanings in `M`. Telugu/Devanagari dash lines in `DASH`. Dhyanam in `DHY`, `DHYD`, `DHYE`.
- Rendering: `render()` builds HTML strings and morphs them into `#app`; `render(1)` replaces fully.
  Top-level views: `view` = 'home' or 'verse'. Home tabs: `HT` = today / prac (Revise) / sat / lib (Learn) / me (You).
  You sub-pages: `HMS`. Owner pages: `OWNP`. Overlays: `ovl()` (guided practice sheet `rpSheet()`, etc.).
- Clicks: one delegated listener on `#app` reads `data-act` (+ `data-v`). Owner actions live in the `OWNA` object.
- Guided practice ("Repeat after me"): `RP` state, `rpStart()`; steps line1 x2, line2 x2, whole x3.
- My slokas: `SLK` list, player state `MYP` (`mypStart`, `mypRound`, `mypQ` piece queue), words timeline `myTimeline`.
  Build 287: Lines in the sound ⋯ menu has ✂ Split the sound in two (myspl, cut at the longest pause near the middle) and 🧩 Learn in 2 small pieces (mypz: cuts sound + words, cut saved in `x.soft`). Learn with guru groups soft-cut pieces (myGroups): piece 1, piece 2, then the full line. Join on a soft cut merges the words back. Words view auto-scrolls to the line being chanted (myScrollLn). Build 290: on Lines in the sound, tap a word (MYWD) to move it (and the words after/before it) to the next line or the line above (mywmv); the sound is not changed. Build 291: Edit sloka has a Sound step (Change › → Record / Audio file → Use this sound: myrepl keeps the words, resets timings, then opens Tap along). After saving a new sloka with 2+ word lines, Tap along opens straight away (MYTAPNEW) with a Skip button (tapskip). Tap along is a visible step on Edit sloka. Build 292: main setup is now one screen "Set up the parts" (myT2Page, MYT2, t2* actions): audio plays, all words shown, tap the first word of each part after a pause; Save rebuilds the words as one line per part and sets x.lt, so sound and words match. Opens after saving a new sloka or changing the sound; old tap along kept under More ways to fix.
- Version: `var APPV=<n>` (Guru Test build number). The app compares it with the server copy and shows "New version ready". Bump it on EVERY change.

## iPhone rules learned the hard way (do not break these)
- Never use Web Audio (AudioContext) for playback: it silenced HTML audio in the Home Screen app.
- `play()` must run inside the user's tap. If a file must load first, play the silent clip `SWSIL` on the same element inside the tap, then swap `src`.
- iPhone sometimes fires an early `ended`, and after a jump back it can briefly report the old position. Guard both (see `myPlaySpan`, the 1.5 s early-ended guard).
- Fixed backgrounds inside scrolling boxes don't stay fixed on iPhone: use a `position:fixed` layer instead.

## Working rules agreed with the owner
1. Change `index-proto.html` only. Bump `APPV` +1 every time.
2. Make it live only when the owner says "go live":
   copy the old index.html to the `backups` branch as backups/index-vNN.html;
   index.html = index-proto.html with title/apple-mobile-web-app-title "Sahasranama Guru",
   manifest-test.webmanifest -> manifest.webmanifest, hsBar() returns '', VLBL='Version N · date',
   remove the "VLBL='Guru Test · build '+APPV" line (keep APPV).
3. Before every push: syntax-check the script (extract <script> blocks, `node --check`), test at phone size (393x852).
4. Anything touching sound: Guru Test first, the owner tests on his iPhone.
5. Never name books, institutes or commercial recordings inside the app. Guide audio = owner's own voice only.
6. Meanings, Telugu/Hindi wording and pronunciation are drafts for the guru's review.
7. Plain, simple wording in the app and in replies to the owner.

## Status and next ideas (8 Nov 2026)
- Live (index.html) = Version 106. Everything newer is only in Guru Test (index-proto.html), waiting for the owner's iPhone test and "go live".
- Being tested in Guru Test, owner still choosing:
  - Today layouts A/B/C/D (S.tdl), switch under the Today card. D (build 284) = clean: small streak pill, verse chips, clearer Swadhyayam card (tdDone, swHomeD), parayanam moves to the top when it is within 2 days (satSoon).
  - Repeat after me screen: old (rpSheet) or new (rpSheet2), S.gsty, "Old screen" button.
    Build 285: in the new style the finish screens (done, revdone, after recording) also use the new look: g2Done(). 
  - Verse meaning picture: slim row (small round picture + caption) while listening/chanting, big band on finish screens (vBand(n,sm), S.vpic Show/Hide), caption from MCAP. Verse 1 has two test pictures (S.v1p a/b: img/mean/v001.jpg, v001b.jpg).
  - My slokas player views (S.mpv): focus / karaoke / mini / full.
  - Vishnu picture behind verses (S.vbg: Soft / Clear / Off).
- Sound fix in build 274 (guided practice re-seeks until the part really plays from its start, because iPhone sometimes ignores a jump back). Must be tested on the owner's iPhone before going live.
- Build 276: verse + read-aloud lines shrink to fit the screen (vFit, never below 62%).
- Build 277: draggable progress bars ([data-seek]) in My slokas player and the PL players.
- Clickable previews (not part of the app): preview-future.html, preview-mysloka.html, preview-108.html.
- Planned: Azure hosting (Static Web Apps + Functions + Cosmos DB free tier) for real satsang booking, messages and sign-in; full chant parts (opening prayers, Dhyanam, 108, Phala-shruti, Lakshmi Ashtottaram) each with its own progress; class satsang with pranayama for the guru's students.

## Rules for any other AI helping (Gemini, Copilot, ChatGPT)
- Work only on index-proto.html (Guru Test). Never edit index.html, sw-proto.js caches, content/students.json or the owner-only areas (Swadhyayam, My plans, OWN/OWNH checks) unless the owner asks in plain words.
- Do not add any analytics, tracking, ads, third-party scripts, fonts or CDNs, cookies, or calls to any server or API that are not already in the file. No new fetch() to outside addresses. Say so clearly if a feature would need one.
- Do not ask for, store or print passwords, tokens, keys, email addresses, the guru's OneDrive link, or the owner's progress file.
- Keep: one file, vanilla JS/CSS, no build step, no framework. Keep the iPhone audio rules above.
- Never name books, institutes or commercial recordings inside the app.
- Bump APPV by 1 for every change. Test at 393x852. Check the script with node --check.
- Give the owner a short list of what changed and how to test it.
