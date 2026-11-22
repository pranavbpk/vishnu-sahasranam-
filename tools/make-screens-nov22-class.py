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

CL="""(st)=>{var r=document.querySelector('.rpsheet .rdpill');var o=document.querySelector('.clsb');if(o)o.remove();var b=document.createElement('span');b.className='clsb';b.innerHTML=st?'👥<small>On</small>':'👥<small>Off</small>';b.style.cssText='display:inline-flex;flex-direction:column;align-items:center;justify-content:center;line-height:1;font-size:1.15rem;width:48px;height:48px;border-radius:50%;margin-left:6px;font-weight:800;'+(st?'background:#0f6b66;color:#fff;border:2px solid #0f6b66':'background:#f3eee6;color:#8a7a60;border:2px dashed #b9a98c;filter:grayscale(1)');b.querySelector('small').style.cssText='font-size:.62rem;margin-top:2px';r.parentNode.insertBefore(b,r.nextSibling)}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
        ctx=await b.new_context(viewport={'width':393,'height':852},device_scale_factor=2)
        pg=await ctx.new_page()
        await pg.goto('http://localhost:8765/index-proto.html');await pg.wait_for_timeout(1500)
        await pg.add_style_tag(content=CSS)
        await pg.evaluate("()=>{"+SET+"sv();beginSession()}");await pg.wait_for_timeout(1600)
        for t in range(3):
            bt=await vis(pg,'OK')
            if bt: await bt.click(); await pg.wait_for_timeout(300)
        await skipto(pg,"t.indexOf('Your turn')>=0&&t.indexOf('Line 1')>=0")
        await freeze(pg); await pg.evaluate(CL,True)
        await note(pg,"<b>👥 Chant with the class · On.</b> On your turn, soft voices chant with you. One tap turns it off, right here. Same switch as in You › Settings.")
        await shot(pg,'13_class_on')
        await pg.evaluate(CL,False)
        await note(pg,"<b>👥 Chant with the class · Off.</b> On your turn, only you. Tap again to turn it back on.")
        await shot(pg,'14_class_off')
        await b.close()
asyncio.run(main())
