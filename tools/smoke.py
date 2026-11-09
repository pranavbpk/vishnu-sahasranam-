# Quick check of every main screen. Needs: pip install playwright && playwright install chromium
# Run a local server in the repo folder first:  python3 -m http.server 8765
# Then:  python3 tools/smoke.py index-dev.html   (prints any JavaScript errors per screen, saves screenshots to /tmp)
import asyncio,json,sys
from playwright.async_api import async_playwright
F=sys.argv[1]
SET="S.uiSet=1;S.setupDone=true;S.rdSeen=1;S.pr=tdy();S.learned=[];for(var q=1;q<=76;q++)S.learned.push(q);S.pos=vIdx(77);S.rev={};[73,74,75,76].forEach(function(n){S.rev[n]={stage:0,due:tdy()}});OWN=true;"
CASES=[
 ('home_today',"view='home';HT='today';OWNP=null;render(1)"),
 ('home_revise',"view='home';HT='prac';OWNP=null;render(1)"),
 ('home_satsang',"view='home';HT='sat';OWNP=null;render(1)"),
 ('home_learn',"view='home';HT='lib';OWNP=null;render(1)"),
 ('home_you',"view='home';HT='me';OWNP=null;render(1)"),
 ('session_new_old',"S.gsty='old';beginSession()"),
 ('session_new_new',"S.gsty='new';rpKill();RP={on:false};view='home';render(1);beginSession()"),
 ('revision_new',"S.gsty='new';rpKill();RP={on:false};view='home';LP='';LST=[{i:vIdx(74),r:1}];LST.single=true;vi=0;tab='say';view='verse';GS={on:true};render(1);rpStart()"),
 ('weekly_recap',"S.gsty='new';rpKill();RP={on:false};LST=[{i:vIdx(70),r:1,rt:'recap'}];vi=0;tab='say';view='verse';GS={on:true};render(1);rpStart()"),
 ('listen_all',"rpKill();RP={on:false};view='home';HT='prac';render(1);try{plStart()}catch(e){window._pe=String(e)}"),
 ('done_screen',"S.gsty='new';rpKill();LST=[{i:vIdx(77)}];vi=0;view='verse';GS={on:true};RP={on:true,phase:'done',n:77,steps:[2,2,2],round:3};render(1)"),
 ('swadhyayam',"rpKill();RP={on:false};PL.on=false;view='home';HT='me';OWNP='sw';render(1)"),
 ('myslokas',"view='home';HT='me';OWNP='my';MYV={m:'list'};render(1)"),
]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
        pg=await b.new_page(viewport={'width':393,'height':852},device_scale_factor=1)
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:160]))
        await pg.goto('http://localhost:8765/'+F);await pg.wait_for_timeout(1500)
        await pg.evaluate("()=>{"+SET+"sv()}")
        for name,js in CASES:
            n0=len(errs)
            await pg.evaluate("()=>{try{"+js+"}catch(e){window._pe=String(e)}}")
            await pg.wait_for_timeout(1800)
            info=await pg.evaluate("()=>{var r={pe:window._pe||'',view:view,rp:RP&&RP.phase,pl:PL&&PL.on,sheets:document.querySelectorAll('.rpsheet,.plsheet,.pls').length};window._pe='';return r}")
            await pg.screenshot(path=f'/tmp/smoke_{name}.png')
            print(f'{name:18s}',json.dumps(info),'NEW ERRORS:' if len(errs)>n0 else '',errs[n0:])
        await b.close()
asyncio.run(main())
