#!/usr/bin/env python3
"""Promote the app between environments. One code file, three copies:

  index-dev.html    Dev   "Guru Dev"            (new work happens here)
  index-proto.html  Test  "Guru Test"           (owner + a few testers)
  index.html        Prod  "Sahasranama Guru"    (everyone)
  index-pre.html    Preview "Guru Preview"      (owner only: prod-like look with every change, his chosen styles fixed:
                                                 Today layout D, circle header, bottom tabs; no test switches)

Usage:
  python3 tools/promote.py dev test     # copy Dev -> Test
  python3 tools/promote.py test prod    # copy Test -> Prod (ONLY after the owner says "go live")
  python3 tools/promote.py dev pre      # copy Dev -> Preview (do this with every dev -> test)
  python3 tools/promote.py check        # show which build each copy is on

The copies differ only in: the ENV line, the page title, the manifest, the version label,
and (prod only) the hidden test switches. Everything else is copied as is.
Each Prod release is tagged in git (v107, v108 ...) so it can be rolled back.
"""
import re, sys, datetime, subprocess, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = {'dev': 'index-dev.html', 'test': 'index-proto.html', 'prod': 'index.html', 'pre': 'index-pre.html'}
NAME = {'dev': 'Guru Dev', 'test': 'Guru Test', 'prod': 'Sahasranama Guru', 'pre': 'Guru Preview'}
MANI = {'dev': 'manifest-dev.webmanifest', 'test': 'manifest-test.webmanifest', 'prod': 'manifest.webmanifest', 'pre': 'manifest-pre.webmanifest'}


def rd(env):
    return open(os.path.join(ROOT, FILES[env]), encoding='utf-8').read()


def wr(env, s):
    open(os.path.join(ROOT, FILES[env]), 'w', encoding='utf-8').write(s)


def env_of(s):
    m = re.search(r"var ENV='(dev|test|prod|pre)';", s)
    return m.group(1) if m else None


def build_of(s):
    m = re.search(r"var APPV=(\d+),", s)
    return int(m.group(1)) if m else None


def sub1(pat, rep, s, what):
    s2, n = re.subn(pat, rep, s, count=1)
    if n != 1:
        sys.exit('promote: could not find ' + what)
    return s2


def retarget(s, src, dst):
    """Turn a copy made for `src` into one for `dst` (dev/test only)."""
    s = sub1(r"var ENV='%s';" % src, "var ENV='%s';" % dst, s, 'ENV line')
    s = sub1(r"<title>%s</title>" % re.escape(NAME[src]), "<title>%s</title>" % NAME[dst], s, 'title')
    s = sub1(r'name="apple-mobile-web-app-title" content="%s"' % re.escape(NAME[src]),
             'name="apple-mobile-web-app-title" content="%s"' % NAME[dst], s, 'apple title')
    s = sub1(r'href="%s"' % re.escape(MANI[src]), 'href="%s"' % MANI[dst], s, 'manifest link')
    s = sub1(r"VLBL='%s';" % re.escape(NAME[src]), "VLBL='%s';" % NAME[dst], s, 'VLBL name')
    s = sub1(r"VLBL='%s \\u00b7 build '\+APPV;" % re.escape(NAME[src]),
             "VLBL='%s \\\\u00b7 build '+APPV;" % NAME[dst], s, 'VLBL build line')
    return s


def to_prod(s):
    old = rd('prod')
    m = re.search(r"VLBL='Version (\d+) ", old)
    ver = int(m.group(1)) + 1 if m else 1
    day = datetime.date.today().strftime('%-d %b %Y')
    s = sub1(r"var ENV='test';", "var ENV='prod';", s, 'ENV line')
    s = sub1(r"<title>Guru Test</title>", "<title>Sahasranama Guru</title>", s, 'title')
    s = sub1(r'name="apple-mobile-web-app-title" content="Guru Test"',
             'name="apple-mobile-web-app-title" content="Sahasranama Guru"', s, 'apple title')
    s = sub1(r'href="manifest-test.webmanifest"', 'href="manifest.webmanifest"', s, 'manifest link')
    s = sub1(r"function hsBar\(\)\{", "function hsBar(){return '';", s, 'hsBar')
    s = sub1(r"VLBL='Guru Test';", "VLBL='Version %d \\\\u00b7 %s';" % (ver, day), s, 'VLBL name')
    s = sub1(r"VLBL='Guru Test \\u00b7 build '\+APPV;", "", s, 'VLBL build line')
    return s, ver


def main():
    a = sys.argv[1:]
    if a == ['check'] or not a:
        for e in ('dev', 'test', 'pre', 'prod'):
            try:
                s = rd(e)
                print('%-5s %-17s ENV=%s build=%s' % (e, FILES[e], env_of(s), build_of(s)))
            except FileNotFoundError:
                print('%-5s %-17s (missing)' % (e, FILES[e]))
        return
    src, dst = a
    if (src, dst) not in (('dev', 'test'), ('test', 'prod'), ('dev', 'pre')):
        sys.exit('promote: only dev -> test, dev -> pre or test -> prod')
    s = rd(src)
    if env_of(s) != src:
        sys.exit('promote: %s does not say ENV=%s' % (FILES[src], src))
    if dst in ('test', 'pre'):
        wr(dst, retarget(s, 'dev', dst))
        print('Dev build %s copied to %s (%s).' % (build_of(s), NAME[dst], FILES[dst]))
    else:
        out, ver = to_prod(s)
        wr('prod', out)
        print('Test build %s copied to Prod as Version %d.' % (build_of(s), ver))
        print('Now commit, then: git tag v%d && git push origin v%d' % (ver, ver))


if __name__ == '__main__':
    main()
