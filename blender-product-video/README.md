# Blender Product Video

Una skill per Claude Code che porta dal materiale grezzo di un prodotto (foto, link, file CAD o disegni tecnici) a un video 3D finito, con grafiche, voce fuori campo, musica, effetti sonori, sottotitoli e file pronti da pubblicare.

È pensata per video di prodotti, macchine, impianti e processi industriali: presentazioni commerciali, contenuti social, video per fiere e siti. Non serve per video senza 3D (reel di girato, podcast, interviste).

---

## Cosa fa

- **Parte da qualsiasi sorgente:** un modello CAD, delle foto, la pagina web di un prodotto, un disegno tecnico o uno schizzo quotato.
- **Ricostruisce il prodotto in Blender** in scala reale, con materiali e colori fedeli al vero.
- **Lo mette in un'ambientazione:** capannone, studio nero, limbo, esterno, showroom, anche partendo da una foto di riferimento.
- **Costruisce le scene una alla volta**, con storyboard e anteprime veloci da approvare prima di spendere ore di render.
- **Monta le scene** in un'unica animazione.
- **Aggiunge grafiche e testi** (titoli, callout, misure, sottotitoli, logo) con HyperFrames.
- **Mostra calcoli e tavole** (facoltativo, con text-to-cad): il pezzo che si piega sotto carico colorato dal blu al rosso, da un calcolo di resistenza vero, e la tavola tecnica quotata che si trasforma nel modello 3D. Muove robot e macchine con i fine corsa veri dei giunti, e porta nel video le schede elettroniche KiCad in 3D.
- **Genera voce, musica ed effetti sonori** con ElevenLabs e adatta la durata delle scene alla voce.
- **Fa il render finale** in alta qualità sulla GPU del Mac (Metal).
- **Prepara i file di consegna:** video master, versione leggera da mandare al telefono, sottotitoli.

## Un percorso guidato, che si ricorda dove sei

All'inizio scegli la modalità:

- **Automatica:** tre domande (cosa hai, dove va il video, cosa deve capire chi guarda) e un riepilogo da confermare. Formato, durata, ambiente, audio e qualità delle bozze li deduce dall'uso. Poi lavora da sola fino al provino completo: controlla lei ogni passaggio sugli snapshot (proporzioni, compenetrazioni, zone sicure, leggibilità, durata delle scene) e si ferma solo per il provino, l'ok al render finale, una spesa fuori budget o un dato che non si inventa. Il budget di ore di render e di crediti lo decidi tu nel riepilogo.
- **Guidata:** fa domande a ogni fase e si ferma per un'approvazione prima di andare avanti. Le correzioni costano poco perché arrivano quando il lavoro è ancora leggero.

Tutte le decisioni (formato, ambiente, palette, voce, scene approvate) vengono scritte in un file **`progetto.md`** nella cartella del progetto. Se riprendi il lavoro il giorno dopo, o in un'altra sessione, la skill riparte da lì senza rifarti le stesse domande.

Non serve ripartire sempre dall'inizio: se chiedi "rifai l'intro", "aggiungi la musica" o "fai partire il render finale", la skill va direttamente alla fase giusta.

| # | Fase | Cosa ti chiede | Cosa ottieni |
|---|---|---|---|
| 0 | **Brief** | Sorgenti, formato (9:16, 16:9, 1:1, 4:5), risoluzione, fps, durata, ambiente e atmosfera, messaggio, palette delle infografiche, logo | `progetto.md` con il brief da confermare |
| 1 | **Il pezzo** | Misure di riferimento, livello di fedeltà, colori e finiture reali, loghi | Il modello 3D in scala, con materiali e ambientazione, mostrato in alcune viste statiche |
| 2 | **Le scene** | Per ogni scena: durata, movimenti della macchina, inquadrature, qualità dell'anteprima | Uno storyboard a griglia (un frame al secondo), poi un'anteprima animata |
| 3 | **Montaggio** | Ordine e ritmo | Tutte le scene unite in un'anteprima unica |
| 4 | **Grafiche e testo** | Testo della voce (lo scrivi tu o lo propone Claude), grafiche necessarie | La composizione HyperFrames, verificata, ancora senza audio |
| 5 | **Audio** | Voce, musica sì/no, effetti sonori sì/no | Voce, musica e SFX sincronizzati, scene adattate alla voce, sottotitoli |
| 6 | **Visione d'insieme** | Giudizio complessivo | Il video completo in bozza, con l'audio |
| 7 | **Render finale** | Ok esplicito, dopo una stima dei tempi | Il video definitivo in alta qualità |
| 8 | **Rifare un pezzo** | Cosa cambiare | Solo i frame interessati vengono rifatti |
| 9 | **Consegna** | Per quali piattaforme | Master, versione leggera, sottotitoli |

Il render finale parte **solo** dopo un ok esplicito. Prima di cancellare file la skill chiede sempre, e di norma li sposta invece di cancellarli. Ogni generazione che consuma crediti (voce, musica, SFX, modelli 3D con AI) e ogni download vengono chiesti prima.

## Da quali sorgenti si può partire

| Hai… | La skill… |
|---|---|
| **Un modello 3D** (GLB, glTF, FBX, OBJ, STL, PLY, USD, ABC) | Lo importa direttamente in scala reale. |
| **Un file CAD nativo** (STEP, IGES, SolidWorks, Inventor, Onshape, Fusion) | Lo STEP lo converte da solo in GLB con [text-to-cad](https://github.com/earthtojake/text-to-cad), con le parti separate e in scala reale. Per gli altri formati ti chiede un export in STEP o GLB dal programma CAD. |
| **Una scheda elettronica KiCad** (`.kicad_pcb`) | La esporta in GLB con i suoi componenti 3D, con [text-to-cad](https://github.com/earthtojake/text-to-cad), e la mette nel video, per esempio dentro la sezione del prodotto. |
| **Un disegno vettoriale** (SVG, DXF, DWG, PDF vettoriale) | Importa direttamente SVG e DWG. Il DWG viene letto con [LibreDWG](https://www.gnu.org/software/libredwg/) e solo nella parte 2D; per i DXF chiede un export in SVG o DWG. Poi estrude i profili e ricostruisce le parti. |
| **Un disegno scansionato o uno schizzo quotato** | Legge le quote e modella il pezzo a partire da quelle. Le quote mancanti le chiede, non le inventa. |
| **Delle foto** | Le usa come riferimento per modellare. Ti dice quali viste mancano (fronte, retro, lati, alto, dettagli) e chiede almeno una misura reale per la scala. |
| **Un link** | Dalla pagina prodotto ricava foto, misure, schede tecniche e codici colore. Se il link punta a un modello 3D scaricabile, chiede l'ok e controlla la licenza. |

### Livello di fedeltà

Prima di modellare, la skill concorda con te cosa aspettarsi:

- **A, da CAD:** geometria esatta.
- **B, da disegno quotato o foto con misure:** forme e proporzioni fedeli (±2–5%), dettagli non visibili semplificati.
- **C, da sole foto:** aspetto credibile, proporzioni approssimate, parti nascoste ricostruite.

## Materiali e texture

La skill chiede i **colori reali** del prodotto (codici RAL o Pantone dalla scheda tecnica, campionati dalle foto o forniti da te), le **finiture** (inox spazzolato, alluminio, verniciato lucido o opaco, plastica, gomma, vetro, zincato) e i **loghi o le etichette** da applicare.

- I materiali sono costruiti con valori fisici realistici.
- Le finiture sono **procedurali** dove possibile (spazzolatura, piccole imperfezioni, usura sui bordi): sono leggere e non richiedono di scartare il modello.
- I file CAD vengono texturizzati senza scartare a mano.
- Le texture fotografiche (per esempio il cemento di un capannone) si scaricano solo se servono e con il tuo ok.
- Il colore del prodotto viene verificato sul frame renderizzato, accanto alla foto o al codice di riferimento.

## Ambiente e atmosfera

Nel brief la skill chiede dove deve stare il prodotto e con che atmosfera:

- **Ambiente:** capannone o reparto produttivo, studio con sfondo nero, limbo bianco o grigio, esterno (cantiere, campo, piazzale), showroom o ufficio, sfondo astratto.
- **Atmosfera e luce:** tecnica e pulita, cinematografica e contrastata, calda o fredda, giorno o notte, con effetti come fumo, polvere o riflessi a terra.
- **Foto di riferimento (facoltativa):**
  - se è una foto a 360°, diventa direttamente l'illuminazione della scena;
  - se è una foto normale, la skill ne ricava luce, colori e materiali e ricostruisce un set simile, oppure la usa come sfondo reale con le ombre del prodotto.

## Colori delle infografiche

La palette serve **solo per le grafiche HyperFrames** (titoli, callout, sottotitoli). In Blender prodotto e ambiente hanno i loro colori reali.

Se i colori del cliente non sono già salvati, la skill **chiede sempre quale palette usare**, in uno di tre modi:

- **a parole**, per esempio "blu scuro e bianco": la skill propone i codici Hex e te li fa confermare;
- **con i codici Hex**, per esempio `#0A3D62`, `#FFFFFF`;
- **con un sito di riferimento**: la skill ricava la palette dal sito e te la mostra per conferma.

Chiede anche il logo e i colori da evitare. Una volta confermata, la palette può essere salvata per i video successivi dello stesso cliente.

## Storyboard e anteprime

Per ogni scena, prima di qualunque anteprima animata, la skill crea uno **storyboard a griglia**: un frame per ogni secondo, compreso l'ultimo, con il numero di frame stampato. È veloce (pochi secondi) e mostra subito se inquadrature e movimenti funzionano.

Poi l'anteprima animata, nella qualità che scegli:

- **Real time (24 fps):** tutti i frame, la più fedele.
- **Medio (12 fps):** un frame ogni due. È il compromesso consigliato.
- **Basso (6 fps):** un frame ogni quattro, per controllare in fretta i movimenti.

Su un M1 Pro, uno storyboard di una scena da 4 secondi esce in circa 5 secondi e l'anteprima a 6 fps in circa 20.

## Audio

Con ElevenLabs, sempre previo ok per i crediti:

- **Voce fuori campo:** scegli tra 2–3 voci proposte; viene generata scena per scena e le scene si allungano da sole per contenerla.
- **Musica di sottofondo:** strumentale, con genere e mood a scelta. In alternativa può essere **composta sul video** stesso, seguendone il ritmo.
- **Effetti sonori:** motore, scorrimento, clic, sportelli, whoosh sulle transizioni, sincronizzati ai movimenti.
- **Sottotitoli:** generati dal testo della voce, come file `.srt` o bruciati nel video per i social.

Voce, musica ed effetti vengono mixati in HyperFrames, con la musica abbassata sotto la voce.

## Consegna

Alla fine la skill prepara:

- **master.mp4:** alta qualità, audio normalizzato a −14 LUFS (lo standard di social e web);
- **light.mp4:** sotto i 28 MB, da mandare al telefono, su WhatsApp o per email;
- **sottotitoli.srt.**

| Piattaforma | Formato consigliato |
|---|---|
| Instagram Reels, TikTok, YouTube Shorts | 9:16, sottotitoli nel video, testi lontani dai bordi |
| Feed Instagram, LinkedIn | 4:5 o 1:1 |
| YouTube, sito | 16:9, sottotitoli come file separato |

Un altro formato dallo stesso progetto si può fare, ma richiede di reimpostare le inquadrature e rifare il render: non basta ritagliare.

Se nel brief lo chiedi, come extra la skill prepara anche una **pagina 3D interattiva** del prodotto con [`/machine`](https://github.com/AirsupHQ/machine-skill): un file HTML con esploso, sezione e numeri di funzionamento, da usare sul sito o su un monitor in fiera. È una versione semplificata del pezzo, separata dal video.

## Gli strumenti inclusi

Nella cartella `scripts/`:

| Script | A cosa serve |
|---|---|
| `check_skills.sh` | Controlla che ci siano le skill Blender obbligatorie (arjun988/blender-skills) e, se mancano, stampa i comandi per installarle. |
| `import_model.py` | Importa in scala reale qualsiasi file accettato (STEP, 3MF, GLB, FBX, OBJ, STL, PLY, USD, ABC, .blend, DWG, SVG, PDF vettoriale) e stampa le dimensioni, per controllare subito la scala. |
| `fea_surface.py`, `fea_to_blend.py` | Portano in Blender il risultato di un calcolo di resistenza di text-to-cad: superficie del pezzo, deformazione esagerata e colori della tensione, animati mentre entra il carico. |
| `preview.sh` (+ `preview.py`) | Storyboard a griglia e anteprima animata a 24, 12 o 6 fps. |
| `render_all.sh` | Renderizza tutte le scene, controlla che non manchino frame, monta il video e scrive `timings.json` con i tempi di ogni scena. Si accorge se cambi la durata di una scena e rifà solo quella. |
| `render_seg_gpu.py` | Renderizza una scena, eventualmente allungandola per la voce. Con `--redo` rifà solo il tratto modificato. Qualità con `SPP` e `JPG_Q`; con `OUT_FPS` ricampiona a qualsiasi fps. |
| `gpu_setup.py` | Attiva il render su GPU Metal, con le impostazioni migliori per il chip del Mac. |
| `fit_vo.py` | Allunga ogni scena quanto basta perché ci stia la sua voce fuori campo. |
| `make_srt.py` | Crea i sottotitoli dal testo della voce e dai tempi delle scene. |
| `contact_sheet.sh` | Crea un provino a griglia di qualunque video. |
| `safe_zone.sh` | Zona sicura del 9:16 per Reels, Stories e TikTok: margini, CSS e guide disegnate su un frame o un video. |
| `storyboard_pdf.py` | Storyboard in PDF per l'approvazione del cliente, brandizzato, e testi della voce in `.md` per ogni lingua. |
| `deliver.sh` | Prepara master e versione leggera, con l'audio normalizzato. |

Nella cartella `evals/` ci sono alcuni casi di prova che descrivono come la skill deve comportarsi. Servono a controllare che le modifiche future non rompano niente.

### L'elenco di montaggio (EDL)

Il video è descritto da un file di testo, `edl.txt`, con una scena per riga:

```
n  file.blend  primo_frame  ultimo_frame  [extra]  [skip_head]
1  intro.blend  1  96  12
2  dettaglio.blend  1  120  0  6
```

- **extra:** frame in più per dare respiro alla voce. L'animazione rallenta in modo fluido, senza toccare i keyframe.
- **skip_head:** frame iniziali da escludere dal montaggio, senza cancellarli.

## Accorgimenti che fanno risparmiare tempo

- **Animazioni procedurali** (driver e geometry nodes, niente simulazioni fisiche): si possono allungare o accorciare senza rifare l'animazione.
- **Render ripartibili:** se il render si interrompe, ripartendo salta i frame già fatti.
- **Rifare solo un pezzo:** se cambia un tratto di animazione, si rifanno solo i frame di quel tratto.
- **Nessun frame perso:** se cambi la durata di una scena, i vecchi frame vengono messi da parte, non mescolati né cancellati.
- **Controllo anti-blocco della GPU:** su Mac il render su Metal si blocca se c'è un Blender aperto con l'interfaccia. Lo script lo verifica prima di partire e, se il render si ferma comunque, lo interrompe e lo segnala invece di aspettare all'infinito.
- **Avviso a fine render:** il render lungo gira in background e Claude riceve la notifica quando finisce.

## Requisiti e installazione

Sistema: macOS con Apple Silicon (provato su M1 Pro). Python 3 è già incluso in macOS.

| Dipendenza | Serve per | Installazione |
|---|---|---|
| [Claude Code](https://claude.com/claude-code) | eseguire la skill | vedi il link |
| [Blender 5.1 o successivo](https://www.blender.org/download/) | modello, scene, render | scarica e sposta in `/Applications` (altro percorso: variabile `BLENDER`) |
| [Blender MCP (Blender Lab)](https://www.blender.org/lab/mcp-server/) | far lavorare Claude dentro Blender | 1) add-on in Blender, seguendo la pagina; 2) server MCP: il pacchetto `.mcpb` dalla [pagina release](https://projects.blender.org/lab/blender_mcp/releases) si apre con Claude Desktop, oppure si installa da sorgente con la [guida di setup](https://projects.blender.org/lab/blender_mcp/wiki/Setup) |
| [Homebrew](https://brew.sh) + [FFmpeg](https://ffmpeg.org) | anteprime, montaggio, consegna | `brew install ffmpeg` (include ffprobe) |
| [Node.js 22+](https://nodejs.org/en/download) | HyperFrames | installer dal link, oppure `brew install node` |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | grafiche, testi, mix audio | `claude plugin marketplace add heygen-com/hyperframes` poi `claude plugin install hyperframes@hyperframes` |
| [ElevenLabs MCP](https://elevenlabs.io/mcp) | voce, musica, effetti sonori | `claude mcp add --transport http elevenlabs https://api.elevenlabs.io/v1/mcp`, poi `/mcp` in Claude Code per accedere |
| [Blender skills](https://github.com/arjun988/blender-skills) | skill di supporto (blender-director, materials, lighting, lookdev, camera-cinematography, environment-artist…) | istruzioni nel README del repo |

Facoltativi:
- [Firecrawl MCP](https://docs.firecrawl.dev/mcp-server): leggere pagine prodotto e ricavare la palette da un sito (in alternativa Claude usa il browser integrato).
- Un account [ElevenLabs](https://elevenlabs.io) con crediti, per voce, musica ed effetti.
- [Ponytail](https://github.com/DietrichGebert/ponytail) (consigliato): fa scrivere a Claude script corti e riusa quelli che ci sono già, quindi meno token, meno errori e anteprime più veloci; `/ponytail-review` controlla gli script prima del render finale. `claude plugin marketplace add DietrichGebert/ponytail` e `claude plugin install ponytail@ponytail`.
- [Higgsfield MCP](https://higgsfield.ai): extra AI facoltativi, sempre previo ok per i crediti: il pezzo dentro la fabbrica o in un mondo più grande (mondo generato, prodotto vero da Blender sopra), persone, grafiche ed effetti più spettacolari con il testo esatto messo da HyperFrames, upscale dei render, cambi di formato. Mai su sezioni, esplosi, calcoli, quote o loghi.
- [text-to-cad](https://github.com/earthtojake/text-to-cad): converte gli STEP in GLB, modella le parti meccaniche in CAD parametrico, fa calcoli di resistenza e tavole tecniche, trova assi e fine corsa dei giunti di robot e macchine, esporta in 3D le schede KiCad, con [build123d](https://github.com/gumyr/build123d) (incluso). Le parti normalizzate (viti, cuscinetti, ingranaggi, tubi, flange) arrivano da [bd_warehouse](https://github.com/gumyr/bd_warehouse), che `cad run` scarica da solo la prima volta. Installazione: vedi il README del repo.
- [LibreDWG](https://www.gnu.org/software/libredwg/): per leggere i disegni DWG di AutoCAD, solo la parte 2D. `brew install libredwg`
- [Machine skill](https://github.com/AirsupHQ/machine-skill): solo per la pagina interattiva extra. `git clone https://github.com/AirsupHQ/machine-skill.git ~/.claude/skills/machine`; per screenshot e video della pagina serve Playwright: `npm i -D playwright && npx playwright install chromium` nella cartella della skill.

Riferimento indicativo: su M1 Pro, 1080x1920 a 40 campioni, circa **10 secondi per frame** su GPU Metal, contro circa 40 su CPU. Un video di 60 secondi a 24 fps richiede quindi circa 4 ore di render finale. La skill dà sempre una stima prima di partire.

## Come si avvia

Basta chiederlo a Claude Code in linguaggio naturale, per esempio:

- "Fammi un video 3D di questo prodotto, ti allego il CAD"
- "Ho queste foto della macchina, voglio un video per Instagram"
- "Da questo disegno tecnico fammi un'animazione di montaggio"
- "Rifai l'intro con la camera più bassa"
- "Aggiungi voce fuori campo e musica"
- "Prepara i file da consegnare"

Su un progetto nuovo la skill parte dal brief; su uno già avviato riprende da dove eri rimasto.
