"""Make the reader PDFs from index-dev.html's own data.

Usage: python3 tools/make_pdfs.py FONTDIR [only]
FONTDIR holds TiroDevanagariSanskrit-Regular.ttf, NotoSerifTelugu.ttf (variable ok), Inter.ttf
(from github.com/google/fonts, ofl/). Output: docs/pdf/*.pdf, each with an echo and a no-echo copy.
Needs: playwright (chromium). Serves the repo on localhost while it runs.
"""
import sys, os, threading, http.server, socketserver, functools, pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = pathlib.Path(sys.argv[1]).resolve()
ONLY = sys.argv[2] if len(sys.argv) > 2 else ''
OUT = ROOT / 'docs' / 'pdf'
OUT.mkdir(parents=True, exist_ok=True)

DOCS = [  # (file stem, kind, lang, title)
    ('fullchant-sa', 'fc', 'sa', 'Vishnu Sahasranamam · full chant (Sanskrit)'),
    ('fullchant-te', 'fc', 'te', 'Vishnu Sahasranamam · full chant (Telugu)'),
    ('fullchant-en', 'fc', 'en', 'Vishnu Sahasranamam · full chant (English letters)'),
    ('meanings-en', 'mean', 'en', 'Vishnu Sahasranamam · meanings (English)'),
    ('meanings-te', 'mean', 'te', 'Vishnu Sahasranamam · meanings (Telugu)'),
    ('meanings-hi', 'mean', 'hi', 'Vishnu Sahasranamam · meanings (Hindi)'),
    ('verses108', 'ft', 'en', 'Vishnu Sahasranamam · 108 verses'),
]

CSS = """
@font-face{font-family:Deva;src:url('%(f)s/TiroDevanagariSanskrit-Regular.ttf')}
@font-face{font-family:Tel;src:url('%(f)s/NotoSerifTelugu.ttf')}
@font-face{font-family:Ui;src:url('%(f)s/Inter.ttf')}
@page{size:A4;margin:16mm 15mm 18mm}
*{box-sizing:border-box}
body{font-family:Ui,Tel,Deva,sans-serif;color:#2b1a0c;font-size:10.5pt;line-height:1.45;margin:0}
.sa,.vt.sa{font-family:Deva,serif}.te,.vt.te{font-family:Tel,serif}.enb{font-family:Ui,sans-serif}
.cover{height:250mm;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;page-break-after:always;border:2px solid #d4a23c;border-radius:10px;padding:20mm}
.cover .om{font-family:Deva;font-size:44pt;color:#a8431a;line-height:1}
.cover h1{font-size:24pt;color:#7a1f1f;margin:10px 0 4px;font-weight:600}
.cover .sub{font-size:13pt;color:#6b4a1a}
.cover .parts{text-align:left;margin:18px auto 0;font-size:11.5pt;color:#3a2600}
.cover .draft{margin-top:26px;font-size:10pt;color:#8a6a3a;font-style:italic}
.cover .brand{margin-top:6px;font-size:10pt;color:#a8431a;letter-spacing:.06em}
.how{page-break-after:always}
h2{color:#7a1f1f;font-size:16pt;margin:0 0 8px;font-weight:600}
.lead{margin:4px 0 8px}
.rule{display:flex;gap:10px;padding:6px 0;border-bottom:1px solid #f0e2c4;page-break-inside:avoid}
.rule .ri{font-family:Deva,Tel;min-width:34px;color:#a8431a;font-size:12pt;text-align:center}
.echb{margin-top:12px;border:1.5px solid #e9c98a;background:#fff8e6;border-radius:10px;padding:8px 12px;page-break-inside:avoid}
.echb .er{display:grid;grid-template-columns:30% 25% 45%;gap:6px;padding:4px 0;border-top:1px dashed #ecd7a8}
.echb small{color:#6b4a1a}.echb i{font-style:normal;color:#0f5c55}.echb .et{margin-top:6px;color:#6b4a1a}
.ech{color:#a8431a;font-size:.72em;vertical-align:super;line-height:0;margin-left:1px}
.part{page-break-before:always}
.sec{border-bottom:2px solid #d4a23c;padding-bottom:4px;margin-bottom:10px}.sec small{font-size:10pt;color:#8a6a3a}
.sp{color:#a8431a;font-weight:600;margin:10px 0 2px 44px}
.it,.mh{display:flex;gap:12px;padding:8px 0;border-bottom:1px solid #f0e2c4;page-break-inside:avoid}
.no{flex:0 0 30px;height:30px;border-radius:50%;background:#7a1f1f;color:#fff;font-weight:600;font-size:10pt;display:flex;align-items:center;justify-content:center;margin-top:2px}
.no.nb{background:none}
.bd{flex:1}
.vt{font-size:13.5pt;line-height:1.55}.vt.te{font-size:12.5pt}.vt.enb{font-size:11.5pt}.vt.sm{font-size:10.5pt;color:#4a3420;margin-top:3px}
.ra{margin-top:4px;color:#0f5c55;font-weight:600;font-size:10.5pt}
.ra .lab{display:block;font-weight:400;font-size:8pt;color:#8a6a3a;letter-spacing:.04em;text-transform:uppercase}
.ra .dl{line-height:1.9}
.ra .dl .fw{display:inline-block;border-bottom:1.3px solid rgba(15,92,85,.45);line-height:1.3;margin:0 .14em .12em 0;padding:0 1px}
.ra .dl .fwm{color:#8a6a3a;font-weight:400}
.te .dl,.ra .dl{font-family:Ui,Tel,Deva,sans-serif}
.tip{margin-top:4px;font-size:9pt;color:#5a4630;background:#fbf4e4;border-radius:6px;padding:3px 7px}
.rf .vt{color:#6b4a1a;font-size:12pt}
.mv{padding:8px 0 10px;border-bottom:1.5px solid #e9c98a;page-break-inside:avoid}
.mv .mh{border:0;padding-bottom:2px}
.mm{margin:4px 0 6px 42px}
.mm b,.bn b{color:#7a1f1f}
.nm{margin-left:42px;width:calc(100% - 42px);border-collapse:collapse;font-size:9.5pt}
.nm th{text-align:left;color:#7a1f1f;font-weight:600;padding:2px 0}
.nm td{padding:2px 6px 2px 0;border-top:1px solid #f3e7cc;vertical-align:top}
.nm td:first-child{width:28%;font-size:10.5pt}.nm td.pr{width:27%;color:#0f5c55}
.bn{margin:6px 0 0 42px;font-size:9.5pt;background:#f2f8ef;border-radius:6px;padding:3px 8px}
"""

FOOT = ('<div style="width:100%;font-size:7.5pt;color:#8a6a3a;text-align:center;font-family:sans-serif">'
        'Sahasranama Guru · %s · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')


def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    h.func.log_message = lambda *a: None
    s = socketserver.TCPServer(('127.0.0.1', 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def main():
    srv = serve()
    port = srv.server_address[1]
    css = CSS.replace('%(f)s', FONTS.as_uri())
    tmp = pathlib.Path('/tmp/sg_pdf')
    tmp.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        app = b.new_page()
        app.route('**/*', lambda r: r.continue_() if r.request.url.startswith('http://127.0.0.1') else r.abort())
        app.goto('http://127.0.0.1:%d/index-dev.html' % port)
        app.wait_for_timeout(1500)
        app.add_script_tag(path=str(ROOT / 'tools' / 'pdf_build.js'))
        doc = b.new_page()
        for stem, kind, lang, title in DOCS:
            if ONLY and ONLY not in stem:
                continue
            for echo in (1, 0):
                body = app.evaluate('([k,l,e])=>PDFB(k,l,e)', [kind, lang, echo])
                html = ('<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s</body></html>'
                        % ({'te': 'te', 'hi': 'hi', 'sa': 'sa'}.get(lang, 'en'), title, css, body))
                f = tmp / (stem + '.html')
                f.write_text(html, encoding='utf-8')
                doc.goto(f.as_uri())
                doc.wait_for_timeout(300)
                name = stem + ('' if echo else '-noecho') + '.pdf'
                doc.pdf(path=str(OUT / name), format='A4', print_background=True, display_header_footer=True,
                        header_template='<div></div>', footer_template=FOOT.replace('%s', title),
                        margin={'top': '16mm', 'bottom': '18mm', 'left': '15mm', 'right': '15mm'})
                print(name, (OUT / name).stat().st_size // 1024, 'KB')
        b.close()
    srv.shutdown()


if __name__ == '__main__':
    main()
