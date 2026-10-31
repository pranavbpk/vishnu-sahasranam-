/* Offline support for Guru Test (index-proto.html) only.
   Requests from the live app (index.html) are never touched. */
var CORE='gt-core-v2', AUD='gt-audio-v2';
var CORE_FILES=['index-proto.html','manifest-test.webmanifest','icon-180.png','icon-192.png','icon-512.png','audio/cuts.json','satsang.json','vishnu-sahasranamam-108-verses.pdf'];

self.addEventListener('install',function(e){
  e.waitUntil(caches.open(CORE).then(function(c){
    return Promise.all(CORE_FILES.map(function(f){return fetch(f,{cache:'no-store'}).then(function(r){if(r.ok)return c.put(f,r)}).catch(function(){})}));
  }).then(function(){return self.skipWaiting()}));
});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(ks){
    return Promise.all(ks.filter(function(k){return k.indexOf('gt-')===0&&k!==CORE&&k!==AUD}).map(function(k){return caches.delete(k)}));
  }).then(function(){return self.clients.claim()}));
});

function isProto(req){
  var u=new URL(req.url);
  if(u.origin!==self.location.origin)return false;
  if(/index-proto\.html$/.test(u.pathname))return true;
  return /index-proto\.html/.test(req.referrer||'');
}
function rel(u){return new URL(u).pathname.replace(/^.*\/vishnu-sahasranam-\//,'').replace(/^\//,'')}

/* Safari asks for audio in byte ranges; answer from the cached file. */
function ranged(req,resp){
  var range=req.headers.get('range');
  if(!range||!resp)return resp;
  return resp.arrayBuffer().then(function(buf){
    var m=/bytes=(\d*)-(\d*)/.exec(range)||[],size=buf.byteLength;
    var start=m[1]?parseInt(m[1],10):0,end=m[2]?parseInt(m[2],10):size-1;
    if(!m[1]&&m[2]){start=Math.max(0,size-parseInt(m[2],10));end=size-1}
    end=Math.min(end,size-1);
    return new Response(buf.slice(start,end+1),{status:206,statusText:'Partial Content',headers:{
      'Content-Type':resp.headers.get('Content-Type')||'audio/mp4','Content-Range':'bytes '+start+'-'+end+'/'+size,
      'Content-Length':String(end-start+1),'Accept-Ranges':'bytes'}});
  });
}

self.addEventListener('fetch',function(e){
  var req=e.request;
  if(req.method!=='GET'||!isProto(req))return;
  var u=new URL(req.url),p=rel(req.url);
  /* the version check (?vc=) always goes to the network */
  if(u.searchParams.has('vc'))return;
  /* the app page: network first, fall back to the saved copy */
  if(req.mode==='navigate'||/index-proto\.html$/.test(u.pathname)){
    e.respondWith(fetch(req).then(function(r){if(r.ok){var cp=r.clone();caches.open(CORE).then(function(c){c.put('index-proto.html',cp)})}return r})
      .catch(function(){return caches.match('index-proto.html',{ignoreSearch:true})}));
    return;
  }
  /* audio: saved copy first, then network (and save it) */
  /* the big 108 file streams straight from the internet (never stored here) */
  if(/^audio\/all108\./.test(p))return;
  if(/^audio\/.*\.(m4a|mp3)$/.test(p)){
    e.respondWith(caches.open(AUD).then(function(c){
      return c.match(p).then(function(hit){
        if(hit)return ranged(req,hit);
        /* not saved yet: play from the internet right away, save a copy quietly */
        e.waitUntil(fetch(p).then(function(r){if(r.ok)return c.put(p,r)}).catch(function(){}));
        return fetch(req);
      });
    }).catch(function(){return fetch(req)}));
    return;
  }
  /* small data files: network first, saved copy when offline */
  if(/\.(json|webmanifest)$/.test(p)){
    e.respondWith(fetch(req).then(function(r){if(r.ok){var cp=r.clone();caches.open(CORE).then(function(c){c.put(p,cp)})}return r})
      .catch(function(){return caches.match(p,{ignoreSearch:true})}));
    return;
  }
  /* icons, PDF and anything else of ours: saved copy first */
  e.respondWith(caches.match(p,{ignoreSearch:true}).then(function(hit){return hit||fetch(req).then(function(r){if(r.ok){var cp=r.clone();caches.open(CORE).then(function(c){c.put(p,cp)})}return r})}));
});

/* the page sends the list of guide audio files to keep on the phone */
self.addEventListener('message',function(e){
  var d=e.data||{};
  if(d.t!=='audio'||!d.urls)return;
  e.waitUntil(caches.open(AUD).then(function(c){
    return d.urls.reduce(function(pr,f){return pr.then(function(){
      return c.match(f).then(function(hit){if(hit)return;return fetch(f).then(function(r){if(r.ok)return c.put(f,r)}).catch(function(){})});
    })},Promise.resolve());
  }));
});
