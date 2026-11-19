# Storyboard PDF for client approval + voice-over texts in .md, one file per language.
# usage: python3 storyboard_pdf.py storyboard.json <out_dir> [--no-pdf]
# storyboard.json: {"title": "...", "langs": ["it","en"], "accent": "#00498a", "per_page": 14,
#   "ink": "#141a26" (brand dark), "shots": [{"img": "preview/1_sb/f_0001.jpg", "start": 0, "end": 8, "piano": {"it": "..."}, "voce": {"it": "...", "en": "..."}}]}
# Writes storyboard_<lang>.pdf (one per language, 7 columns x 2 rows, A4 landscape) and vo_<lang>.md.
import json, sys, os, subprocess, html, pathlib
a = sys.argv[1:]; cfg = json.load(open(a[0])); out = pathlib.Path(a[1]); out.mkdir(parents=True, exist_ok=True)
base = pathlib.Path(a[0]).resolve().parent; pdf = "--no-pdf" not in a
shots, langs = cfg["shots"], cfg.get("langs", ["it"]); acc = cfg.get("accent", "#00498a"); ink = cfg.get("ink", "#141a26"); per = cfg.get("per_page", 14)
L = {"it": ("INQUADRATURA", "VOCE"), "en": ("SHOT", "VOICE")}
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
def tc(s): return f"{int(s // 60)}:{s % 60:04.1f}"
def t(d, lg): return d.get(lg) or next(iter(d.values()), "") if isinstance(d, dict) else (d or "")
total = tc(shots[-1]["end"]) if shots else "0:00.0"

for lg in langs:
    # voice-over script to take to a recording session or a TTS tool
    md = [f"# {cfg['title']} · VO ({lg})", "", f"Durata totale {total}. Circa 2,5 parole al secondo." if lg == "it" else f"Total length {total}. About 2.5 words per second.", ""]
    md += [("| # | tempo | durata | parole | testo |" if lg == "it" else "| # | time | length | words | text |"), "|---|---|---|---|---|"]
    for i, s in enumerate(shots, 1):
        v = t(s.get("voce", ""), lg).strip() or "—"; d = s["end"] - s["start"]
        md.append(f"| {i:02d} | {tc(s['start'])}–{tc(s['end'])} | {d:.1f} s | {len(v.split()) if v != '—' else 0} | {v.replace('|', '/')} |")
    md += ["", "## Testo continuo" if lg == "it" else "## Full text", ""] + [f"**{i:02d}** {t(s.get('voce',''), lg).strip()}" for i, s in enumerate(shots, 1) if t(s.get("voce", ""), lg).strip() not in ("", "—")]
    (out / f"vo_{lg}.md").write_text("\n".join(md) + "\n")
    if not pdf: continue
    pages = [shots[i:i + per] for i in range(0, len(shots), per)]; P, V = L.get(lg, L["en"]); body = []
    IT = lg == "it"; logo = (pathlib.Path(__file__).resolve().parent.parent / "assets/logo.svg").as_uri()
    for p, pg in enumerate(pages, 1):
        cells = []
        for k, s in enumerate(pg):
            n = (p - 1) * per + k + 1; v = html.escape(t(s.get("voce", ""), lg)) or "—"
            cells.append(f'<article><div class="im"><img src="{(base / s["img"]).as_uri()}"><b>{n:02d}</b></div><div class="tx">'
                         f'<div class="tc">{tc(s["start"])} – {tc(s["end"])} <i>{s["end"]-s["start"]:.1f} s</i></div>'
                         f'<h4>{P}</h4><p>{html.escape(t(s.get("piano", ""), lg))}</p><h4>{V}</h4><p class="v">{v}</p></div></article>')
        ok = "" if p < len(pages) else (f'<div class="ok"><b>{"Approvazione" if IT else "Approval"}</b><span>{"Approvato da" if IT else "Approved by"}</span><span>{"Data" if IT else "Date"}</span><span>{"Note" if IT else "Notes"}</span></div>')
        body.append(f'<section><header><div><small>{"STORYBOARD PER APPROVAZIONE" if IT else "STORYBOARD FOR APPROVAL"}</small><h1>{html.escape(cfg["title"])}</h1></div>'
                    f'<dl><div><dt>{"Scene" if IT else "Shots"}</dt><dd>{len(shots)}</dd></div><div><dt>{"Durata" if IT else "Length"}</dt><dd>{total}</dd></div><div><dt>{"Lingua" if IT else "Language"}</dt><dd>{lg.upper()}</dd></div></dl></header>'
                    f'<div class="g">{"".join(cells)}</div>{ok}<footer><img src="{logo}"><span><b>Blender Product Video</b> · {"skill per Claude Code di" if IT else "a Claude Code skill by"} Mario Mele</span><span>{p} / {len(pages)}</span></footer></section>')
    css = f"""@page{{size:A4 landscape;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}body{{font:10px/1.4 -apple-system,"Helvetica Neue",Helvetica,sans-serif;color:#1b2130}}
section{{width:297mm;height:210mm;padding:8mm 10mm 0;background:#f5f7fa;page-break-after:always;overflow:hidden;display:flex;flex-direction:column}}
header{{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:4mm;border-bottom:1.5px solid {acc};margin-bottom:5mm}}
small{{font-size:9px;letter-spacing:.14em;color:{acc};font-weight:700}}h1{{color:{ink};font-size:22px;letter-spacing:-.01em;margin-top:2px}}
dl{{color:{ink};display:flex;gap:7mm}}dt{{font-size:8.5px;font-weight:600;letter-spacing:.1em;color:#7b8494;text-transform:uppercase}}dd{{font-size:14px;font-weight:600}}
.g{{display:grid;grid-template-columns:repeat(7,1fr);gap:4mm 3.5mm;flex:1;align-content:start}}
article{{background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 0 0 .5px #dde2ea}}.im{{position:relative}}
.im img{{width:100%;height:46mm;object-fit:cover;display:block;background:#e7ebf1}}
.im b{{position:absolute;left:5px;top:5px;background:{acc};color:#fff;font-size:12px;padding:2px 5px;border-radius:4px}}
.tx{{padding:5px 6px 6px}}.tc{{font-weight:700;font-size:10px;font-variant-numeric:tabular-nums}}.tc i{{font-style:normal;font-weight:500;color:#5a6372}}
h4{{font-size:8px;font-weight:800;letter-spacing:.1em;color:{acc};margin-top:4px}}p{{font-size:9.5px;color:#2a3140;font-weight:500}}.v{{color:{ink};font-weight:600}}
.ok{{display:grid;grid-template-columns:auto 1fr 1fr 2fr;gap:6mm;align-items:end;margin-top:3mm;padding:3mm 4mm;background:#fff;border-radius:6px;box-shadow:0 0 0 .5px #dde2ea}}
.ok b{{font-size:12px;color:{acc}}}.ok span{{border-bottom:.7px solid #9aa3b2;padding-bottom:5mm;font-size:8.5px;font-weight:600;color:#5a6372;text-transform:uppercase;letter-spacing:.08em}}
footer{{display:flex;align-items:center;gap:6px;height:11mm;margin-top:auto;color:#5a6372;font-size:9px;font-weight:500}}footer img{{width:16px;height:16px}}footer span:last-child{{margin-left:auto}}footer b{{color:#1b2130}}"""
    hp = out / f"storyboard_{lg}.html"; hp.write_text(f"<!doctype html><meta charset=utf-8><style>{css}</style>{''.join(body)}")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={out / f'storyboard_{lg}.pdf'}", hp.as_uri()], check=True, capture_output=True)
    hp.unlink(); print(f"PDF_OK {out / f'storyboard_{lg}.pdf'}")
print("VO_OK " + " ".join(str(out / f"vo_{l}.md") for l in langs))
