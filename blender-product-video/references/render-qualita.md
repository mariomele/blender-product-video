# Qualità dei render: la domanda delle tre scale

Ogni render usa tre scale da 1 a 4 (1 = più leggero, 4 = massimo). L'utente risponde con un codice `risoluzione-fps-qualità`, per esempio `2-3-4`; un quarto numero facoltativo cambia solo il JPG (`2-3-4-1` = qualità 4 con JPG 50); vanno bene anche valori liberi, per esempio `1440x2560-24-JPG70/spp60`. Proponi il codice adatto a quel passaggio, con la stima dei tempi, e scrivi la scelta in `progetto.md`.

```
Render <cosa> · rispondi risoluzione-fps-qualità (es. 2-4-1)
Risoluzione  1) 25%   2) 50%   3) 75%   4) 100% (<WxH del progetto>)
Fps          1) 3     2) 6     3) 12    4) 24 (massimo)
Qualità      1) 8 spp·JPG 50   2) 24 spp·JPG 60   3) 40 spp·JPG 75   4) 96 spp·JPG 95
JPG (facoltativo) 1) 50   2) 60   3) 75   4) 95
Proposta: <codice> · circa <tempo>
```

## Tempi

Misurati su M1 Pro, Metal, 1080x1920, una scena reale di macchina con denoise, al 100% di risoluzione: circa 6 s per frame sono fissi (preparazione della scena e denoise), il resto cresce con gli spp. A risoluzione più bassa i tempi scendono; su scene più leggere o più pesanti scalano in proporzione. Su CPU circa 4 volte di più. A 8 spp il denoise lascia qualche macchia sulle superfici grandi e uniformi.

| qualità | quando | variabili |
|---|---|---|
| 1 | bozza: prove di camera e tempi, da buttare | `SPP=8 JPG_Q=50` · 9 s/frame · 53 KB |
| 2 | bozza da mostrare al cliente, scadenza stretta | `SPP=24 JPG_Q=60` · 19 s/frame · 57 KB |
| 3 | web e social | `SPP=40 JPG_Q=75` · 25 s/frame · 69 KB |
| 4 | fiere, schermi grandi, color grading o archivio | `SPP=96 JPG_Q=95` · 56 s/frame · 190 KB |

Stima prima di partire: frame totali × s/frame. Un video di 60 s a 24 fps sono 1440 frame: a qualità 3 circa 10 h, a qualità 4 circa 22 h.

Proposte di partenza: storyboard `1-·-1` (fps fisso a 1 frame al secondo), anteprima di una scena `1-3-1`, anteprima del montaggio `2-4-1`, render finale `4-4-3` (`4-4-4` per schermi grandi e color grading).

## Dal codice agli script

- `render_all.sh` (montaggio e finale) accetta qualsiasi combinazione: `SPP=<n> JPG_Q=<q> $K/render_all.sh <progetto> edl.txt <res%> <fps> [WxH]`. Se gli fps scelti sono diversi da quelli del .blend, ogni shot viene ricampionato con i subframe e dura gli stessi secondi. Se cambi anche solo una variabile su uno shot già fatto, i vecchi frame vengono spostati in `<shot>.old_<data>` e lo shot si rifà. Al 100% i frame vanno in `final_jpg/`, sotto il 100% in `preview_jpg/`.
- `preview.sh` (storyboard e anteprima di una scena): `JPG_Q=<q> $K/preview.sh <scena.blend> <first> <last> <step> <out> <res%> <spp>` con step = 24 ÷ fps scelti (3 → 8, 6 → 4, 12 → 2, 24 → 1).
- `fit_vo.py` vuole gli fps del .blend, non quelli scelti per il render.
- Il tempo dipende quasi tutto da risoluzione, campioni e numero di frame (fps). La qualità JPG cambia il peso dei file e il dettaglio, non il tempo.
