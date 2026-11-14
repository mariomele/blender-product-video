# Sets each EDL scene's `extra` so the shown scene lasts at least its voice-over clip + pad seconds. Rewrites the EDL.
# usage: python3 fit_vo.py <edl.txt> <fps> <n=voice.mp3> [n=voice.mp3 ...] [--pad 0.5]
# Scenes without a clip keep their extra. Never shortens below the master length (extra >= 0).
import sys, math, subprocess

def dur(path):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))

def fit(L, skip, seconds, fps, pad):
    return max(0, math.ceil((seconds + pad) * fps) - L + skip)

assert fit(48, 0, 3.0, 24, 0.5) == 36 and fit(100, 0, 1.0, 24, 0.5) == 0 and fit(48, 6, 2.0, 24, 0) == 6

if __name__ == '__main__':
    args = sys.argv[1:]; pad = 0.5
    if '--pad' in args:
        i = args.index('--pad'); pad = float(args[i + 1]); del args[i:i + 2]
    edl, fps, clips = args[0], int(args[1]), dict(c.split('=', 1) for c in args[2:])
    out = []
    for line in open(edl):
        p = line.split()
        if len(p) >= 4 and p[0] in clips:
            p += ['0'] * (6 - len(p))
            L = int(p[3]) - int(p[2]) + 1
            p[4] = str(fit(L, int(p[5]), dur(clips[p[0]]), fps, pad))
            print(f"scena {p[0]}: vo {dur(clips[p[0]]):.2f}s -> extra {p[4]}")
            line = ' '.join(p) + '\n'
        out.append(line)
    open(edl, 'w').writelines(out)
