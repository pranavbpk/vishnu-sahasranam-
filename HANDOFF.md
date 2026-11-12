# Sahasranama Guru: handoff for another developer or AI

Owner: Pranav. Repo: https://github.com/pranavbpk/vishnu-sahasranam-
Live site (GitHub Pages): https://pranavbpk.github.io/vishnu-sahasranam-/
Updated: 9 Nov 2026 (live = Version 106, Guru Test and Guru Dev = build 305).

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
- `docs/GEMINI-BRIEF.md`: one-page brief to paste into another AI. `tools/smoke.py`: checks every main screen for errors.
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
  Build 287: Lines in the sound ⋯ menu has ✂ Split the sound in two (myspl, cut at the longest pause near the middle) and 🧩 Learn in 2 small pieces (mypz: cuts sound + words, cut saved in `x.soft`). Learn with guru groups soft-cut pieces (myGroups): piece 1, piece 2, then the full line. Join on a soft cut merges the words back. Words view auto-scrolls to the line being chanted (myScrollLn). Build 290: on Lines in the sound, tap a word (MYWD) to move it (and the words after/before it) to the next line or the line above (mywmv); the sound is not changed. Build 291: Edit sloka has a Sound step (Change › → Record / Audio file → Use this sound: myrepl keeps the words, resets timings, then opens Tap along). After saving a new sloka with 2+ word lines, Tap along opens straight away (MYTAPNEW) with a Skip button (tapskip). Tap along is a visible step on Edit sloka. Build 292: main setup is now one screen "Set up the parts" (myT2Page, MYT2, t2* actions): audio plays, all words shown, tap the first word of each part after a pause; Save rebuilds the words as one line per part and sets x.lt, so sound and words match. Opens after saving a new sloka or changing the sound; old tap along kept under More ways to fix. Build 293: layout D compact Today list (tdCompact): one row with all revision numbers, one row per new verse, real total minutes; Listen/Chant pills and step strip hidden in D. Build 294: layout D home rebuilt (bigHome → dhHead + practice card + dhTiles). Header style S.dhs: big / circle (default) / portrait / arch, switch "Test · header" under the Today layout switch. Tiles: Swadhyayam wide (owner/students only) + Parayanam, Learned wide + Verses a day. 🔔 opens Satsang (badge = events in 30 days). Revision numbers tap to the meaning view. Build 299: Swadhyayam links (swLinkBox, swlink: YouTube → l.yt plays in an in-app youtube-nocookie iframe sheet swYtSheet, minutes counted from the player state via postMessage; audio link → l.url plays in the normal player), sleep timer chip (swslp, SWSLP checked in swTick), one line a day card after 20 min (swLineCard, S.swtk, listed in All my notes). My slokas guide help/my-slokas.html (English/Telugu/Hindi, ?l=) opened from the small ? in the My slokas headers (myHelpU). Build 300: soft echo at line ends (echoW in wordsHTML): last word ending ah/ih/uh (or ః / ः) shows the echo in small raised letters; setting S.echo (You → Look, default Show). Build 301: small examples card (echCard, ECH en/te/hi) inside How to read (rdTable): end of line = soft echo, middle = as written, no h = nothing. Build 304: old practice screen header is two lines (no New screen chip; '✨ Try the new practice screen' link at the bottom); its end screen fits one view (More tiles in one row, Show verse + Stop here side by side, dvRow/DVN); .rpsheet .rpverse no longer shrinks/clips on small phones (vFit measures scrollHeight, floor 0.82, sheet scrolls). Swadhyayam: real listening log S.swlog (swLog: class, day, start/end, seconds heard, from→to, kind a/y/v) from swTick, YouTube and the video sheet (video now counts); 'Last heard' line + 📊 Details page (swHist: By day / By class with Clear/Partly/Hear again, ⭐ recall check, my 3 points l.pts); 'heard' only counts after real listening (l.acc ≥ 50%). My slokas: ⋯ › 📤 Share or save (share with someone / copy for me / words only / just the sound; MYSH sheet, two taps so iPhone allows the share), 🛟 Keep and share card (📦 Back up all, 📥 Add from a file: myImport, .sloka.json with base64 sound), storage.persist(), Save my progress now carries sloka words and timings (restored as x.nos = needs sound). Drag bars: Guru explains/stories (data-seek gx), My slokas full view, old Listen page (myl). Build 305: shared/backed-up sloka files are now a readable page (<name>.html: name, words, playable sound; data in <script id="sg-sloka">, sound only once in the <audio> tags; myHtml/myUnHtml; old .sloka.json still imports). YouTube and class videos open in a floating player (#swfl, outside #app so it keeps playing across screens; ⌄ Small / ⤢ / ⇅ move / ✕; flShowYt, flShowVid, flSync, flClear). Now-playing bar (#npbar, npSync every 0.7 s) for Swadhyayam audio when you leave its page: tap to go back, ⏸/▶, ✕ hides.
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

## Build 306 (12 Nov 2026) — Dev only
- After the last revision verse, the "Wonderful! ... learn something new" page (transMsg) counts down 8 s and starts the new verse by itself (TRC, trcStart/trcStop); "Start now" and "✋ Wait, I need a moment". Setting S.autoc ('0' = wait for a tap) in Language & display › Repeating.
- Top messages (tmShow) never float over the completion screen (END); they wait 2 s after it closes (TMEND/TMHOLD).
- Repeat after me pauses (Paused card, same round kept via GRES) when the view leaves the practice screen (check at the top of render()) or when other sound starts (HTMLMediaElement.play wrapper: Swadhyayam, My slokas, videos, the PL players). rpAway() is shared with the screen-lock pause.
- Echo letters: default saffron #a8431a at .7em (contrast 5.7:1 on ivory; old gold was 3:1). S.ecol s/m/g (Saffron, Maroon, Gold old) in Language & display, with a preview; html[data-ec].
- My slokas ⋯ menu: ⏱ Fix timing (tap along) opens the tap page directly; 📑 Duplicate copies words, timings and sound (new id, "(copy)", practice history cleared).

## Build 307 (12 Nov 2026) — Dev only
- Old | New practice-screen switch (gsw()) at the top of every Repeat after me screen (both styles, all phases); the old screen's How to say chip is icon-only (🗣) there to make room. Setting moved to Language & display › How I practise › Practice screen (removed from Look). The bottom "Try the new practice screen" link is gone.
- Read-aloud (dash) lines have their own setting S.dl (English default; తెలుగు / हिन्दी), in Language & display › Language & reading, with a preview. dashL() no longer follows the app language or the Read in chips (S.rd); My slokas (scLine) and Dhyanam follow dashL() too.
- Nothing on the practice screens shrinks any more (.rpsheet>*{flex-shrink:0}); the screen scrolls instead. Fixes the squashed record card on smaller phones.
- Your-turn sound S.tbell: 'bell' (default; 880/1320/1760 Hz, ~1 s, louder), 'soft' (old 660 Hz beep), 'off'. Same AudioContext chime() as before (v60 baseline), only the notes changed. Tapping a choice plays it.

## Build 308 (12 Nov 2026) — Dev only
- Your-turn sound (S.tbell): 'temple' (default; old 'bell' maps to it), 'hand' (3 quick high rings), 'voice' (speechSynthesis "Your turn" / మీ వంతు / अब आप in the app language), 'both' (temple bell + voice), 'soft', 'off'. Bells are synthesised in the same AudioContext as before (tbPlay: strike noise + inharmonic partials with a slow shimmer); no sound files. Voice needs an iPhone check (speech may change the phone's sound settings for the next guide clip).
- New practice screen header: the How-to-say button is now 🗣 (same as the old screen), not 📖.

## Build 309 (12 Nov 2026) — Dev only
- Bells lower and softer: temple bell 300 Hz with fewer bright partials, hand bell 620 Hz, overall gain 0.32 (peak ~0.23, about the old beep). No bell when the learner taps Skip ahead (RP.nobell); the bell rings only when the guru finishes by himself.

## Build 310 (12 Nov 2026) — Dev only
- Old practice screen header: Old|New, then 🗣, then a 14 px gap (.gcgap) before Close, so Close is not hit by mistake.
- New screen finish (g2Done): compact step strip (stepStrip in .g2-ss, title line hidden): Listen ✓ Chant ✓ Record Meaning Finish/Next.
- Hidden verse (from memory) on both screens: a note card on top of the blurred verse (hidOv, .hidw/.hidov) "🙈 Hidden · chant from memory / Tap to peek"; tapping it shows the verse for that round (RP.peekR = n:round, checked in hideNow). Banner no longer adds "· from memory" (it was cut off).

## Build 311 (12 Nov 2026) — Dev + Test
- Old practice screen's "Take saved / Finish today" page (gcontSheet, shown after recording and after reading the meaning) now has the same top bar as the other old screens: verse title, Old|New switch (gsw), 🗣, gap, Close (gstop). Before, it had no switch, so you could not change to the new screen there.

## Build 312 (12 Nov 2026) — Dev only (batch 2: documents)
- New reader PDFs in `docs/pdf/` (made by `python3 tools/make_pdfs.py FONTDIR`, which loads index-dev.html and runs `tools/pdf_build.js` on the app's own data; fonts from github.com/google/fonts: TiroDevanagariSanskrit, NotoSerifTelugu, Inter). Each file has an echo copy and a `-noecho` copy:
  - `fullchant-sa|te|en.pdf`: all parts (opening prayers, Yudhiṣṭhira/Bhīṣma, nyāsa, dhyānam, 108 verses, phala-śruti, ending), How to read page (RB rules + echo card), read-aloud lines, per-verse tips (sa/en only; tips are English).
  - `meanings-en|te|hi.pdf`: every verse with read-aloud line, meaning, each name, special benefit.
  - `verses108.pdf`: new copy of the 108-verse PDF (the old root file `vishnu-sahasranamam-108-verses.pdf` stays for live).
- App: `docBtn(stem,name,sub)` = "⬇ Save or share the PDF" (prefetch `docLoad`, `docShare` → share sheet with the file, else opens the PDF). On Full text (108), The full chant (follows the script chip), Verse meanings (follows the language chip), Dhyanam. `docUrl` picks `-noecho` when S.echo='0'.
- Echo: `echoChips()` (Show/Hide, same S.echo) on Full text and The full chant; echo now shown on Full text, full chant read-aloud lines and the verse meaning page (`echoLn`).
- Fixed: Full text page was 58 px wider than the phone (long nowrap words).
- Rebuild the PDFs whenever verse text, dash lines, meanings or tips change.

## Build 313 (12 Nov 2026) — Dev only
- The full chant · text (fcPage) redesigned: one reader for all 7 parts incl. the 108 verses (FCSEC 'v108', jump row 1·10…100, ids fcv1..108). Numbered part pills (.fc2nav, current one centred by fcNavC), part header card (Part N of 7, title, one line; Dhyānam shows the dhyanam picture), script segmented control + echo on/off chip, verse rows with number badge and green read-aloud line, big Next part button (last part: Save or share). ⬇ PDF chip opens a small sheet (FCPDF): Whole chant in the current script, or Just the 108 verses. Read-along note moved to a folded "About this text" at the bottom. Dhyānam part links to the Dhyanam page (LPBACK 'fc' brings you back).
- Chant correctly: "Full text of all 108 verses" row removed (now inside the reader); Dhyanam row kept. ftPage still reachable from the home Read panel.

## Build 314 (12 Nov 2026) — Dev only
- Full chant reader: Opening line is now "Prayers before we begin" (no other deities named). Slimmer part header (title + "N / 7 · range" on one line), smaller Dhyānam picture (16:6). ⬇ PDF opens a compact two-button row (Whole chant · script / 108 verses only). Dashed line between verse and read-aloud lines, stronger line between verses.
- Test looks (S.fcst, chips "Test · look" at the bottom): a Cards (default), b Book (centred, ॥ n ॥, ❁ between verses, read-aloud on a soft green panel), c Simple (saffron rule on the left, "Verse n" label).

## Build 315 (12 Nov 2026) — Dev only
- Full chant reader: each read-aloud word is underlined (fcLn: span.fw, marks like | ||1|| span.fwm not underlined), so you see which syllables are read as one word. Same underlines in all PDFs (rebuilt).
- Look (Cards / Book / Simple, S.fcst) moved off the page into Language & display, next to the soft echo setting. Echo chip removed from the page (the echo setting still applies). The page now has only: parts row, part header, script switch, verses, Next.

## Build 316 (12 Nov 2026) — Dev only
- Echo on/off chip back on the full chant reader (default on, same S.echo as settings).
- Names: Learn rows "The full chant, start to end" = the reader (LP 'fc'); the old arrangement page (ARR, LP 'arr') is now "How the full chant is arranged" (te/hi too).

## Build 317 (12 Nov 2026) — Dev only
- How to read (rbBody) starts with rd4(): "Read in 4 steps" (RD4 en/te/hi drafts): underlined = one word (▶ audio/ex/dash), aa/ee/oo longer (▶ long), h at the end = soft echo (▶ h), | and ॥ pauses; then "▶ Hear it all together: verse 1" (audio/v001.m4a via rdplay '../v001') with verse 1's underlined read-aloud lines. Old tables, chanting rules and 8 rules fold under "More rules ›" (details.rd4m). The first-day card on Today (S.rdSeen) is now rd4(1) with Got it. The in-practice 🗣 sheet still uses rdTable.

## Build 318 (12 Nov 2026) — Dev + Test (builds 312–318 promoted to Test)
- 🗣 How to say sheet in practice: "All reading rules" (and the sheet outside a verse) now show rd4More() = the 4 steps (without the verse 1 button, rd4(0,1)) + "More rules ›" with the old table. The verse's own tips stay on top.

## Build 319 (12 Nov 2026) — Dev + Test (batch 3: easier My slokas sync)
- 👆 Set up the parts (myT2Page) no longer needs live tapping. On open it decodes the sound (x.vs) and suggests the parts itself (myAutoT2): with 2+ typed lines, one part per line, each line start matched to the best pause (myAlign, DP); with one long line, one part per clear breath (pause ≥ max(0.3 s, 45% of the longest)), each pause matched to a word boundary by syllable length (mySyW/myMora: long syllables 1.3) with a bonus after | । ॥ and never before a mark.
- Tap a word = hear it (myT2Times spreads each part's words over its voiced time; myT2Play lights the word and part). ✂ between words = new part there (time = nearest pause to the word); ✂ join = merge. ◀ ▶ on a part = move it to the pause before/after (then plays it). － Fewer / ＋ More = re-suggest with one part less/more. ▶ Play all with word highlight. Re-opening a set-up sloka keeps its saved parts.
- Cuts now go in the middle of the silence (myGapCut, never more than 0.45 s before the voice): myCutsFromLines uses myGapAt for every line start, so piece ends no longer clip the soft echo. Old Tap along unchanged.
- Tested on the 108 guide recordings (audio/cuts.json): typed in 2 lines, the split lands in the right pause for 108/108 (106 within 0.35 s of the known cut, 2 in the same long pause, nearer the voice) in Devanagari, Telugu and English letters. Pasted as one line: the line-2 split is at the right word for 101/108 (Devanagari/Telugu) and 98/108 (English letters); the misses are one word off, fixed with one ✂. Test script: tools/test_sync.py.
- Help page (help/my-slokas.html) step 2 text updated en/te/hi; its screenshot b_tap still shows the old screen.

## Build 320 (12 Nov 2026) — Dev + Test
- New sound player (myNewPlayer, mynewplay/mynewsk, seek 'mynew'): after recording or choosing an audio file (Add a sloka and Edit sloka › Sound › Change), ▶/⏸, drag bar, time, ⏪ 5 s / 5 s ⏩. Uses the shared MYA element with dataset.id='new'.
- No bleeding into the next line: mySpanFix(x,sp) moves a part's start and end into the middle of the silence around it (myGapCut). Used by the player (mypStart span + piece-by-piece queue) and Learn with guru (prSpan), so older slokas (cuts at voice start − 0.08 s) are fixed too, without re-saving. Player end check every 50 ms (was 80). Checked on 347 parts of the 108 verse recordings: every end is in silence, at least 0.12 s before the next voice.
- Repeats now stop and restart inside the silence, so the round-to-round restart is softer. Fading is not possible: iPhone ignores audio.volume, and Web Audio is banned for playback (see iPhone rules).

## Build 321 (12 Nov 2026) — Dev + Test
- Line matching for typed lines (myAlignL) also checks that each line's voiced length fits its syllables (DP over line → pause), so a long last line can't land in a 1 s tail of sound. Tested with the owner's Dvayam recording (108 s, 11 typed lines, 19 breaths): before, the last line was put at 106.9 s; now the ślokas' boundaries land on the long pauses (40.6 s, 86.1 s). 108-verse test unchanged (tools/test_sync.py).

## Build 322 (12 Nov 2026) — Dev + Test
- Repeat fix (owner: "audio stops after 1 repetition"): rounds never run into the file end any more (MYP.e capped at dur − 0.12 s, also for line-by-line pieces), and mypTick re-seeks/re-plays for up to 3 s until playback is really inside the round (MYP.ok, like myPlaySpan). Reproduced in Playwright with an iPhone-like copy (play() after 'ended' does nothing, first seek after 'ended' ignored): build 321 whole sloka × 3 stopped after round 2; 322 finishes every round in every mode.
- Parts follow the breaths (myAutoT2(x,null)): breath = pause longer than an Otsu split of the pause lengths on a log scale (myBreathThr); typed line breaks are always part starts too (myAlignL → Am); words matched by myAlignB (DP that can skip a breath, checks each part's sound length against its syllables, never starts a part on | । ॥). myTrimVs ignores a short sound (< 1.5 s) after a long silence (≥ 2.5 s) at the start/end; x.tend set before it. myAutoT2(x,-1) = old line-only matching.
- Tests (tools/test_sync.py): typed lines → line break right 107/108 (the other in the same pause); one pasted line → 106/108 Devanagari/Telugu, 100/108 English letters. Owner's Dvayam (108 s): 21 parts; ślokas 2 and 3 and the last śloka split exactly at the metre's breaks.
- Save goes straight to practice: myQuickParts (after myMakePieces / new sound) sets the parts by itself (myApplyParts, shared with t2save) and opens the player; note "✅ Parts follow the pauses in the sound · Check them ›" (x.chk, ✕ = mychk). Set up the parts no longer opens by itself.
- Player: "How to learn" row: 🗣 Repeat after me (Learn with guru) · 🪜 Line by line · 🔁 Whole. Line by line (mypLineQ) = for each line, its small pieces (cut at the tiny pauses inside it, each ≥ 0.8 s, max 6) then the whole line, each N times (MYP.ql labels, MYP.qli line index; Previous/Next and tapping a line jump by line). Card header shows "Line 4 of 21 · piece 1 of 2" (mypHd).
- Help page step 2 updated (en/te/hi drafts).

## Build 323 (12 Nov 2026) — Dev + Test (owner: still some bleeding on iPhone, e.g. end of line 2 of his Dvayam)
- Owner's case: "…vaan" fades out by 11.45 s, clean silence, next voice at 12.55 s; 322 stopped at 12.11 s (middle of silence, max 0.45 s before the voice) and still bled on iPhone, so the phone keeps playing for a while after pause().
- Parts now STOP soon after the voice ends (myGapEnd: gap start + min(0.25 s, 40% of the gap)) and START just before the next voice (myGapCut, unchanged). mySpanFix uses myGapEnd for ends; Line by line pieces only cut at pauses ≥ 0.25 s, with separate stop/start points; Set up the parts "Hear part" and ◀ ▶ use mySpanFix too.
- Stop delay learning: myLagLearn reads where the sound really stopped 350 ms after pause() and keeps a running value S.mylag (0–0.5 s); myStopAt asks to stop that much earlier (player mypTick and myPlaySpan, so also Learn with guru and the setup page). Starting value 0.15 s on iPhone/iPad, 0.03 s elsewhere; it learns downwards too. Shown in the player ☰ sheet: "Phone stop delay: N s".
- Tests (Playwright, owner's Dvayam, Line by line): simulated phone that stops 0.3 s late → 322: 8 of 15 stops ran into the next voice; 323: 15/15 in silence after the first stop, last word kept (≥ 0.11 s tail). No-delay browser: learns ~0, 15/15 in silence, no word clipped. Repeat test (iPhone rules) still finishes every round.

## Build 324 (12 Nov 2026) — Dev + Test
- Owner: Line by line in the player still bled, while Lines in the sound played cleanly. Difference: the player tick (mypTick) redrew words/progress (mypGlow, mypInfo → mfTick may render()) BEFORE checking the stop; the lines page uses the light myPlaySpan. Now mypTick checks the stop first and, when the stop is < 0.25 s away, sets an exact setTimeout for it (MYP.arm; guarded by round key and paused state). myPlaySpan has the same exact timer. Simulated busy screen (120 ms per redraw): stops land on time (learned delay ~0 instead of 0.12). Repeat test (iPhone rules) still finishes every round; nothing ever reaches the file end now.
