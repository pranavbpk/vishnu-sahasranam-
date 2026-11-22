import asyncio
from playwright.async_api import async_playwright
SET="S.uiSet=1;S.setupDone=true;S.rdSeen=1;S.qtSeen=1;S.pr=tdy();S.learned=[];for(var q=1;q<=60;q++)S.learned.push(q);S.pos=vIdx(61);S.rev={};S.gsty='old';"
CSS="""
.mknote{position:fixed;left:10px;right:10px;bottom:12px;z-index:99999;background:#2d1a0c;color:#fff;border-radius:14px;padding:10px 12px;font:600 13px/1.35 system-ui;box-shadow:0 6px 20px rgba(0,0,0,.3)}
.mknote b{color:#f5c84b}
.eyeb{font-size:1.05rem;padding:6px 10px!important;border:2px solid #0f6b66!important;color:#0f6b66!important;background:#e8f4f2!important;font-weight:800}
.hidv{text-align:center;padding:38px 10px;color:#6b5a45;font-size:1.05rem;line-height:1.5}.hidv big{font-size:2.6rem;display:block}
.mkcard{background:#fffaf0;border:1px solid #ecd9b0;border-radius:18px;padding:16px;margin:12px 0;text-align:center}
.mkcard h3{margin:4px 0 6px;font-size:1.25rem;color:#2d1a0c}.mkcard .sm{color:#7a6a55;font-size:.95rem}
.mkcd{width:74px;height:74px;border-radius:50%;margin:12px auto;display:flex;align-items:center;justify-content:center;font-size:2.2rem;font-weight:900;color:#0f6b66;border:4px solid #0f6b66}
.mkbtns{display:flex;gap:10px;margin-top:10px}.mkbtns button{flex:1;padding:13px;border-radius:14px;font-weight:800;font-size:1rem;border:0}
.mkp{background:#0f6b66;color:#fff}.mkg{background:#fff;color:#0f6b66;border:2px solid #0f6b66!important}
.mkmean{background:linear-gradient(#fff6dc,#ffefc2);border:3px solid #e0a526;border-radius:20px;padding:14px;margin:12px 0;box-shadow:0 0 0 6px rgba(240,180,40,.22),0 8px 22px rgba(160,100,0,.18);text-align:left}
.mkmean .tg{display:inline-block;background:#b5651d;color:#fff;font-weight:800;font-size:.8rem;padding:3px 10px;border-radius:20px}
.mkmean img{width:100%;border-radius:14px;margin:10px 0 6px;max-height:170px;object-fit:cover}
.mkmean .one{font-size:1.12rem;line-height:1.45;color:#2d1a0c;font-weight:600}
.mkcarry{margin-top:10px;background:#fff;border-radius:14px;padding:10px 12px;border:1px dashed #d4a84b}
.mkcarry small{color:#7a6a55}.mkcarry .sa{font-size:1.4rem;color:#7a2e0e;font-family:Georgia,serif}
.mkcel{position:fixed;left:18px;right:18px;top:150px;z-index:9999;background:linear-gradient(#fff7e0,#ffe9b3);border:3px solid #e0a526;border-radius:24px;padding:22px 16px;text-align:center;box-shadow:0 14px 40px rgba(0,0,0,.25)}
.mkcel big{font-size:3rem;display:block}.mkcel h3{margin:6px 0;font-size:1.5rem;color:#7a2e0e}.mkcel p{margin:6px 0 14px;color:#4a3a28;font-size:1.05rem}
.mkconf{position:fixed;inset:0;z-index:9998;background:rgba(45,26,12,.35)}
"""
async def vis(pg,t):
    l=pg.locator('button:visible',has_text=t)
    return l.first if await l.count() else None
async def note(pg,txt):
    await pg.evaluate("t=>{var n=document.querySelector('.mknote');if(!n){n=document.createElement('div');n.className='mknote';document.body.appendChild(n)}n.innerHTML=t}",txt)
async def freeze(pg): await pg.evaluate("()=>{window._R=render;render=function(){};try{rpKill&&0}catch(e){}}")
async def thaw(pg): await pg.evaluate("()=>{if(window._R)render=window._R;var n=document.querySelector('.mknote');n&&n.remove()}")
async def shot(pg,name): await pg.wait_for_timeout(500); await pg.screenshot(path=f'/tmp/mock/{name}.png')
async def skipto(pg,cond):
    for k in range(120):
        ok=await pg.evaluate("c=>{var e=document.querySelector('.rpph');var t=e?e.innerText:'';return (new Function('t','return '+c))(t)}",cond)
        if ok: return True
        await pg.evaluate("()=>{var b=[].slice.call(document.querySelectorAll('.rpctl button')).filter(function(b){return /Skip ahead|I.m done$/.test(b.innerText.trim())})[0];if(b)b.click()}")
        await pg.wait_for_timeout(600)
    return False
HDR="()=>{var l=document.querySelector('.lvch');var r=l;var o=document.querySelector('.eyeb');if(o)o.remove();if(r){var b=document.createElement('span');b.className='eyeb';b.textContent=window._EYE||'👁';b.style.cssText='display:inline-flex!important;align-items:center;border-radius:20px;margin-top:4px;white-space:nowrap;visibility:visible;opacity:1';r.parentNode.insertBefore(b,r);r.remove()}}"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required','--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream'])
        ctx=await b.new_context(viewport={'width':393,'height':852},device_scale_factor=2,permissions=['microphone'])
        pg=await ctx.new_page()
        await pg.goto('http://localhost:8765/index-proto.html');await pg.wait_for_timeout(1500)
        await pg.add_style_tag(content=CSS)
        await pg.evaluate("()=>{"+SET+"sv();beginSession()}");await pg.wait_for_timeout(1200)
        
        await pg.wait_for_timeout(400)
        for t in range(3):
            bt=await vis(pg,'OK')
            if bt: await bt.click(); await pg.wait_for_timeout(300)
        print(await skipto(pg,"t.indexOf('Listen')>=0&&t.indexOf('Line 1')>=0"));await pg.wait_for_timeout(2500);print(await pg.evaluate("()=>[(document.querySelector('.rpph')||{}).innerText,!!document.querySelector('.rpverse'),view,RP&&RP.phase]"))
        await freeze(pg); await pg.evaluate(HDR)
        await pg.evaluate("()=>{window._VS=document.querySelector('.rpverse').outerHTML}")
        await note(pg,"<b>1 · 👁 on the Old screen.</b> Level chip gone from here (set once, in You › Settings). One 👁 button to hide / show the verse at any time.")
        await shot(pg,'01_eye_old_screen'); await thaw(pg)
        await skipto(pg,"t.indexOf('Your turn')>=0&&t.indexOf('Line 1')>=0")
        await freeze(pg); await pg.evaluate(HDR)
        await pg.evaluate("()=>{[].forEach.call(document.querySelectorAll('.rpctl button'),function(b){if(b.innerText.indexOf('done')>=0){b.textContent='✓ I\\'ve got it ›';b.style.cssText='background:#0f6b66;color:#fff;font-weight:800'}})}")
        await note(pg,"<b>5 · “I've got it”.</b> Skips the rest of this line's repeats and goes to the next line. Beginners just let it run.")
        await shot(pg,'02_ive_got_it'); await thaw(pg)
        await skipto(pg,"t.indexOf('Your turn')>=0&&t.indexOf('Whole verse')>=0")
        await freeze(pg); window_eye=await pg.evaluate("()=>{window._EYE='🙈'}"); await pg.evaluate(HDR)
        await pg.evaluate("()=>{var v=document.querySelector('.rpverse');var s=v.querySelector('.rdsel');v.innerHTML='';if(s)v.appendChild(s);var d=document.createElement('div');d.className='hidv';d.innerHTML='<big>🙈</big>Verse hidden. Say it from memory.<br><small>Tap 🙈 at the top to peek</small>';v.appendChild(d)}")
        await note(pg,"<b>1 · Verse hides by your level.</b> 🌿 Normal: hidden on your own turn. Tap 🙈 to peek, any time.")
        await shot(pg,'03_verse_hidden'); await thaw(pg); await pg.evaluate("()=>{window._EYE=null}")
        await skipto(pg,"false||!!Array.prototype.find.call(document.querySelectorAll('button'),function(b){return b.offsetParent&&b.innerText.indexOf('Tap to record')>=0})")
        await freeze(pg); await pg.evaluate(HDR)
        await pg.evaluate("()=>{[].forEach.call(document.querySelectorAll('.rpsheet *'),function(e){if(e.children.length<6&&/Meaning of verse/.test(e.innerText||'')&&e.innerText.length<80){var c=e;while(c.parentElement&&!/rpsheet/.test(c.parentElement.className)&&c.parentElement.innerText.length<90)c=c.parentElement;c.style.display='none'}})}")
        await note(pg,"<b>2 · Meaning card gone from here.</b> Record first. The meaning comes after you hear yourself.")
        await shot(pg,'04_record_no_meaning'); await thaw(pg)
        bt=await vis(pg,'Tap to record'); await bt.evaluate("e=>e.click()"); await pg.wait_for_timeout(4000)
        bt=await vis(pg,'Stop recording'); await bt.evaluate("e=>e.click()"); await pg.wait_for_timeout(1500);print(await pg.evaluate("()=>document.querySelector('.rpsheet').innerText.slice(0,300)"))
        await freeze(pg); await pg.evaluate("()=>{try{stopAll&&stopAll()}catch(e){};[].forEach.call(document.querySelectorAll('audio'),function(a){a.pause()})}")
        FIND="function fc(rx){var best=null;[].forEach.call(document.querySelectorAll('.rpsheet *'),function(e){if(rx.test(e.innerText||'')&&e.innerText.length<400&&(!best||e.innerText.length>best.innerText.length))best=e});return best}"
        await pg.evaluate("()=>{"+FIND+";window._H=fc(/Hear yourself/);window._M=fc(/Before you go/);}");await pg.evaluate(HDR)
        await pg.evaluate("()=>{_M.style.display='none';_H.innerHTML='<div class=\"mkcard\" style=\"margin:0;border:0\"><div style=\"color:#0f6b66;font-weight:800\">🎙 Take saved</div><h3>Now listen: you, then the guide</h3><div class=\"sm\">Notice where they sound different.</div><div class=\"mkcd\">3</div><div class=\"mkbtns\"><button class=\"mkp\">Start now</button><button class=\"mkg\">Skip</button></div></div>'}")
        await note(pg,"<b>3 · A short gap first.</b> 3-second countdown (or Start now), so you are ready before your voice plays.")
        await shot(pg,'05_gap_before_compare')
        VS="window._VS.replace(/<div class=\"rdsel[\\s\\S]*?<\\/div>/,'')"
        await pg.evaluate("()=>{var vs="+VS+";_H.innerHTML='<div style=\"text-align:center;font-weight:800;color:#0f6b66;margin:6px 0 10px\">Now playing</div><div class=\"mkbtns\" style=\"margin:0 0 10px\"><button class=\"mkp\">🙂 You</button><button class=\"mkg\" style=\"opacity:.45\">🔊 Guide</button></div>'+vs;var v=_H.querySelector('.rpverse');v.style.margin='0';[].forEach.call(v.querySelectorAll('.ln.l2'),function(l){l.style.opacity='.35'});[].forEach.call(v.querySelectorAll('.ln.l1'),function(l){l.style.background='#fff1c9';l.style.borderRadius='8px'})}")
        await note(pg,"<b>4 · Verse on screen while comparing.</b> The line being heard lights up: first your take, then the guide.")
        await shot(pg,'06_verse_while_comparing')
        await pg.evaluate("()=>{var a=document.createElement('div');a.className='mkcard';a.innerHTML='<h3>Did it sound the same?</h3><div class=\"mkbtns\"><button class=\"mkp\">👍 Close enough</button><button class=\"mkg\">🎙 Try again</button></div><div class=\"sm\" style=\"margin-top:10px\">🔁 Hear both again</div>';_H.appendChild(a);[].forEach.call(_H.querySelectorAll('.ln'),function(l){l.style.background='';l.style.opacity='1'});a.scrollIntoView({block:'end'})}")
        await note(pg,"<b>4 · Then one question.</b> 👍 moves on. 🎙 records again.")
        await shot(pg,'07_compare_question')
        await pg.evaluate("()=>{_H.innerHTML='<div class=\"mkmean\"><span class=\"tg\">📖 Meaning of verse 61</span><img src=\"img/mean/v061.jpg\"><div class=\"one\">The Lord holds a mighty bow and an axe. He is stern with evil, kind to the good, and sees everything.</div><div class=\"mkcarry\"><small>🌼 Carry one name today</small><div class=\"sa\">वाचस्पतिः · Vaa-chas-pa-tih</div><div>Lord of speech</div></div><div style=\"margin-top:10px;font-weight:700;color:#7a4a12\">📖 Full meaning and all 9 names ›</div></div>';_H.style.cssText='background:none;border:0;box-shadow:none;padding:0';_H.scrollIntoView({block:'start'});window.scrollBy(0,-90);document.querySelector('.rpsheet').scrollTop=0}")
        await note(pg,"<b>2 · Meaning comes now, highlighted.</b> After recording and comparing. Gold card, picture, one line, and one name to carry today.")
        await shot(pg,'08_meaning_after_recording'); await thaw(pg)
        # home celebration
        await pg.evaluate("()=>{rpKill();RP={on:false};S.learned=[];for(var q=1;q<=27;q++)S.learned.push(q);S.pos=vIdx(28);view='home';HT='today';render(1)}");await pg.wait_for_timeout(1800)
        await freeze(pg)
        await pg.evaluate("()=>{var c=document.createElement('div');c.className='mkconf';document.body.appendChild(c);var d=document.createElement('div');d.className='mkcel';d.innerHTML='<big>🌟</big><h3>27 verses!</h3><p>A quarter of the Sahasranamam is now yours.<br>🔥 12-day streak</p><div class=\"mkbtns\"><button class=\"mkp\">🙏 Thank you</button><button class=\"mkg\">📤 Share</button></div>';document.body.appendChild(d)}")
        await note(pg,"<b>6 · Small celebrations</b> only at 10, 27, 54 and 108 verses. Shown once, one tap to close.")
        await shot(pg,'09_celebration_27'); await thaw(pg)
        pg2=await ctx.new_page()
        await pg2.goto('http://localhost:8765/preview-nov22.html');await pg2.wait_for_timeout(800)
        await pg2.evaluate("()=>{localStorage.setItem('pv22',JSON.stringify({setup:true,who:'me',lvl:'n',done:{61:1},rec:'',today:1,todayD:new Date().toDateString(),last:61,lot:12,kdone:{},kidx:1}))}")
        await pg2.reload();await pg2.wait_for_timeout(800)
        await pg2.add_style_tag(content=CSS+".ph{margin-top:0!important}body,html{background:#f6efe2!important}")
        await pg2.evaluate("()=>{var p=document.querySelector('.ph');var e=p.previousElementSibling;while(e){e.style.display='none';e=e.previousElementSibling}}")
        await pg2.evaluate("()=>{VIEW='fin';draw()}");await pg2.wait_for_timeout(800)
        await note(pg2,"<b>7 · Today's kainkaryam fits one screen.</b> Title, 3 numbers, name for today, Done. Blessing one tap away.")
        await pg2.evaluate("()=>{var n=document.querySelectorAll('.note');n.forEach(function(x){x.remove()})}")
        await shot(pg2,'10_kainkaryam')
        await pg2.evaluate("()=>{ST.who='kid';VIEW='khome';KV='khome';draw()}");await pg2.wait_for_timeout(800)
        await note(pg2,"<b>Kids mode (own profile).</b> One name a day, picture, Hear · Say · Story · Game, a 108-lotus garland.")
        await shot(pg2,'11_kids_home')
        await pg2.evaluate("()=>{KV='kgame';var k=kv().kid;KS={ph:'',r:0,pick:[],bad:-1,sh:shuf(k.words.length)};KS.pick=[0];draw()}");await pg2.wait_for_timeout(500)
        await note(pg2,"<b>Kids mode · word game.</b> Tap the words in the right order to earn a lotus.")
        await shot(pg2,'12_kids_game')
        await b.close()
asyncio.run(main())
