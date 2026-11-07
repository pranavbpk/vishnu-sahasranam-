# Using another AI (Gemini, Copilot, ChatGPT) on Sahasranama Guru

For Pranav. Read part A once. Paste part B as your FIRST message in a new chat. Then attach the files in part C.

---

## A. Before you start (2 minutes, once per AI)

Turn off training on your chats (menu names change; look for these words):
- **Gemini:** gemini.google.com › Settings › Activity › turn off "Gemini Apps Activity" (or "Keep activity"). Google may still keep chats for a short time for safety.
- **Copilot:** Settings › Privacy › turn off "Model training on text" (and on voice).
- **ChatGPT:** Settings › Data controls › turn off "Improve the model for everyone". Or use a Temporary chat.

Never paste or upload:
- Passwords, 2-step codes, GitHub tokens, Azure keys.
- The guru's OneDrive folder link.
- Your "Save my progress" file (it has your plans, notes and doubts).
- Students' names or emails, or content/students.json.
- Your 5-tap passcode.

Good to know:
- The app's code is already public on GitHub. Sharing it is not a risk.
- Your own practice data lives on your phone, not in the code.
- No AI can promise you "no tracking" for its own service. What you control: what you paste, and the settings above.

Do not give another AI write access to GitHub. Let it give you the changed file. You test it as Guru Test (index-proto.html), and later ask Claude to check and push it.

---

## B. Paste this as the first message

```
I am building a free web app called Sahasranama Guru that teaches Vishnu Sahasranamam the guru-shishya way (listen, repeat after the guide, say the whole verse, record, meaning, revision). I will attach HANDOFF.md and the app files. Please read HANDOFF.md fully before suggesting anything.

Rules for you (please confirm you will follow them before we start):
1. Privacy: do not ask me for, store, repeat or print any password, token, key, email address, cloud-folder link or personal progress file. If you think you need one, stop and tell me why instead.
2. No tracking: do not add analytics, ads, cookies, third-party scripts, outside fonts or CDNs, or any call to a server or API that is not already in the code. If a feature would need one, tell me first and wait.
3. Work only on index-proto.html (the test copy). Never change index.html, content/students.json, the offline helper's cache names, or the owner-only areas (Swadhyayam, My plans, owner checks).
4. Keep it one HTML file, plain JavaScript and CSS, no framework, no build step.
5. Follow the iPhone audio rules in HANDOFF.md exactly (no Web Audio for playback, play() inside the tap, guard against early 'ended' and ignored seeks).
6. Do not name any book, institute or commercial recording inside the app.
7. For every change: increase APPV by 1, keep everything else working, and give me (a) the full updated index-proto.html or exact find-and-replace edits, (b) a short plain-English list of what changed, (c) how to test it on an iPhone.
8. For design ideas, show me a preview or picture first and wait for my OK before changing the app.
9. Plain, simple language. Short bullet points.

Reply "Understood" and a 5-line summary of how the app is built, then wait for my first request.
```

---

## C. Files to attach

From the zip (sahasranama-guru-for-other-ai.zip):
- HANDOFF.md (how the code works + rules)
- project-brief.md, project-brief-2.md, project-brief-3.md (history and decisions)
- index-proto.html (the test copy to change)
- index.html (live copy, for reference only)
- Optional: preview-*.html, content/*.json, audio/*.json

Tip: if the AI can't read a 2 MB file, ask it to work on one part at a time ("only the My slokas player functions").

---

## D. When the AI gives you a change

1. Save its file as index-proto.html. Put it on GitHub yourself (GitHub website › repo › index-proto.html › Edit › paste › Commit), or keep it and give it to Claude later.
2. Open Guru Test with ?v=NNN on your iPhone and test: Today, Repeat after me with sound, My slokas, Chant all 108.
3. Search the new file for "http" and "fetch(". Anything new pointing somewhere you don't know is a warning sign.
4. If something breaks: every old version is on GitHub (history and the backups branch). Claude can restore it.
5. When Claude is back: say "another AI changed X, please check it" and attach the file.
