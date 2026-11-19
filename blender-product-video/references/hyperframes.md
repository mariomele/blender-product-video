# HyperFrames: zone sicure, cambio formato, verifica

Leggila quando costruisci o cambi le grafiche (fase 4), dopo `fit_vo.py` e quando cambi formato.

## Zone sicure

**Nel 9:16** le interfacce di Reels, Stories e TikTok coprono l'alto, il basso e il lato destro. `$K/safe_zone.sh <WxH> <reels|stories|tiktok|all>` stampa i margini e la regola CSS `.safe`; senza indicazioni usa `all`, la più stretta delle tre (su 1080x1920: alto 250, basso 484, sinistra 60, destra 140 px).
- I testi importanti (titoli, numeri, misure, sottotitoli, CTA, logo) stanno sempre dentro la zona sicura, in un contenitore `.safe` (linea verde).
- Gli elementi secondari (icone, linee, cornici, decorazioni, bordi dei box) possono sconfinare nel margine al più del 20% in alto e in basso e del 10% ai lati (linea rossa), mai oltre.
- Sfondi, effetti e il render 3D possono occupare tutto il frame.

**Nel 16:9** non ci sono zone delle piattaforme: basta la zona sicura standard (azione al 90%, titoli e testi all'80% del frame), quella che HyperFrames già segue.

## Cambiare formato

Vuol dire rifare l'impaginazione, non copiarla. Da 9:16 a 16:9 (o 1:1, 4:5) e viceversa:
- **scala** testi, grafiche, callout e logo in proporzione al nuovo frame: con gli stessi px, nel 16:9 sembrano piccoli. Nelle composizioni usa misure relative al frame (percentuali, o una variabile di scala) invece di px fissi;
- **reimpagina** sugli spazi del nuovo formato: nel 16:9 testo e prodotto affiancati, nel 9:16 uno sopra l'altro; i callout seguono dove cade il pezzo nella nuova inquadratura; gli split screen di solito cambiano verso;
- **zone sicure del formato di arrivo** (sopra);
- poi rifai gli snapshot di controllo e guarda che i testi si leggano alla stessa distanza di prima.

Il render 3D non si ritaglia: nei .blend si reimposta la camera e si rifà il render.

## Verifica, prima di mostrare (skill **hyperframes-cli**)

1. `npx hyperframes lint` dopo ogni modifica strutturale;
2. `npx hyperframes check --json` e correggi ogni errore (layout, contrasto, elementi fuori campo);
3. `npx hyperframes snapshot --at <inizio, metà e fine di ogni grafica, da timings.json>` e guarda i PNG in `.hyperframes/artifacts/snapshots/`; nel 9:16 passa ogni PNG in `$K/safe_zone.sh <WxH> <piattaforma> <png> <png_guide>` e controlla che i testi importanti stiano dentro la linea verde e le grafiche secondarie dentro la rossa;
4. `npx hyperframes preview --background` e dai il link all'utente.

## Dopo `fit_vo.py` (o qualunque cambio di durata)

Le scene si allungano e `timings.json` cambia: le grafiche fatte sui tempi vecchi entrano in anticipo. Rileggi i tempi dal `timings.json` nuovo (`final_jpg/` per il finale, `preview_jpg/` per la bozza), sposta entrate e uscite di ogni elemento, aggiorna `grafiche.md`, poi rifai i passi 2 e 3 della verifica. Se cambiano solo i tempi e i controlli passano, non serve una nuova sosta.
