# Sahasranama Guru: handoff for another developer or AI

Owner: Pranav. Repo: https://github.com/pranavbpk/vishnu-sahasranam-
Live site (GitHub Pages): https://pranavbpk.github.io/vishnu-sahasranam-/
Updated: 9 Nov 2026 (live = Version 106, Guru Test and Guru Dev = build 296).

## What the app is
A free web app (PWA) for learning Vishnu Sahasranamam the guru-shishya way:
listen, repeat each line after the guide, say the whole verse, record yourself,
then read the meaning. One new verse a day, revision after 1, 3 and 7 days.
Extras: Swadhyayam (guru's class recordings, owner and students only),
My slokas (owner only: add any audio + words and practise it), Satsang dates,
Learn (meanings, stories, how to read), Telugu/Hindi interface.

## Files
- Three copies of ONE code file (Dev → Test → Prod), from 9 Nov 2026:
  - `index-dev.html`: "Guru Dev" (red DEV tag). ALL new work goes here first.
  - `index-proto.html`: "Guru Test" (amber TEST tag). Owner + a few testers.
  - `index.html`: the LIVE app (Prod). One file: HTML + CSS + vanilla JS. No framework, no build step.
  - The copies differ only in the `var ENV='dev'|'test'|'prod'` line (top of the first script), title, manifest
    and version label. Never hand-edit Test or Prod: use `python3 tools/promote.py dev test` and,
    only after the owner says "go live", `python3 tools/promote.py test prod` + `git tag vNNN`.
    `python3 tools/promote.py check` shows each copy's build.
  - Storage: Dev/Test prefix every localStorage key, IndexedDB name and Cache name with `dev_` / `test_`
    (env block patches Storage/IDBFactory/CacheStorage). On first open they copy the live data once,
    read only (flags `<prefix>__init`, `<prefix>__idb_<name>`). Prod keeps the plain names. Live data is never written by Dev/Test.
  - Shared files (audio/, img/, content/, satsang.json): only add; never change a format Prod reads. New format = new file name.
- `sw-proto.js`: service worker (offline cache) for all pages.
- `manifest.webmanifest` (live), `manifest-test.webmanifest` (Guru Test), `manifest-dev.webmanifest` (Guru Dev).
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

## How the code is organised (inside index-dev.html)
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
  Build 287: Lines in the sound ⋯ menu has ✂ Split the sound in two (myspl, cut at the longest pause near the middle) and 🧩 Learn in 2 small pieces (mypz: cuts sound + words, cut saved in `x.soft`). Learn with guru groups soft-cut pieces (myGroups): piece 1, piece 2, then the full line. Join on a soft cut merges the words back. Words view auto-scrolls to the line being chanted (myScrollLn). Build 290: on Lines in the sound, tap a word (MYWD) to move it (and the words after/before it) to the next line or the line above (mywmv); the sound is not changed. Build 291: Edit sloka has a Sound step (Change › → Record / Audio file → Use this sound: myrepl keeps the words, resets timings, then opens Tap along). After saving a new sloka with 2+ word lines, Tap along opens straight away (MYTAPNEW) with a Skip button (tapskip). Tap along is a visible step on Edit sloka. Build 292: main setup is now one screen "Set up the parts" (myT2Page, MYT2, t2* actions): audio plays, all words shown, tap the first word of each part after a pause; Save rebuilds the words as one line per part and sets x.lt, so sound and words match. Opens after saving a new sloka or changing the sound; old tap along kept under More ways to fix. Build 293: layout D compact Today list (tdCompact): one row with all revision numbers, one row per new verse, real total minutes; Listen/Chant pills and step strip hidden in D. Build 294: layout D home rebuilt (bigHome → dhHead + practice card + dhTiles). Header style S.dhs: big / circle (default) / portrait / arch, switch "Test · header" under the Today layout switch. Tiles: Swadhyayam wide (owner/students only) + Parayanam, Learned wide + Verses a day. 🔔 opens Satsang (badge = events in 30 days). Revision numbers tap to the meaning view. Build 299: Swadhyayam links (swLinkBox, swlink: YouTube → l.yt plays in an in-app youtube-nocookie iframe sheet swYtSheet, minutes counted from the player state via postMessage; audio link → l.url plays in the normal player), sleep timer chip (swslp, SWSLP checked in swTick), one line a day card after 20 min (swLineCard, S.swtk, listed in All my notes). My slokas guide help/my-slokas.html (English/Telugu/Hindi, ?l=) opened from the small ? in the My slokas headers (myHelpU). Build 300: soft echo at line ends (echoW in wordsHTML): last word ending ah/ih/uh (or ః / ः) shows the echo in small raised letters; setting S.echo (You → Look, default Show). Build 301: small examples card (echCard, ECH en/te/hi) inside How to read (rdTable): end of line = soft echo, middle = as written, no h = nothing.
- Version: `var APPV=<n>` (Guru Test build number). The app compares it with the server copy and shows "New version ready". Bump it on EVERY change.

## iPhone rules learned the hard way (do not break these)
- Never use Web Audio (AudioContext) for playback: it silenced HTML audio in the Home Screen app.
- `play()` must run inside the user's tap. If a file must load first, play the silent clip `SWSIL` on the same element inside the tap, then swap `src`.
- iPhone sometimes fires an early `ended`, and after a jump back it can briefly report the old position. Guard both (see `myPlaySpan`, the 1.5 s early-ended guard).
- Fixed backgrounds inside scrolling boxes don't stay fixed on iPhone: use a `position:fixed` layer instead.

## Working rules agreed with the owner
1. Change `index-dev.html` only. Bump `APPV` +1 every time. When it works, `tools/promote.py dev test`.
2. Make it live only when the owner says "go live": `tools/promote.py test prod` (does the title, manifest,
   hsBar() returns '', VLBL='Version N · date', removes the build label), commit, `git tag vN`, push the tag.
   Roll back = check out the previous tag's index.html.
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
- Work only on index-dev.html (Guru Dev), then promote to Test. Never edit index.html, sw-proto.js caches, content/students.json or the owner-only areas (Swadhyayam, My plans, OWN/OWNH checks) unless the owner asks in plain words.
- Do not add any analytics, tracking, ads, third-party scripts, fonts or CDNs, cookies, or calls to any server or API that are not already in the file. No new fetch() to outside addresses. Say so clearly if a feature would need one.
- Do not ask for, store or print passwords, tokens, keys, email addresses, the guru's OneDrive link, or the owner's progress file.
- Keep: one file, vanilla JS/CSS, no build step, no framework. Keep the iPhone audio rules above.
- Never name books, institutes or commercial recordings inside the app.
- Bump APPV by 1 for every change. Test at 393x852. Check the script with node --check.
- Give the owner a short list of what changed and how to test it.
