# Builds an .srt from the voice-over text per scene and timings.json (scene start/end in seconds).
# usage: python3 make_srt.py <timings.json> <vo.txt> <out.srt> [audio/vo_<n>.mp3 pattern, e.g. audio/vo_{n}.mp3]
# vo.txt: one line per scene, "<n>|<text>". Cues are split on sentences (max ~84 chars, 2 lines)
# and spread over the voice clip length (or the scene length without clips), proportionally to their characters.
import sys, json, re, subprocess, os

def chunks(text, maxc=84):
    out = []
    for sent in re.split(r'(?<=[.!?;:])\s+', text.strip()):
        cur = ''
        for w in sent.split():
            if cur and len(cur) + 1 + len(w) > maxc:
                out.append(cur); cur = w
            else:
                cur = f"{cur} {w}".strip()
        if cur: out.append(cur)
    return out

def wrap(c, w=42):
    if len(c) <= w: return c
    i = c.rfind(' ', 0, len(c) // 2 + 10)
    return c[:i] + '\n' + c[i + 1:] if i > 0 else c

def cues(start, length, text):
    parts = chunks(text); total = sum(len(p) for p in parts); t = start; res = []
    for p in parts:
        d = length * len(p) / total; res.append((t, t + d, wrap(p))); t += d
    return res

def ts(s):
    ms = round(s * 1000); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"

c = cues(10, 4, "Uno due tre. Quattro cinque sei sette.")
assert len(c) == 2 and c[0][0] == 10 and abs(c[-1][1] - 14) < 1e-9 and ts(3661.5) == "01:01:01,500"

if __name__ == '__main__':
    timings, votxt, out = sys.argv[1:4]; pat = sys.argv[4] if len(sys.argv) > 4 else None
    scenes = {str(s['scene']): s for s in json.load(open(timings))}
    lines, k = [], 0
    for row in open(votxt, encoding='utf-8'):
        if '|' not in row: continue
        n, text = row.split('|', 1); s = scenes[n.strip()]
        length = s['end'] - s['start']
        clip = pat.replace('{n}', n.strip()) if pat else None
        if clip and os.path.exists(clip):
            length = min(length, float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', clip])))
        for a, b, t in cues(s['start'], length, text):
            k += 1; lines.append(f"{k}\n{ts(a)} --> {ts(b)}\n{t}\n")
    open(out, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f"SRT_OK {k} cues -> {out}")
