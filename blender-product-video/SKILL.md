---
name: blender-product-video
description: Workflow guidato per video 3D di prodotti, macchine, impianti o processi industriali fatti in Blender, partendo da foto, link, file CAD (STEP, GLB, STL, OBJ…) o disegni tecnici. Fa domande a ogni fase e tiene lo stato del progetto: modello e materiali, ambientazione, scene con storyboard e anteprime, montaggio, grafiche HyperFrames, voce/musica/SFX con ElevenLabs, render Cycles su GPU Metal, file di consegna. Usala quando l'utente vuole un video 3D o un'animazione Blender di un prodotto, o lavora su un progetto di questo tipo già avviato (storyboard o anteprima di una scena Blender, allungare le scene per la voce, rifare un pezzo, render finale su Metal, infografiche, voce o musica sopra un render 3D). Non usarla per video senza 3D (reel, montaggi di girato, podcast).
---

# Blender product video

Flusso guidato per un video 3D di un prodotto. Rispondi in italiano.

## Come lavorare
- **Guida con domande.** All'inizio di ogni fase fai le sue domande con `AskUserQuestion` (opzioni concrete, la consigliata per prima). Chiudi la fase con un **checkpoint**: mostra il risultato e chiedi l'ok prima di passare alla successiva. Non chiedere quello che sai già.
- **Tieni lo stato in `progetto.md`** (vedi sotto). Leggilo all'inizio di ogni sessione e aggiornalo a ogni checkpoint. Le decisioni dell'utente stanno lì, non solo nella conversazione.
- **Entra nella fase giusta** (vedi "Da dove partire"): il brief completo si fa solo per un progetto nuovo.
- **Mai partire per inerzia** con un render lungo, un download o una generazione a pagamento (voce, musica, SFX, modelli AI): chiedi prima. Prima di cancellare file chiedi sempre; meglio spostare in `old_*`.

Cartella di progetto: `progetto.md`, `source/` (materiale originale, mai modificato), `*.blend`, `render_scripts/`, `edl.txt`, `preview/`, `preview_jpg/`, `final_jpg/`, `hyperframes/`, `audio/`, `delivery/`. Gli script stanno in `K=~/.claude/skills/blender-product-video/scripts`. Blender di default è `/Applications/Blender.app`; un'altra installazione si indica con la variabile `BLENDER=<percorso dell'eseguibile>`.

### progetto.md
```markdown
# <Nome progetto>
Fase attuale: <0–9> — <cosa manca>
## Brief
Formato: 9:16 1080x1920, 24 fps · Durata: 45 s · Uso: Instagram
Sorgenti: source/… · Fedeltà: A/B/C (vedi fase 1)
Ambiente: … · Atmosfera: … · Foto ref: source/…
Palette infografiche (solo HyperFrames): #…, #… · Logo: source/… · Da evitare: …
Racconto: …
## Scene
| n | file | frame | durata | movimento / camera | storyboard | anteprima | finale |
## Audio
Voce: <nome, voice_id> · Musica: … · SFX: …
## Decisioni e note
- <data> …
```

## Da dove partire
| L'utente dice… | Vai a |
|---|---|
| un prodotto e del materiale nuovo, "fammi un video 3D di…" | 0. Brief |
| "rifai/cambia la scena X", "rifai l'intro" | 2 per quella scena (poi 8 se il finale c'è già) |
| "storyboard", "anteprima di…" | 2, solo storyboard o anteprima |
| "allunga le scene per la voce" | 5, `fit_vo.py` |
| "metti un'infografica / un titolo / i sottotitoli" | 4 |
| "voce", "musica", "effetti sonori" | 5 |
| "render finale", "passa a Metal" | 7 (controlla in `progetto.md` che ci sia l'ok della fase 6) |
| "esporta", "mandamelo", "versione per Instagram" | 9 |
Se manca `progetto.md` ma il progetto esiste (ci sono .blend ed EDL), ricostruiscilo dai file e chiedi conferma solo dei buchi. Se per la richiesta serve un dato che manca (es. formato prima di un render), chiedi solo quello.

## 0. Brief
Chiedi, se non lo sai già:
- **Sorgenti**: foto, link, CAD o disegno. Cosa deve essere fedele (misure, colori, loghi) e cosa può essere approssimato.
- **Formato, prima di qualunque scena o render**: aspect ratio (9:16 1080x1920 · 16:9 1920x1080 · 1:1 1080x1080 · 4:5 1080x1350), risoluzione e fps (24 · 25 · 30). Vanno impostati in ogni .blend.
- **Durata totale** e uso (social, sito, fiera, presentazione).
- **Ambiente e atmosfera**:
  - ambiente: capannone o reparto produttivo, studio con sfondo nero, limbo bianco/grigio, esterno (cantiere, campo, piazzale), showroom o ufficio, sfondo astratto;
  - atmosfera e luce: tecnica e pulita, cinematografica e contrastata, calda o fredda, giorno o notte, fumo/polvere/riflessi a terra;
  - foto di riferimento dell'ambientazione o del look (facoltativa).
  Proponi 2–3 combinazioni adatte all'uso (social → scuro e contrastato; catalogo → limbo chiaro).
- **Racconto**: cosa deve capire chi guarda, scene di massima, testo del voice-over se c'è già.
- **Palette delle infografiche** (vale **solo per HyperFrames**: in Blender prodotto e ambiente hanno i loro colori reali). Se il cliente è in memoria usa i suoi colori e i suoi divieti. Altrimenti chiedi sempre, in uno di tre modi:
  - a parole ("blu scuro e bianco"): proponi tu gli Hex e falli confermare;
  - codici Hex;
  - un sito di riferimento: ricava la palette con `firecrawl_scrape` (formato `branding`) o dal CSS, mostrala e falla confermare.
  Chiedi anche il logo (SVG/PNG) e i colori da evitare. Con l'ok salva la palette in memoria per i video successivi dello stesso cliente.
- **Extra facoltativo**: chiedi se serve anche una pagina 3D interattiva (esploso, sezione, numeri di funzionamento) per sito o fiera. Si fa in fase 9 con la skill `/machine`, se è installata.
Checkpoint: crea `progetto.md` con il brief e fallo confermare.

## 1. Il pezzo: modello, materiali, ambientazione

### 1a. Modello
Obiettivo: il prodotto in **metri reali**, centrato sull'origine e appoggiato a terra. Per modelli 3D e SVG:
`blender -b --factory-startup --python $K/import_model.py -- <file> <out.blend> [m|cm|mm|in]`
Stampa `SIZE_M L x P x H`: confrontalo con una misura nota. Se è sbagliata di 10, 100 o 1000 volte, hai sbagliato l'unità.

| Sorgente | Come procedere |
|---|---|
| **GLB/glTF, FBX, OBJ, STL, PLY, USD, ABC** | `import_model.py`. STL e OBJ da CAD sono quasi sempre in `mm`. |
| **CAD nativo** (STEP, IGES, SolidWorks, Inventor, Onshape, Fusion) | Blender non li apre. Chiedi l'export in **GLB** (tiene colori e parti separate) oppure OBJ/STL. Fallback senza CAD: `pip install cadquery-ocp` in un venv nello scratchpad e tassellatura STEP→STL (chiedi prima, circa 100 MB). |
| **Disegno vettoriale** (DXF, DWG, SVG, PDF vettoriale) | SVG → `import_model.py`. DXF/DWG → chiedi l'export in SVG o PDF, oppure installa l'estensione "Import AutoCAD DXF" (con ok). Poi estrudi i profili o ricostruisci le parti. |
| **Disegno raster o schizzo** | Leggilo, trascrivi le quote in una tabella dentro `progetto.md` e **modella proceduralmente** in Python (geometry nodes / bmesh). Le quote mancanti si chiedono, non si inventano. |
| **Foto** | Vedi sotto. |
| **Link** | Pagina prodotto → leggila (`firecrawl_scrape` o il browser integrato) per foto, misure, schede tecniche, codici colore; poi procedi come per foto/disegni. Link a un modello (GrabCAD, TraceParts, produttore, Sketchfab) → chiedi l'ok, controlla la licenza, poi `import_model.py`. Salva tutto in `source/`. |

**Da foto.** È la sorgente più lenta e la meno precisa: dillo subito.
- Foto che servono: fronte, retro, due lati, alto, una o due 3/4, primi piani di giunzioni, loghi, etichette, comandi. Luce diffusa, niente grandangolo spinto, possibilmente un metro o un oggetto di misura nota nell'inquadratura.
- Almeno **una misura reale** (lunghezza totale o altezza): senza, la scala è inventata.
- Monta le foto come riferimento (`bpy.ops.image.import_as_mesh_planes` o Empty immagine sugli assi) e modella a blocchi, poi dettaglia. Skill: **blender-director**, **hard-surface**, **prop-artist**.
- L'image-to-3D con AI (Higgsfield `generate_3d`, Magnific `models3d_generate`) serve solo per una bozza o per oggetti di contorno, mai per parti tecniche. Costa crediti: chiedi.

**Livello di fedeltà**, da concordare e scrivere in `progetto.md`:
- **A — da CAD**: geometria esatta.
- **B — da disegno quotato o foto + misure**: forme e proporzioni fedeli (±2–5%), dettagli non visibili semplificati.
- **C — da sole foto**: aspetto credibile, proporzioni approssimate, parti nascoste inventate.

Pulizia: merge dei vertici duplicati, normali, shade auto smooth, nomi chiari delle parti. Oltre ~2 M di triangoli: **asset-optimization** o decimate sulle parti nascoste. Migliaia di oggetti da CAD: unisci per materiale le parti ferme.

### 1b. Materiali e texture
Chiedi:
- **Colori reali del prodotto**: codici RAL/Pantone dalla scheda tecnica, oppure campionati dalle foto (zona ben illuminata, non in ombra né sul riflesso), oppure dall'utente. Converti in sRGB e scrivili in `progetto.md`.
- **Finiture**: acciaio inox spazzolato o lucido, alluminio, verniciato (lucido/opaco/goffrato), plastica, gomma, vetro, zincato.
- **Loghi, etichette, targhe**: file del cliente (SVG/PNG) o foto, applicati come decal.
Come farli (skill **materials**, **texture-workflow**, **lookdev**):
- Principled BSDF con valori fisici: metalli `metallic 1`, roughness 0,15–0,45; vernici `metallic 0`, roughness 0,3–0,6, coat per il lucido; gomma roughness 0,7–0,9.
- **Procedurale prima di tutto** (noise, voronoi, anisotropia per lo spazzolato, piccola variazione di roughness, usura sui bordi con pointiness/AO): non serve l'UV ed è leggero.
- Mesh da CAD senza UV: mappatura **box/triplanare** su coordinate oggetto, non unwrap a mano. UV solo dove va un decal (UV project dalla vista).
- Texture a immagine (Poly Haven, ambientCG) solo se servono davvero (es. cemento del capannone), con l'ok per il download. Tienile in `source/textures/`.
- Il colore reale del prodotto va verificato sul **frame renderizzato** accanto alla foto o al codice di riferimento, perché la view transform di Blender (AgX) lo sposta. Se il cliente è pignolo sul colore, usa la view transform Standard o correggi il materiale.

### 1c. Ambientazione
Dal brief, con **environment-artist**, **set-dressing**, **lighting**, **lookdev**:
- **Studio nero o limbo**: piano curvo senza orizzonte, luce a tre punti o softbox, riflesso leggero a terra.
- **Capannone, esterno, showroom**: set essenziale (pavimento, pareti, pochi elementi di contorno) e HDRI coerente. HDRI e asset gratuiti (Poly Haven) solo con l'ok per il download.
- **Con foto di riferimento**:
  - foto a 360° equirettangolare → HDRI del mondo;
  - foto normale → ricavane direzione e durezza della luce, colori e materiali dell'ambiente, altezza della camera, e ricostruisci un set simile. Se va usata come sfondo vero (backplate), allinea la camera alla prospettiva e metti un piano shadow catcher.
- L'ambiente è contorno: il protagonista è il prodotto. Profondità di campo e volumetrici costano tempo di render: dillo prima.
Checkpoint: 3–4 viste statiche (fronte, 3/4, dettaglio, materiale da vicino) nell'ambientazione scelta, accanto alla foto di riferimento se c'è, con `preview.sh` su un frame (`<f> <f> 1`). Chiedi se forma, proporzioni, materiali e atmosfera vanno bene.

## 2. Le scene, una alla volta
Per **ogni** scena, prima di costruirla, chiedi:
- **Durata** in secondi.
- **Movimenti della macchina/del prodotto**: cosa si muove, a che velocità, in che ordine (es. nastro che scorre, sportello che si apre, esploso, montaggio dei pezzi).
- **Inquadrature**: tipo (totale, dettaglio, orbita, carrello, dolly-in, POV) e movimento della camera. Proponi 2–3 opzioni con **camera-cinematography**.
Costruisci con **Blender MCP** (`get_objects_summary`, `execute_blender_code`) o `blender -b file.blend --python script.py` (script in `render_scripts/`). Skill: **animation**, **geometry-nodes**, **procedural-modeling**.
- Animazione **procedurale** (driver + geometry nodes, niente simulazioni): così si può campionare a subframe e allungare i tempi senza toccare i keyframe.
- Prima di patchare un .blend salvane una copia nello scratchpad. Ogni patch è uno script Python rieseguibile.

**Storyboard (1 frame al secondo)**, prima di qualunque anteprima animata:
`$K/preview.sh <scena.blend> <first> <last> <fps_scena> preview/<n>_sb`
Rende un frame al secondo, con il numero di frame stampato, e crea `grid.jpg`. Guarda tu la griglia, poi mandala all'utente come storyboard. Ripeti finché non la approva.

**Anteprima animata.** Chiedi la qualità:
- **Real time**: tutti i frame (step 1 → 24 fps su una scena a 24);
- **Medio**: un frame ogni 2 (step 2 → 12 fps). Consigliato;
- **Basso**: un frame ogni 4 (step 4 → 6 fps), il più veloce.
`$K/preview.sh <scena.blend> <first> <last> <step> preview/<n>_p [res%=25] [spp=8]` → `preview.mp4` a velocità reale.
Checkpoint: ok sulla scena, segnato in `progetto.md`, prima di passare alla successiva.

## 3. Montaggio multi-scena
- `edl.txt`, una scena per riga: `n file.blend first last [extra] [skip_head]`.
  - `extra`: frame aggiunti tramite subframe per dare respiro alla voce.
  - `skip_head`: primi N frame esclusi dal montaggio, senza cancellarli.
- Anteprima di tutto: `$K/render_all.sh <progetto> edl.txt 50 <fps>` (res 50%, 12 spp) → `preview_jpg/final.mp4` + `timings.json` (inizio e fine di ogni scena in secondi).
- `$K/contact_sheet.sh preview_jpg/final.mp4 preview/montaggio.jpg 1` per un provino.
- Se cambiano `first`, `last`, `extra` o la risoluzione di uno shot, `render_all.sh` sposta i frame vecchi in `<shot>.old_<data>` e rifà lo shot (i vecchi frame non corrispondono più agli stessi istanti).
Checkpoint: ordine, ritmo, transizioni.

## 4. HyperFrames: testo e grafiche
- Chiedi se il **testo del voice-over** lo dà l'utente o lo scrivi tu. In quel caso scrivilo scena per scena, entro la durata di `timings.json` (circa 2,5 parole al secondo), in `audio/vo.txt` con una riga per scena: `n|testo`. Fallo approvare.
- Chiedi quali **grafiche** servono: titoli, callout, misure, conteggi, lower third, sottotitoli, logo finale.
- Costruisci in `hyperframes/` con la skill **hyperframes** (contratto di render, animazioni, overlay e audio), nel formato del brief, **solo con la palette confermata**, `final.mp4` come sfondo e i tempi presi da `timings.json`. Le misure a schermo vengono dalla sorgente, mai stimate.
- **Verifica** prima di mostrare (skill **hyperframes-cli**):
  1. `npx hyperframes lint` dopo ogni modifica strutturale;
  2. `npx hyperframes check --json` e correggi ogni errore (layout, contrasto, elementi fuori campo);
  3. `npx hyperframes snapshot --at <metà di ogni scena da timings.json>` e guarda i PNG in `.hyperframes/artifacts/snapshots/`;
  4. `npx hyperframes preview --background` e dai il link all'utente.
Checkpoint: bozza HyperFrames muta.

## 5. Audio: voce, musica, SFX (ElevenLabs MCP)
Ogni generazione costa crediti: chiedi l'ok prima, con il numero di clip.
- **Voce**: `creative_list_voices` → proponi 2–3 voci (lingua, tono) e fanne scegliere una → `creative_generate_speech` scena per scena → `audio/vo_<n>.mp3`. Annota voce e voice_id in `progetto.md`.
- **Adatta le scene alla voce**: `python3 $K/fit_vo.py edl.txt <fps> 1=audio/vo_1.mp3 2=audio/vo_2.mp3 … [--pad 0.5]` riscrive `extra` perché ogni scena duri almeno quanto la sua voce più il margine. Poi rifai l'anteprima della fase 3 (gli shot con `extra` cambiato vengono rifatti).
- **Sottotitoli**: `python3 $K/make_srt.py preview_jpg/timings.json audio/vo.txt delivery/sottotitoli.srt 'audio/vo_{n}.mp3'`. Servono come file `.srt` per YouTube/LinkedIn o bruciati in HyperFrames per i social.
- **Musica di sottofondo** (opzionale): chiedi genere, mood, tempo e se deve chiudersi sul logo. Con `creative_generate_in_flow`:
  - nodo `music` (modello `eleven_music_v2_5`, `instrumental: true`, `duration_seconds` = durata del video);
  - oppure nodo `video-to-music` collegato all'anteprima `preview_jpg/final.mp4`: compone su misura del ritmo del video.
  In alternativa la skill **media-use**.
- **SFX** (opzionale): proponi una lista di suoni legati ai movimenti (motore, scorrimento, clic, sportello, whoosh sulle transizioni), ciascuno con l'istante preso da `timings.json`. Nodo `sfx` (`eleven_text_to_sound_v2`, 0,5–30 s, `loop: true` per i suoni continui di macchina).
- **Mix** in HyperFrames (skill **hyperframes**, parte audio): voce in primo piano, musica abbassata sotto la voce, SFX sincronizzati ai movimenti.

## 6. Visione d'insieme
Render di bozza della composizione completa (`npx hyperframes render --quality draft -o preview/insieme.mp4`): anteprima + grafiche + audio. Mandalo all'utente e chiedi un giudizio complessivo: ritmo, voce, musica, leggibilità dei testi. Le correzioni tornano alla fase giusta (scena → 2, testo/grafica → 4, audio → 5).
Checkpoint: **ok esplicito al render finale**, scritto in `progetto.md`. Senza quell'ok non si parte.

## 7. Render finale (GPU Metal)
- **Chiudi ogni Blender con GUI aperto** (anche quello dell'MCP): se è aperto, Metal in headless si blocca all'avvio (0% CPU). `render_all.sh` lo controlla e si ferma (`GUI_BLENDER_OPEN`, exit 3). Se si blocca durante il render, il watchdog lo interrompe dopo `HANG_MIN` minuti (default 10) senza frame nuovi ed esce con `HANG` (exit 2). Allora diagnostica (cubo con `--factory-startup`, `ps` per altri Blender): non ripiegare in silenzio sulla CPU.
- Prima di partire dai una stima: frame totali × s/frame. Riferimento: M1 Pro, 1080x1920, 40 spp → circa 10 s/frame su Metal, circa 40 s su CPU.
- `$K/render_all.sh <progetto> edl.txt 100 <fps> [WxH]` con Bash `run_in_background`, così arriva la notifica a fine render. Avanzamento: `ls final_jpg/*/f*.jpg | wc -l`. Usa `gpu_setup.py` (Metal on, CPU off, MetalRT off su M1/M2 e automatico su M3+) e `render_seg_gpu.py` (shot `[a,b]` allungato di `extra` frame tramite subframe, JPG q95, ripartibile).
- Poi la composizione HyperFrames finale con `final_jpg/final.mp4` come sfondo: `npx hyperframes render --quality delivery -o delivery/video.mp4`. Controlla che la durata (`ffprobe`) coincida con quella della composizione.

## 8. Rifare un pezzo senza ri-renderizzare tutto
- Animazione cambiata solo nei frame master `[x,y]` di uno shot, con stessi `a b extra`:
  `blender -b scena.blend --python $K/gpu_setup.py --python $K/render_seg_gpu.py -- a b extra final_jpg/<dir_shot> 100 [WxH] --redo x y`
  Sovrascrive solo i frame che campionano `[x-1, y+1]`. Poi rilancia `render_all.sh` (salta i frame esistenti e rimonta) e verifica la giunzione con `contact_sheet.sh`.
- Se cambiano `extra` o la durata dello shot, ci pensa `render_all.sh` (fase 3): rifà lo shot intero e sposta i vecchi frame da parte.

## 9. Consegna
`$K/deliver.sh delivery/video.mp4 delivery [max_mb=28]` produce:
- `master.mp4`: H.264 alta qualità, audio normalizzato a **−14 LUFS** (−1 dBTP), faststart;
- `light.mp4`: sotto `max_mb` (default 28 MB), da mandare al telefono, su WhatsApp o per email.
Più `sottotitoli.srt` dalla fase 5. Limiti utili delle piattaforme:

| Piattaforma | Formato | Note |
|---|---|---|
| Instagram Reels / TikTok / Shorts | 9:16 1080x1920 | testi lontani dai bordi alti e bassi (~250 px), sottotitoli bruciati |
| Feed Instagram / LinkedIn | 4:5 1080x1350 o 1:1 | LinkedIn accetta il `.srt` separato |
| YouTube / sito | 16:9 1920x1080 | `.srt` separato |
Altri formati dallo stesso progetto: chiedi se servono. Vuol dire reimpostare la camera nei .blend e rifare il render: non basta ritagliare.
Manda il `light.mp4` con SendUserFile; per file oltre 30 MB indica il percorso.

**Extra: pagina interattiva** (solo se chiesta nel brief e se `/machine` è installata). Usa `/machine` per creare `delivery/<nome>.html`: un file unico in three.js, da aprire nel browser o mettere in un iframe, con esploso, sezione, radiografia e numeri calcolati. Passale le misure, la distinta dei pezzi con i materiali e i dati tecnici raccolti in `progetto.md`. Avvisa che `/machine` ricostruisce il pezzo con forme proprie: è una versione semplificata, non carica il modello Blender e ha una resa diversa da Cycles. Per questo non va montata dentro il video. Mostrala con uno screenshot e falla approvare a parte.

## Trappole
- Blender 5.x: action a livelli → `action.layers[].strips[].channelbags[].fcurves`; l'opzione MetalRT si chiama `metalrt` (non `metal_rt`).
- Aliasing a ruota di carro: se un movimento ripetitivo supera ~0,3 celle per frame, rallentalo o alterna i colori.
- macOS: niente `timeout` né `sed \n`; usa un ciclo di attesa e Python.
