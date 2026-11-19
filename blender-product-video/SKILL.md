---
name: blender-product-video
description: Workflow guidato per video 3D di prodotti, macchine, impianti o processi industriali fatti in Blender, partendo da foto, link, file CAD (STEP, 3MF, GLB, FBX, STL, OBJ, USD, .blend…) o disegni tecnici (DWG, SVG, PDF). In modalità guidata fa domande a ogni fase, in modalità automatica chiede solo il brief e poi va avanti da sola fino al provino, dentro un budget di render e crediti; tiene lo stato del progetto: modello e materiali, ambientazione, scene con storyboard e anteprime, montaggio, grafiche HyperFrames, voce/musica/SFX con ElevenLabs, render Cycles su GPU Metal, file di consegna. Usala quando l'utente vuole un video 3D o un'animazione Blender di un prodotto, o lavora su un progetto di questo tipo già avviato (storyboard o anteprima di una scena Blender, allungare le scene per la voce, rifare un pezzo, render finale su Metal, infografiche, voce o musica sopra un render 3D). Non usarla per video senza 3D (reel, montaggi di girato, podcast).
---

# Blender product video

Flusso guidato per un video 3D di un prodotto. Rispondi in italiano.

## Come lavorare
- **Due modalità, scelte nel brief** (riga `Modalità` di `progetto.md`; se manca, è guidata):
  - **guidata**: le domande e i checkpoint di ogni fase, come scritti sotto;
  - **automatica**: dopo il brief vai avanti da solo dalla fase 1 alla 6. Le domande di una fase diventano scelte tue, fatte con le regole di questa skill e con il brief: scrivile in `progetto.md` (Decisioni, una riga con il perché). I checkpoint diventano **controlli tuoi** (sotto, "Controlli in automatica"). Ti fermi e chiedi solo alle **soste**: il riepilogo del brief, il provino completo della fase 6, l'ok al render finale, una spesa fuori budget, una cancellazione di file, un dato che non si inventa (testo della voce se il cliente lo vuole suo, carichi e materiali di un calcolo, colori del brand che non trovi, fedeltà di una parte che non si vede nelle sorgenti). Fra una sosta e l'altra dai solo brevi aggiornamenti su cosa stai facendo.
- **Guida con domande** (modalità guidata). All'inizio di ogni fase fai le sue domande con `AskUserQuestion` (opzioni concrete, la consigliata per prima). Chiudi la fase con un **checkpoint**: mostra il risultato e chiedi l'ok prima di passare alla successiva. Non chiedere quello che sai già.
- **Tieni lo stato in `progetto.md`** (vedi sotto). Leggilo all'inizio di ogni sessione e aggiornalo a ogni checkpoint. Le decisioni dell'utente stanno lì, non solo nella conversazione.
- **Entra nella fase giusta** (vedi "Da dove partire"): il brief completo si fa solo per un progetto nuovo.
- **Ogni render usa tre scale da 1 a 4** (1 = più leggero, 4 = massimo). Le qualità delle bozze (storyboard, anteprime, montaggio, redo di bozza) si fissano una volta sola nel brief (fase 0, riga `Bozze` di `progetto.md`):
  - **predefinite**: usa i codici scritti in `Bozze` senza chiedere a ogni passaggio; dì solo in una riga quale codice usi e la stima dei tempi. Se l'utente chiede una qualità diversa per un passaggio, usala solo lì;
  - **passo passo**: fai la domanda qui sotto prima di ogni render di bozza.
  Il **render finale** e i suoi redo hanno sempre la loro domanda, anche con le bozze predefinite: non lanciarli mai senza la risposta, anche quando l'utente dice solo "renderizza". Se `Bozze` manca (progetto vecchio), chiedi come nel passo passo. L'utente risponde con un codice `risoluzione-fps-qualità`, per esempio `2-3-4`; un quarto numero facoltativo cambia solo il JPG (`2-3-4-1` = qualità 4 con JPG 50); vanno bene anche valori liberi, per esempio `1440x2560-24-JPG70/spp60`. Proponi il codice adatto a quel passaggio, con la stima dei tempi, e scrivi la scelta in `progetto.md`. Mostra la domanda così:

  ```
  Render <cosa> — rispondi risoluzione-fps-qualità (es. 2-4-1)
  Risoluzione  1) 25%   2) 50%   3) 75%   4) 100% (<WxH del progetto>)
  Fps          1) 3     2) 6     3) 12    4) 24 (massimo)
  Qualità      1) 8 spp·JPG 50   2) 24 spp·JPG 60   3) 40 spp·JPG 75   4) 96 spp·JPG 95
  JPG (facoltativo) 1) 50   2) 60   3) 75   4) 95
  Proposta: <codice> · circa <tempo>
  ```

  Tempi e pesi misurati su M1 Pro, Metal, 1080x1920, una scena reale di macchina con denoise, al 100% di risoluzione: circa 6 s per frame sono fissi (preparazione della scena e denoise), il resto cresce con gli spp. A risoluzione più bassa i tempi scendono; su scene più leggere o più pesanti scalano in proporzione. A 8 spp il denoise lascia qualche macchia sulle superfici grandi e uniformi.

  | qualità | quando | variabili |
  |---|---|---|
  | 1 | bozza: prove di camera e tempi, da buttare | `SPP=8 JPG_Q=50` · 9 s/frame · 53 KB |
  | 2 | bozza da mostrare al cliente, scadenza stretta | `SPP=24 JPG_Q=60` · 19 s/frame · 57 KB |
  | 3 | web e social | `SPP=40 JPG_Q=75` · 25 s/frame · 69 KB |
  | 4 | fiere, schermi grandi, color grading o archivio | `SPP=96 JPG_Q=95` · 56 s/frame · 190 KB |

  Proposte di partenza: storyboard `1-·-1` (fps fisso a 1 frame al secondo), anteprima di una scena `1-3-1`, anteprima del montaggio `2-4-1`, render finale `4-4-3`.
  Come si applica:
  - `render_all.sh` (montaggio e finale) accetta qualsiasi combinazione: `SPP=<n> JPG_Q=<q> $K/render_all.sh <progetto> edl.txt <res%> <fps> [WxH]`. Se gli fps scelti sono diversi da quelli del .blend, ogni shot viene ricampionato con i subframe e dura gli stessi secondi. Se cambi anche solo una variabile su uno shot già fatto, i vecchi frame vengono spostati in `<shot>.old_<data>` e lo shot si rifà. Al 100% i frame vanno in `final_jpg/`, sotto il 100% in `preview_jpg/`.
  - `preview.sh` (storyboard e anteprima di una scena): `JPG_Q=<q> $K/preview.sh <scena.blend> <first> <last> <step> <out> <res%> <spp>` con step = 24 ÷ fps scelti (3 → 8, 6 → 4, 12 → 2, 24 → 1).
  - `fit_vo.py` vuole gli fps del .blend, non quelli scelti per il render.
  - Il tempo dipende quasi tutto da risoluzione, campioni e numero di frame (fps). La qualità JPG cambia il peso dei file e il dettaglio, non il tempo.
- **Codice minimo con Ponytail** (se il plugin è installato; consigliato): ogni script che scrivi per il progetto (scene, patch, build123d, composizioni HyperFrames) segue `/ponytail`. Usa prima gli script di `$K` e quelli già in `render_scripts/`, poi la patch più corta che funziona; niente astrazioni, opzioni o codice "per dopo". Script brevi vuol dire meno token, meno errori e anteprime più veloci da rifare. Prima del render finale (fase 7) passa `/ponytail-review` sugli script del progetto: un errore trovato lì vale ore di GPU.
- **Mai partire per inerzia** con un render lungo, un download o una generazione a pagamento (voce, musica, SFX, modelli AI): chiedi prima. In automatica vale il **budget** del brief (riga `Budget` di `progetto.md`): dentro il budget vai, e segna ogni spesa e ogni render con il suo tempo nella riga `Speso`; prima di una spesa o di un render che lo farebbe superare, fermati e chiedi. Le installazioni e i download chiedono l'ok sempre. Prima di cancellare file chiedi sempre; meglio spostare in `old_*`.

Cartella di progetto: `progetto.md`, `source/` (materiale originale, mai modificato), `*.blend`, `render_scripts/`, `edl.txt`, `preview/`, `preview_jpg/`, `final_jpg/`, `hyperframes/`, `audio/`, `delivery/`. Gli script stanno in `K=~/.claude/skills/blender-product-video/scripts`. Blender di default è `/Applications/Blender.app`; un'altra installazione si indica con la variabile `BLENDER=<percorso dell'eseguibile>`.

### progetto.md
```markdown
# <Nome progetto>
Fase attuale: <0–9> — <cosa manca>
## Brief
Formato: 9:16 1080x1920, 24 fps · Durata: 45 s · Uso: Instagram
Bozze: predefinite · storyboard 1-·-1 · anteprima 1-3-1 · montaggio 2-4-1 (oppure: passo passo)
Modalità: automatica (oppure: guidata) · Budget: render bozze ≤ 3 h GPU · crediti ElevenLabs ≤ 5000 · AI ≤ 0
Speso: render 0 h · ElevenLabs 0 · AI 0
Sorgenti: source/… · Fedeltà: A/B/C (vedi fase 1)
Ambiente: … · Atmosfera: … · Foto ref: source/…
Palette infografiche (solo HyperFrames): #…, #… · Logo: source/… · Da evitare: …
Racconto: …
## Scene
| n | file | frame | durata | piano | movimento / camera | cosa racconta | storyboard | anteprima | finale |
## Audio
Voce: <nome, voice_id> · Musica: … · SFX: …
## Decisioni e note
- <data> …
```

### Controlli in automatica
Al posto di ogni checkpoint guardi tu il risultato (`Read` sui JPG e sui PNG di snapshot) e lo correggi prima di passare oltre. Ogni controllo fatto va in `progetto.md`, sotto Decisioni: cosa hai visto, cosa hai corretto. Se dopo due correzioni un problema resta, è una sosta: mostralo e chiedi.
| Fase | Controlla |
|---|---|
| 1 modello | proporzioni e colori contro le foto di riferimento, scala reale (una misura nota), nessuna parte mancante o capovolta, normali e materiali senza nero o rosa |
| 2 scene | il soggetto resta in quadro, nessuna compenetrazione, i giunti dentro i limiti, la camera non attraversa oggetti, il movimento si legge (né troppo lento né a scatti) |
| 3 montaggio | ordine come il racconto, niente due piani uguali di fila, un piano largo ogni 2–3 stretti, durata totale entro ±10% del brief, scene da 5–10 s e intermezzi da 2–3 s senza testo |
| 4 grafiche | testi dentro le zone sicure (`safe_zone.sh`), leggibili alla dimensione del telefono, solo colori della palette, misure uguali alla sorgente |
| 5 audio | ogni scena dura quanto la sua voce più il margine (`fit_vo.py`), pronuncia di nomi e sigle, musica sotto la voce |
Alla fase 6 il provino completo (`preview/insieme.mp4`) va all'utente con il riepilogo dei controlli: è la seconda sosta, e l'unico giudizio d'insieme che gli chiedi.

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

## Skill Blender: obbligatorie, le piloti tu
Questa skill è il regista: decide fasi, domande, checkpoint e stato. Il mestiere Blender (modellazione, materiali, luce, camera, animazione, render) sta nelle skill di [arjun988/blender-skills](https://github.com/arjun988/blender-skills) (MIT), che sono **obbligatorie**.
- **All'avvio di ogni sessione** lancia `$K/check_skills.sh`. Se stampa `MISSING`, fermati: mostra all'utente quali mancano e i comandi di installazione che stampa, e installale solo dopo il suo ok. Senza quelle skill non si va oltre il brief.
- **Prima di iniziare ogni passo della tabella, caricala con lo strumento Skill** (non basta averla nominata): una volta per sessione, poi tienine le regole. Le sue regole valgono dentro i limiti di questa skill: domande, checkpoint, `progetto.md`, scala reale, regole di render e consegna restano quelli scritti qui. Se una sua regola va contro questa skill, vince questa; se va contro una richiesta dell'utente, vince l'utente.
- Non seguire il routing di **blender-director** verso stili da videogioco, LOD, export per motori o retopologia: qui si fa un video, con materiali e misure veri.

| Passo | Carica |
|---|---|
| 1a modello da foto, link o disegno | **blender-director**, poi **hard-surface** e **prop-artist** |
| 1a modello da CAD (import o pulizia) | **hard-surface** |
| 1b materiali e texture | **materials**, **texture-workflow**, **lookdev** |
| 1c ambientazione e luce | **lighting**, **lookdev** |
| 2 scaletta, piani e camera | **camera-cinematography** |
| 2 animazione, esploso, cavi, scatter | **animation**, **geometry-nodes**, **procedural-modeling** |
| 2 anteprime, 7 render finale | **rendering** |

## 0. Brief
**Prima domanda, sempre: la modalità.** Con `AskUserQuestion`: "Automatica (consigliato): ti chiedo poco adesso, poi vado avanti da solo e ti fermo solo per il provino, il render finale e le spese" oppure "Guidata: ti chiedo a ogni fase".

**Brief rapido (automatica).** Chiedi solo tre cose, in un solo giro di `AskUserQuestion`: cosa c'è di sorgente (file, foto, link), **dove va il video** (Instagram/TikTok, sito o YouTube, fiera, presentazione) e cosa deve capire chi guarda. Il resto lo deduci dall'uso con le impostazioni qui sotto, più quello che trovi in memoria per il cliente (palette, logo, divieti):

| Uso | Formato | Durata | Ambiente e luce | Audio | Bozze |
|---|---|---|---|---|---|
| Instagram, TikTok, Shorts | 9:16 1080x1920, zona sicura `all` | 30 s | sfondo scuro, luce contrastata | voce + musica | predefinite |
| sito, YouTube | 16:9 1920x1080 | 45 s | limbo chiaro o studio nero | voce + musica, `.srt` | predefinite |
| fiera, schermo grande | 16:9 1920x1080 | 60 s, in loop | studio nero o capannone | solo musica, testi a schermo | predefinite |
| presentazione | 16:9 1920x1080 | 60 s | limbo chiaro, luce tecnica | voce, musica bassa | predefinite |

Budget di partenza, da confermare: render di bozza al massimo 3 h di GPU, crediti ElevenLabs per una voce e una musica (stima dai caratteri del testo e dalla durata), AI generativa 0 se il cliente non la chiede. Il render finale ha il suo ok a parte.
Poi mostra un **riepilogo in una schermata** (tutte le righe del Brief di `progetto.md`, compresi racconto in scene da 5–10 s (30 s ≈ 4 scene più qualche intermezzo), palette, modalità e budget) e chiedi una sola conferma, con la possibilità di cambiare qualsiasi riga. È la prima sosta: dopo l'ok non si torna sul brief se non lo chiede l'utente.
Le domande delle fasi successive (storyboard in PDF, lingue della voce, voce da scegliere, piattaforme) vanno in questo riepilogo, se servono: dopo non si chiedono più.

**Brief completo (guidata).** Chiedi, se non lo sai già:
- **Sorgenti**: foto, link, CAD o disegno. Cosa deve essere fedele (misure, colori, loghi) e cosa può essere approssimato.
- **Formato, prima di qualunque scena o render**: aspect ratio (9:16 1080x1920 · 16:9 1920x1080 · 1:1 1080x1080 · 4:5 1080x1350), risoluzione; gli fps sono sempre 24. Vanno impostati in ogni .blend. Per il 9:16 chiedi anche le piattaforme (Reels, Stories, TikTok o tutte): decidono la zona sicura per testi e grafiche (fase 4) e vanno nel brief, alla riga Formato.
- **Durata totale** e uso (social, sito, fiera, presentazione).
- **Qualità delle bozze**: chiedi con `AskUserQuestion` se fissare ora le qualità predefinite delle bozze, così non le chiedi a ogni passaggio, o se sceglierle passo passo. Opzioni: "Predefinite (consigliato)" con le proposte di partenza (storyboard `1-·-1`, anteprima di una scena `1-3-1`, montaggio `2-4-1`), "Predefinite, più veloci" (`1-·-1`, `1-2-1`, `1-3-1`), "Passo passo". L'utente può anche dare codici suoi. Il render finale si chiede comunque a parte.
- **Ambiente e atmosfera**:
  - ambiente: capannone o reparto produttivo, studio con sfondo nero, limbo bianco/grigio, esterno (cantiere, campo, piazzale), showroom o ufficio, sfondo astratto;
  - atmosfera e luce: tecnica e pulita, cinematografica e contrastata, calda o fredda, giorno o notte, fumo/polvere/riflessi a terra;
  - foto di riferimento dell'ambientazione o del look (facoltativa).
  Proponi 2–3 combinazioni adatte all'uso (social → scuro e contrastato; catalogo → limbo chiaro).
- **Racconto**: cosa deve capire chi guarda, scene di massima, testo del voice-over se c'è già. Costruiscilo come un arco, non come una lista di viste: aggancio (1–3 s, un dettaglio o un movimento che incuriosisce) → presentazione del pezzo intero → come funziona, dal fuori al dentro (sezione, esploso) → il beneficio o il numero chiave → chiusura con il prodotto intero e il logo.
- **Palette delle infografiche** (vale **solo per HyperFrames**: in Blender prodotto e ambiente hanno i loro colori reali). Se il cliente è in memoria usa i suoi colori e i suoi divieti. Altrimenti chiedi sempre, in uno di tre modi:
  - a parole ("blu scuro e bianco"): proponi tu gli Hex e falli confermare;
  - codici Hex;
  - un sito di riferimento: ricava la palette con `firecrawl_scrape` (formato `branding`) o dal CSS, mostrala e falla confermare.
  Chiedi anche il logo (SVG/PNG) e i colori da evitare. Con l'ok salva la palette in memoria per i video successivi dello stesso cliente.
- **Calcoli e tavole (facoltativo, con text-to-cad)**: chiedi se il video deve mostrare quanto regge un pezzo, sotto quale carico e con quale materiale, o una tavola tecnica quotata. Diventano scene in fase 2.
- **Alternativa veloce con `/teardown`** (se è installata): quando serve un video di "come funziona" in poco tempo e la fedeltà al prodotto vero non conta (idea, pitch, spiegazione di un principio), proponila al posto di Blender. `/teardown` ricostruisce la macchina a codice in three.js e registra un tour in mp4 con il suo sonoro: minuti invece di ore di render, ma forme e proporzioni sono approssimate e la resa non è quella di Cycles. Non usarla se servono misure, loghi o materiali veri, né mescolarla con scene Blender nello stesso video. Se l'utente la sceglie, segui la sua skill; da questa riprendi la domanda del render (risoluzione e durata; fps e qualità se `/teardown` li supporta), le zone sicure del 9:16 per i testi e la consegna (fase 9).
- **Extra facoltativo**: chiedi se serve anche una pagina 3D interattiva (esploso, sezione, numeri di funzionamento) per sito o fiera. Si fa in fase 9 con la skill `/machine` o `/teardown`, se installate.
Checkpoint: crea `progetto.md` con il brief e fallo confermare (in automatica è il riepilogo della prima sosta).

## 1. Il pezzo: modello, materiali, ambientazione

### 1a. Modello
Obiettivo: il prodotto in **metri reali**, centrato sull'origine e appoggiato a terra. Un solo comando per ogni file 3D o disegno 2D:
`blender -b --factory-startup --python $K/import_model.py -- <file> <out.blend> [m|cm|mm|in]`
Stampa `SIZE_M L x P x H`: confrontalo con una misura nota. Se è sbagliata di 10, 100 o 1000 volte, hai sbagliato l'unità.

**Formati accettati.** Quando l'utente chiede cosa mandare: **STEP** è il migliore (misure esatte, parti separate con il loro nome, pronto per esplosi e sezioni), poi **GLB**.

| Formato | Entra con `import_model.py` | Serve | Unità |
|---|---|---|---|
| **STEP / STP** | sì | **text-to-cad** (comando `cad`) | automatica: le parti restano separate con il loro nome |
| **3MF** | sì | **text-to-cad** | automatica |
| **GLB / glTF** | sì | niente | `m` (tiene colori e parti) |
| **Scheda KiCad** (`.kicad_pcb`) | sì, dopo `cad kicad_pcb export <scheda>.kicad_pcb --to glb --out source/pcb.glb` | **text-to-cad** (skill **text-to-cad:pcb**) | `m`; i componenti senza modello 3D restano fuori e l'export li nomina: chiedi i loro STEP o accetta la scheda senza |
| **Scheda KiCad** (`.kicad_pcb`) | sì, dopo `cad kicad_pcb export <scheda>.kicad_pcb --to glb --out source/pcb.glb` | **text-to-cad** (skill **text-to-cad:pcb**) | `m`; i componenti senza modello 3D restano fuori e l'export li nomina: chiedi i loro STEP o accetta la scheda senza |
| **FBX, OBJ, STL, PLY, USD/USDZ/USDC, ABC** | sì | niente | STL e OBJ da CAD sono quasi sempre in `mm` |
| **.blend** | sì, viene aperto e centrato | niente | `m` |
| **DWG** (solo 2D) | sì | **LibreDWG** (`brew install libredwg`, chiedi l'ok) | `mm` di default: chiedi l'unità del disegno |
| **SVG** | sì | niente | chiedi l'unità del disegno |
| **PDF vettoriale** | sì, la pagina 1, a grandezza reale sulla carta | **poppler** (`brew install poppler`, chiedi l'ok) | se il disegno è in scala 1:N, moltiplica per N e controlla una quota |
| **DXF** | no | chiedi l'export in SVG, DWG o PDF, oppure installa l'estensione "Import AutoCAD DXF" (con ok) | |
| **IGES/IGS, SolidWorks (SLDPRT/SLDASM), Inventor (IPT/IAM), Fusion (F3D), CATIA (CATPart), Creo (PRT/ASM), Parasolid (X_T), Rhino (3DM), SketchUp (SKP), Onshape** | no, Blender non li apre | chiedi l'export in **STEP** (con l'assieme, non il pezzo singolo) o in **GLB** | |

Note:
- STEP e 3MF passano da `cad ... export` in un GLB in metri (tolleranza 0,05 mm, curve lisce anche nei primi piani). Senza `cad` lo script lo dice: chiedi l'export GLB dal CAD.
- DWG: legge solo il 2D, cioè linee, archi e polilinee. Quote, testi e retini non vengono letti, e un DWG solo 3D, vuoto o di una versione recente non letta dà errore: in quel caso chiedi un export in SVG, PDF o STEP.
- Dai disegni 2D (DWG, SVG, PDF) si estrudono i profili o si ricostruiscono le parti in build123d (sotto). Controlla sempre la scala su una quota nota.

Altre sorgenti:

| Sorgente | Come procedere |
|---|---|
| **Disegno raster o schizzo** | Leggilo, trascrivi le quote in una tabella dentro `progetto.md` e modella in **build123d** (vedi sotto) con quelle quote come parametri. Le quote mancanti si chiedono, non si inventano. Senza `cad`, modella in Blender in Python (bmesh / geometry nodes). |
| **Foto** | Vedi sotto. |
| **Link** | Pagina prodotto → leggila (`firecrawl_scrape` o il browser integrato) per foto, misure, schede tecniche, codici colore; poi procedi come per foto/disegni. Link a un modello (GrabCAD, TraceParts, produttore, Sketchfab) → chiedi l'ok, controlla la licenza, poi `import_model.py`. Salva tutto in `source/`. |

**Da foto.** È la sorgente più lenta e la meno precisa: dillo subito.
- Foto che servono: fronte, retro, due lati, alto, una o due 3/4, primi piani di giunzioni, loghi, etichette, comandi. Luce diffusa, niente grandangolo spinto, possibilmente un metro o un oggetto di misura nota nell'inquadratura.
- Almeno **una misura reale** (lunghezza totale o altezza): senza, la scala è inventata.
- Monta le foto come riferimento (`bpy.ops.image.import_as_mesh_planes` o Empty immagine sugli assi) e modella a blocchi, poi dettaglia. Skill: **blender-director**, **hard-surface**, **prop-artist**.
- L'image-to-3D con AI (Higgsfield `generate_3d`, Magnific `models3d_generate`) serve solo per una bozza o per oggetti di contorno, mai per parti tecniche. Costa crediti: chiedi.

**Modellare in CAD parametrico (build123d)**, se è installato text-to-cad: per le parti meccaniche è più preciso e più veloce che modellare in Blender. Vale per disegni, schizzi, foto con misure e per le parti interne di una sezione.
- Script Python in `source/cad/<nome>.py`, eseguito con `cad run`: build123d è già incluso. Per le regole di modellazione usa la skill **text-to-cad:cad**.
- **Parti normalizzate da bd_warehouse**, a misura ISO vera, invece di inventarle: viti, dadi, rondelle, cuscinetti, ingranaggi, pulegge, filetti, tubi, flange. Lo script lo dichiara in testa:
  ```python
  # /// script
  # dependencies = ["bd_warehouse"]
  # ///
  ```
  Per esempio: `SpurGear(module=2, tooth_count=24, pressure_angle=20, root_fillet=0.5, thickness=10)`, `SingleRowDeepGrooveBallBearing(size="M8-22-7")`, `SocketHeadCapScrew(size="M6-1", length=20)`.
- **Una parte, un oggetto**: dai un `label` a ogni parte e salva il gruppo con `export_step(Compound(children=[...], label="Gruppo"), "<nome>.step")`. Con `Compound([...])`, senza `children`, le parti si fondono in una sola mesh, e poi esploso e animazione non si possono fare. Poi `cad step export` → GLB → `import_model.py`. Lo stesso cuscinetto arriva in Blender con anelli e sfere separati.
- Per controllare forma e misure prima di Blender: `cad step snapshot` (veduta rapida) e `cad step inspect` (ingombri).

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
**Scaletta delle inquadrature**, prima della prima scena: una tabella con tutte le scene in ordine, e per ognuna il piano, il movimento di camera e cosa racconta (la frase del voice-over, se c'è). Falla approvare e copiala nella tabella Scene di `progetto.md`. Piani, tradotti per una macchina (skill **camera-cinematography**):
- **ELS/LS** (totale): la macchina intera nel suo ambiente, con la scala umana se serve;
- **MS** (figura intera): la macchina riempie il quadro;
- **MCU**: un gruppo o un'unità (motore + pompa, la testa di taglio);
- **CU**: un componente (girante, ingranaggio, comando);
- **ECU/macro**: materiale, saldatura, logo, una vite che entra;
- **POV**: il punto di vista di un pezzo o del prodotto lavorato (la camera viaggia sul nastro, dentro il condotto, segue il fluido);
- **dall'alto / dal basso**: per il layout di un impianto o per dare imponenza.
Regole del montaggio:
- **Alterna i piani**: mai due tagli di fila con lo stesso piano e la stessa altezza di camera. Fra due scene cambia almeno piano o angolo di 30° o più.
- **Apri largo, poi stringi**: LS → MS → CU. Dopo 2–3 piani stretti torna a un piano largo, così chi guarda si riorienta e capisce dove si trova il dettaglio.
- **Il piano segue il racconto**: largo per presentare e dare contesto, stretto per spiegare e per i dettagli, POV o sezione per il momento "wow", largo per chiudere.
- **Durata delle scene: 5–10 s di default**, il tempo per leggere i testi e ascoltare la voce (a 2,5 parole al secondo, una frase di 15–20 parole vuole 6–8 s). Le scene con più testo, misure o un esploso stanno verso i 10 s. Le scene da **2–3 s** sono solo **intermezzi** (un dettaglio, un raccordo, un colpo di camera fra due scene), senza testo da leggere e al massimo una parola di voce; segnale nella scaletta con «intermezzo» e non metterne due di fila. Fa eccezione l'aggancio dei social, che può tagliare entro 2–3 s.
- **Continuità**: resta dallo stesso lato della macchina (regola dei 180°) e mantieni la direzione del movimento fra un taglio e l'altro. Taglia sul movimento (match cut) quando un pezzo si muove in due piani di fila.
- **Movimenti di camera**: alterna anche questi (orbita, dolly-in, carrello laterale, camera ferma). Non mettere due orbite di fila nello stesso verso.

**Riprese spettacolari**: oltre ai piani di presentazione e a quelli classici, ogni video ne ha diverse, circa una scena ogni 2–3. Sono quelle che sembrano impossibili, o fatte con un braccio robotico (motion control) o con un drone FPV. Proponile sempre, anche se l'utente non le chiede:
- **Velocità estreme e speed ramp**: un movimento lentissimo, tipo slow-mo, su un istante chiave (pezzo che si incastra, scintilla, goccia), poi un'accelerazione di colpo; oppure passaggi velocissimi con motion blur. In 3D lo slow-mo è gratis: l'animazione è procedurale, quindi basta rimappare il tempo con una curva (proprietà `t` sull'oggetto, letta dai driver) e campionare più fitto.
- **Follow e POV**: la camera segue un pezzo lungo il percorso, imparentata o con `Follow Path` e `Damped Track` (il prodotto sul nastro, il fluido nel condotto, la catena sugli ingranaggi). Oppure entra dentro la macchina passando da una fessura.
- **Braccio robotico**: traiettorie lunghe e precise che passano a pochi centimetri dalle parti, sfiorano un bordo, si fermano di colpo su un dettaglio e ripartono. Fai curve Bezier lisce, con accelerazioni nette all'inizio e alla fine.
- **Contromovimento**: mentre la macchina o un pezzo ruota, la camera orbita in verso opposto, così la rotazione sembra doppia. Funziona anche con un carrello laterale contro il nastro.
- **Cambio di vista in continuità**: senza tagli si passa dall'esploso alla sezione, o dal prodotto intero alla sezione, con il cutter che si apre mentre la camera entra. Oppure la camera attraversa un pannello che diventa trasparente.
- **Angolazioni insolite**: da sotto la macchina, da dentro un tubo, dall'alto a piombo con la camera che ruota sull'asse, a filo di pavimento, inclinata (dutch). Anche un dolly zoom (vertigo), o un fuoco che passa da un dettaglio all'altro (rack focus).
- **Raccordo veloce**: una frusta (whip pan) o un passaggio stretto fra due parti, che diventa il taglio verso la scena dopo.
Le scene spettacolari stanno fra piani più calmi, che danno respiro e contesto. Nella scaletta segnale con ★. Il motion blur e le traiettorie vicine alle parti si controllano nell'anteprima, non nello storyboard: il blur costa tempo di render, quindi attivalo solo nelle scene veloci.

Per **ogni** scena, prima di costruirla, chiedi:
- **Durata** in secondi.
- **Movimenti della macchina/del prodotto**: cosa si muove, a che velocità, in che ordine (es. nastro che scorre, sportello che si apre, esploso, montaggio dei pezzi).
- **Inquadrature**: il piano dalla scaletta (LS, MS, MCU, CU, ECU, POV, alto/basso) e il movimento della camera. Proponi 2–3 opzioni con **camera-cinematography**, almeno una spettacolare, sempre guardando i piani della scena prima e di quella dopo.
Costruisci con **Blender MCP** (`get_objects_summary`, `execute_blender_code`) o `blender -b file.blend --python script.py` (script in `render_scripts/`). Skill: **animation**, **geometry-nodes**, **procedural-modeling**.
- Animazione **procedurale** (driver + geometry nodes, niente simulazioni): così si può campionare a subframe e allungare i tempi senza toccare i keyframe.
- Prima di patchare un .blend salvane una copia nello scratchpad. Ogni patch è uno script Python rieseguibile.
- Proponi le inquadrature che una ripresa vera non può dare, sono il punto di forza del 3D:
  - **sezione**: modificatore Boolean `DIFFERENCE` (solver `EXACT`, `material_mode='TRANSFER'`) con un cutter che toglie un quarto verso la camera; il materiale del cutter colora le facce tagliate, di solito un rosso scuro. Prima svuota i gusci, con un cutter interno che ha lo stesso materiale del pezzo, e aggiungi le parti interne che servono al racconto (albero, rotore, girante). Se mancano dal CAD, falle in build123d, con cuscinetti, ingranaggi e viti veri presi da bd_warehouse. Animare il cutter fa aprire la sezione in scena;
  - **esploso** e rimontaggio, parti trasparenti o in radiografia, cambio di finitura o di colore.

**Storyboard (1 frame al secondo)**, prima di qualunque anteprima animata:
`JPG_Q=<q> $K/preview.sh <scena.blend> <first> <last> <fps_scena> preview/<n>_sb <res%> <spp>` (codice da `Bozze`, o domanda se passo passo; proposta `1-·-1`)
Rende un frame al secondo, con il numero di frame stampato, e crea `grid.jpg`. Guarda tu la griglia e controlla che il piano sia quello della scaletta e che non si ripeta con la scena vicina, poi mandala all'utente come storyboard. Ripeti finché non la approva.

**Storyboard da approvare: in chat o anche in PDF.** Quando tutte le scene hanno lo storyboard, chiedi: "Lo storyboard lo vuoi solo qui in chat, o anche in PDF da mandare al cliente per l'approvazione? In quali lingue?". Per il PDF scegli un frame per inquadratura (quello che la racconta meglio) e scrivi `storyboard.json` con titolo, lingue, colori del brand (`accent`, `ink`, da `progetto.md`) e per ogni inquadratura immagine, inizio e fine in secondi, piano e voce per lingua. Poi:
`python3 $K/storyboard_pdf.py storyboard.json delivery/storyboard` → `storyboard_<lingua>.pdf` (A4 orizzontale, 14 inquadrature per pagina, riquadro di approvazione nell'ultima, firma "Blender Product Video · Mario Mele" in fondo) e `vo_<lingua>.md`. Regole del PDF:
- testo sempre leggibile: niente corpi piccoli né pesi sottili (minimo 9,5 px per i testi, peso 500 o più); se non ci sta, accorcia il testo, non rimpicciolirlo;
- solo i colori del brand del cliente: `accent` per numeri ed etichette, `ink` per titoli e voce; mai colori fuori palette;
- guardalo tu prima di mandarlo (`sips -s format png` sulla prima pagina).

**Anteprima animata.** Usa il codice di `Bozze`, o fai la domanda delle tre scale se passo passo (proposta `1-3-1`: 25%, 12 fps, 8 spp), poi:
`JPG_Q=<q> $K/preview.sh <scena.blend> <first> <last> <step> preview/<n>_p <res%> <spp>` → `preview.mp4` a velocità reale.
**Scene facoltative con text-to-cad** (servono il comando `cad` e il pezzo in STEP):
- **Resistenza (FEA)**: il pezzo che si piega sotto carico mentre si colora dal blu al rosso, dove regge e dove è al limite. Con la skill **text-to-cad:fea**: scegli le facce bloccate e caricate (`cad step solve <pezzo>.step` le elenca), e prendi carico e materiale dal cliente: non si inventano. Poi `cad step solve <pezzo>.step --study study.json --out fea/`, e da lì:
  `cad run --with meshio $K/fea_surface.py fea/result.vtu fea/surface.npz`
  `blender -b --factory-startup --python $K/fea_to_blend.py -- fea/surface.npz fea/fea.blend <snervamento_MPa> [scala|auto] [first] [last]`
  Il .blend contiene l'oggetto `FEA`. Fra `first` e `last` il carico entra: il pezzo si deforma e passa dal metallo ai colori. Il rosso corrisponde allo snervamento, quindi rosso vuol dire "qui cede". Aggiungi camera e luci come in ogni scena, o collega l'oggetto (`Append`) nella scena del prodotto. In sovrimpressione, con HyperFrames, metti la scala colori, il carico in N o kg e il coefficiente di sicurezza da `result.json`. La deformazione è esagerata (il fattore lo stampa lo script): dillo in un testo a schermo. Fai approvare i numeri al cliente prima del render.
- **Movimento vero di un robot o di una macchina con giunti**: con la skill **text-to-cad:robot-simulation**, partendo dallo STEP del costruttore (la sua ricetta "from a vendor STEP": raggruppa le parti in link e trova gli assi dalla geometria). `cad model ranges <id>` trova i fine corsa di ogni giunto dove le parti si toccano; se il cliente ha la scheda tecnica con le escursioni degli assi, valgono quelle. In Blender metti il perno di ogni parte sull'asse del giunto e un vincolo `Limit Rotation` (o `Limit Location` per gli assi lineari) con quei limiti, poi anima dentro i limiti: il braccio si muove come quello vero, senza compenetrazioni. Scrivi gli assi e i limiti in `progetto.md`. URDF e MJCF servono solo se il cliente li vuole per la simulazione: non sono necessari per il video.
- **Movimento vero di un robot o di una macchina con giunti**: con la skill **text-to-cad:robot-simulation**, partendo dallo STEP del costruttore (la sua ricetta "from a vendor STEP": raggruppa le parti in link e trova gli assi dalla geometria). `cad model ranges <id>` trova i fine corsa di ogni giunto dove le parti si toccano; se il cliente ha la scheda tecnica con le escursioni degli assi, valgono quelle. In Blender metti il perno di ogni parte sull'asse del giunto e un vincolo `Limit Rotation` (o `Limit Location` per gli assi lineari) con quei limiti, poi anima dentro i limiti: il braccio si muove come quello vero, senza compenetrazioni. Scrivi gli assi e i limiti in `progetto.md`. URDF e MJCF servono solo se il cliente li vuole per la simulazione: non sono necessari per il video.
- **Tavola tecnica**: con la skill **text-to-cad:engineering-drawing** crea il PDF quotato dal modello, e convertilo in immagine con `sips -s format png`. Usi possibili nel video: la tavola che si dissolve nel pezzo 3D con la camera allineata alla vista frontale, oppure la tavola come piano in scena, con le linee che si accendono. Il PDF si consegna anche in fase 9.

Checkpoint: ok sulla scena, segnato in `progetto.md`, prima di passare alla successiva.

## 3. Montaggio multi-scena
- `edl.txt`, una scena per riga: `n file.blend first last [extra] [skip_head]`.
  - `extra`: frame aggiunti tramite subframe per dare respiro alla voce.
  - `skip_head`: primi N frame esclusi dal montaggio, senza cancellarli.
- Anteprima di tutto (codice da `Bozze`, o domanda se passo passo; proposta `2-4-1`): `SPP=8 JPG_Q=50 $K/render_all.sh <progetto> edl.txt 50 <fps>` → `preview_jpg/final.mp4` + `timings.json` (inizio e fine di ogni scena in secondi).
- `$K/contact_sheet.sh preview_jpg/final.mp4 preview/montaggio.jpg 1` per un provino.
- Se cambiano `first`, `last`, `extra` o la risoluzione di uno shot, `render_all.sh` sposta i frame vecchi in `<shot>.old_<data>` e rifà lo shot (i vecchi frame non corrispondono più agli stessi istanti).
Checkpoint: ordine, ritmo, transizioni. Sul provino controlla l'alternanza dei piani: niente due piani uguali di fila, un piano largo almeno ogni 2–3 piani stretti.

### Extra AI con Higgsfield MCP (facoltativo, costa crediti)
Il render Blender resta la base, e l'AI si usa solo dove migliora qualcosa senza cambiare il prodotto. Prima di ogni generazione controlla i crediti con `balance`, di' quanto costa e chiedi l'ok. Controlla ogni risultato fotogramma per fotogramma: l'AI può cambiare forme, loghi, scritte e numero di pezzi.
Usi consigliati:
- **Upscale** (`upscale_video`, `upscale_image`): render a risoluzione più bassa e poi upscale. Si risparmiano ore di GPU, ma va provato su uno shot prima.
- **Il pezzo in un mondo più grande**: la fabbrica dove lavora, la linea intera, la città o il cantiere che la usa, il prodotto finito che esce dalla macchina e arriva al cliente. Sono scene troppo grandi o complesse da costruire in Blender. Due modi, in ordine di fedeltà:
  1. **Composito**: Higgsfield genera solo il mondo (`generate_video` o `generate_image`, senza il prodotto, con camera e prospettiva descritte come la scena Blender), poi il prodotto renderizzato in Blender con sfondo trasparente (`film_transparent`, PNG RGBA) ci va sopra, con ombre da un piano shadow catcher. Il prodotto resta quello vero. Allinea altezza della camera, lunghezza focale e direzione della luce al plate generato.
  2. **Video da frame Blender**: si parte (o si arriva) su un frame Blender e l'AI fa il resto, per esempio la camera che si allontana dal pezzo fino a mostrare tutta la fabbrica. Il prodotto deve diventare piccolo in fretta. Il taglio torna su Blender per ogni dettaglio.
- **Persone** (`generate_video` / `generate_image` da un frame Blender): un operatore alla macchina, mani che montano un pezzo, il prodotto in uso. Blender non le fa bene. Il prodotto deve restare piccolo nell'inquadratura o fuori fuoco.
- **Intro e chiusure d'atmosfera**: fumo, luce, ambiente, che partono da un frame Blender o finiscono su un frame Blender, così il passaggio è invisibile.
- **Formati** (`reframe`, `outpaint_image`): da 16:9 a 9:16 o 1:1 senza ri-renderizzare, solo se il prodotto non viene tagliato.
- **Ambiente**: sfondi, backplate o texture generati (cemento, capannone) da usare in Blender.
Mai su sezioni, esplosi, FEA, quote, loghi, scritte o primi piani del prodotto: lì servono la geometria vera e i numeri veri, solo Blender. Segna in `progetto.md` quali scene contengono AI. Nella scaletta delle inquadrature proponi tu dove una scena AI farebbe la differenza (apertura nel mondo, chiusura sul prodotto in uso), perché l'utente spesso non sa che si può fare.

## 4. HyperFrames: testo e grafiche
- Chiedi se il **testo del voice-over** lo dà l'utente o lo scrivi tu. In quel caso scrivilo scena per scena, entro la durata di `timings.json` (circa 2,5 parole al secondo), in `audio/vo.txt` con una riga per scena: `n|testo`. Fallo approvare. Per registrare fuori (speaker, studio, altro TTS) genera anche i file `vo_<lingua>.md`, uno per lingua richiesta, con tempo, durata, numero di parole e testo per scena: `python3 $K/storyboard_pdf.py storyboard.json delivery/vo --no-pdf`.
- Chiedi quali **grafiche** servono: titoli, callout, misure, conteggi, lower third, sottotitoli, logo finale.
- Chiedi lo **stile delle grafiche**:
  - **solo HyperFrames**: pulite, precise, sempre nella palette. È il default;
  - **effetti Higgsfield + testo HyperFrames**: Higgsfield genera la parte spettacolare (transizioni, flussi di energia o di fluido, particelle, luci, sfondi animati per i titoli, intro d'impatto), sempre senza testo e senza numeri, chiedendo nel prompt i colori della palette. Sopra, HyperFrames mette titoli, numeri, misure e logo esatti. I modelli AI sbagliano le lettere e inventano cifre, quindi il testo non va mai generato. Costa crediti: chiedi l'ok, e prima prova un effetto solo. Gli effetti generati vanno in `hyperframes/assets/` e si usano come video di sfondo o in fusione (`screen`, `add`) sopra il render.
- Costruisci in `hyperframes/` con la skill **hyperframes** (contratto di render, animazioni, overlay e audio), nel formato del brief, **solo con la palette confermata**, `final.mp4` come sfondo e i tempi presi da `timings.json`. Le misure a schermo vengono dalla sorgente, mai stimate.
- **Zona sicura nel 9:16**: le interfacce di Reels, Stories e TikTok coprono l'alto, il basso e il lato destro. `$K/safe_zone.sh <WxH> <reels|stories|tiktok|all>` stampa i margini e la regola CSS `.safe`; senza indicazioni usa `all`, la più stretta delle tre (su 1080x1920: alto 250, basso 484, sinistra 60, destra 140 px). I testi importanti (titoli, numeri, misure, sottotitoli, CTA, logo) stanno sempre dentro la zona sicura, in un contenitore `.safe` (linea verde). Gli elementi secondari e le grafiche (icone, linee, cornici, decorazioni, bordi dei box) possono sconfinare nel margine al più del 20% in alto e in basso e del 10% ai lati (linea rossa), mai oltre. Sfondi, effetti e il render 3D possono occupare tutto il frame.
- **Nel 16:9 non ci sono zone delle piattaforme**: basta la zona sicura standard (azione al 90%, titoli e testi al 80% del frame), quella che HyperFrames già segue.
- **Cambiare formato vuol dire rifare l'impaginazione, non copiarla.** Da 9:16 a 16:9 (o 1:1, 4:5) e viceversa:
  - **scala** testi, grafiche, callout e logo in proporzione al nuovo frame: se li lasci con gli stessi px, nel 16:9 sembrano piccoli. Nelle composizioni usa misure relative al frame (percentuali, o una variabile di scala) invece di px fissi, così il cambio di formato le porta con sé;
  - **reimpagina** sugli spazi del nuovo formato: nel 16:9 testo e prodotto stanno affiancati, nel 9:16 uno sopra l'altro; i callout seguono dove cade il pezzo nella nuova inquadratura;
  - **zone sicure del formato di arrivo**: verso il 9:16 sempre `safe_zone.sh` con le piattaforme del brief, verso il 16:9 la zona standard;
  - poi rifai gli snapshot di controllo (sotto) sul nuovo formato e guarda che i testi si leggano alla stessa distanza di prima.
- **Verifica** prima di mostrare (skill **hyperframes-cli**):
  1. `npx hyperframes lint` dopo ogni modifica strutturale;
  2. `npx hyperframes check --json` e correggi ogni errore (layout, contrasto, elementi fuori campo);
  3. `npx hyperframes snapshot --at <metà di ogni scena da timings.json>` e guarda i PNG in `.hyperframes/artifacts/snapshots/`; nel 9:16 passa ogni PNG in `$K/safe_zone.sh <WxH> <piattaforma> <png> <png_guide>` e controlla che i testi importanti stiano dentro la linea verde e le grafiche secondarie dentro la rossa;
  4. `npx hyperframes preview --background` e dai il link all'utente.
Checkpoint: bozza HyperFrames muta (in automatica: controlli della fase 4, senza fermarti).

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
- Se c'è Ponytail, prima del render passa `/ponytail-review` su `render_scripts/` e sugli script delle scene, e correggi quello che trova.
- **Domanda delle tre scale** (vedi "Come lavorare"), proposta `4-4-3`, o `4-4-4` per schermi grandi e color grading.
- Prima di partire dai una stima: frame totali × s/frame. Riferimento: M1 Pro, 1080x1920, scena reale con denoise, su Metal: 8 spp circa 9 s/frame, 24 spp 19 s, 40 spp 25 s, 96 spp 56 s (la tabella in "Come lavorare"). Su CPU circa 4 volte di più.
- `$K/render_all.sh <progetto> edl.txt 100 <fps> [WxH]` con Bash `run_in_background`, così arriva la notifica a fine render. Avanzamento: `ls final_jpg/*/f*.jpg | wc -l`. Usa `gpu_setup.py` (Metal on, CPU off, MetalRT off su M1/M2 e automatico su M3+) e `render_seg_gpu.py` (shot `[a,b]` allungato di `extra` frame tramite subframe, JPG con qualità `JPG_Q`, ripartibile).
- Poi la composizione HyperFrames finale con `final_jpg/final.mp4` come sfondo: `npx hyperframes render --quality delivery -o delivery/video.mp4`. Controlla che la durata (`ffprobe`) coincida con quella della composizione.

## 8. Rifare un pezzo senza ri-renderizzare tutto
- Animazione cambiata solo nei frame master `[x,y]` di uno shot, con stessi `a b extra`:
  `SPP=<n> JPG_Q=<q> blender -b scena.blend --python $K/gpu_setup.py --python $K/render_seg_gpu.py -- a b extra final_jpg/<dir_shot> 100 [WxH] --redo x y` (stessi `SPP` e `JPG_Q` del render; il numero di frame lo riprende dal file `n` dello shot)
  Sovrascrive solo i frame che campionano `[x-1, y+1]`. Poi rilancia `render_all.sh` (salta i frame esistenti e rimonta) e verifica la giunzione con `contact_sheet.sh`.
- Se cambiano `extra` o la durata dello shot, ci pensa `render_all.sh` (fase 3): rifà lo shot intero e sposta i vecchi frame da parte.

## 9. Consegna
`$K/deliver.sh delivery/video.mp4 delivery [max_mb=28]` produce:
- `master.mp4`: H.264 alta qualità, audio normalizzato a **−14 LUFS** (−1 dBTP), faststart;
- `light.mp4`: sotto `max_mb` (default 28 MB), da mandare al telefono, su WhatsApp o per email.
Più `sottotitoli.srt` dalla fase 5. Limiti utili delle piattaforme:

| Piattaforma | Formato | Note |
|---|---|---|
| Instagram Reels / Stories / TikTok / Shorts | 9:16 1080x1920 | testi dentro la zona sicura (`safe_zone.sh`, fase 4), sottotitoli bruciati |
| Feed Instagram / LinkedIn | 4:5 1080x1350 o 1:1 | LinkedIn accetta il `.srt` separato |
| YouTube / sito | 16:9 1920x1080 | `.srt` separato |
Altri formati dallo stesso progetto: chiedi se servono. Vuol dire reimpostare la camera nei .blend e rifare il render: non basta ritagliare. Anche le grafiche HyperFrames vanno riscalate e reimpaginate per il nuovo formato, con le sue zone sicure (fase 4, "Cambiare formato").
Manda il `light.mp4` con SendUserFile; per file oltre 30 MB indica il percorso.

**Tavola tecnica**: se è stata fatta, consegna anche `delivery/<nome>_tavola.pdf`.

**Extra: pagina interattiva** (solo se chiesta nel brief e se `/machine` o `/teardown` è installata; con tutte e due chiedi quale). Usa la skill scelta per creare `delivery/<nome>.html`: un file unico in three.js, da aprire nel browser o mettere in un iframe, con esploso, sezione, radiografia e numeri calcolati. Passale le misure, la distinta dei pezzi con i materiali e i dati tecnici raccolti in `progetto.md`. Avvisa che la skill ricostruisce il pezzo con forme proprie: è una versione semplificata, non carica il modello Blender e ha una resa diversa da Cycles. Per questo non va montata dentro il video. Mostrala con uno screenshot e falla approvare a parte.

## Trappole
- Blender 5.x: action a livelli → `action.layers[].strips[].channelbags[].fcurves`; l'opzione MetalRT si chiama `metalrt` (non `metal_rt`).
- Aliasing a ruota di carro: se un movimento ripetitivo supera ~0,3 celle per frame, rallentalo o alterna i colori.
- macOS: niente `timeout` né `sed \n`; usa un ciclo di attesa e Python.
