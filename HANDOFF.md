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

## Build 325 (12 Nov 2026) — Dev + Test
- My slokas guide PDF (2 pages, English): docs/pdf/my-slokas-guide.pdf (+ identical -noecho copy, because docUrl adds -noecho when echo is hidden). Source: tools/guide/my-slokas-guide.html, printed with Playwright page.pdf (A4). Sections: A the simple way (record yourself, 1 s pause after each line, one line of words per pause), B a recording by someone else (break lines where the chanter breathes, then Check them › once), C How to learn, If something is not right. No sources named.
- In the app: My slokas › ⓘ How it works card ends with "📄 Guide: record, add and practise" + docBtn (⬇ Save or share the PDF). Step 3 text of the card updated (Repeat after me, Line by line, whole).

## Build 326 (12 Nov 2026) — Dev + Test
- My slokas guide PDF rebuilt: 4 pages with an example in every section and real screenshots (owner asked: where to press Enter, audio pauses). tools/guide/img/: add.png (words box with "↵ Enter" badges drawn by a mirror-div overlay), wave_good.png / wave_other.png (matplotlib waveforms of the owner's Dvayam: closing sloka with ~1 s pauses, and sloka 1's breaths), play.png (player after Save, How to learn boxed), check.png (Set up the parts: part 3 = only "pra:rabdham", tap "join 3 and 4" — a real result of the auto parts). Order: A record it yourself → C How to learn → B someone else's recording → fixes. Card text says "4 pages with screenshots and examples".

## Build 327 (12 Nov 2026) — Dev + Test (batch 4: play by voice, floating video)
- Link `?play=N` opens the verse player on verse N (`&x=3` = 3 times; `?play=learned`, `?play=all`). The query is removed with history.replaceState. If iPhone blocks autoplay, the player shows "Tap ▶ Play to start verse N" (PL.vc flag). Helper `vcPlay(n,rep)`.
- In-app mic: 🎤 chip in Revise › Play a verse (`data-act="vcmic"`, `vcMic()`), Web Speech API (`webkitSpeechRecognition`, lang en-IN, 5 alternatives). `vcParse()` understands digits and English number words up to 108, "N times"/twice/thrice, "stop", "all learned". Messages go through JMSG.
- You › MORE › "🗣 Play by voice" (HMS 'voice', `vcCard()`): mic how-to + Siri Shortcut steps (Ask for Input: Number → Open URLs `<page>?play=` + Provided Input → name "Play verse"), copy link button (`vcCopy`), "Try it: verse 1". Note shown: Shortcut links open in Safari, so progress there is separate from the home-screen app.
- Floating player (#swfl): the small box is dragged by its top bar (pointer events, `flDragInit`), position saved as viewport fractions in `S.flp`, clamped on screen (top ≥ 30 px) and on resize. ⇅ button removed. Class videos get a ⧉ picture-in-picture button (`flPip`, standard API or `webkitSetPresentationMode`) and `autopictureinpicture`. YouTube can't be put in PiP from the page (cross-origin iframe): footer tells the user to use full screen › PiP inside the YouTube player.
- New text is English only (te/hi drafts not made).
- 328: Siri steps clearer (owner added "Ask for URL" by mistake): step 3 says search "Open URLs", not "Ask for URL", insert Provided Input after play=; step 4 shows what the finished shortcut reads.
- 329: Siri steps now 3 actions: Ask for Input (Number) → URL action (link + Provided Input) → Open URLs. Owner's 328 attempt failed ("couldn't convert from Rich text to URL"): the link had been typed as the Provided Input variable's name.
- 330: ?play link: the language picker (first visit in Safari) no longer covers the player; an empty or bad ?play= goes to Revise › Play a verse with a message ("no verse number after play=") instead of silently showing Today.
- 331: ?play= value parsed with vcParse (accepts "Twelve", "verse twelve", "12 three times", "12.0"). A bad or empty link leaves a lasting note (VCLM) on Revise › Play a verse saying what arrived. Siri steps now use Ask for Input type Text (Siri handles spoken numbers better). Owner: the direct link worked; via Siri it landed on Revise (= empty or unreadable number).
- 332: 🎤 now opens a text box and focuses it; the user taps the keyboard's own dictation mic (owner: web speech recognition just listened and did nothing on iPhone). Box plays by itself 1.3 s after a valid number arrives (vcKey, vcTry, VCK, VCV); Enter or ▶ Play also work. Old vcMic() kept but unused.
- 333: Swadhyayam links: YouTube playlists (youtube.com/playlist?list=…) now play (embed videoseries?list=, ytList/ytSrc/ytOut, l.ytl; l.src keeps the original link). Before, a playlist link had no v= so it was saved as an audio link (l.url) and silently failed. Old saved YouTube links are fixed on display/open (swFixYt). A YouTube link with neither video nor playlist gives a "copy it again" message; non-audio, non-YouTube links get a warning when added. Each item in "On this phone and links" has ⋯ options (SWOPT): Rename (SWREN), Heard it (+1), Start fresh, Open in YouTube/link, Copy link, Delete (2 taps).
- 334: small video player drag fixed for fingers: in mini mode a see-through layer (.fl-ov, FLOV) sits over the video, so a finger on the video drags the box (the YouTube iframe used to swallow the touch; only the thin top bar could drag). Tap without moving = make big. touchmove preventDefault stops page scroll while dragging. New ⏯ button in the small player (flPP: video element play/pause, YouTube via postMessage pauseVideo/playVideo).

## Build 346 (14 Nov 2026) — Dev + Test
- Bug: on the new practice screen, "Next verse ›" after a revision (data-act revgo) was caught by the Revise-tab handler, so the screen only moved on by the 3 s auto timer; opening Meaning/Benefit/How to say did not stop that timer, so the next verse opened under the meaning. Now any tap on the revdone screen (except revgo) cancels the timer (RP.hold hides the old screen's bar) and revgo in revdone calls revGo().
- Telugu/Hindi: new screen banner/header/dock text split into spans and ~90 UIT entries + UIP patterns added (block after var UIT, "b346"). Scan of Today, Revise, both practice screens, done/saved/meaning sheet, full chant reader in te/hi shows no English left except satsang details and dash words.
- Read-aloud lines on practice screens bigger: min(1.45rem,5.9vw) (dash-first 1.6rem); vFit still fits the screen.
- Revise › Your verses headings: coloured bars with icon + count (vh-d 🔔 Revise today, vh-s ⏳ Coming back for revision, vh-o 📿 All learned · tap a number).
- Revision done for today: slim card with a "Next · Tomorrow / In N days · k verses" chip (revNext()).
- Meanings: each name follows the meaning language (nmS: te → Telugu via toTe, en → English letters from the dash form, hi → Devanagari); Library verse meaning shows the verse in Telugu when the language is Telugu.
- Today: "Paused midway…" replaced by a small pill "⏸ Paused | N to revise · M new" (.tpz2).
- Full chant reader: "▶ Play the whole chant" (fcWholeBtn, FCORD, fcWholeKeys, FCA.whole): Opening → The question → Nyāsa → Dhyānam → 108 verses as one queue, switches part and scrolls as it goes; ✕ stops; "Play all from this part" on later parts. Phala-śruti/Ending have no audio yet. v108 keys always use audio/vNNN.m4a.

## Build 347 (14 Nov 2026) — Dev + Test
- Chant together (S.tog, default on; setting "Chant together at the end" in Repeat after me): one extra whole-verse round appended to the normal steps (RP.togR = its round). Guru audio plays, banner "Chant together" (teal, .g2-st.tog / old screen "🙏 Chant together"), words highlight; when the audio ends rpTurn() skips the turn and calls rpNext(). Counts exclude that round (stCnt()).
- One counting style: "time N of M" + dots (.g2-dots) on the new screen; old screen rpLabel "Whole verse · time 2 of 3"; dock "N to go".
- Parayanam on Today: full banner only on the day/live; 1–2 days before a slim strip (.satsl) with ✕ (S.satx = date|id hides it for today); earlier only the 🔔 badge and Satsang tab (satDays()).
- Layout D: learned / verses a day / parayanam tiles moved into a side tab on the right edge (.sdtab, SDO) that slides out a "My progress" drawer (.sdrw.dts) with the same tiles (Learned → all verses sheet, Change → pace sheet). Owner's Swadhyayam tile stays in the panel. S.sdt='0' brings the old tiles back.
- Name pill: "🪷 Vishnu Sahasranamam" (big) + "Part N of 6 · name ▾"; "Sloka Guru" title kept.

## Build 348 (14 Nov 2026) — Dev + Test
- ROOT BUG of 347: a new helper satDays(x) overwrote the existing satDays() (Satsang special days), so home() → hsSat → satDaysCard threw on every Today render and the Satsang tab: taps on Today (bell, sloka library close, side tab, Done for today) did nothing. Renamed to parDays(). Check for duplicate `function name(` before adding helpers.
- Any tap other than the side tab closes the My progress drawer (SDO=false in the delegate).
- Side tab → maroon/saffron ribbon bookmark (.rib, dhRib) hanging beside the picture inside .dh (scrolls with the page, doesn't cover the card): %, learned of total, verses a day, ⋯. Drawer header in the ribbon colours.
- Chant together: before the round a 3 s intro (togIntro/togCue: hand bell + spoken "Now, all together" in the app language, purple banner with 3-2-1, pause/skip work), then the guru plays; banner purple (.g2-st.tog) so it differs from Listen/Whole verse.
- Button sweep (work/sweep.py: every visible data-act on 13 screens, touch taps, Chromium): 207 taps, no errors.

## Build 349 (14 Nov 2026) — Dev + Test
- Today "Practice done" card (tdDone, layout D) = style A3 chosen by owner: header "✅ Practice done today · 🙏 time" (duplicate streak pill removed), row "📗 Learned" and row "🔁 Revised", at most 3 number chips each, then "+N ›" (data-act tdmore, TDM='l'|'r') opening a bottom sheet with all numbers; every chip opens its verse meaning (mvopen). CSS .tdD3*.
- Ribbon unchanged; first-time hint bubble "👆 Tap for your progress" (.ribh) until the ribbon is tapped once (S.ribSeen).

## Build 350 (14 Nov 2026) — Dev + Test, not live
- Practice banner (new screen): sub line is now just the part ("Line 1 · time 1 of 2", "Whole verse", recap "Verse N"); "Guru says / Say" removed. Big word stays Listen / Your turn / Chant together.
- Read-aloud lines in Telugu/Hindi (DASH.te / DASH.sa, 108 verses) now follow the same chanting sounds as English: final visarga → స్/स् (s), శ్/श् (sh, ష్/ष् before ట/ఠ), ఫ్/फ़् (soft f before p), dropped where English drops it (v13). 220 words. How to read 'f' row in te/hi updated. Draft for guru check.
- Full chant reader: dash words light up while a verse plays (fcHL every 110 ms, syllable-weighted, line split from audio/cuts.json for the 108 or TCUT for parts; TRIM gives speech start/end). In 'Play the whole chant' the next 108 verse starts 0.25 s after the last sound (fcEarly on timeupdate); gap after 'ended' 700 → 150 ms.
- 📤 Send to guru: on both Take saved screens and on every take in a verse's takes list and My recordings. Uses the share sheet with the audio file and a short note (en/te/hi); falls back to a download. recSend/recFind/recLatest, data-act recsend ('n:N' = latest take of verse N).
- Swadhyayam: each item is a Guru's class (od folder or phone file) or Other listening (YouTube/links), swGuru(l), change with ⋯ › "🪔 Guru's class · change" (l.cat g/o). Only guru minutes go to S.swd (daily target/streak); other minutes to S.swo. My listening page: 7-day split card and new first tab "📜 What I heard" (one row per item per day, 🪔/🌼, minutes). By day rows show 🪔/🌼.
- My plans: added Hear the meaning, Remember the order, Time to learn each verse (Next) and Automatic check of my recording (Later).

## Build 351 (14 Nov 2026) — Dev + Test, not live
- Full chant: the 1000 names part always uses the Sahasranamam data (fc108(): TRKD.vsn when another part is being learned). Before, with Dhyānam chosen on Home, the 1000 names page listed the Dhyānam verses.
- Jumping while "Play the whole chant" plays: tapping a part tab plays from that part, "Jump to N" plays from verse N, ▶ on any verse carries on the whole chant from there. A part without audio (Blessings, Ending) can be opened to read; the audio keeps going and the view stays (FCA.hold).
- Telugu/Devanagari read-aloud lines (108) re-aligned syllable by syllable with the English line: lone half-letters joined (మా-న్ → మాన్), consonants moved to match (చ-క్ర → చక్-ర, వస్-థా → వ-స్థా, తి ర → తిర్ అ), regrouped into the same words as English, visarga per syllable (భః-శ → భశ్ శ). 162 lines changed; v38 line 2 fixed by hand (ద్ధిర్ ఋద్-ధో).
- Ribbon: shows on the Big header too (regex missed the style attribute); Portrait/Arch keep 64 px free on the right so the name pill isn't covered (class hasrib).
- ⚙️ and 🔔 on Today (layout D) open You / Satsang with ✕ Close back to Today (meopen, satgo + MEFROM).
- Swadhyayam card on Today: wide centred play button (Continue listening / Play the class / Pause, time below).

## Build 352 (14 Nov 2026) — Dev + Test, not live
- One sound at a time: HTMLMediaElement.prototype.play is wrapped (medHook). Any verse/guide/player/full-chant sound pauses Swadhyayam audio (swTick + swStop(1)) and the Swadhyayam YouTube player (postMessage pauseVideo). Starting Swadhyayam pauses the last verse sound (guided practice via rpPause). Muted plays ignored. Sound change: owner to test on iPhone.
- Swadhyayam card on Today: round gold ▶ on the right, same look as the Tomorrow's verse strip (.dt-plr); the wide button from 351 is gone.

## Build 353 (14 Nov 2026) — Dev + Test
- Swadhyayam ▶ on Today: green (2e9b57 radial) and 42 px, same size as the Tomorrow's verse button.

## Build 354 (14 Nov 2026) — Dev + Test, not live
- Whole chant now plays ONE file: audio/full.m4a (146 pieces: opening 1–6 + om, question 7–22, nyāsa 1–7, dhyānam 1–8, 108 verses; each trimmed to speech, 0.35 s between verses, 1 s between parts; AAC 64k mono, 33.3 min, 16 MB) with audio/full.json {key:[start,dur,cut]}. Built by work/full.py (TRIM for the 108, energy detection for parts). Lets it keep playing when the iPhone locks. sw-proto.js lets full.* bypass the cache like all108.
- fcPlay(k,true) in whole mode → fcOnePlay (seek in the file); single ▶ per verse and "Listen to this part" still use the per-verse files (fcPlay2). fcOneTick on timeupdate follows the verse (FULL), switches part, scrolls, saves S.fcres every 4 s; highlight uses FULL start/dur/cut.
- Settings › Full chant: speed (S.fcsp 1 / 1.1 / 1.2, pitch kept), pause between verses (S.fcgap s/m/l = +0, +0.6, +1.2 s; extra pause only while the screen is on), sound (S.fcmute: muted, words still light up, Wake Lock keeps the screen on). Same three as chips in a sticky bar under "Playing the whole chant".
- Carry on: stopping, closing the reader or pausing remembers the spot (S.fcres); the reader shows "Carry on · whole chant · Part N · verse M" and "↺ Start from the beginning".
- Sound change: owner to test on iPhone (locked screen, speed, sound off).

## Build 355 (14 Nov 2026) — Dev + Test
- Full chant reader, not playing: fcHero() card (maroon→saffron, gold border, 🪔): "Play the whole chant", or after a stop "You stopped at Part N · verse M" + two buttons "▶ Carry on" (gold) and "↺ Start again" (outline); small line with the current speed/pause/sound.
- Playing: sticky bar "Whole chant · playing" + ✕ + 🔊/🔇 button; two clear choice rows "⏩ Speed: Normal | Bit faster | Faster" and "⏸ Pause: Short | Medium | Long" (classes fcsr/fcsl/fcsb — don't reuse .seg, it is used elsewhere).

## Build 356 (14 Nov 2026) — Dev + Test
- Full chant card made small and calm: one light sage row (fch2: ▶ + "Play the whole chant" / "Carry on · whole chant · Stopped at Part 5 · verse 23") + small "↺ Start again" box. Playing bar and Speed/Pause rows in the same light sage; chosen option white with a green ring. Settings summary line removed.

## Build 357 (14 Nov 2026) — Dev + Test
- Full chant playing card (fcpc): round play/pause, "Whole chant · Part N · verse M", "■ Stop" pill (no ✕); three small boxes SPEED / PAUSE / SOUND showing the current choice; Speed and Pause open a small choice strip (FCPOP) with the chosen one green with ✓; Sound toggles (box turns soft red when off). Light sage colours.

## Build 358 (14 Nov 2026) — Dev + Test
- Whole chant keeps playing when you leave the reader: "⌄ Hide" button in the player card (fcmin) and Close ✕ of the reader (lpclose) no longer stop it while it plays (paused → still stops and remembers the spot). Mini player #fcbar (fcBarSync every 700 ms, sits above the tab bar and above the Swadhyayam bar): 🪷 Whole chant · Playing · Part N · verse M · "Open ⌃" (back to the reader at the right part), ▶/❚❚, ■ stop. Hidden on the reader, in practice and in Play a verse. fcOneTick re-renders only on the reader.

## Build 359 (14 Nov 2026) — Dev + Test
- Full chant reader names the two halves: a small map under the part tabs "Pūrvāṅgam (parts 1–4) → Sahasranāma (part 5) → Uttarāṅgam (parts 6–7)" (tap jumps to that group, current one highlighted), and a coloured tag on each part card ("Pūrvāṅgam · the opening, before the names" etc.). te/hi in UIT.

## Build 360 (14 Nov 2026) — Dev + Test
- Full chant player (ideas from owner's Gemini mock-ups): ⏮ / ⏭ beside play (fcprev: restart verse if >2.5 s in, else previous; fcnext), "Verse i of n · Part N · name", a tappable verse progress strip for the current part (fcgo), a "Whole chant | This part only (n)" switch (S.fcsc; This part stops at the end of the part, FCA.part), a 4th box FOLLOW On/Off (S.fcfol; Off = page does not scroll or switch part), Speed gets Slow (0.85). Also in Settings. Rejected from the mock-ups: dark karaoke bar, verse-loop button, 1.5x.

## Build 361 (14 Nov 2026) — Dev + Test
- 4 full chant player styles to choose from, temporary switch "Test · player style A B C D" above the player (S.fcps): A card (current), B bottom dock like a music app with ⚙ opening a settings sheet (FCSET), C warm temple card with one row of small chips (fcPopH for the choice strip), D one slim pill with ⚙ for the rest. Remove the unchosen ones and the switch once owner picks.

## Build 362 (14 Nov 2026) — Dev + Test
- Revise › Your verses: Weekly recap / Listen to all learned moved up, above the "All learned" grid (owner: they were lost under 89 numbers). Grid folds to the latest 16 (+ the chosen verse) when more than 24 are learned, with "Show all N ▾" / "Show fewer ▴" (VSALL).

## Build 363 (14 Nov 2026) — Dev + Test
- Revise › All learned: range tabs (1–20 · 21–40 · …, only ranges with learned verses; VSR, follows the chosen verse unless a tab was tapped) instead of the long grid / Show all; 🔍 in the header opens the type-a-number box (jsr).

## Build 364 (14 Nov 2026) — Dev + Test
- Revise › All learned: three coloured boxes with counts replace the colour legend: 🔔 N Revise today · ⏳ N Coming back · 🌿 N Strong. Tap one to show only those numbers ("Showing … only · Show all N"); tap again to show all. Range tabs only for the shown list (VSST).

## Build 365 (14 Nov 2026) — Dev + Test + NEW Preview
- New 4th copy: index-pre.html "Guru Preview" (ENV=pre, storage prefix pre_, purple PREVIEW tag, manifest-pre.webmanifest so it can be its own Home Screen icon). Prod-like: owner's chosen look fixed in code when ENV===pre: Today layout D (tdL), circle header (dhS), bottom tabs (HS=B); test switches hidden (hsBar, tdlBar, dhStyleBar, mypStyleBar, full chant player-style switch). Full chant player = style A until owner picks.
- tools/promote.py dev pre — run it together with dev test after every build.

## Build 366 (14 Nov 2026) — new app order, Dev + Preview only (NEWORG(): ENV dev or pre)
- Learn: search, Today verse, LISTEN & READ (The full chant, Meanings), CHANT CORRECTLY (How to read the dash lines, Dhyānam, Full text and PDF), GO DEEPER (Stories, Verses for life's needs, Why we chant), Coming later folded in a <details>.
- You: progress card, My journey, MY THINGS (recordings, Back up my progress), SETTINGS (Language & display, Reminders, Start again last), HELP (How to use, Play by voice), ONLY YOU (ownYou) + Guru tools, Swadhyayam time card, Works offline as a small line at the end.
- Revise "Chant all 108 with me" (allBtn, data-act fc108) opens the full chant player at Part 5 with This part only (carries on in the 108 if stopped there). Old Chant all 108 player kept for Test/Live.
- When owner approves: make NEWORG() return true everywhere.

## Build 367 (15 Nov 2026) — Dev + Preview only (not Test, not live). All behind NEWORG()
- Full chant reader: part tabs, Pūrvāṅgam map, part header card and the big "Listen to this part" button replaced by one journey card (fcJourney): three columns Pūrvāṅgam / Sahasranāma / Uttarāṅgam with numbered dots 1–4 · 5 · 6–7 (tap = open part; current group tinted), then "Part N of 7 · verses …", part name, one line, and a small "▶ Listen · this part" pill (fcPartBtn, same fcall action); Dhyānam shows a round picture; link "ⓘ How the full chant is arranged ›" opens LP 'arr'. Play the whole chant row stays on top.
- Revise: Weekly recap and Listen to all moved to two labelled buttons in the Revise title bar (.rvq). "Your verses" card now only the Revise today / Coming back lists; new card "🎧 Practise any verse" (status boxes, range tabs, number grid, 🔍) with vsSelNew(): chosen verse number + first line, "How many times 1× 3× 5×", big Play, 🎤. Legend line dropped.
- Today: sloka chooser is a full-width card (.dh-slk3): lotus icon, LEARNING NOW + "Change ▾" pill, Vishnu Sahasranamam, Part N of 6 · name.

## Build 368 (15 Nov 2026) — Dev + Preview only, behind NEWORG()
- Revise: "Strong" box/label renamed "By heart" (te కంఠస్థం, hi कंठस्थ); Practise any verse header says "All N learned". The "Chant all 108 with me" card on Revise replaced by a slim "📜 Chant along · The full chant, or any part" row that opens the full chant page (one place for all parts).
- styles/players.html: mock-ups of 3 full chant player styles (A Now playing, B Read along + dock, C Parayanam mode) + mini player and lock screen; not wired into the app. Owner to pick.

## Build 369 (15 Nov 2026) — Dev + Preview only, behind NEWORG()
- All three full chant players built for the owner to test (S.fcpn: na A Now playing full screen · nb B Read along + teal dock with Options sheet · nc C Parayanam mode, dark). Switch in the ⋯ menu (A/C), in the dock page (B) and on the page under the hero. fcNew() replaces fcWholeBtn in NEWORG. FCOV = big player open; "📖 Read all the verses" closes it to a sticky "Open player" bar; ⌄ = the old mini bar above the tabs (tap Open brings the big player back). New actions fcpn, fcmenu, fcread, fcov, fcpdfo, fcfols, qts, fcpprev/fcpnext (part jumps). "Listen · this part" now uses the one-file player in This part only. Progress bar updated from fcOneTick (fcNpTick). Big verse uses class fc2v with data-fck and is rendered before the list, so the word highlight lands on it.
- Quiet time (S.qt, on by default; setting in Repeat after me + player menus): screen stays on while the full chant plays; New version bar hidden while practising/chanting (html.qton); one-time tip how to turn on Do Not Disturb (OK / Don't show again, S.qtTip).
- "By heart" → "Kaṇṭhastham" (te కంఠస్థం, hi कण्ठस्थम्).
- YouTube embed (Swadhyayam): iframe now sends referrerpolicy strict-origin-when-cross-origin + origin/widget_referrer params (YouTube refuses embeds with no referrer: black player, no controls). Needs owner's check.
- Testing tip: python http.server has no byte ranges, so seeks in full.m4a fail; use a range server (scratch rs.py) to test jumps.

## 15 Nov 2026 — preview page only (not in the app): styles/parayanam.html
- Light Parayanam mode mock, working (fake timer, no sound): words light up and verses move on by themselves; header ⌄ · ⓘ how to do parayanam · अ/అ language (Sanskrit/Telugu/Hindi/English, show verse+read-aloud / read-aloud only / verse only, text size auto fit A−/A+) · ⚙ settings (whole/this part, speed, pauses, sound, move on by itself / when I tap, quiet time). "Where am I" box (part + verse + ⏱ min left, tap → all 7 parts with "Chant only this"); two styles: top line or side rail. Views: One verse (auto-fit big text) · All verses (scrolls with chant) · Book (PDF-style pages, sound on/off). 💡 Tip and 📖 Meaning on the verse. "Joining a parayanam" Satsang card mock. Real verse text/dash/tips/meanings for 1–4 from the app.

## Build 370 (15 Nov 2026) — Dev + Preview only, behind NEWORG()
- Player D "Parayanam (light)", owner chose the top-line layout; now the default style (S.fcpn||'nd'); A/B/C still in the style switch (⚙ sheet / page chips).
- fcD(): header ⌄ · ⓘ (FCDS how) · अ/అ (lang: FCSC sa/te/hi/en, S.fcshow both/dash/scr, S.fcfs −1/0/1) · ⚙ (scope, speed, pauses, sound, S.fcauto "Next verse comes by itself / when I tap ▶", quiet time, PDF, Stop, style). Where box (part, verse, ⏱ fcLeft() min left, updated in fcNpTick) → map sheet with all 7 parts, minutes from FULL (fcSecTimes), "▶ Only this" (fcall, now also for v108 via FULL keys). 7-part bar + Pūrvāṅgam/Sahasranāma/Uttarāṅgam labels. Views S.fcdv: one (fcDCard big + fcFitD auto font size, then script grown into spare room), list (all verses of the part, current scrolled to centre), book (page style, sound on/off, Save PDF). 💡 Tip / 📖 Meaning sheets from fcMeta() (V.tip / M.v for 108; TMEAN / DHY.m for parts); chant keeps going.
- Hindi script option in the full chant (Devanagari verse + Devanagari read-aloud lines: DASH.sa / FC.d / FCDH.d); FCSC remembered in S.fcscr.
- fcauto off: fcOneTick pauses at the start of each new verse.

## Build 371 (15 Nov 2026) — Dev + Preview only, behind NEWORG()
- Learn › LISTEN & READ: new first row "🪔 Parayanam mode" (data-act paray): opens the full chant in player D and starts the whole chant (carries on from S.fcres if saved).
- Player D colours (S.fcth, ⚙ › Colour, 8 swatches): lt Chandan (default, light), mr Temple (dark maroon), kum Kumkum (red), kes Kesari (saffron), hal Haldi (turmeric yellow), tul Tulasi (green), nil Neela (Vishnu blue), kam Kamala (lotus pink). All colours are CSS variables on .fnd (.fnd.th-xx).
- Big text in All verses (current verse larger, others dimmed) and Book (current verse marked with a coloured edge); size follows A−/A+ via --fz. Current verse scrolls to the top of the list so the next verses follow below.
- Full screen (S.fcfull, ⤢ in the header or ⚙): one slim line on top (part · verse · minutes left · ⚙), verse area fills the screen, small ◀ ❚❚ ▶ and view switch 1 / ☰ / 📖 at the bottom; ⤡ leaves full screen.

## Build 372 (15 Nov 2026) — Dev + Preview only, behind NEWORG()
- Verse codes on every verse in all 3 views (fcCode): Op Opening, Qn The question, Ny Nyāsa, Dh Dhyānam, SN Sahasranāma (108), Ph Phala-śruti, End Ending (e.g. "SN 18", "Op ॐ"). Explained in ⓘ.
- Ornament between the verse and the read-aloud lines (fcOrn: line · ❁ · line in the colour's accent) when both are shown.
- Header bigger (46 px icons, title .86rem bold); ⤢ Full moved next to the view switch at the bottom. Full screen bottom: bigger view buttons with icon + word (One / All / Book), bigger ◀ ❚❚ ▶.
- Words in the read-aloud lines stay whole (inline-block); only a word longer than the line splits at a dash. fcFitD now only checks height/width, so text is bigger.
- The verse line being said glows softly (fcHL sets .lnon on .fc2t>div, mapped from the read-aloud line). "Verse only" keeps the read-aloud lines hidden in the page (fnd-hide) so the glow still follows the voice.

## Build 373 (15 Nov 2026) — Dev + Preview only, behind NEWORG()
- Parayanam mode (player D) is follow-only: no ◀ ▶ verse buttons. Bottom = ☰ Parts · ❚❚ · ■ Stop (full screen: ❚❚ only; parts via the top line). Map sheet renamed "Choose a part": rows not tappable; each part has "▶ This part only" (fcall) and "▶ From here to the end" (new action fcfrom: whole chant from that part). "Next verse: Comes by itself / Wait for me (tap ▶ to go on)".
- All verses / Book: fcFitCur() shrinks the current verse (--fzc down to 0.55) until it fits the scroll area; fcFollowWord() (called from fcHL when the yellow word changes) scrolls so the current verse (or the word, if the verse is taller than the screen) stays in view. Smaller spacing and bottom padding 30vh so the last verse can reach the top.

## Build 374 (15 Nov 2026) — Dev + Test + Preview (owner: "push it to dev and test and preview"). NOT live.
- NEWORG() is now true for test too (dev, test, pre), so the new Learn/You order, Revise changes and all players are in Guru Test.
- Player D: ◀ ▶ verse buttons are back (owner). Bottom: ☰ Parts · ◀ · ❚❚ · ▶ · ■ Stop; full screen: ◀ ❚❚ ▶.
- Parayanam style (⚙ › 🪔 Parayanam style, and app Settings › Repeat after me area: Tradition + Saṅkalpa): S.fctrad gen|vai (General / Vaishnava), S.fcsk saṅkalpa screen before starting (default on: date, tradition, "I chant for" chips, optional name, Begin / Carry on / Start from a part; saved in S.fcskl), S.fcbell temple bell at start and end (default on, tbPlay 'temple'), S.fcrep repeat SN 108 once/2/3 times (fcOneTick + ended handler, shows "time k of n"), S.fcgrp group style tags "🙋 Leader" first half / "👥 All" second half, S.parc parayanams completed (counted when a whole-chant run ends) + closing screen "सर्वं श्रीकृष्णार्पणमस्तु".
- Tradition order (fcFlow2, draft for guru): General = Opening → Question → Nyāsam → Dhyānam → Pañcapūjā* → 108 → Phala-śruti* → Ending*; Vaishnava = Guru vandanam (ācārya taniyans)* → Opening → Question → Nyāsam → Dhyānam → 108 → Phala-śruti* → Ending*. (* = to be recorded, shown in Choose a part as "to be recorded" and skipped.)
- Settings sheet chips always readable on dark colours.

## Build 375 (15 Nov 2026) — Dev + Test + Preview. Not live.
- Full names instead of short codes (fcCode → "Sahasranāma · verse 18", "Phala-śruti · verse 1", "Opening prayers · Om"); legend removed from ⓘ.
- Divider now reads "❁ READ ALOUD ❁" (same idea as the PDF's "READ ALOUD" label). Verse stays ~80% of the read-aloud size.
- Soft picture behind the verse (S.fcbg, ⚙ › Picture behind the verse, on by default): fcPicU() → Dhyānam: img/story/dhyanam.jpg; 108 verse: img/mean/vNNN.jpg if MPIC, else its story picture (STO[x].v + hasPic); everything else: the home Vishnu picture (IMG, via an injected .fnd-bgp.dflt rule). opacity .13 (.2 on dark colours) with a radial mask. Shown in One verse and on the current verse in All verses.
- Leader can start anywhere: "Where to start" sheet has "Start at a verse": part dropdown + verse number (book numbering, e.g. The question 7–22) + ▶ Start (action fcat; wrong number shows the valid range). Whole chant then continues in order.
- Picture idea pending: Yudhiṣṭhira asking Bhīṣma (owner to make with AI; would become the background for The question).

## Build 376 (15 Nov 2026) — Dev + Test + Preview. Not live.
- Learn: "The full chant" row removed (it opened the same Parayanam player); one entry "🪔 Parayanam mode · Chant, listen or read along · whole chant or any part". Revise "Chant along" row now opens Parayanam mode (paray). Reading only: Learn › Full text and PDF. The old reader page (fcPage) is still the page behind the player.
- ■ Stop in Parayanam mode closes the player (LP='') instead of showing the old reader page.
- App Settings › 🪔 Parayanam: "Read-aloud lines (the dash lines)": Show with the verse / Hide · verse only / Read-aloud only (same S.fcshow as अ/అ › Show).
- Echo letters (sup.ech: ha, hi, hu) in their own colour in the player: --ech saffron #c8641e on Chandan, blue #1565c0 on Haldi/Kesari/Kamala, light blue #7fd8ff on dark colours; bigger and bolder.

## Build 377 (15 Nov 2026) — Dev + Test + Preview. Not live.
- Learn › "📜 The full chant · Read and listen · every part, verse by verse" is back (action fcread2, flag FCRD=true): the reader page with ▶ on each verse, Listen this part, Play the whole chant as the plain inline card player (old fcWholeBtn path, no Parayanam overlay). Stop there keeps you on the page. "🪔 Parayanam mode" (paray) sets FCRD=false; the mini bar "Open" returns to Parayanam if it was started there.
- Verse heading badge (fnd-no) colours per theme via --bdg/--bdgc: Chandan saffron/white, Temple·Tulasi·Neela gold/dark, Kumkum gold/red, Kesari maroon/cream, Haldi kumkum red/white, Kamala magenta/white; list badges use the same colour.

## Build 378 (15 Nov 2026) — Dev + Test + Preview. Not live.
- One verse view, "Verse only" and "Read-aloud only" were huge (auto-fit filled the card). fcFitD now caps the size at 30 px when only one block shows (40 px for the read-aloud lines when both show, script grown up to 34 px); a hidden read-aloud block no longer counts; A+ / A− still scale from there.

## Build 379 (15 Nov 2026) — Dev + Test + Preview. Not live.
- Default Parayanam colour is Haldi (S.fcth||'hal').
- Old players A/B/C removed from use (owner): fcPn() always 'nd', fcSw() returns '' (no style switch anywhere). The full chant page always uses the plain card player (style 'a'), no "Test · player style" row. Code for A/B/C still in the file, unused.
- Owner reported YouTube in Swadhyayam now working (after build 369 referrer fix).

## Build 380 (15 Nov 2026) — Dev + Test + Preview. Not live.
- Parayanam mode: tap the verse area (data-act fcqk on .fnd-st) to show a quick bar at the top (fcQkH, FCQK, fcQk timer 5 s): 🔊/🔇 Sound (fcmu), Speed cycles Slow→Normal→Bit faster→Faster (fcqsp), A− / A+ (fcqfs, S.fcfs −1..1), 🎨 Colour cycles FCTH (fcqth), ⚙ More (opens settings). A tap never pauses or skips. Works in normal and full screen.
- Bell fix: the bell + "parayanam completed" count rang when iPhone fired 'ended' early. fcOneTick now keeps FCA.ok (last position reached by smooth playback, jumps over 6 s ignored). The 'ended' handler only finishes if FCA.ok is within 6 s of the end of v108:108; otherwise it carries on from FCA.ok (up to 3 times, then pauses and saves the spot).

## Build 381 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Parayanam mode top = Option A (owner picked from preview-paray-top.html): header ⌄ ⓘ | big serif "Parayanam" + "Vishnu Sahasranamam" | अ/అ ⚙ (.fnd-hd2, .fnd-hic — note .fnd-ic was already used for the verse-card chips). One "journey" card (fcJour(I), button data-act fcds/map): ring medallion with verse n of N (ॐ for parts without numbers), PART n · group, part name ("The 1000 names" for part 5), paused / "time k of n" / "Tap to choose a part ›", minutes-left box (#fndln, updated in fcNpTick via fcLeftA), track grouped Pūrvāṅgam ✓ / ◆ Sahasranāma / Uttarāṅgam (.fnj-dn/.fnj-on — plain .dn clashes with an old rule). Colours from theme vars; time box uses --bdg/--bdgc. Full-screen top unchanged. Old where box + segs code left unused in fcD.
- Home progress badge shapes (from preview-ribbon.html) selectable: You › Language & display › Progress badge on Home: 🎗 Ribbon (default) · ⭕ Ring · 📿 Mala (108 beads) · 🪟 Glass · 🚩 Flag. S.ribst, ribSt(), RIBST, dhRib() (.rb2 .rb-ring/.rb-mala/.rb-gl/.rb-fl). Same tap → My progress. Badge only shows on Today layout D (as before).

## Build 382 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Old practice screen: "Chant together" banner now purple like the new screen (.rpph.tog, added in rpSheet when ph==='listen' && (togNow()||RP.togin)).
- Well done screen (endHTML): wrapped in .endw (min-height calc(100svh - 150px)); hero fills the space, bigger stars/title/quote/buttons. Draft Sri Vaishnava look in preview-welldone.html (not in the app yet).
- Screen lock in Parayanam: fcWake() kept a dead lock (iPhone drops it on its own) and never asked again. Now wkLive() checks .released, a 'release' listener clears FCWL, qtSync (every 1 s) re-asks, plus on visibility and on any tap/click. If the phone refuses 3 times or has no Wake Lock, a 1-px muted looping video (NSV, nsOn) keeps the screen awake. wkWant() also covers Repeat after me (RP.on && !RP.paused) when Quiet time is on. Tested with a stand-in lock: dropped lock re-taken within 1 s.
- Known, not fixed (suggested to owner): parayanam count (S.parc) adds one if the run ends with Whole chant, even if it started mid-way or was "This part only" earlier. Unmark only exists as "undo all" in Verses I already know.

## Build 383 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Well done screen styles (You › Language & display › Well done screen): S.wdst c Classic (default) | k Kaavi (temple wall stripes) | p Pattu (silk + zari) | n Neela (Perumal blue); S.wdnm t Thenkalai | v Vadakalai. "👁 Show me" (wdshow) opens a demo. svEnd(): SVDEF (inline SVG defs: svchak chakra, svshk conch, svnT/svnV namam), SVMED medallion (namam on a lotus seat). Chakra on the viewer's left, conch on the right (as held by Perumal). From the owner's Gemini mock: śubhamastu pill, 3 real tiles (verses learned, days in a row, today's verses), flower shower svPetals() (once per screen, 🌸 Puṣpa vṛṣṭi to repeat, off with reduced motion), Tiruppallāṇḍu 1 (Telugu script + IAST + meaning) on alternate days with Gita 18.66, 📤 Share the blessing (svShare). Not taken from Gemini: the "99% Chandas & Swara" tile (not measured), the hexagram chakra.
- This part only during a chant: strip under the journey card (fcPStrip) "stops after <part> · Whole chant"; at the end of the part fcPartDone() (FCPDN) offers Carry on (fcfrom next part), this part again, Close. Parayanam mode always starts as Whole chant (paray sets S.fcsc='w'). Count: FCA.c0 (passed the very start, fcT0) and !FCA.wasP, kept in S.fcres.c0 for resume; closing screen says when not counted (FCNC).
- Unmark one verse: ✎ on the chosen verse in Revise › Practise any verse → unSheet: Needs more practice (unwork: S.rev[n]={stage:0,due:today}, stays learned) or Not learned yet (unnot: removed from learned/known/rev, S.pos moved back to it). After a session S.pos now skips verses already learned.
- Swadhyayam video in the page (FLM 2): #flslot at the top of swPage; flPlace() (rAF loop flLoop while FLM 2) lays the same #swfl player over the slot; scrolled away or on another screen → .dock small player top-left; tap it (fl-dk) → back to the slot / Swadhyayam page. ⤢ big (FLM 0), ⌄ Small from big returns to the page. Drag only for the old free small player (FLM 1).

## Build 384 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Well done: owner liked both the first Sri Vaishnava design and the Gemini-style one → Layout setting S.wdly s Simple (svEndS: stripe, śrīmate line, conch · namam · chakra row, kaiṅkaryam, quote, ācārya line) | g Grand (svEnd, default). Two more colours from the Gemini mock: ch Chandan (sandalwood cream, gold frame) and ra Rātri (night brown, gold). Settings: Classic · Kaavi · Pattu · Neela · Chandan · Rātri, Layout, Namam.
- Docked Swadhyayam video is now a slim bar across the top (like the owner's example): small video left; ⤢ back to the class, ↺10, ↻10 (flSeek: <video> currentTime or YouTube seekTo with SWYTC from infoDelivery), ▶/❚❚ (flPPIcon), ✕. Tap the small video → back to the page. Fix: inline check uses the slot's own height.

## Build 385 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Change several verses at once: Revise › Practise any verse › ✎ (unmode) → tap numbers (unpick, UNSEL; works across range tabs, "Select all shown") → 🔔 Needs more practice / ↩ Not learned yet → one confirm (UNASK) → undo2. Same rules as the single-verse ✎ (build 383). S.pos moves back to the earliest verse taken off.

## Build 386 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Owner agreed the app was getting heavy. Language & display: Well done screen and Progress badge folded into "🎨 More looks" (MLK). Default Well done look: Vaishnava tradition (fcTr()==='vai') → Kaavi (Grand); General → Classic; only if S.wdst not set.
- Unmark: "Needs more practice" is the main choice (single sheet and select bar); "Not learned yet" is a small link "Or start … again from the beginning".
- Copies explained to owner: Dev = Claude only; Guru Test = every new build, try new things; Guru Preview = owner's daily practice; Live = family and everyone, only on "go live".

## Build 387 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Bug (owner): did verse 1 in Preview, marked 1–75 as known; Today showed 76 but tapping opened verse 2. Not reproducible from a fresh load; cause: an open/paused practice list in memory (e.g. pace 2 → [1,2]) still held verse 2. Fix lstFix(): after mkdo / mkundo (and on gresume) any list holding a new verse that is now learned is dropped (rpKill, LST=[], GPAUSED/GRES cleared); gresume with no list starts a fresh session.
- Tirumaṇ progress badge (owner idea): RIBST 'nm' (default for Vaishnava tradition, else Ribbon). Namam shape follows S.wdnm (Thenkalai/Vadakalai); the red śrīcūrṇam fills from the bottom with % learned (clipPath); "76 of 108" pill and "2 a day · 70%".

## Build 388 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Gemini's three progress badges (owner's mock), in More looks: gd Golden tirumaṇ (gold namam on a gold lotus, red line fills with %, pills "75 / 108", "69%", "1 a day") — default for Vaishnava tradition; ar Temple arch (three bars white-red-white fill with %); md Medallion (bronze disc, namam inside, red progress ring). Namam paths shared in NMP (t/v). Watch for class name clashes: .arb was taken → .rbab/.rbaw.
- Swadhyayam: folder link history S.swlh (last 5, swLH on save/copy) shown under the link box when no link is set ("Links you used before · Use"). "🔁 Bring from another copy" (swCopyBox/swCopyFrom) in More: reads the other copy's raw localStorage (window.LSRAW, set before the ENV prefix patch) and its IndexedDB sg_own 'lec' (window.IDBRAW, only if indexedDB.databases() lists it), merges sw* settings (fills gaps, merges maps/arrays) and classes with web links (YouTube/OneDrive/http); phone-file classes are skipped. Source copy is not changed.

## Build 389 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Golden tirumaṇ badge redrawn to match the owner's Gemini picture exactly: wide ivory arms with gold edge and slanted tops, tapered red-orange flame in the middle (fills from the bottom with %; the rest shows faintly), gold lotus under the neck, pills: maroon "75 / 108" with gold border, tan "69%", white "1 a day". Now the default badge for everyone (S.ribst unset → 'gd'); other shapes stay in More looks.

## Build 390 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Owner: the drawn golden tirumaṇ didn't look like Gemini's. Now the badge uses the Gemini picture itself (GDIMG, cut out of the owner's screenshot with a transparent background, 183×267, 12 KB PNG), shown 56 px wide; pills stay live. The picture's red line is fixed (no fill); progress is in the pills. Swap GDIMG for a cleaner original if the owner sends one.

## Build 391 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Owner sent the clean original Gemini picture. GDIMG now cut from that file (namam + lotus only, transparent, 168×254, 128-colour PNG, ~9.5 KB). Same size on screen (56 px wide); pills stay live; red line fixed (no fill).

## Build 392 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Owner asked for a smaller tirumaṇ: .rb-gd .gdi width 56px → 44px. Pills unchanged.

## Build 393 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Bug (owner, Preview): after today's practice, "Continue · verse 76" opened verse 2. Real cause: verse 2 was due for revision, and beginSession() puts due revisions first. Build 387's stale-list guess was not the cause. Fix: when S.doneDay===tdy() (extra-verse button), beginSession keeps only the new verse(s); due revisions stay in Revise. The main "Start today's practice" still does revisions first (its card lists them).

## Decision (16 Nov 2026) — no build
- Show script / dash lines choice: previewed (preview-dash.html), owner asked if it adds confusion. Advice taken: keep script + dash lines for everyone, no new setting. Revisit only if real users ask.

## Build 394 (16 Nov 2026) — Dev + Test only (Preview and Live not changed).
- Home top from the owner's Gemini mock: new badge style sc "🐚 Shankha & chakra" (now the default when S.ribst is unset; listed first in More looks). Shankha left ("91 / 108 · learned"), chakra right ("84% · 1 a day"), each on a gold arc open at the bottom that fills with progress (scArc). Pictures cut from the owner's Gemini screenshot (SCIMG.s / SCIMG.c, ~5 and 7 KB) — swap for sharper originals if he sends them. Vishnu circle 146→164 px, less zoom (background-size 132%) so more of the figure shows, via .dh:has(.scb). No "Tap for your progress" hint for this style (it covered the title). Both sides open progress (sdo).

## Build 395 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Owner: in Preview the Home screen style colours did nothing. Cause: they only styled the old Home (bigHome bv1..7); the D · Clean header (dhHead) ignored hmV(), and Classic (0) even switched Preview back to the old Home. Now dhHead adds class dv+hmV() to .dh; CSS .dh.dv0..dv7 colours the top (background, title, pills/icons, Learning now card, Listen/Chant/Meaning, circle ring; dark ones 2 Temple, 4 Festival, 6 Royal get a rounded dark panel with gold). 1 Sunrise = the look it had. The bigHome condition now also runs for Classic when tdL()===D.

## Benchmark 1 (16 Nov 2026) — build 395, commit 20847e5
- Owner chose D · Clean Home with bottom tabs as the app's look. Whole app as of build 395 (all old Home layouts A/B/C/Now, header styles big/portrait/arch, test switches) saved on GitHub branch benchmark-1-build395 (also archive/all-home-styles-b395, same commit). Tags cannot be pushed through the session proxy, so branches are used. Do not delete these branches.

## Build 396 (16 Nov 2026) — Dev + Test + Preview. Not live.
- D · Clean is the only Home in every copy: tdL() always D, dhS() always circle, HS always B; test bars (tdlBar, dhStyleBar, hsBar) return empty; Settings rows "New home look (test)" and "Today layout (test)" removed; Gemini look (S.gem) always on. Old code paths are still in the file (not deleted yet) — only switched off. Delete later after a few weeks, once nothing is missed.

## Build 397 (16 Nov 2026) — Dev + Test + Preview. Not live.
- Owner picked option A from preview-align.html: .dh-circ .dh-c 124 → 136 px, background-size 150%, position 50% 40% (Vishnu centred crown to feet), margin -14px auto 16px so the colour rings (Royal has 8 px of rings) no longer touch "Sloka Guru". Shankha & chakra style keeps its own size rule.

## Build 398 (17 Nov 2026) — Dev + Test only (Preview and Live not changed).
- New practice screen (.g2): read-aloud lines bigger (min(1.55rem,5.8vw)), verse smaller and softer on top (sa/enb 1.05rem, te 1.12rem, opacity .8). sheetVerse() adds class sh<both|scr|dash> to .rpverse.
- One setting S.fcshow (both / scr = verse only / dash = read-aloud only) now used by practice AND Parayanam. Moved to You › Language & display › "👁 What to show while chanting" (removed the duplicate chips under 🪔 Parayanam). In practice, "Verse only" still shows both for a NEW verse (!it.r, not recap). Old practice screen keeps its sizes; only the show/hide rule applies.

## Build 399 (17 Nov 2026) — Dev + Test only (Preview and Live not changed).
- Practice and Parayanam now have separate show choices: S.prshow (practice, sheetVerse) and S.fcshow (Parayanam, unchanged, also set from Parayanam's अ/అ menu). Both in You › Language & display › How I practise › "👁 What to show while chanting" as two rows (Practice / Parayanam), default both. data-act 'prshow'.

## Build 400 (17 Nov 2026) — Dev + Test only (Preview and Live not changed).
- Revise (NEWORG): the "Your verses" card is gone. vsTop() puts the three counts (🔔 Revise today · ⏳ Coming back · 🌿 Kaṇṭhastham) right under the revision bar. Tap Revise today / Coming back → its list opens just below (tap again closes; VSO, session only; null = auto: Revise today opens by itself when verses are due). Revise today list: up to 6 + "Start revision ›"; Coming back: up to 8 + "+N more". Kaṇṭhastham toggles the old VSST filter on the Practise any verse numbers. The counts row inside Practise any verse is removed in NEWORG.
- Range tabs in NEWORG show the fixed block (81–100), so a block with one verse no longer shows "81" twice.

## Build 401 (17 Nov 2026) — Dev + Test only (Preview and Live not changed).
- Swadhyayam new look (owner chose the mix of Gemini's tabs + this-week card; preview swadhyayam-mix-preview.html). swPage0() now returns swNew(): progress line (#ow-today kept) + 📊 (swhist) + ⚙️ (swset); tabs SWT2 L/B/N:
  - Listen: calm twilight-blue hero (.swn-hero, gold play) around swPlayer(l,pl,{svg:1}); label "THIS WEEK'S CLASS" when l is swWeek(), else NOW PLAYING; nothing playing → swWeekCard() or swContinue() in the hero (.swn-idle); then swLineCard() + swUpNext().
  - Library: swClasses({noWeek:1}) + swLocal() + Add a link + Add from phone files.
  - Notes: chips SWNF all/doubt/notes/line → swDoubtCard / swNotesList / swLines.
  - ⚙️ bottom sheet (SWSET): reminder and goal, bring from another copy, how-to, account and folder, 🎓 My students (OWN only, "only you see this").
- The 6 page-style chips are no longer shown; old style code kept, unused. OWNA handlers swt2/swnf/swset are added right after MSF is declared (OWNA must exist first — adding them earlier broke the whole script in testing).

## Build 402 (17 Nov 2026) — Dev + Test only.
- Swadhyayam fixes from the owner's iPhone test: note box Cancel was white on white (now dark); "This class · N notes" has its own soft panel with space below and a ⌄/⌃ arrow; ✕ delete buttons 40px circles; top line shows "N min to go today"; bigger › arrows on folders and fold rows (.swn scope).
- Library: msPanel(o.flat) always shows the list (the Hide/Show fold could not close when a folder held only sub-folders, so Hide did nothing). Tapping a class (msplay) or a phone file/link (swopen) now switches to the Listen tab and scrolls up, so you see the player (before, it started in the background on the Library tab and looked like nothing happened). Wrappers are added after try{msRedirect()} because OWNA.msplay is defined there.
- On this phone and links: swLocal2() — type icon (YouTube / link / phone), title, "YouTube · 36 min · heard 0 of 3", progress bar, big round play, 44px ⋯.

## Build 403 (17 Nov 2026) — Dev + Test only.
- Practise any verse: header ✎ is now a "✎ Edit" pill (✕ Done when on), 🔍 42px, per-verse ✎ (.vsun) 44px; headphone icon hidden in that header and subtitle shortened to "N learned · tap a number" so the title fits on one line.

## Build 404 (17 Nov 2026) — Dev + Test only.
- Read-aloud lines bigger than the verse on EVERY chanting screen, not only the new practice screen: CSS moved from `.g2 .rpverse.sh*` to `.rpverse.sh*` (old practice screen, Weekly recap), and plSheet (Listen to all, Play a verse, Chant all 108) now adds the sh<both|scr|dash> class and follows S.prshow.
- Revise lists (Revise today / Coming back) show 3 rows, then "Show all N ⌄" / "Show less ⌃" (VSMORE, session only).

## Build 405 (17 Nov 2026) — Dev + Test only.
- Practise any verse: the 🔍 number box was a full-width box. Now one compact line: "Verse number [ 96px box ] ✕" (vsSelNew wraps #jv in .vsjv); ✕ and 🔍 toggle JSR (jsr action now toggles and only focuses when opening).

## Build 406 (17 Nov 2026) — Dev + Test only. To undo: index-proto.html/index-dev.html from commit 1451d68 (build 405).
- Swadhyayam (from swadhyayam-clickable.html, owner said go ahead):
  - 📊 / ⚙️ are 58px tiles with labels "My listening" / "Settings".
  - Listen: swJoin() card "Swamy's class · <when> · Join on Teams/WhatsApp ›" above the player; swWeekBars() (7 days, bar = minutes vs goal, tap a day, "N of 7 days with your full 60 min"); swFromClass(l) (open doubts / notes of the playing class → Notes tab filtered, action swnf2); then Up next.
  - Class link: swClsCheck() reads class-link*.txt from the ROOT of the guru's OneDrive folder (MSF.path[0]) after each msList, at most every 4 h (↻ Check the file now in ⚙️, owner only). Line with https = link; first other line = when. Stored in S.swcls {u,w,at}. Students see it after signing in; nothing is stored in the app code.
  - Library: heading "Swamy's classes" (crumb hidden at the root), slim folder rows; swLocal3(): "My other listening · N", filters All / YouTube / Links / Phone (only when >3), 3 rows then Show all, slim rows; one "＋ Add a link or a file" button opens a sheet (SWADD) with the link box and the phone-file picker (sheet closes after adding).

## Build 407 (17 Nov 2026) — Dev + Test only.
- Bug in 406: an extra </div> after "Check the file now" (owner-only class-link section) closed the ⚙️ sheet early, so Reminder, How to, Account and folder, My students fell outside the sheet (owner saw them missing). Fixed.
- Join card now shows on the Listen tab even when no class is playing yet (was only added next to the player card).

## Build 408 (17 Nov 2026) — Dev + Test only. To undo the 5 ideas: commit c467779 (build 407).
- From swadhyayam-clickable-2.html (owner said go ahead):
  - swRing(m,g): minutes ring floated in the hero (top bar removed; header keeps "N of 60 min · to go" text).
  - swPlan(m,g,l): Today's plan, ticks by itself: Listen (minutes ≥ goal) · Recall your 3 points (a class whose points are due: never recalled and not written today, or last recall ≥3 days; button swrc) or Write 3 points from this class (swnf2) · One line from today (S.swtk[today]; button swline forces the line card via SWLINEF).
  - swTip(l): one tip, hidden for the day with ✕ (S.swtipno).
  - Notes › All starts with swPtsSec(l): current class 3 inputs (swpts3) or its points; other classes with points (latest 3) with 🧠 Recall check (SWRC hides the text) → I remembered ✓ (x.rc=today) / Show me; ✎ Edit.
  - l.pts stays the OLD string format ("1. …\n2. …") so the older 3-points textarea keeps working; swPA() reads both string and array. New fields: l.ptsd (date written), l.rc (last recall date). Note: an action named swpts already existed (old textarea) — new one is swpts3.
  - Library: "YOU ARE HERE" tag on the class that is playing; that row gets a blue border.

## Build 409 (17 Nov 2026) — Dev + Test only. To undo the look only: commit c1a9e87 (build 408).
- Swadhyayam polished look (preview swadhyayam-polish-preview.html, Peacock): SVI line icons (tabs, My listening/Settings, Important/Note/Doubt via swPolish() on the swNew output, folders, YouTube/link/phone rows, tip, add); swRing() is now a japa mala (beads = goal/2, 15–45; one bead per 2 min at a 60-min goal; gold, green when done); "‖ श्रीमते रामानुजाय नमः ‖" line at the top of Listen (owner asked for Ramanuja sampradaya wording instead of Sri Gurubhyo namah; draft for guru review); teal Peacock hero with gold; soft borderless cards with shadows; bigger sentence-case section titles; Notes tab badge is a red count.

## Build 410 (17 Nov 2026) — Dev + Test only.
- Owner: Close and Back buttons in different colours. A MutationObserver (after msRedirect) tags buttons after each render: text "Close"/"✕ Close" → .btn-close (soft red: #fdeceb bg, #a3352a text); text starting ‹ / ← / Back, and folder crumbs except the current one (msup with a next sibling) → .btn-back (soft teal: #e7f2ef bg, #0d5c58 text). Applies across the whole app.
