---
name: blender-product-video
description: Workflow guidato per video 3D di prodotti, macchine, impianti o processi industriali fatti in Blender, partendo da foto, link, file CAD (STEP, 3MF, GLB, FBX, STL, OBJ, USD, .blend…) o disegni tecnici (DWG, SVG, PDF). In modalità guidata fa domande a ogni fase, in automatica chiede solo il brief e va avanti da sola fermandosi quattro volte (brief, testi, video con i testi, consegna) dentro un budget di render e crediti, in agentica divide il lavoro fra subagenti in parallelo (regista, sceneggiatore, motion designer, controllo del funzionamento, revisore tecnico, audio, riprese vere, spettatore) e manda le soste sul telefono. Il modello deve funzionare come la macchina vera (moti, versi, rapporti, ciclo), ricavato da CAD, PDF, testo, sito o video di riferimento; le riprese vere entrano come b-roll o in split screen con il 3D; tiene lo stato del progetto: modello e materiali, ambientazione, scene con storyboard e anteprime, montaggio, grafiche HyperFrames, voce/musica/SFX con ElevenLabs, render Cycles su GPU Metal, file di consegna. Usala quando l'utente vuole un video 3D o un'animazione Blender di un prodotto, o lavora su un progetto di questo tipo già avviato (storyboard o anteprima di una scena Blender, allungare le scene per la voce, rifare un pezzo, render finale su Metal, infografiche, voce o musica sopra un render 3D). Non usarla per video senza 3D (reel, montaggi di girato, podcast).
---

# Blender product video

Flusso guidato per un video 3D di un prodotto. Rispondi in italiano. I dettagli lunghi stanno in `references/`: ogni rimando dice quando leggerli.

## Come lavorare
- **Tre modalità**, chieste sempre come prima domanda del brief e scritte nella riga `Modalità` di `progetto.md`. Se la riga manca è un progetto vecchio: trattalo come guidato.
  - **guidata**: le domande e i checkpoint di ogni fase, come scritti sotto. Chiudi ogni fase con un **checkpoint**: mostra il risultato e chiedi l'ok prima di passare alla successiva. Le domande si fanno con `AskUserQuestion` (opzioni concrete, la consigliata per prima); non chiedere quello che sai già.
  - **automatica**: dopo il brief vai avanti da solo. Le domande delle fasi diventano scelte tue, fatte con le regole di questa skill e con il brief, scritte in `progetto.md` (Decisioni, una riga con il perché); i checkpoint diventano controlli tuoi. Ti fermi solo alle **quattro soste** (1 brief e scaletta, 2 testi, 3 video con i testi, 4 consegna) e per una spesa fuori budget, una cancellazione di file, un dato che non si inventa (testo della voce se il cliente lo vuole suo, carichi e materiali di un calcolo, colori del brand che non trovi, fedeltà di una parte che non si vede nelle sorgenti). Fra una sosta e l'altra solo brevi aggiornamenti.
  - **agentica**: il percorso dell'automatica, con il lavoro diviso fra subagenti che lavorano in parallelo e si controllano a vicenda, e le soste sul telefono. Variante **senza soste**, solo su richiesta.
  Per automatica e agentica leggi `references/automatica-agentica.md` (percorso, controlli, squadra, telefono, senza soste) all'inizio del progetto e a ogni sessione che lo riprende.
- **Stato in `progetto.md`**: leggilo all'inizio di ogni sessione, aggiornalo a ogni checkpoint o sosta. Le decisioni dell'utente stanno lì, non solo nella conversazione.
- **Entra nella fase giusta** ("Da dove partire"): il brief completo si fa solo per un progetto nuovo.
- **Qualità dei render**: ogni render ha un codice `risoluzione-fps-qualità` (domanda, tabella dei tempi e variabili degli script in `references/render-qualita.md`; leggila prima del primo render). Il **codice di bozza** (storyboard, anteprime, montaggio, redo di bozza) viene dalla riga `Bozze`: se è `predefinite` usa quel codice senza chiedere e dì in una riga quale usi e la stima dei tempi; se è `passo passo` o manca, fai la domanda prima di ogni render di bozza. Se l'utente chiede un'altra qualità per un passaggio, usala solo lì; con "d'ora in poi" aggiorna `Bozze`.
- **Ok al render finale, una regola sola.** Il render finale e i suoi redo partono solo con un ok esplicito che contiene il codice di qualità e la stima delle ore, scritto nella riga `Ok render finale` di `progetto.md`. "Renderizza" senza codice non basta: fai la domanda. In guidata l'ok arriva al checkpoint della fase 6; in automatica e agentica alla sosta 3, insieme all'ok alla voce; senza soste vale il codice del brief entro `finale ≤ N h` del budget. Una stima oltre il budget si chiede sempre a parte.
- **Spese**: mai partire per inerzia con un render lungo, un download o una generazione a pagamento (voce, musica, SFX, modelli AI). In automatica e agentica vale la riga `Budget`: dentro il budget vai e segna ogni spesa e ogni render con il suo tempo in `Speso`; prima di superarlo fermati e chiedi. Installazioni e download chiedono sempre l'ok. Prima di cancellare file chiedi sempre; meglio spostare in `old_*`.
- **L'utente comanda sempre**, anche fra una sosta e l'altra:
  - **"stop"**: fermi subito quello che gira (i frame già fatti restano, `render_all.sh` riparte da lì), aggiorni `progetto.md` con il punto in cui sei e aspetti "continua";
  - **"rifai…" o una richiesta nuova** ("cambia l'ambiente", "aggiungi una scena"): vai alla fase giusta, fai solo quel pezzo e rifai a valle solo quello che dipende da lui;
  - **"rifai questa scena"**: solo quella scena (fase 2 per animazione o camera, fase 8 per rifare dei frame), poi il montaggio rifà solo i suoi shot.
- **Codice minimo con Ponytail** (se il plugin è installato; consigliato): ogni script del progetto (scene, patch, build123d, composizioni HyperFrames) segue `/ponytail`. Usa prima gli script di `$K` e quelli già in `render_scripts/`, poi la patch più corta che funziona. Prima del render finale passa `/ponytail-review` sugli script del progetto: un errore trovato lì vale ore di GPU.
- **Mandare file all'utente**: `SendUserFile` (status `proactive` alle soste). Se non c'è, o il file supera 30 MB, scrivi il percorso completo.

Cartella di progetto: `progetto.md`, `funzionamento.md`, `storyboard.json`, `source/` (materiale originale, mai modificato; le riprese vere in `source/video/`), `*.blend`, `render_scripts/`, `edl.txt`, `preview/`, `preview_jpg/`, `final_jpg/`, `hyperframes/`, `audio/`, `delivery/`. Gli script stanno in `K=~/.claude/skills/blender-product-video/scripts`. Blender: `B=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}`; nei comandi usa sempre `"$B"`, mai `blender` da solo.

### progetto.md
```markdown
# <Nome progetto>
Fase attuale: <0–9> · <cosa manca>
## Brief
Formato: 9:16 1080x1920, 24 fps · Piattaforme: Reels, TikTok · Durata: 45 s · Uso: Instagram
Cosa deve capire chi guarda: <una frase>
Lingue: storyboard it · voce it, en
Bozze: predefinite · storyboard 1-·-1 · anteprima 1-3-1 · montaggio 2-4-1 (oppure: passo passo)
Modalità: automatica (oppure: guidata, agentica, agentica senza soste) · Agenti: max 3 insieme
Budget: bozze ≤ 3 h GPU · finale ≤ 12 h GPU (codice 4-4-3) · ElevenLabs ≤ 5000 crediti · AI ≤ 0
Speso: render 0 h · ElevenLabs 0 · AI 0
Ok render finale: <data, codice, stima ore> (vuoto finché non c'è)
Sorgenti: source/… · Fedeltà: A/B/C (fase 1b)
Funzionamento: funzionamento.md (fase 1a) · Riprese vere: source/video/… (b-roll, split, vero→3D)
Ambiente: … · Atmosfera: … · Foto ref: source/…
Palette infografiche (solo HyperFrames): #…, #… · Logo: source/… · Da evitare: …
Racconto: … · Trattamento: trattamento.md (agentica)
## Scene
| n | file | frame | durata | piano | movimento / camera | cosa racconta | storyboard | anteprima | finale |
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
| "non funziona così", "controlla che si muova come la vera" | 1a, poi 2 per le scene che sbagliano |
| "ho dei video veri", "split screen", "b-roll" | `references/riprese-vere.md` (e la scaletta in 2) |
| "metti un'infografica / un titolo / i sottotitoli" | 4 |
| "voce", "musica", "effetti sonori" | 5 |
| "render finale", "passa a Metal" | 7 (con l'ok scritto in `progetto.md`) |
| "esporta", "mandamelo", "versione per Instagram" | 9 |
Se manca `progetto.md` ma il progetto esiste (ci sono .blend ed EDL), ricostruiscilo dai file e chiedi conferma solo dei buchi. Se per la richiesta serve un dato che manca (es. formato prima di un render), chiedi solo quello.

## Skill Blender: obbligatorie, le piloti tu
Questa skill è il regista: decide fasi, domande, checkpoint e stato. Il mestiere Blender sta nelle skill di [arjun988/blender-skills](https://github.com/arjun988/blender-skills) (MIT), **obbligatorie**.
- **All'avvio di ogni sessione** lancia `$K/check_skills.sh`. Se stampa `MISSING`, fermati: mostra quali mancano e i comandi di installazione che stampa, e installale solo dopo l'ok. Senza quelle skill non si va oltre il brief. `OPTIONAL_MISSING` non ferma: quelle si caricano solo se il passo le usa, e se mancano lo fai senza.
- **Prima di ogni passo della tabella, caricala con lo strumento Skill** (una volta per sessione). Le sue regole valgono dentro i limiti di questa skill: se una va contro questa skill vince questa, se va contro l'utente vince l'utente.
- Non seguire il routing di **blender-director** verso stili da videogioco, LOD, export per motori o retopologia: qui si fa un video, con materiali e misure veri.

| Passo | Carica |
|---|---|
| 1b modello da foto, link o disegno | **blender-director**, poi **hard-surface** e **prop-artist** |
| 1b modello da CAD (import o pulizia) | **hard-surface** (oltre ~2 M triangoli: **asset-optimization**, facoltativa) |
| 1c materiali e texture | **materials**, **texture-workflow**, **lookdev** |
| 1d ambientazione e luce | **lighting**, **lookdev** (set: **environment-artist**, **set-dressing**, facoltative) |
| 2 scaletta, piani e camera | **camera-cinematography** |
| 2 animazione, esploso, cavi, scatter | **animation**, **geometry-nodes**, **procedural-modeling** |
| 2 anteprime, 7 render finale | **rendering** |

## 0. Brief
**Prima domanda, sempre: la modalità.** Con `AskUserQuestion`: "Automatica (consigliato): ti chiedo poco adesso, poi vado avanti da solo e mi fermo quattro volte: brief e scaletta, testi, video con i testi, consegna", "Agentica: come l'automatica, ma con una squadra di agenti (regista, sceneggiatore, motion designer, controllo del funzionamento, revisori) che lavorano in parallelo e si controllano a vicenda, e le soste sul telefono; più controllata, consuma più token" oppure "Guidata: ti chiedo a ogni fase". La variante senza soste solo se l'utente la chiede.

**Brief rapido (automatica e agentica).** Quattro domande in un solo giro di `AskUserQuestion`: cosa c'è di sorgente (file, foto, link, PDF, descrizione di come funziona, video della macchina vera o riprese da inserire), **dove va il video** (Instagram/TikTok, sito o YouTube, fiera, presentazione), **cosa deve capire chi guarda**, e **la sua idea di storia**: "Hai già un'idea di come raccontarlo? Anche in due righe (cosa si vede all'inizio, cosa si mostra, come finisce), oppure Decidi tu". Con un'idea la scaletta parte da lì e la rispetta; con "Decidi tu" la costruisci dall'arco del racconto (sotto). Il resto lo deduci dall'uso, più quello che trovi in memoria per il cliente (palette, logo, divieti):

| Uso | Formato | Durata | Ambiente e luce | Audio |
|---|---|---|---|---|
| Instagram, TikTok, Shorts | 9:16 1080x1920, piattaforme `all` | 30 s | sfondo scuro, luce contrastata | voce + musica |
| sito, YouTube | 16:9 1920x1080 | 45 s | limbo chiaro o studio nero | voce + musica, `.srt` |
| fiera, schermo grande | 16:9 1920x1080 | 60 s, in loop | studio nero o capannone | solo musica, testi a schermo |
| presentazione | 16:9 1920x1080 | 60 s | limbo chiaro, luce tecnica | voce, musica bassa |

Bozze `predefinite`. Budget di partenza, da confermare: bozze ≤ 3 h di GPU, finale con la stima del codice `4-4-3` sulla durata (`references/render-qualita.md`), crediti ElevenLabs per una voce e una musica (stima in fase 5), AI generativa 0 se il cliente non la chiede.
Poi un **riepilogo in una schermata**: tutte le righe del Brief di `progetto.md` (lingue di storyboard e voce, voce, musica sì o no, piattaforme, modalità e budget), la scheda di funzionamento con le domande aperte e la scaletta (sua o tua). Chiedi una sola conferma, con la possibilità di cambiare qualsiasi riga. È la sosta 1: dopo non si torna sul brief se non lo chiede l'utente.

**Brief completo (guidata).** Chiedi, se non lo sai già:
- **Sorgenti**: foto, link, CAD o disegno. Cosa deve essere fedele (misure, colori, loghi) e cosa può essere approssimato.
- **Come funziona**: tutto quello che spiega il funzionamento (scheda tecnica o manuale, descrizione a parole, pagina del sito, video della macchina in lavoro). Serve alla fase 1a.
- **Riprese vere da montare** (facoltative): video del cliente per b-roll, split screen o passaggio vero→3D, in `source/video/`, con l'ok a usarle (diritti, persone riconoscibili).
- **Formato, prima di qualunque scena o render**: aspect ratio (9:16 1080x1920 · 16:9 1920x1080 · 1:1 1080x1080 · 4:5 1080x1350), risoluzione; fps sempre 24, da impostare in ogni .blend. Nel 9:16 anche le piattaforme (Reels, Stories, TikTok o tutte): decidono la zona sicura dei testi.
- **Durata**, uso, **cosa deve capire chi guarda**, **lingue** di storyboard e voce.
- **Qualità delle bozze**: "Predefinite (consigliato)" (`1-·-1`, `1-3-1`, `2-4-1`), "Predefinite, più veloci" (`1-·-1`, `1-2-1`, `1-3-1`) o "Passo passo"; vanno bene codici suoi.
- **Ambiente e atmosfera**: capannone, studio nero, limbo bianco/grigio, esterno, showroom o ufficio, sfondo astratto; luce tecnica o cinematografica, calda o fredda, giorno o notte, fumo, polvere, riflessi a terra; foto di riferimento facoltativa. Proponi 2–3 combinazioni adatte all'uso (social → scuro e contrastato; catalogo → limbo chiaro).
- **Racconto**: scene di massima, testo della voce se c'è già. È un racconto con un problema da risolvere, non una lista di viste o di dati: **aggancio** (1–3 s: una domanda, un problema, un dettaglio che incuriosisce) → il problema di chi usa la macchina → la macchina intera → come lo risolve, dal fuori al dentro (sezione, esploso) → la prova (il numero chiave) → cosa cambia per chi la usa → chiusura con il prodotto intero e il logo.
- **Palette delle infografiche** (solo HyperFrames: in Blender prodotto e ambiente hanno i colori reali). Se il cliente è in memoria usa i suoi colori e divieti. Altrimenti a parole (proponi tu gli Hex), codici Hex, o da un sito (`firecrawl_scrape` formato `branding`, o dal CSS), sempre da confermare. Chiedi anche logo (SVG/PNG) e colori da evitare; con l'ok salva la palette in memoria per il cliente.
- **Facoltativi**: calcoli di resistenza, movimento vero di un robot o tavola quotata (`references/text-to-cad.md`); video veloce senza fedeltà o pagina 3D interattiva (`references/teardown-machine.md`).
Checkpoint: crea `progetto.md` con il brief e fallo confermare.

## 1. Il pezzo: funzionamento, modello, materiali, ambientazione

### 1a. Funzionamento
Il modello deve replicare **come funziona** la macchina, non solo come appare: cosa si muove, in che verso, a che velocità, in che ordine, mosso da cosa. Un ingranaggio che gira nel verso sbagliato lo nota subito chi la macchina la conosce, cioè il cliente. Prima di modellare scrivi `funzionamento.md` da tutte le sorgenti (CAD, PDF, testo, sito, video), una riga per parte mobile con la sua fonte, più ciclo, flussi e vincoli. Quello che non si ricava si chiede, non si inventa. Scheda, cinematica e verifica con `motion_probe.py`: `references/funzionamento.md`.

### 1b. Modello
Obiettivo: il prodotto in **metri reali**, centrato sull'origine e appoggiato a terra, con le parti mobili della scheda come oggetti separati, perno sul loro asse. Un solo comando per ogni file 3D o disegno 2D:
`"$B" -b --factory-startup --python $K/import_model.py -- <file> <out.blend> [m|cm|mm|in]`
Stampa `SIZE_M L x P x H`: confrontalo con una misura nota. Se è sbagliata di 10, 100 o 1000 volte, hai sbagliato l'unità. Formati accettati (STEP il migliore, poi GLB), disegni, foto, link e CAD parametrico con build123d: `references/sorgenti-modello.md`.

**Livello di fedeltà**, da concordare e scrivere in `progetto.md`: **A** da CAD, geometria esatta; **B** da disegno quotato o foto + misure, forme e proporzioni fedeli (±2–5%), dettagli non visibili semplificati; **C** da sole foto, aspetto credibile, proporzioni approssimate, parti nascoste inventate.
Pulizia: merge dei vertici duplicati, normali, shade auto smooth, nomi chiari delle parti. Oltre ~2 M di triangoli: decimate sulle parti nascoste. Migliaia di oggetti da CAD: unisci per materiale le parti ferme.

### 1c. Materiali e texture
Chiedi i **colori reali** (RAL/Pantone dalla scheda, campionati dalle foto in una zona ben illuminata, o dall'utente; in sRGB in `progetto.md`), le **finiture** (inox spazzolato o lucido, alluminio, verniciato lucido/opaco/goffrato, plastica, gomma, vetro, zincato) e **loghi, etichette, targhe** (SVG/PNG del cliente, come decal).
- Principled BSDF con valori fisici: metalli `metallic 1`, roughness 0,15–0,45; vernici `metallic 0`, roughness 0,3–0,6, coat per il lucido; gomma roughness 0,7–0,9.
- **Procedurale prima di tutto** (noise, voronoi, anisotropia per lo spazzolato, piccola variazione di roughness, usura sui bordi con pointiness/AO): niente UV, leggero.
- Mesh da CAD senza UV: mappatura **box/triplanare** su coordinate oggetto. UV solo dove va un decal (UV project dalla vista).
- Texture a immagine (Poly Haven, ambientCG) solo se servono davvero, con l'ok per il download, in `source/textures/`.
- Il colore si verifica sul **frame renderizzato** accanto alla foto o al codice: la view transform (AgX) lo sposta. Se il cliente è pignolo, view transform Standard o correggi il materiale.

### 1d. Ambientazione
- **Studio nero o limbo**: piano curvo senza orizzonte, luce a tre punti o softbox, riflesso leggero a terra.
- **Capannone, esterno, showroom**: set essenziale (pavimento, pareti, pochi elementi di contorno) e HDRI coerente. HDRI e asset gratuiti solo con l'ok per il download.
- **Con foto di riferimento**: a 360° equirettangolare → HDRI del mondo; normale → ricavane luce, colori, materiali e altezza della camera e ricostruisci un set simile. Come backplate vero: allinea la camera alla prospettiva e metti un piano shadow catcher.
- L'ambiente è contorno: il protagonista è il prodotto. Profondità di campo e volumetrici costano tempo di render: dillo prima.
Checkpoint: 3–4 viste statiche (fronte, 3/4, dettaglio, materiale da vicino) nell'ambientazione, accanto alla foto di riferimento, con `preview.sh` su un frame (`<f> <f> 1`). Chiedi se forma, proporzioni, materiali e atmosfera vanno bene.

## 2. Le scene, una alla volta
**Scaletta delle inquadrature**, prima della prima scena: tutte le scene in ordine, con piano, movimento di camera e cosa racconta (la frase della voce, se c'è). Falla approvare e copiala nella tabella Scene. Piani (skill **camera-cinematography**): **ELS/LS** la macchina intera nel suo ambiente; **MS** la macchina riempie il quadro; **MCU** un gruppo (motore + pompa); **CU** un componente; **ECU/macro** materiale, saldatura, logo; **POV** il punto di vista di un pezzo (sul nastro, dentro il condotto); **dall'alto / dal basso** per il layout o l'imponenza. Ogni 2–3 scene una ripresa spettacolare, segnata ★ (`references/riprese-spettacolari.md`); le scene con riprese vere segnate «vero», «split», «vero→3D»; le scene AI solo da `references/higgsfield.md`.

**Regole del montaggio** (valgono per scaletta, provino e controlli):
- **Alterna i piani**: mai due tagli di fila con lo stesso piano e la stessa altezza di camera; fra due scene cambia piano o angolo di almeno 30°. Alterna anche i movimenti di camera: mai due orbite di fila nello stesso verso.
- **Apri largo, poi stringi** (LS → MS → CU) e dopo 2–3 piani stretti torna a un piano largo. Largo per presentare e chiudere, stretto per spiegare, POV o sezione per il momento "wow".
- **Durata: scene da 5–10 s**, il tempo di leggere i testi e ascoltare la voce (a 2,5 parole al secondo, 15–20 parole vogliono 6–8 s). Le scene da **2–3 s** sono solo **intermezzi** («intermezzo» in scaletta): niente testo da leggere, al massimo una parola di voce, mai due di fila. Fa eccezione l'aggancio dei social. Un video di 30 s ≈ 4 scene più qualche intermezzo.
- **Continuità**: stesso lato della macchina (regola dei 180°), stessa direzione del movimento fra un taglio e l'altro, match cut quando un pezzo si muove in due piani di fila.

Per **ogni** scena chiedi: **durata**; **cosa si muove** (il moto viene dalla scheda della fase 1a: si sceglie solo quale parte del ciclo mostrare e se rallentarla); **inquadratura** e movimento di camera, con 2–3 opzioni di cui almeno una spettacolare, guardando la scena prima e quella dopo.
Costruisci con **Blender MCP** (`get_objects_summary`, `execute_blender_code`) o `"$B" -b file.blend --python script.py` (script in `render_scripts/`).
- Animazione **procedurale** (driver + geometry nodes, niente simulazioni), tutta da una proprietà `t`: così si campiona a subframe e si allungano i tempi senza toccare i keyframe. Dopo ogni scena animata, la verifica con `motion_probe.py` (`references/funzionamento.md`).
- Prima di patchare un .blend salvane una copia nello scratchpad. Ogni patch è uno script Python rieseguibile.
- Le inquadrature che una ripresa vera non può dare: **sezione** (Boolean `DIFFERENCE`, solver `EXACT`, `material_mode='TRANSFER'`, cutter che toglie un quarto verso la camera e colora le facce tagliate di rosso scuro; prima svuota i gusci e aggiungi le parti interne del racconto, da build123d con pezzi veri di bd_warehouse; animare il cutter apre la sezione in scena), **esploso** e rimontaggio, parti trasparenti o in radiografia, cambio di finitura.

**Storyboard (1 frame al secondo)**, prima di qualunque anteprima animata, con il codice di bozza: `JPG_Q=<q> $K/preview.sh <scena.blend> <first> <last> <fps_scena> preview/<n>_sb <res%> <spp>`. Crea `grid.jpg` con il numero di frame: controlla che il piano sia quello della scaletta e non si ripeta con la scena vicina, poi mandala come storyboard e ripeti finché non è approvata.
**Storyboard in PDF.** `storyboard.json` è la fonte unica dei testi: titolo, lingue, colori del brand (`accent`, `ink`) e per ogni scena dell'EDL, nello stesso ordine, immagine, inizio e fine in secondi, piano, testo a schermo e voce per lingua. Lo scrivi solo tu. Poi `python3 $K/storyboard_pdf.py storyboard.json delivery/storyboard` → `storyboard_<lingua>.pdf` (A4 orizzontale, riquadro di approvazione, firma "Blender Product Video · Mario Mele"), `vo_<lingua>.md` (da registrare o da far correggere) e `vo_<lingua>.txt` (`n|testo`, per voce e sottotitoli). Testo sempre leggibile (minimo 9,5 px, peso 500 o più; se non ci sta accorcia il testo), solo i colori del brand; guardalo tu prima di mandarlo (`sips -s format png` sulla prima pagina). In guidata chiedi se il PDF serve e in quali lingue; in automatica si fa sempre, alla sosta 2.
**Anteprima animata**, con il codice di bozza: `JPG_Q=<q> $K/preview.sh <scena.blend> <first> <last> <step> preview/<n>_p <res%> <spp>` → `preview.mp4` a velocità reale.
`preview.sh` si ferma con `GUI_BLENDER_OPEN` (exit 3) e `HANG` (exit 2) come `render_all.sh`: vedi fase 7.
Checkpoint: ok sulla scena, segnato in `progetto.md`, prima di passare alla successiva.

## 3. Montaggio multi-scena
- `edl.txt`, una scena per riga: `n file.blend first last [extra] [skip_head]`. `extra`: frame aggiunti con i subframe per dare respiro alla voce; `skip_head`: primi N frame esclusi dal montaggio, senza cancellarli.
- Anteprima di tutto, con il codice di bozza: `SPP=<n> JPG_Q=<q> $K/render_all.sh <progetto> edl.txt <res%> <fps> [WxH]` → `preview_jpg/final.mp4` + `timings.json` (inizio e fine di ogni scena in secondi). Ripartibile: salta i frame già fatti. Se cambiano `first`, `last`, `extra`, risoluzione, fps o qualità di uno shot, sposta i frame vecchi in `<shot>.old_<data>` e lo rifà.
- `$K/contact_sheet.sh preview_jpg/final.mp4 preview/montaggio.jpg 1` per un provino.
- Riprese vere: `references/riprese-vere.md`.
Checkpoint: ordine, ritmo, transizioni; sul provino le regole del montaggio della fase 2.

## 4. HyperFrames: testo e grafiche
- **Chi scrive i testi**: chiedi se la voce la dà l'utente o la scrivi tu (in agentica lo sceneggiatore, che ti rende `testi.md`). I testi vanno in `storyboard.json`, scena per scena, entro la durata di `timings.json` (circa 2,5 parole al secondo); poi `storyboard_pdf.py` (anche con `--no-pdf`) rigenera `vo_<lingua>.md` e `vo_<lingua>.txt`. Le correzioni dell'utente sui `.md` le riporti in `storyboard.json` e rilanci lo script.
- **Scrivere voce e testi: racconto, non elenco**:
  - segui l'arco del racconto (fase 0): ogni scena porta avanti il filo del problema risolto, non aggiunge una scheda tecnica;
  - **ogni dato risponde a "e quindi?"**: non "portata 1200 kg/h" ma "1200 kg all'ora: un turno intero senza fermarsi"; al massimo **un numero per scena**, ed è la prova della frase;
  - **voce e testo a schermo non si ripetono**: la voce dice il perché, il testo dice il nome o il numero;
  - **un'idea per scena**, frasi corte da dire ad alta voce, verbi attivi, niente sigle non spiegate, il tono del cliente;
  - **aggancio**: proponine 2–3 diversi (una domanda, un problema, un'immagine) e fai scegliere;
  - **niente affermazioni senza fonte**: ogni numero viene da `funzionamento.md` o dalle sorgenti; superlativi solo se il cliente li documenta;
  - **chiusura**: cosa resta a chi guarda, poi il logo; una call to action solo se il brief la chiede.
- **Grafiche animate: controlla il movimento, non solo i fotogrammi** (in agentica il motion designer):
  - **tempi**: ogni testo entra quando la voce lo nomina o quando il pezzo si muove, ed esce dopo; resta almeno 1 s più 0,3 s per parola;
  - **gerarchia**: una cosa alla volta; il titolo della scena prima, il dettaglio dopo; mai due testi che entrano insieme in punti diversi;
  - **coerenza**: stesse curve, stessi tempi di entrata e uscita, stessa posizione per lo stesso tipo di elemento in tutto il video;
  - **spazio**: i callout indicano la parte senza coprirla e la seguono se si muove;
  - **controllo**: snapshot all'inizio, a metà e alla fine di ogni grafica, e `grafiche.md` con entrata, uscita e durata di ogni elemento confrontate con la voce.
- Chiedi quali **grafiche** servono (titoli, callout, misure, conteggi, lower third, sottotitoli, logo finale) e lo **stile**: solo HyperFrames (pulite, nella palette; il default) o effetti Higgsfield sotto testi HyperFrames (`references/higgsfield.md`, costa crediti).
- Costruisci in `hyperframes/` con la skill **hyperframes**, nel formato del brief, **solo con la palette confermata**, `final.mp4` come sfondo (con le riprese vere, la sequenza di `references/riprese-vere.md`) e i tempi di `timings.json`. Le misure a schermo vengono dalla sorgente, mai stimate.
- Zone sicure, cambio formato e verifica (`lint`, `check`, snapshot, preview): `references/hyperframes.md`, da leggere prima di costruire.
Checkpoint: bozza HyperFrames muta (in automatica la sosta 3 arriva dopo questa fase).

## 5. Audio: voce, musica, SFX (ElevenLabs MCP)
Ogni generazione costa crediti: chiedi l'ok prima, con la stima. **Stima**: `creative_generate_speech` con `estimate_only: true` dà il costo esatto; a occhio la voce costa circa 1 credito per carattere del testo (circa la metà con i modelli flash e turbo), per ogni lingua e ogni take (di default lo strumento ne fa 2). Musica e SFX: chiedi la stima allo strumento prima di lanciarli.
- **Voce**: `creative_list_voices` → 2–3 voci (lingua, tono), fanne scegliere una → `creative_generate_speech` scena per scena dalle righe di `vo_<lingua>.txt`, sullo stesso flow. **Scaricale**: `creative_get_generations` dà il `full_res_url` di ogni take; `curl -L -o audio/vo_<lingua>_<n>.mp3 '<url>'` con la take scelta. Se un URL non si scarica, chiedi all'utente di salvare i file dal flow in `audio/` con quei nomi. Voce e voice_id in `progetto.md`.
- **Adatta le scene alla voce**: `python3 $K/fit_vo.py edl.txt <fps del .blend> 1=audio/vo_it_1.mp3 2=audio/vo_it_2.mp3 … [--pad 0.5]` riscrive `extra` perché ogni scena duri almeno quanto la sua voce più il margine (con più lingue usa la più lunga per scena). Poi rifai il montaggio (fase 3, gli shot con `extra` cambiato vengono rifatti).
- **Dopo `fit_vo.py` le grafiche vanno riallineate**: `timings.json` cambia e i testi entrerebbero in anticipo. Segui "Dopo fit_vo.py" in `references/hyperframes.md`, sul `timings.json` del render che stai per usare.
- **Sottotitoli** dal render finale: `python3 $K/make_srt.py final_jpg/timings.json delivery/storyboard/vo_<lingua>.txt delivery/sottotitoli_<lingua>.srt 'audio/vo_<lingua>_{n}.mp3'` (per la bozza `preview_jpg/timings.json`). File `.srt` per YouTube/LinkedIn, o bruciati in HyperFrames per i social.
- **Musica** (opzionale): genere, mood, tempo e se chiude sul logo. Con `creative_generate_in_flow`: nodo `music` (`eleven_music_v2_5`, `instrumental: true`, `duration_seconds` = durata del video), oppure nodo `video-to-music` collegato a `preview_jpg/final.mp4`. In alternativa la skill **media-use**. Si scarica come la voce, in `audio/musica.mp3`.
- **SFX** (opzionale): suoni legati ai movimenti (motore, scorrimento, clic, sportello, whoosh), ciascuno con l'istante da `timings.json`. Nodo `sfx` (`eleven_text_to_sound_v2`, 0,5–30 s, `loop: true` per i suoni continui).
- **Mix** in HyperFrames (skill **hyperframes**, parte audio): voce in primo piano, musica abbassata sotto la voce, SFX sincronizzati.

## 6. Visione d'insieme
Bozza della composizione completa (`npx hyperframes render --quality draft -o preview/insieme.mp4`): anteprima + grafiche + audio. Mandala e chiedi un giudizio su ritmo, voce, musica, leggibilità. Le correzioni tornano alla fase giusta (scena → 2, testo/grafica → 4, audio → 5).
Checkpoint (guidata): **ok al render finale** con codice e stima, nella riga `Ok render finale` (regola in "Come lavorare").

## 7. Render finale (GPU Metal)
- **Chiudi ogni Blender con GUI aperto** (anche quello dell'MCP): con un Blender GUI aperto, Metal in headless si blocca all'avvio (0% CPU). `render_all.sh` e `preview.sh` lo controllano e si fermano (`GUI_BLENDER_OPEN`, exit 3). Se si blocca durante il render, il watchdog lo interrompe dopo `HANG_MIN` minuti (default 10) senza frame nuovi (`HANG`, exit 2). Allora diagnostica (cubo con `--factory-startup`, `ps` per altri Blender): non ripiegare in silenzio sulla CPU.
- Se c'è Ponytail, prima passa `/ponytail-review` su `render_scripts/` e sugli script delle scene.
- Controlla che `Ok render finale` ci sia, con il codice (proposta `4-4-3`, o `4-4-4` per schermi grandi e color grading) e la stima (frame totali × s/frame, tabella in `references/render-qualita.md`).
- `SPP=<n> JPG_Q=<q> $K/render_all.sh <progetto> edl.txt 100 <fps> [WxH]` con Bash `run_in_background`, così arriva la notifica a fine render. Avanzamento: `ls final_jpg/*/f*.jpg | wc -l`. Usa `gpu_setup.py` (Metal on, CPU off, MetalRT off su M1/M2 e automatico su M3+) e `render_seg_gpu.py` (shot allungato di `extra` frame con i subframe, ripartibile).
- Poi la composizione HyperFrames finale con `final_jpg/final.mp4` come sfondo e i tempi di `final_jpg/timings.json` (riallinea e ricontrolla le grafiche se sono cambiati): `npx hyperframes render --quality delivery -o delivery/video.mp4`. Controlla che la durata (`ffprobe`) coincida con quella della composizione.

## 8. Rifare un pezzo senza ri-renderizzare tutto
- Animazione cambiata solo nei frame master `[x,y]` di uno shot, con stessi `a b extra`:
  `SPP=<n> JPG_Q=<q> OUT_FPS=<fps del render> "$B" -b scena.blend --python $K/gpu_setup.py --python $K/render_seg_gpu.py -- a b extra final_jpg/<dir_shot> 100 [WxH] --redo x y`
  Stessi `SPP`, `JPG_Q`, fps e `WxH` del render (sono nel file `params` dello shot). Sovrascrive solo i frame che campionano `[x-1, y+1]`. Poi rilancia `render_all.sh` (salta i frame esistenti e rimonta) e verifica la giunzione con `contact_sheet.sh`.
- Se cambiano `extra` o la durata dello shot, ci pensa `render_all.sh` (fase 3): rifà lo shot intero e sposta i vecchi frame da parte.

## 9. Consegna
`$K/deliver.sh delivery/video.mp4 delivery [max_mb=28]` produce `master.mp4` (H.264 alta qualità, audio a **−14 LUFS**, −1 dBTP, faststart) e `light.mp4` (sotto `max_mb`, per telefono, WhatsApp o email). Più i `sottotitoli_<lingua>.srt` della fase 5 e, se c'è, `delivery/<nome>_tavola.pdf`.

| Piattaforma | Formato | Note |
|---|---|---|
| Instagram Reels / Stories / TikTok / Shorts | 9:16 1080x1920 | sottotitoli bruciati |
| Feed Instagram / LinkedIn | 4:5 1080x1350 o 1:1 | LinkedIn accetta il `.srt` separato |
| YouTube / sito | 16:9 1920x1080 | `.srt` separato |
Altri formati dallo stesso progetto: chiedi se servono. Vuol dire reimpostare la camera nei .blend, rifare il render e reimpaginare le grafiche (`references/hyperframes.md`, "Cambiare formato"): non basta ritagliare.
Manda il `light.mp4` (vedi "Mandare file all'utente"). Pagina interattiva, se chiesta: `references/teardown-machine.md`.

## Trappole
- Blender 5.x: action a livelli → `action.layers[].strips[].channelbags[].fcurves`; l'opzione MetalRT si chiama `metalrt` (non `metal_rt`).
- Aliasing a ruota di carro: se un movimento ripetitivo supera ~0,3 celle per frame, rallentalo o alterna i colori.
- macOS: niente `timeout` né `sed \n`; usa un ciclo di attesa e Python.
- Riprese da telefono: fps variabili e rotazione nei metadati fanno sbagliare durata e sincronia dello split; convertile sempre a fps costanti.
- `motion_probe.py` misura il moto relativo al genitore: per il rapporto fra due parti confronta parti con lo stesso genitore.
