/* Builds the HTML for the reader PDFs from the app's own data (V, M, DASH, FC, DHY, FCDH, RB, ECH, BEN).
   Loaded into index-dev.html by tools/make_pdfs.py. Nothing here is part of the app.
   PDFB(kind, lang, echo): kind 'fc' (full chant: lang sa/te/en), 'mean' (meanings: en/te/hi), 'ft' (108 verses). */
(function(){
var TT={
 en:{fc:'Śrī Viṣṇu Sahasranāma Stotram',fcs:'The full chant · read-along text',mean:'Vishnu Sahasranamam · verse meanings',means:'The meaning of every verse and every name',
  ft:'Vishnu Sahasranamam · 108 verses',fts:'Sanskrit, Telugu and the read-aloud lines',
  draft:'Draft text for the guru’s review.',ra:'Read aloud',tip:'Tip',m:'Meaning',names:'Each name',ben:'Special benefit',v:'Verse',
  howh:'How to read',dash:'The dash lines (read-aloud lines) show how to say each word: read them as written, one small part at a time.',
  echoOn:'The small raised letters at the end of a line are the soft echo: say them half as loud and half as long.',
  echoOff:'In this copy the soft echo is not marked.',parts:'Parts',page:'page',
  S:{open:'Opening prayers',dial:'Yudhiṣṭhira asks, Bhīṣma answers',nyasa:'Nyāsa',dhy:'Dhyānam',v108:'The 108 verses',phala:'Phala-śruti',end:'Ending'}},
 te:{fc:'శ్రీ విష్ణు సహస్రనామ స్తోత్రం',fcs:'పూర్తి పారాయణం · చదువుకునే పాఠం',mean:'విష్ణు సహస్రనామం · శ్లోకాల అర్థాలు',means:'ప్రతి శ్లోకం, ప్రతి నామం అర్థం',
  draft:'గురువుగారి పరిశీలన కోసం చిత్తు ప్రతి.',ra:'ఇలా చదవండి',tip:'చిట్కా',m:'అర్థం',names:'ప్రతి నామం',ben:'ప్రత్యేక ప్రయోజనం',v:'శ్లోకం',
  howh:'ఎలా చదవాలి',dash:'డాష్ పంక్తులు ప్రతి పదాన్ని ఎలా పలకాలో చూపిస్తాయి: రాసినట్టే, చిన్న చిన్న భాగాలుగా చదవండి.',
  echoOn:'పంక్తి చివర చిన్నగా పైకి ఉన్న అక్షరాలు మృదువైన ప్రతిధ్వని: సగం గట్టిగా, సగం సేపు పలకండి.',
  echoOff:'ఈ ప్రతిలో మృదువైన ప్రతిధ్వని గుర్తు లేదు.',parts:'భాగాలు',page:'పేజీ',
  S:{open:'ప్రారంభ ప్రార్థనలు',dial:'యుధిష్ఠిరుని ప్రశ్నలు, భీష్ముని జవాబు',nyasa:'న్యాసం',dhy:'ధ్యానం',v108:'108 శ్లోకాలు',phala:'ఫలశ్రుతి',end:'ముగింపు'}},
 hi:{mean:'विष्णु सहस्रनाम · श्लोकों के अर्थ',means:'हर श्लोक और हर नाम का अर्थ',
  draft:'गुरुजी की समीक्षा के लिए मसौदा।',ra:'ऐसे पढ़ें',tip:'सुझाव',m:'अर्थ',names:'हर नाम',ben:'विशेष लाभ',v:'श्लोक',
  howh:'कैसे पढ़ें',dash:'डैश वाली पंक्तियाँ बताती हैं कि हर शब्द कैसे बोलें: जैसा लिखा है वैसा, छोटे-छोटे भागों में पढ़ें।',
  echoOn:'पंक्ति के अंत में छोटे, ऊपर उठे अक्षर हल्की गूँज हैं: आधे ज़ोर से, आधी देर बोलें।',
  echoOff:'इस प्रति में हल्की गूँज नहीं दिखाई गई है।',page:'पृष्ठ'}
};
function esc(s){return String(s)}
function teL(l){return toTe(l).replace(/౐/g,'ఓం')}
/* one read-aloud line, echo on its last word (wordsHTML honours S.echo) */
function dl(line){return '<div class="dl">'+wordsHTML(line,0,0)+'</div>'}
function vt(lines,cls){return '<div class="vt '+cls+'">'+lines.map(function(l){return '<div>'+ndn(l)+'</div>'}).join('')+'</div>'}
function css(){return ''}
function cover(t,sub,lang,list){var T=TT[lang]||TT.en;return '<section class="cover"><div class="om">ॐ</div><h1 class="'+(lang==='te'?'te':lang==='hi'?'sa':'')+'">'+t+'</h1><div class="sub">'+sub+'</div>'+(list?'<ol class="parts">'+list.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ol>':'')+'<div class="draft">'+T.draft+'</div><div class="brand">Sahasranama Guru</div></section>'}
function howPage(lang){var T=TT[lang]||TT.en,l=lang==='te'?'te':lang==='hi'?'hi':'en',e=ECH[l]||ECH.en;
 var h='<section class="how"><h2>'+T.howh+'</h2><p class="lead">'+T.dash+'</p><p class="lead">'+(S.echo==='0'?T.echoOff:T.echoOn)+'</p>';
 h+='<div class="rules">'+RB.map(function(r,i){return '<div class="rule"><div class="ri">'+r.ic+'</div><div><b>'+(i+1)+'. '+r.t[l]+'</b><div>'+r.d[l]+'</div></div></div>'}).join('')+'</div>';
 h+='<div class="echb"><b>'+e.h+'</b>'+e.r.map(function(r){return '<div class="er"><span>'+r[0]+'</span><small>'+r[1]+'</small><i>'+r[2]+'</i></div>'}).join('')+'<div class="et">'+e.t+'</div></div></section>';
 return h}
function sec(id,title,sub){return '<h2 class="sec" id="'+id+'">'+title+(sub?' <small>'+sub+'</small>':'')+'</h2>'}
/* full chant in one script: sa = Devanagari + English read-aloud; te = Telugu + Telugu read-aloud; en = English letters + English read-aloud */
function fcDoc(lang){var T=TT[lang==='te'?'te':'en'],cls=lang==='te'?'te':lang==='en'?'enb':'sa';
 var ord=['open','dial','nyasa','dhy','v108','phala','end'];
 var h=cover(lang==='te'?TT.te.fc:TT.en.fc,T.fcs,lang==='te'?'te':'en',ord.map(function(k){return T.S[k]}))+howPage(lang==='te'?'te':'en');
 function item(x){var lines=lang==='en'?x.tr:lang==='te'?x.sa.map(teL):x.sa,sp=x.sp?(lang==='en'?x.spt:lang==='te'?toTe(x.sp):x.sp):'';
  var d=lang==='te'?(x.d||[]).map(teL):(x.de||[]);
  return (sp?'<div class="sp '+cls+'">'+sp+'</div>':'')+'<div class="it'+(x.n?'':' rf')+'">'+(x.n?'<div class="no">'+x.n+'</div>':'<div class="no nb"></div>')+'<div class="bd">'+vt(lines,cls)+(d.length?'<div class="ra"><span class="lab">🗣 '+T.ra+'</span>'+d.map(dl).join('')+'</div>':'')+'</div></div>'}
 ord.forEach(function(k){h+='<section class="part">'+sec(k,T.S[k]);
  if(k==='dhy')h+=DHY.map(function(d,i){return item({n:i+1,sa:d.sa,tr:[].concat(d.tr),d:FCDH[i].d,de:FCDH[i].de})}).join('');
  else if(k==='v108')h+=V.slice().sort(function(a,b){return a.n-b.n}).map(function(v){var lines=lang==='en'?v.en:lang==='te'?v.te:v.sa,d=lang==='te'?(DASH.te[v.n]||v.pr):v.pr;
   return '<div class="it"><div class="no">'+v.n+'</div><div class="bd">'+vt(lines,cls)+'<div class="ra"><span class="lab">🗣 '+T.ra+'</span>'+d.map(dl).join('')+'</div>'+(lang!=='te'&&v.tip?'<div class="tip"><b>'+T.tip+':</b> '+v.tip+'</div>':'')+'</div></div>'}).join('');
  else h+=FC.filter(function(x){return x.s===k}).map(item).join('');
  h+='</section>'});
 return h}
/* meanings in one language: en = Devanagari + English read-aloud; te = Telugu + Telugu read-aloud; hi = Devanagari + Devanagari read-aloud */
function meanDoc(lang){var T=TT[lang],k=LI[lang]||0,cls=lang==='te'?'te':'sa';
 var h=cover(T.mean,T.means,lang)+'<section class="how"><h2>'+T.howh+'</h2><p class="lead">'+T.dash+'</p><p class="lead">'+(S.echo==='0'?T.echoOff:T.echoOn)+'</p></section>';
 V.slice().sort(function(a,b){return a.n-b.n}).forEach(function(v){var m=M[v.n]||{},lines=lang==='te'?v.te:v.sa,d=lang==='te'?(DASH.te[v.n]||v.pr):lang==='hi'?(DASH.sa[v.n]||v.pr):v.pr;
  var b=(typeof BEN!=='undefined'&&BEN[v.n])?BEN[v.n]:null;
  h+='<div class="mv"><div class="mh"><div class="no">'+v.n+'</div><div class="bd">'+vt(lines,cls)+'<div class="ra">'+d.map(dl).join('')+'</div></div></div>'
   +(m.v?'<div class="mm"><b>'+T.m+'</b> '+m.v[k]+'</div>':'')
   +(m.w?'<table class="nm"><tr><th colspan="3">'+T.names+'</th></tr>'+m.w.map(function(x){return '<tr><td class="'+cls+'">'+(lang==='te'?toTe(x[0]):x[0])+'</td><td class="pr">'+x[1]+'</td><td>'+x[2+k]+'</td></tr>'}).join('')+'</table>':'')
   +(b?'<div class="bn">'+b.ic+' <b>'+T.ben+':</b> '+(b.t[lang]||b.t.en)+'</div>':'')+'</div>'});
 return h}
/* the 108 verses: Devanagari, Telugu, English read-aloud (same as the old PDF) */
function ftDoc(){var T=TT.en;var h=cover(TT.en.ft,TT.en.fts,'en');
 h+=V.slice().sort(function(a,b){return a.n-b.n}).map(function(v){return '<div class="it"><div class="no">'+v.n+'</div><div class="bd">'+vt(v.sa,'sa')+vt(v.te,'te sm')+'<div class="ra">'+v.pr.map(dl).join('')+'</div></div></div>'}).join('');
 return h}
window.PDFB=function(kind,lang,echo){var keep=S.echo;S.echo=echo?'1':'0';try{return kind==='fc'?fcDoc(lang):kind==='mean'?meanDoc(lang):ftDoc()}finally{S.echo=keep}};
window.PDFT=TT;
})();
