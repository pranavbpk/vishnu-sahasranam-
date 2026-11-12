# Checks the My slokas auto parts (build 319) against the 108 guide recordings and audio/cuts.json.
# Run a local server in the repo folder (python3 -m http.server 8765), then: python3 tools/test_sync.py index-dev.html
import asyncio,json,sys
from collections import Counter
from playwright.async_api import async_playwright
CORE=''
PAGE=sys.argv[1] if len(sys.argv)>1 else 'index-dev.html'
INJ=len(sys.argv)<=2
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--no-sandbox'])
        pg=await b.new_page()
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
        await pg.goto('http://localhost:8765/'+PAGE);await pg.wait_for_timeout(1500)
        
        r=await pg.evaluate("""async()=>{var cuts=await (await fetch('audio/cuts.json')).json(),out=[];
 for(var n=1;n<=108;n++){var bl=await (await fetch('audio/v'+String(n).padStart(3,'0')+'.m4a')).blob();var ab=await myDecode(bl),an=myPauses(ab);var v=V[n-1];
  var res={n:n,gt:cuts[n]};
  [['sa',v.sa],['en',v.en],['te',v.te]].forEach(function(q){var key=q[0],lines=q[1];
   var x={text:lines.join('\\n'),vs:an.V,dur:ab.duration,mode:'line'};var A=myAutoT2(x,-1);var C=myAutoT2(x,null);var k1=myWords(lines[0]).length;
   res[key+'A']=A.length===1&&A[0].k===k1?A[0].c:null;var hc=C.filter(function(t){return t.k===k1})[0];res[key+'C']=hc?hc.c:null;res[key+'Cn']=C.length+1;
   var y={text:lines.join(' '),vs:an.V,dur:ab.duration,mode:'line'};var B=myAutoT2(y,null);var hit=B.filter(function(t){return t.k===k1})[0];
   res[key+'Bn']=B.length+1;res[key+'B']=hit?hit.c:null;res[key+'Bnear']=B.filter(function(t){return Math.abs(t.c-cuts[n])<0.35}).map(function(t){return t.k-k1});
  });out.push(res)}return out}""")
        json.dump(r,open('/tmp/sync_res.json','w'))
        print('errors',errs[:3])
        for key in ['sa','en','te']:
            okA=sum(1 for x in r if x[key+'A'] is not None and abs(x[key+'A']-x['gt'])<=0.35)
            okB=sum(1 for x in r if x[key+'B'] is not None and abs(x[key+'B']-x['gt'])<=0.35)
            nearwrong=[ (x['n'],x[key+'Bnear']) for x in r if x[key+'Bnear'] and 0 not in x[key+'Bnear']]
            okC=sum(1 for x in r if x[key+'C'] is not None and abs(x[key+'C']-x['gt'])<=0.5)
            print(key,'typed lines, breath parts: line break ok',okC,'/108 parts',Counter(x[key+'Cn'] for x in r).most_common(4))
            print(key,'A ok',okA,'/108  B line-split ok',okB,'/108  parts',Counter(x[key+'Bn'] for x in r).most_common(6),' pause found but wrong word:',nearwrong[:12])
            badA=[(x['n'],x[key+'A'],x['gt']) for x in r if not(x[key+'A'] is not None and abs(x[key+'A']-x['gt'])<=0.35)]
            print('  A misses',badA[:10])
        await b.close()
asyncio.run(main())
