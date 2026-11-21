# Makes preview-way-b.html and preview-way-c.html from index-proto.html (Guru Test).
# They are exact copies of Guru Test with:
#  - their own storage (wayb_ / wayc_), first filled once from Guru Test's saved progress (test_ keys),
#    so nothing they do changes Guru Test or the live app;
#  - a "WAY B" / "WAY C" tag;
#  - the new-verse order changed (Way B: meaning first; Way C: guru vandanam first, samarpanam at the end).
# Run again after Guru Test changes:  python3 tools/make-way-previews.py
import re, sys
SRC = 'index-proto.html'
src = open(SRC, encoding='utf-8').read()
m = re.search(r'var APPV=(\d+)', src); build = m.group(1)

def must(s, a, b, count=1):
    if s.count(a) < 1:
        sys.exit('pattern not found: ' + a[:80])
    return s.replace(a, b, count)

def make(way):
    s = src
    env = 'way' + way
    lbl = 'WAY ' + way.upper()
    s = must(s, "var ENV='test';", "var ENV='%s';" % env)
    s = must(s, '<title>Guru Test</title>', '<title>Preview · Way %s</title>' % way.upper())
    s = must(s, "d.className=ENV;d.textContent=ENV==='pre'?'PREVIEW':ENV.toUpperCase();",
             "d.className='test';d.textContent='%s';" % lbl)
    s = must(s, "function NEWORG(){return ENV==='pre'||ENV==='dev'||ENV==='test'}",
             "function NEWORG(){return ENV==='pre'||ENV==='dev'||ENV==='test'||/^way/.test(ENV)}")
    # first open: copy Guru Test's saved data (test_ keys), not the live app's
    s = must(s, "var ks=[];for(var i=0;i<ls.length;i++){var k=ls.key(i);if(k&&!/^(dev|test)_/.test(k))ks.push(k)}ks.forEach(function(k){if(G.call(ls,P+k)===null)St.call(ls,P+k,G.call(ls,k))});",
             "var ks=[],tk=[];for(var i=0;i<ls.length;i++){var k=ls.key(i);if(k&&/^test_/.test(k)&&!/^test___/.test(k))tk.push(k);else if(k&&!/^(dev|test|pre|way[a-z])_/.test(k))ks.push(k)}if(tk.length)tk.forEach(function(k){var nk=P+k.slice(5);if(G.call(ls,nk)===null)St.call(ls,nk,G.call(ls,k))});else ks.forEach(function(k){if(G.call(ls,P+k)===null)St.call(ls,P+k,G.call(ls,k))});")
    s = must(s, "var old=(list||[]).filter(function(d){return d.name===n})[0];",
             "var old=(list||[]).filter(function(d){return d.name==='test_'+n})[0];")
    s = must(s, "var ro=IO.call(indexedDB,n,old.version);", "var ro=IO.call(indexedDB,'test_'+n,old.version);")
    s = must(s, "VLBL='Guru Test \\u00b7 build '+APPV;", "VLBL='Preview Way %s \\u00b7 copy of Guru Test build '+APPV;" % way.upper())
    s = must(s, 'manifest-test.webmanifest', 'manifest-dev.webmanifest')
    add = open('tools/way-%s.js' % way, encoding='utf-8').read()
    i = s.rfind('</body>')
    s = s[:i] + '<script>\n' + add + '\n</script>\n' + s[i:]
    out = 'preview-way-%s.html' % way
    open(out, 'w', encoding='utf-8').write(s)
    print(out, 'made from Guru Test build', build)

make('b'); make('c')
