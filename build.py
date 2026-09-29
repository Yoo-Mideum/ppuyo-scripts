# -*- coding: utf-8 -*-
"""scripts/*.md + episodes.json → 루트 index.html + epNN/index.html (self-contained)"""
import json, re, html, datetime as dt, pathlib

ROOT = pathlib.Path(__file__).parent
D = json.load(open(ROOT/'episodes.json', encoding='utf-8'))
R = D['rule']
W = '일월화수목금토'

def fmt(d): return f"{d:%Y-%m-%d} ({W[(d.weekday()+1)%7]})"
def date(s): return dt.date.fromisoformat(s)
def add(s, n): return date(s) + dt.timedelta(days=n)

CSS = """
:root{--bg:#FAF7F2;--card:#fff;--ink:#1F2933;--mut:#6B7280;--line:#E7E1D8;--acc:#D97706;--acc-soft:#FDE68A;--screen-bg:#EEF2FF;--screen-ink:#3730A3;--quote-bg:#FFFBEB;--quote-ink:#78350F}
@media(prefers-color-scheme:dark){:root{--bg:#0F1216;--card:#171B21;--ink:#F3F4F6;--mut:#9CA3AF;--line:#2A3039;--acc:#F59E0B;--acc-soft:#7C5A0B;--screen-bg:#1E2540;--screen-ink:#A5B4FC;--quote-bg:#2A2410;--quote-ink:#FDE68A}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Gowun Dodum','Noto Sans KR',system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:600px;margin:0 auto;padding:28px 18px 80px}
.eyebrow{font-size:12px;color:var(--mut);letter-spacing:.08em}
h1{font-size:24px;margin:4px 0 6px;line-height:1.35}
.sub{font-size:14px;color:var(--mut);margin:0 0 22px}
.sub b{color:var(--ink)}
h2{font-size:17px;margin:30px 0 10px}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 18px;margin:0 0 12px;text-decoration:none}
.card.hero{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.card .k{font-size:12px;color:var(--mut)} .card.hero .k{opacity:.7;color:inherit}
.card .v{font-size:22px;font-weight:700;margin:2px 0}
.card .s{font-size:13px;color:var(--mut)} .card.hero .s{opacity:.8;color:inherit}
.ep{display:flex;gap:14px;align-items:flex-start}
.ep .n{flex:0 0 44px;height:44px;border-radius:12px;background:var(--acc-soft);color:var(--ink);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px}
.ep .t{font-weight:700;font-size:15px;line-height:1.45}
.ep .d{font-size:12.5px;color:var(--mut);margin-top:4px;line-height:1.6}
.ep .d span{white-space:nowrap;margin-right:10px}
.badge{display:inline-block;padding:1px 9px;border-radius:999px;font-size:11.5px;font-weight:600;margin-top:6px}
.s0{background:var(--line);color:var(--mut)}.s1{background:#FEF3C7;color:#92400E}.s2{background:#DCFCE7;color:#166534}.s3{background:#DBEAFE;color:#1E40AF}.s4{background:var(--ink);color:var(--bg)}
.guide{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 16px 14px 32px;font-size:14px;margin:0}
.guide li{margin:6px 0}
code{background:var(--line);padding:1px 6px;border-radius:6px;font-size:12.5px}
footer{text-align:center;color:var(--mut);font-size:12px;margin-top:36px}
/* episode */
.back{font-size:13px;color:var(--mut);text-decoration:none;display:inline-block;margin-bottom:10px}
.meta{display:flex;gap:12px;flex-wrap:wrap;font-size:13px;color:var(--mut);margin:6px 0 16px} .meta b{color:var(--ink)}
.tools{display:flex;gap:8px;margin-bottom:18px}
.tools button{flex:1;background:var(--ink);color:var(--bg);border:0;border-radius:12px;padding:12px;font-size:14px;font-family:inherit;cursor:pointer}
.toc{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px}
.toc a{font-size:12.5px;text-decoration:none;color:var(--mut);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:4px 10px}
.toc a b{color:var(--acc);margin-right:4px;font-variant-numeric:tabular-nums}
article{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 20px;font-size:16.5px;line-height:1.9}
article h2{font-size:18px;margin:34px 0 12px;padding-top:18px;border-top:1px solid var(--line);scroll-margin-top:14px}
article h2:first-child{border-top:0;margin-top:0;padding-top:0}
.time{display:inline-block;background:var(--ink);color:var(--bg);font-size:11.5px;padding:1px 8px;border-radius:6px;margin-right:8px;vertical-align:middle;font-variant-numeric:tabular-nums}
article p{margin:0 0 13px}
.note{margin:0 0 18px;padding:9px 14px;border-left:3px solid var(--acc);background:var(--quote-bg);color:var(--quote-ink);font-size:13.5px;border-radius:0 10px 10px 0}
.screen{display:flex;gap:9px;align-items:flex-start;background:var(--screen-bg);color:var(--screen-ink);border-radius:10px;padding:8px 12px;font-size:13.5px;margin:4px 0 16px;line-height:1.5}
.screen span{flex:0 0 auto;background:var(--screen-ink);color:var(--screen-bg);font-size:10.5px;padding:1px 6px;border-radius:5px;margin-top:3px}
mark{background:var(--acc-soft);color:var(--ink);padding:0 4px;border-radius:4px}
figure{margin:6px 0 20px} figure img{width:100%;border-radius:12px;display:block} figcaption{font-size:12px;color:var(--mut);margin-top:6px;text-align:center}
.src{font-size:12px;color:var(--mut);margin-top:22px;padding-top:12px;border-top:1px dashed var(--line)} .src a{word-break:break-all}
/* prompter */
.pr{position:fixed;inset:0;background:#000;color:#fff;z-index:50;display:none;flex-direction:column}
.pr.on{display:flex}
.pbar{display:flex;gap:12px;align-items:center;padding:10px 14px;background:#111;font-size:12.5px;color:#aaa;flex-wrap:wrap}
.pbar button{background:#333;color:#fff;border:0;padding:7px 12px;border-radius:8px;font-family:inherit}
.pbar input{width:90px;vertical-align:middle}
.ptext{flex:1;overflow:auto;padding:40vh 7% 60vh;font-size:38px;line-height:1.7;font-weight:600}
.ptext p{margin:0 0 .9em}.ptext h3{color:#F59E0B;font-size:.55em;margin:1.6em 0 .6em}.ptext .ps{font-size:.45em;color:#818CF8;font-weight:400;margin:0 0 1em}
@media print{.tools,.toc,.back,.pr{display:none!important}article{border:0;padding:0;font-size:14px}}
"""
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">'
HEAD = lambda title: f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>{FONT}<style>{CSS}</style></head><body>'

def badge(s):
    i = {'시작 전':0,'대본 작성 중':1,'대본 완료':2,'촬영 완료':3,'공개 완료':4}.get(s,0)
    return f'<span class="badge s{i}">{html.escape(s)}</span>'

def inline(s):
    s = html.escape(s)
    s = re.sub(r'【([^】]*)】', r'<mark>【\1】</mark>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s

def render(md, ep):
    """md → (article html, toc list, prompter html, syllables)"""
    art, toc, pr, syl = [], [], [], 0
    for line in md.split('\n'):
        s = line.strip()
        if not s or s == '---' or s.startswith('# '): continue
        m = re.match(r'^## (\S+)\s+(.*)$', s)
        if m:
            t, name = m.groups(); i = 't' + t.replace(':', '-')
            art.append(f'<h2 id="{i}"><span class="time">{t}</span>{html.escape(name)}</h2>')
            toc.append(f'<a href="#{i}"><b>{t}</b>{html.escape(name)}</a>')
            pr.append(f'<h3>{t} · {html.escape(name)}</h3>'); continue
        if s.startswith('>'):
            art.append(f'<div class="note">{inline(s[1:].strip())}</div>'); continue
        if s.startswith('[화면:'):
            v = re.sub(r'^\[화면:\s*', '', s)[:-1]
            art.append(f'<div class="screen"><span>화면</span>{inline(v)}</div>')
            pr.append(f'<div class="ps">{html.escape(v)}</div>'); continue
        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', s)
        if m:
            alt, src = m.groups()
            art.append(f'<figure><img src="../{src}" alt="{html.escape(alt)}"><figcaption>{html.escape(alt)}</figcaption></figure>'); continue
        art.append(f'<p>{inline(s)}</p>'); pr.append(f'<p>{html.escape(s)}</p>')
        syl += len(s.replace(' ', ''))
    return '\n'.join(art), '\n'.join(toc), '\n'.join(pr), syl

PROMPTER_JS = """
const P=document.getElementById('pr'),T=document.getElementById('pt');let sp=2,run=false,raf;
const tick=()=>{if(run)T.scrollTop+=sp/2;raf=requestAnimationFrame(tick)};
document.getElementById('tp').onclick=()=>{P.classList.add('on');T.scrollTop=0;run=false;cancelAnimationFrame(raf);tick()};
document.getElementById('pc').onclick=()=>{P.classList.remove('on');run=false;cancelAnimationFrame(raf)};
document.getElementById('pp').onclick=()=>run=!run;
document.getElementById('sp').oninput=e=>sp=+e.target.value;
document.getElementById('sz').oninput=e=>T.style.fontSize=e.target.value+'px';
document.addEventListener('keydown',e=>{if(!P.classList.contains('on'))return;
 if(e.code==='Space'){e.preventDefault();run=!run}
 if(e.code==='ArrowUp'){sp=Math.min(8,sp+.5);document.getElementById('sp').value=sp}
 if(e.code==='ArrowDown'){sp=Math.max(0,sp-.5);document.getElementById('sp').value=sp}
 if(e.code==='Escape')document.getElementById('pc').click()});
"""

# ---- episode pages ----
today = dt.date.today()
for e in D['episodes']:
    if not e.get('file'): continue
    md = open(ROOT/e['file'], encoding='utf-8').read()
    art, toc, pr, syl = render(md, e)
    mins = syl / R['syllablesPerMin']
    shoot, pub = add(e['given'], R['shootOffset']), add(e['given'], R['publishOffset'])
    srcs = ''.join(f'<div>· <a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a></div>' for t, u in e.get('sources', []))
    src_html = f'<div class="src"><b>참고·출처</b> (촬영일 기준 재확인){srcs}</div>' if srcs else ''
    page = HEAD(f"{e['n']}화 · {e['title']}") + f"""
<div class="wrap">
<a class="back" href="../">← 대본 보드</a>
<div class="eyebrow">뿌요 · {e['n']}화</div>
<h1>{html.escape(e['title'])}</h1>
<div class="meta"><span>음절 <b>{syl:,}</b></span><span>예상 <b>{mins:.1f}분</b></span><span>{badge(e['status'])}</span></div>
<div class="meta"><span>제공 {fmt(date(e['given']))}</span><span>촬영 {fmt(shoot)}</span><span>공개 {fmt(pub)}</span></div>
<div class="tools"><button id="tp">텔레프롬프터</button><button onclick="window.print()">인쇄</button></div>
<div class="toc">{toc}</div>
<article>{art}{src_html}</article>
<footer>뿌요 짠테크 유튜브 · 대본 보드</footer>
</div>
<div class="pr" id="pr"><div class="pbar"><button id="pc">닫기</button><button id="pp">▶ / ❚❚</button><label>속도 <input id="sp" type="range" min="0" max="8" step=".5" value="2"></label><label>글자 <input id="sz" type="range" min="24" max="64" step="2" value="38"></label></div><div class="ptext" id="pt">{pr}</div></div>
<script>{PROMPTER_JS}</script>
</body></html>"""
    out = ROOT / f"ep{e['n']:02d}" / 'index.html'; out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding='utf-8')
    e['_syl'], e['_min'] = syl, mins

# ---- hub ----
nxt = None; cards = []
for e in D['episodes']:
    g = e.get('given')
    shoot = add(g, R['shootOffset']) if g else None
    pub = add(g, R['publishOffset']) if g else None
    if not nxt and pub and pub >= today: nxt = (e, shoot, pub)
    href = f"ep{e['n']:02d}/" if e.get('file') else None
    dates = f"<span>제공 {fmt(date(g))}</span><span>촬영 {fmt(shoot)}</span><span>공개 {fmt(pub)}</span>" if g else ''
    extra = f"<span>{e['_syl']:,}음절 · {e['_min']:.1f}분</span>" if '_syl' in e else ''
    hook = f'<div class="d" style="margin-top:6px;font-style:italic">“{html.escape(e["hook"])}”</div>' if e.get('hook') else ''
    body = f'<div class="ep"><div class="n">{e["n"]}</div><div><div class="t">{html.escape(e["title"])}</div><div class="d">{dates}{extra}</div>{hook}{badge(e["status"])}</div></div>'
    cards.append(f'<a class="card" href="{href}">{body}</a>' if href else f'<div class="card">{body}</div>')
hero = ''
if nxt:
    e, shoot, pub = nxt; dd = (pub - today).days
    hero = f'<div class="card hero"><div class="k">다음 공개</div><div class="v">{e["n"]}화 · D-{dd}</div><div class="s">{fmt(pub)} 공개 · 촬영 {fmt(shoot)} · {html.escape(e["status"])}</div></div>'
hub = HEAD('뿌요 대본 보드') + f"""
<div class="wrap">
<div class="eyebrow">YOUTUBE 롱폼 · 대본 보드</div>
<h1>{html.escape(D['channel'])}</h1>
<p class="sub">대본 <b>수요일</b> 제공 → 촬영 <b>+{R['shootOffset']}일</b> (금) → 공개 <b>+{R['publishOffset']}일</b> (다음주 토)</p>
{hero}
<h2>회차</h2>
{''.join(cards)}
<h2>가이드</h2>
<ul class="guide">
<li><b>톤</b> — 전문가 톤. 감탄사·'여러분'·'~잖아요' 금지. 짧은 단정형.</li>
<li><b>훅</b> — 숫자 + 반전 + 약속, 15초 안에. 오픈 루프는 3~4분 지점까지 닫지 않기.</li>
<li><b>신뢰</b> — 매 회차 '이건 안 됩니다' 솔직 구간 1개. 구독 CTA는 마지막 한 번.</li>
<li><b>길이</b> — 10분 ≈ 3,000음절(분당 {R['syllablesPerMin']}). 각 회차 페이지 상단에 자동 계산.</li>
<li><b>추가</b> — <code>scripts/NN_제목.md</code> + <code>episodes.json</code> 항목 → <code>python build.py</code> → push.</li>
</ul>
<footer>뿌요 짠테크 유튜브 · 대본 보드</footer>
</div></body></html>"""
(ROOT/'index.html').write_text(hub, encoding='utf-8')
print('built', [f"ep{e['n']:02d}" for e in D['episodes'] if e.get('file')])
