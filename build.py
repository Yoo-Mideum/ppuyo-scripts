# -*- coding: utf-8 -*-
"""scripts/*.md + episodes.json → 루트 index.html + epNN/index.html (self-contained)"""
import json, re, html, datetime as dt, pathlib

ROOT = pathlib.Path(__file__).parent
D = json.load(open(ROOT/'episodes.json', encoding='utf-8'))
R = D['rule']
W = '일월화수목금토'

def fmt(d): return f"{d:%Y-%m-%d}"
def fmtw(d): return f"{d:%Y-%m-%d} ({W[(d.weekday()+1)%7]})"
def date(s): return dt.date.fromisoformat(s)
def add(s, n): return date(s) + dt.timedelta(days=n)

# 뿌요 팔레트 — 샴페인 → 골드 → 앰버 → 브론즈, 채도 낮은 웜톤 4단계
CSS = """
:root{
  --g1:#F1E3B0;--g2:#E2C35C;--g3:#C9A227;--g4:#8A6D12;
  --grad:linear-gradient(90deg,var(--g1),var(--g2),var(--g3),var(--g4));
  --bg:#FBFAF6;--card:#FFFFFF;--tile:#F4F1E8;--ink:#1F1E1A;--mut:#77726A;--line:#E9E4D8;
  --acc:#C9A227;--acc-ink:#8A6D12;--acc-soft:#F6ECC4;--sec:#6B7F5A;--sec-soft:#E8EEE2;
  --screen-bg:#EEF2EC;--screen-ink:#4F6544;--quote-bg:#F9F3DF;--quote-ink:#6E5A16
}
@media(prefers-color-scheme:dark){:root{
  --bg:#121210;--card:#1A1916;--tile:#242219;--ink:#EEE9DC;--mut:#928B7E;--line:#2C2A22;
  --acc:#D9B33A;--acc-ink:#E8C95C;--acc-soft:#3A3116;--sec:#9DB08A;--sec-soft:#26301F;
  --screen-bg:#1F2620;--screen-ink:#A9C29A;--quote-bg:#27231A;--quote-ink:#DCC479
}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Gowun Dodum','Noto Sans KR',system-ui,sans-serif;line-height:1.7;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:600px;margin:0 auto;padding:26px 18px 80px}
.topline{height:2px;background:var(--grad);opacity:.8;border-radius:999px;margin-bottom:22px}
.head{display:flex;justify-content:space-between;font-size:12.5px;color:var(--mut);letter-spacing:.04em}
h1{font-size:27px;margin:8px 0 8px;line-height:1.3;color:var(--ink);font-weight:400}
.sub{font-size:14px;color:var(--mut);margin:0 0 24px}
.sub b{color:var(--ink);font-weight:400}
h2{font-size:17px;margin:30px 0 10px;font-weight:400}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px 18px 18px;margin:0 0 16px}
.chips{display:flex;gap:8px;align-items:center;margin-bottom:10px}
.badge{display:inline-block;padding:3px 12px;border-radius:999px;font-size:12px}
.s0{background:var(--tile);color:var(--mut)}
.s1{background:var(--acc-soft);color:var(--acc-ink)}
.s2{background:var(--acc);color:#1A1612}
.s3{background:var(--g4);color:#fff}
.s4{background:var(--ink);color:var(--bg)}
.n{display:inline-block;padding:3px 10px;border-radius:999px;font-size:12px;background:var(--tile);color:var(--mut)}
.card .t{font-size:19px;line-height:1.45;color:var(--acc-ink);margin:0 0 8px}
.card .hook{font-size:14px;color:var(--mut);margin:0 0 14px;line-height:1.6}
.dates{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px}
.tile{background:var(--tile);border-radius:12px;padding:10px 12px}
.tile .k{font-size:11.5px;color:var(--mut)} .tile .v{font-size:14.5px;font-variant-numeric:tabular-nums;margin-top:2px}
.tile .w{font-size:11px;color:var(--mut)}
.btns{display:flex;gap:8px;flex-wrap:wrap}
.btn{display:inline-block;padding:9px 16px;border-radius:999px;border:1px solid var(--acc);color:var(--acc-ink);font-size:14px;text-decoration:none;background:transparent;font-family:inherit;cursor:pointer}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#1A1612}
.btn:disabled{opacity:.4;cursor:default}
.vlink{font-size:13px;color:var(--mut);margin-top:10px;word-break:break-all}
.vlink a{color:var(--acc-ink)}
.memo{font-size:12.5px;color:var(--mut);margin-top:10px}
.hero{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px 18px;margin-bottom:18px;display:flex;gap:16px;align-items:center}
.hero .big{font-size:30px;color:var(--acc-ink);white-space:nowrap;font-variant-numeric:tabular-nums}
.hero .s{font-size:13.5px;color:var(--mut);line-height:1.5} .hero .s b{font-weight:400;color:var(--ink)}
.guide{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px 16px 14px 32px;font-size:14px;margin:0}
.guide li{margin:6px 0} .guide b{font-weight:400;color:var(--acc-ink)}
code{background:var(--tile);padding:1px 6px;border-radius:6px;font-size:12.5px}
footer{text-align:center;color:var(--mut);font-size:12px;margin-top:36px}
.sec-h{display:flex;align-items:center;gap:10px;margin:28px 0 12px;font-size:13px;color:var(--mut);letter-spacing:.06em}
.sec-h:after{content:"";flex:1;height:1px;background:var(--line)}
.sec-h b{font-weight:400;color:var(--ink);font-size:15px}
.s1{background:var(--acc-soft);color:var(--acc-ink)}
.s0{background:var(--sec-soft);color:var(--sec)}
.card.plan{border-style:dashed;background:transparent}
.card.plan .t{color:var(--ink)}
details.done{border:1px solid var(--line);border-radius:18px;background:var(--card);margin-top:8px}
details.done summary{list-style:none;cursor:pointer;padding:16px 18px;display:flex;justify-content:space-between;align-items:center;font-size:15px}
details.done summary::-webkit-details-marker{display:none}
details.done summary .cnt{font-size:12px;color:var(--mut)}
details.done summary:after{content:"＋";color:var(--mut);margin-left:10px}
details.done[open] summary:after{content:"－"}
.done-list{list-style:none;margin:0;padding:0 18px 10px;border-top:1px solid var(--line)}
.done-list li{display:flex;gap:12px;align-items:baseline;padding:10px 0;border-bottom:1px solid var(--line);font-size:14px}
.done-list li:last-child{border-bottom:0}
.done-list .n{flex:0 0 auto}
.done-list a{text-decoration:none;flex:1}
.done-list .d{font-size:12px;color:var(--mut);white-space:nowrap}
.gbox{border:1.5px solid var(--acc);border-radius:18px;padding:18px 18px 14px;margin-top:8px;position:relative}
.gbox .gt{position:absolute;top:-11px;left:16px;background:var(--bg);padding:0 8px;font-size:12.5px;color:var(--acc-ink);letter-spacing:.06em}
.gbox ul{margin:0;padding:0 0 0 18px;font-size:14px}
.gbox li{margin:7px 0} .gbox li b{font-weight:400;color:var(--acc-ink)}
.gbox .tlink{display:inline-block;margin-top:10px;font-size:13.5px;color:var(--acc-ink);text-decoration:none;border-bottom:1px solid var(--acc)}
.back{font-size:13px;color:var(--mut);text-decoration:none;display:inline-block;margin-bottom:10px}
.meta{display:flex;gap:12px;flex-wrap:wrap;font-size:13px;color:var(--mut);margin:6px 0 14px} .meta b{color:var(--ink);font-weight:400}
.tools{display:flex;gap:8px;margin-bottom:18px}
.tools .btn{flex:1;text-align:center}
.toc{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px}
.toc a{font-size:12.5px;text-decoration:none;color:var(--mut);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:4px 10px}
.toc a b{color:var(--acc-ink);margin-right:4px;font-variant-numeric:tabular-nums;font-weight:400}
article{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px 20px;font-size:16.5px;line-height:1.9}
article h2{font-size:18px;margin:34px 0 12px;padding-top:18px;border-top:1px solid var(--line);scroll-margin-top:14px}
article h2:first-child{border-top:0;margin-top:0;padding-top:0}
.time{display:inline-block;background:var(--acc-soft);color:var(--acc-ink);font-size:11.5px;padding:1px 8px;border-radius:6px;margin-right:8px;vertical-align:middle;font-variant-numeric:tabular-nums}
article p{margin:0 0 13px}
.note{margin:0 0 18px;padding:9px 14px;border-left:2px solid var(--acc);background:var(--quote-bg);color:var(--quote-ink);font-size:13.5px;border-radius:0 10px 10px 0}
.screen{display:flex;gap:9px;align-items:flex-start;background:var(--screen-bg);color:var(--screen-ink);border-radius:10px;padding:8px 12px;font-size:13.5px;margin:4px 0 16px;line-height:1.5}
.screen span{flex:0 0 auto;border:1px solid var(--screen-ink);color:var(--screen-ink);font-size:10.5px;padding:0 6px;border-radius:5px;margin-top:3px}
mark{background:var(--acc-soft);color:var(--ink);padding:0 4px;border-radius:4px}
figure{margin:6px 0 20px} figure img{width:100%;border-radius:12px;display:block} figcaption{font-size:12px;color:var(--mut);margin-top:6px;text-align:center}
.src{font-size:12px;color:var(--mut);margin-top:22px;padding-top:12px;border-top:1px dashed var(--line)} .src a{word-break:break-all;color:var(--acc-ink)}
.pr{position:fixed;inset:0;background:#000;color:#fff;z-index:50;display:none;flex-direction:column}
.pr.on{display:flex}
.pbar{display:flex;gap:12px;align-items:center;padding:10px 14px;background:#111;font-size:12.5px;color:#aaa;flex-wrap:wrap}
.pbar button{background:#333;color:#fff;border:0;padding:7px 12px;border-radius:8px;font-family:inherit}
.pbar input{width:90px;vertical-align:middle}
.ptext{flex:1;overflow:auto;padding:40vh 7% 60vh;font-size:38px;line-height:1.7;font-weight:600}
.ptext p{margin:0 0 .9em}.ptext h3{color:#D2AA6C;font-size:.55em;margin:1.6em 0 .6em}.ptext .ps{font-size:.45em;color:#A9C2B8;font-weight:400;margin:0 0 1em}
@media print{.tools,.toc,.back,.pr,.topline{display:none!important}article{border:0;padding:0;font-size:14px}}
"""
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">'
HEAD = lambda title: f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>{FONT}<style>{CSS}</style></head><body>'

STATUS = {'시작 전':0,'대본 작성 중':1,'대본 완료':2,'촬영 완료':3,'공개 완료':4}
def badge(s): return f'<span class="badge s{STATUS.get(s,0)}">{html.escape(s)}</span>'

def inline(s):
    s = html.escape(s)
    s = re.sub(r'【([^】]*)】', r'<mark>【\1】</mark>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s

def render(md):
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

HUB_JS = """
// 영상 링크: 이 브라우저에만 저장(localStorage). episodes.json의 video 값이 있으면 그걸 우선.
const K='ppuyo_video_links';let S={};try{S=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
document.querySelectorAll('[data-ep]').forEach(c=>{
  const n=c.dataset.ep, box=c.querySelector('.vlink'), btn=c.querySelector('.reg');
  const show=u=>{box.innerHTML=u?`영상: <a href="${u}" target="_blank" rel="noopener">${u}</a>`:''};
  show(c.dataset.video||S[n]||'');
  if(btn)btn.onclick=()=>{const u=prompt(n+'화 영상 링크를 붙여넣으세요 (비우면 삭제)',S[n]||c.dataset.video||'');
    if(u===null)return; if(u.trim()){S[n]=u.trim()}else{delete S[n]}
    try{localStorage.setItem(K,JSON.stringify(S))}catch(e){} show(S[n]||c.dataset.video||'')};
});
"""

today = dt.date.today()

# ---- episode pages ----
for e in D['episodes']:
    if not e.get('file'): continue
    md = open(ROOT/e['file'], encoding='utf-8').read()
    art, toc, pr, syl = render(md)
    mins = syl / R['syllablesPerMin']
    shoot, pub = add(e['given'], R['shootOffset']), add(e['given'], R['publishOffset'])
    srcs = ''.join(f'<div>· <a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a></div>' for t, u in e.get('sources', []))
    src_html = f'<div class="src"><b>참고·출처</b> (촬영일 기준 재확인){srcs}</div>' if srcs else ''
    page = HEAD(f"{e['n']}화 · {e['title']}") + f"""
<div class="wrap">
<div class="topline"></div>
<a class="back" href="../">← 대본 보드</a>
<div class="head"><span>뿌요 · {e['n']}화</span><span>{html.escape(e['status'])}</span></div>
<h1>{html.escape(e['title'])}</h1>
<div class="meta"><span>음절 <b>{syl:,}</b></span><span>예상 <b>{mins:.1f}분</b></span><span>제공 {fmtw(date(e['given']))}</span><span>촬영 {fmtw(shoot)}</span><span>공개 {fmtw(pub)}</span></div>
<div class="tools"><button class="btn primary" id="tp">텔레프롬프터</button><button class="btn" onclick="window.print()">인쇄</button></div>
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


# ---- topics page ----
T = json.load(open(ROOT/'topics.json', encoding='utf-8'))
done = {e['n'] for e in D['episodes'] if e.get('file')}
planned = {e['n']: e for e in D['episodes'] if not e.get('file')}
sections = []
for ph in T['phases']:
    items = []
    for it in ph['items']:
        n = it['n']
        tag = '<span class="badge s2">대본 완료</span>' if n in done else ('<span class="badge s1">다음 회차</span>' if n in planned else '')
        items.append(f"""<div class="card">
<div class="chips"><span class="n">{n}화 후보</span>{tag}</div>
<div class="t">{html.escape(it['title'])}</div>
<p class="hook">“{html.escape(it['hook'])}”</p>
<div class="memo">{html.escape(it['note'])}</div>
</div>""")
    sections.append(f"<h2>{html.escape(ph['name'])}</h2>" + ''.join(items))
extra = ''.join(f'<li>{html.escape(x)}</li>' for x in T.get('extra', []))
topics_page = HEAD('뿌요 · 이후 대본 주제') + f"""
<div class="wrap">
<div class="topline"></div>
<a class="back" href="../">← 대본 보드</a>
<div class="head"><span>뿌요 유튜브</span><span>이후 대본 주제 후보</span></div>
<h1>이후 대본 주제 20</h1>
<p class="sub">{html.escape(T['intro'])}</p>
{''.join(sections)}
<h2>번외 후보</h2>
<ul class="guide">{extra}</ul>
<footer>뿌요 짠테크 유튜브 · 대본 보드</footer>
</div></body></html>"""
(ROOT/'topics').mkdir(exist_ok=True)
(ROOT/'topics'/'index.html').write_text(topics_page, encoding='utf-8')

# ---- hub ----
def tile(k, d): return f'<div class="tile"><div class="k">{k}</div><div class="v">{fmt(d)}</div><div class="w">{W[(d.weekday()+1)%7]}요일</div></div>'
def card(e, plan=False):
    g = e.get('given'); n = e['n']
    shoot = add(g, R['shootOffset']) if g else None
    pub = add(g, R['publishOffset']) if g else None
    has = bool(e.get('file'))
    chips = f'<span class="n">{n}화</span>' + (badge(e['status']) if not plan else '<span class="badge s0">예정</span>')
    hook = f'<p class="hook">“{html.escape(e["hook"])}”</p>' if e.get('hook') else ''
    dates = f'<div class="dates">{tile("제공", date(g))}{tile("촬영", shoot)}{tile("공개", pub)}</div>' if g else ''
    extra = f' · {e["_syl"]:,}음절 · {e["_min"]:.1f}분' if '_syl' in e else ''
    open_btn = f'<a class="btn primary" href="ep{n:02d}/">대본 열기</a>' if has else '<button class="btn" disabled>대본 준비 중</button>'
    memo = f'<div class="memo">{html.escape(e.get("memo",""))}{extra}</div>' if e.get('memo') or extra else ''
    video = html.escape(e.get('video', ''))
    cls = ' plan' if plan else ''
    return (f'<div class="card{cls}" data-ep="{n}" data-video="{video}">'
            f'<div class="chips">{chips}</div><div class="t">{html.escape(e["title"])}</div>{hook}{dates}'
            f'<div class="btns">{open_btn}<button class="btn reg">영상 링크 등록</button></div>'
            f'<div class="vlink"></div>{memo}</div>')

todo = [e for e in D['episodes'] if e['status'] in ('대본 작성 중','대본 완료','촬영 완료')]
plan = [e for e in D['episodes'] if e['status'] == '시작 전']
done = [e for e in D['episodes'] if e['status'] == '공개 완료']
todo.sort(key=lambda e: e.get('given','')); plan.sort(key=lambda e: e.get('given','')); done.sort(key=lambda e: e.get('given',''), reverse=True)

nxt = None
for e in todo:
    if e.get('given'):
        pub = add(e['given'], R['publishOffset'])
        if pub >= today: nxt = (e, add(e['given'], R['shootOffset']), pub); break
hero = ''
if nxt:
    e, shoot, pub = nxt; dd = (pub - today).days
    hero = f'<div class="hero"><div class="big">D-{dd}</div><div class="s"><b>{e["n"]}화 공개 {fmtw(pub)}</b><br>촬영 {fmtw(shoot)} · {html.escape(e["status"])}</div></div>'

todo_html = ''.join(card(e) for e in todo) or '<div class="card plan"><div class="memo">진행 중인 회차가 없습니다.</div></div>'
plan_html = ''.join(card(e, plan=True) for e in plan)
done_items = ''.join(
    f'<li><span class="n">{e["n"]}화</span><a href="ep{e["n"]:02d}/">{html.escape(e["title"])}</a><span class="d">공개 {fmt(add(e["given"], R["publishOffset"]))}</span></li>'
    for e in done)
done_html = (f'<details class="done"><summary><span>공개 완료</span><span class="cnt">{len(done)}편</span></summary>'
             f'<ul class="done-list">{done_items}</ul></details>') if done else ''
plan_sec = '<div class="sec-h"><b>예정</b><span>다음 회차</span></div>' + plan_html if plan_html else ''
done_sec = '<div class="sec-h"><b>완료</b><span>공개됨</span></div>' + done_html if done_html else ''

hub = HEAD('뿌요 대본 보드') + f"""
<div class="wrap">
<div class="topline"></div>
<div class="head"><span>뿌요 유튜브</span><span>롱폼 대본 · 일정</span></div>
<h1>뿌요 짠테크 대본</h1>
<p class="sub">대본 제공 <b>수요일</b> → 촬영 <b>금요일</b> → 공개 <b>다음주 토요일</b>. 각 회차 카드에서 대본을 열고, 공개 후 “영상 링크 등록”으로 링크를 남겨주세요.</p>
{hero}
<div class="sec-h"><b>해야 할 것</b><span>진행 중</span></div>
{todo_html}
{plan_sec}
{done_sec}
<div class="sec-h"><b>가이드라인</b></div>
<div class="gbox"><div class="gt">뿌요 대본 규칙</div>
<ul>
<li><b>톤</b> — 전문가 톤. 감탄사·'여러분'·'~잖아요' 금지. 짧은 단정형.</li>
<li><b>훅</b> — 숫자 + 반전 + 약속, 15초 안에. 오픈 루프는 3~4분 지점까지 닫지 않기.</li>
<li><b>신뢰</b> — 매 회차 '이건 안 됩니다' 솔직 구간 1개. 구독 CTA는 마지막 한 번.</li>
<li><b>길이</b> — 10분 ≈ 3,000음절(분당 {R['syllablesPerMin']}). 각 회차 페이지 상단에 자동 계산.</li>
<li><b>영상 링크</b> — 버튼으로 등록한 링크는 이 기기 브라우저에만 저장. 모두에게 보이려면 <code>episodes.json</code>의 <code>video</code>에 넣고 push.</li>
</ul>
<a class="tlink" href="topics/">이후 대본 주제 20 보기 →</a>
</div>
<footer>뿌요 짠테크 유튜브 · 대본 보드</footer>
</div>
<script>{HUB_JS}</script>
</body></html>"""
(ROOT/'index.html').write_text(hub, encoding='utf-8')
print('built', [f"ep{e['n']:02d}" for e in D['episodes'] if e.get('file')])
