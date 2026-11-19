<p align="center">
  <img src="docs/assets/logo.svg" width="96" alt="Blender Product Video logo">
</p>

<h1 align="center">Blender Product Video</h1>

<p align="center"><b>Turn your machine into an explainer video.</b><br>
  Got a machine or a mechanical part? Give <a href="https://claude.com/claude-code">Claude Code</a> photos, a CAD file or a drawing,<br>
  and get an explainer video made with the power of Blender, in a few simple steps.<br>
  All vibe coding: no Blender or CAD skills needed.
</p>

<p align="center"><i>
  <b>Trasforma la tua macchina in un video explainer.</b><br>
  Hai una macchina o un pezzo meccanico? Dai a Claude Code foto, un file CAD o un disegno,<br>
  e ottieni un video explainer fatto con la potenza di Blender, in pochi passi semplici.<br>
  Tutto in vibe coding: senza conoscere Blender o il CAD.
</i></p>

<p align="center">Created by / Ideata da <b>Mario Mele</b></p>

<p align="center">
  <a href="https://mariomele.github.io/blender-product-video/"><b>Project page</b></a> ·
  <a href="#english">English</a> ·
  <a href="#italiano">Italiano</a> ·
  <a href="blender-product-video/README.md">Full docs (IT)</a>
</p>

<p align="center">
  <img src="docs/assets/og.png" alt="Blender Product Video: sample renders of a 6-axis robot arm" width="820">
</p>

---

## How it works · Come funziona

![From your part to an explainer video in three steps](docs/assets/examples/how_it_works_en.jpg?v=3)

▶ **[Watch the 17-second demo](https://mariomele.github.io/blender-product-video/assets/examples/demo.mp4?v=3)**: CAD, motion, exploded view, cutaway and settings, all made by the skill.
*Guarda la demo di 17 secondi: CAD, movimento, esploso, sezione e ambienti, tutto fatto dalla skill.*

## What a real camera can't show · Quello che una ripresa vera non può mostrare

Open the machine up, take it apart in mid-air, swap its finish in a click: shots that are impossible, or very expensive, with real footage.
*Apri la macchina, smontala a mezz'aria, cambia finitura con un clic: inquadrature impossibili, o molto costose, con riprese reali.*

| Cutaway · Sezione | Exploded view · Esploso | Materials and textures · Materiali e texture |
|---|---|---|
| ![Cutaway of the shoulder: motor, gearbox and bearing with red section faces](docs/assets/examples/sezione.jpg?v=3) | ![Exploded view](docs/assets/examples/esploso.jpg?v=3) | ![Painted joint, finned servo motor, zinc-plated bolts](docs/assets/examples/dettaglio_materiali.jpg?v=3) |

**Any setting, realistic light · Qualsiasi ambiente, luce realistica**

| Black studio · Studio nero | Limbo | Warehouse · Magazzino |
|---|---|---|
| ![Black studio](docs/assets/examples/ambiente_nero.jpg?v=3) | ![Light limbo](docs/assets/examples/ambiente_limbo.jpg?v=3) | ![Warehouse](docs/assets/examples/ambiente_capannone.jpg?v=3) |
| **Laboratory · Laboratorio** | **Production hall · Reparto con carroponte** | **Logistics hall · Capannone logistico** |
| ![Laboratory](docs/assets/examples/ambiente_laboratorio.jpg?v=3) | ![Production hall](docs/assets/examples/ambiente_officina.jpg?v=4) | ![Logistics hall](docs/assets/examples/ambiente_logistica.jpg?v=4) |

Every image was made with the skill's scripts, from a procedurally modelled 6-axis robot arm ([`build_robot.py`](docs/assets/examples/build_robot.py), [`cut_robot.py`](docs/assets/examples/cut_robot.py)).
*Tutte le immagini sono generate con gli script della skill, partendo da un braccio robotico a 6 assi modellato proceduralmente.*

---

<a id="english"></a>
## English

> The skill talks to you in Italian: its questions, notes and full documentation are in Italian. Claude Code understands requests in any language.

### What it is

You have a machine, a plant or a mechanical part and want to explain how it works. This skill lets you do it by just chatting: Claude Code drives Blender for you, from the 3D model to the final video. You never touch Blender or a CAD program.

It guides Claude Code, and you, through the whole making of a 3D product video: machines, plants, components, industrial processes. Built for sales presentations, social content, trade fairs and websites.

- **Starts from any source:** CAD (STEP, 3MF, GLB, FBX, OBJ, STL, USD or a .blend, all opened with one command; SolidWorks, Inventor, Fusion, CATIA and the like via a STEP export), photos, the product's web page, technical drawings (DWG, SVG, vector PDF) and dimensioned sketches.
- **Automatic or guided:** in automatic mode it asks three things and one summary, works out format, length, setting, audio and draft quality from where the video goes, checks every step itself on snapshots, and stops at three points: the silent video with the PDF storyboard and the voice-over scripts in .md to correct, the video with its text, and delivery. After your ok on the video with text it generates the voice with ElevenLabs and renders the final video, within your budget. In guided mode it asks at every phase and stops for your approval, so fixes come when they are cheap.
- **Remembers where you are:** every decision goes into `progetto.md`, and a request like "redo the intro" jumps straight to the right phase.
- **Tells a story with the camera:** a shot list with alternating shot sizes (LS, MS, CU, ECU, POV) and, every few scenes, a spectacular move: slow-mo and speed ramps, follow shots, robotic-arm paths, counter-movement, exploded view to cutaway in one shot.
- **Shows what a camera can't:** cutaways, exploded views, realistic materials and textures, any setting.
- **Shows the engineering (optional):** a real stress analysis turned into an animation, the part bending under load as it turns from blue to red, and the dimensioned drawing that becomes the 3D model.
- **AI extras (optional):** with the Higgsfield MCP, the part inside its factory or a bigger world (AI world, real Blender product composited on top), people, flashier graphics and effects with exact text laid on by HyperFrames, upscaled renders, new aspect ratios. Never on the product's geometry, numbers or logos.
- **Renders on Metal GPU** with a hang watchdog, resumable renders and the option to redo only the frames that changed.

### The phases

| # | Phase | What you get |
|---|---|---|
| 0 | **Brief** | format, length, environment and mood, infographic palette, saved in `progetto.md` |
| 1 | **The product** | real-scale model, materials and environment, shown as still views |
| 2 | **The scenes** | for each one: 1 fps storyboard, then a preview at 24, 12 or 6 fps |
| 3 | **Edit** | all scenes in one preview, with timings in `timings.json` |
| 4 | **Graphics and text** | titles, callouts, dimensions and subtitles in [HyperFrames](https://github.com/heygen-com/hyperframes); in 9:16 it follows the Reels, Stories and TikTok safe zones, so the app interface never covers important text |
| 5 | **Audio** | voice, music and sound effects with [ElevenLabs](https://elevenlabs.io/mcp); scenes fitted to the voice |
| 6 | **Full review** | the complete draft video, for approval |
| 7 | **Final render** | Cycles on Metal GPU, with a time estimate and a notification when done |
| 8 | **Redo a part** | only the frames that changed |
| 9 | **Delivery** | `master.mp4` at −14 LUFS, `light.mp4` under 28 MB, `sottotitoli.srt`; optional interactive 3D page |

### Install

**1. The skill**

```bash
git clone https://github.com/mariomele/blender-product-video.git
cp -r blender-product-video/blender-product-video ~/.claude/skills/
```

Restart Claude Code: the skill turns on by itself when you ask for a 3D product video.

**2. Dependencies**

System: macOS on Apple Silicon (tested on M1 Pro). Python 3 ships with macOS. Every command is below, ready to paste.

| You want… | Install |
|---|---|
| a quick look, a storyboard | the required set |
| a finished video with text and voice | + HyperFrames, ElevenLabs |
| leaner, faster code from Claude | + Ponytail |
| to start from a STEP, a drawing or a sketch | + text-to-cad |
| to start from an AutoCAD DWG | + LibreDWG |
| to start from a product web page | + Firecrawl |
| to show strength or a technical drawing | + text-to-cad |
| to move a robot or a machine within its real joint limits | + text-to-cad |
| to show a KiCad circuit board in 3D | + text-to-cad |
| the factory, a bigger world, people, flashier graphics | + Higgsfield |
| an interactive 3D page too | + Machine |

**Required**

- **[Homebrew](https://brew.sh)**: installs the other tools. *When:* once, before everything else (skip if `brew -v` answers).

  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

- **[Claude Code](https://claude.com/claude-code)**: the assistant you talk to: it reads the skill and drives every tool. *When:* always.

  ```bash
  curl -fsSL https://claude.ai/install.sh | bash
  ```

- **[Blender 5.1+](https://www.blender.org/download/)**: model, materials, scenes, Cycles render on Metal. *When:* always (in `/Applications`, or set the `BLENDER` variable).

  ```bash
  brew install --cask blender
  ```

- **[Blender MCP (Blender Lab)](https://www.blender.org/lab/mcp-server/)**: lets Claude see and change the open Blender file live. *When:* when you work with Blender open; headless renders don't need it.

  ```bash
  brew install uv
  git clone https://projects.blender.org/lab/blender_mcp.git ~/blender_mcp
  claude mcp add blender -- uv --directory ~/blender_mcp/mcp run blender-mcp
  ```

  ```bash
  curl -L -o ~/Downloads/blender-mcp-addon.zip "https://projects.blender.org/lab/blender_mcp/releases/download/v1.0.3/mcp-1.0.3.zip"
  ```

  Then in Blender: *Edit → Preferences → Get Extensions → Install from Disk*, pick the zip.

- **[FFmpeg](https://ffmpeg.org)**: previews, edit, audio mix, delivery files. *When:* always.

  ```bash
  brew install ffmpeg
  ```

- **[Blender skills](https://github.com/arjun988/blender-skills)**: **required.** The skill pilots them: at each step it loads the right one (blender-director and hard-surface for modelling, materials and lookdev for shading, lighting, camera-cinematography, animation, rendering). At the start it runs `scripts/check_skills.sh` and stops if any is missing. *When:* phases 1, 2 and 7.

  ```bash
  git clone https://github.com/arjun988/blender-skills.git /tmp/blender-skills
  cp -r /tmp/blender-skills/.claude/skills/* ~/.claude/skills/
  ```


**For the finished video**

- **[Node.js 22+ and HyperFrames](https://github.com/heygen-com/hyperframes)**: titles, callouts, measurements, subtitles, end logo, with exact text in your palette. *When:* phase 4; skip only for a video with no text.

  ```bash
  brew install node
  claude plugin marketplace add heygen-com/hyperframes
  claude plugin install hyperframes@hyperframes
  ```

- **[ElevenLabs MCP](https://elevenlabs.io/mcp)**: voice-over, music, sound effects; scenes stretched to fit the voice. *When:* phase 5, if the video has sound; needs an account with credits, asked each time.

  ```bash
  claude mcp add --transport http elevenlabs https://api.elevenlabs.io/v1/mcp
  ```

  Then `/mcp` in Claude Code to sign in.


- **[Ponytail](https://github.com/DietrichGebert/ponytail)**: makes Claude write the shortest code that works and reuse the skill's scripts first: fewer tokens, fewer bugs, faster previews; `/ponytail-review` checks the project's scripts. *When:* every phase where Claude writes scripts, plus a review before the final render.

  ```bash
  claude plugin marketplace add DietrichGebert/ponytail
  claude plugin install ponytail@ponytail
  ```

**Optional, by use**

- **[text-to-cad (with build123d and bd_warehouse)](https://github.com/earthtojake/text-to-cad)**: opens STEP files with separate parts at real scale; parametric CAD with [build123d](https://github.com/gumyr/build123d); real ISO screws, bearings, gears from [bd_warehouse](https://github.com/gumyr/bd_warehouse); stress analyses and dimensioned drawings; joint axes and limits of robots and machines; KiCad boards exported to 3D. *When:* you have a STEP, a drawing or a sketch; a cutaway needs real internals; you want to show strength or a drawing; a robot must move like the real one; the product has a circuit board to show.

  ```bash
  curl -fsSL https://texttocad.dev/install.sh | sh
  ```

- **[LibreDWG](https://www.gnu.org/software/libredwg/)**: reads AutoCAD DWG drawings, 2D only, at real scale. *When:* your source is a `.dwg`.

  ```bash
  brew install libredwg
  ```

- **[Firecrawl MCP](https://docs.firecrawl.dev/mcp-server)**: reads product pages and data sheets, pulls a palette from a website. *When:* you start from a link (otherwise Claude uses the built-in browser).

  ```bash
  claude mcp add --transport http firecrawl https://mcp.firecrawl.dev/v2/mcp-oauth
  ```

  Then `/mcp` to sign in.

- **[Higgsfield MCP](https://higgsfield.ai/mcp)**: AI on top of Blender: the part in its factory or a bigger world, people, spectacular effects under exact HyperFrames text, upscale, reframing. *When:* social and launch videos that need scale; never on cutaways, exploded views, numbers or logos; credits asked first.

  ```bash
  claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp
  ```

  Then `/mcp` to sign in.

- **[Teardown skill](https://github.com/elvarofficial/teardown)**: fast alternative without Blender: rebuilds the machine in three.js and records a tour video in minutes, or makes an interactive page. Shapes are approximate. *When:* a quick "how it works" video or a pitch where the real product's fidelity doesn't matter.

  ```bash
  npx skills add elvarofficial/teardown -g -a claude-code
  ```
  Then, once, in the installed folder: `npm install && npx playwright install chromium`.

- **[Machine skill](https://github.com/AirsupHQ/machine-skill)**: an interactive 3D web page of the product. *When:* you also want a page for a website or a trade-fair screen.

  ```bash
  git clone https://github.com/AirsupHQ/machine-skill.git ~/.claude/skills/machine
  cd ~/.claude/skills/machine && npm i -D playwright && npx playwright install chromium
  ```


**3. Quick check**

```bash
/Applications/Blender.app/Contents/MacOS/Blender --version
ffmpeg -version | head -1
node -v
claude mcp list
```

### How to use it

Just ask Claude Code, for example:

- "Make a 3D video of this product, CAD attached"
- "I have these photos of the machine, I want a video for Instagram"
- "Redo the intro with a lower camera"
- "Add voice-over and music"
- "Prepare the delivery files"

### Repo layout

```
blender-product-video/      the skill (copy it to ~/.claude/skills/)
  SKILL.md                  instructions for Claude
  README.md                 full documentation (Italian)
  scripts/                  import, previews, render, voice, subtitles, delivery
  evals/                    behaviour test cases
docs/                       project page (GitHub Pages), logo, sample images
```

### License

Created by Mario Mele. [MIT](LICENSE)

---

<a id="italiano"></a>
## Italiano

### Cos'è

Hai una macchina, un impianto o un pezzo meccanico e vuoi spiegare come funziona. Con questa skill lo fai parlando: Claude Code guida Blender al posto tuo, dal modello 3D al video finale. Non devi mai aprire Blender o un programma CAD.

Guida Claude Code, e te, in tutto il percorso di un video 3D di prodotto: macchine, impianti, componenti, processi industriali. Pensata per presentazioni commerciali, contenuti social, fiere e siti.

- **Parte da qualsiasi sorgente:** CAD (STEP, 3MF, GLB, FBX, OBJ, STL, USD o un .blend, tutti aperti con un solo comando; SolidWorks, Inventor, Fusion, CATIA e simili passando da un export STEP), foto, la pagina web del prodotto, disegni tecnici (DWG, SVG, PDF vettoriale) e schizzi quotati.
- **Automatica o guidata:** in automatica chiede tre cose e un riepilogo, deduce formato, durata, ambiente, audio e qualità delle bozze da dove va il video, controlla da sola ogni passaggio sugli snapshot e si ferma in tre punti: il video muto con lo storyboard in PDF e i testi della voce in .md da correggere, il video con i testi, la consegna. Dopo l'ok al video con i testi genera la voce con ElevenLabs e fa il video finale, dentro il tuo budget. In guidata fa domande a ogni fase e si ferma per un'approvazione, così le correzioni arrivano quando costano poco.
- **Si ricorda dove sei:** tutte le decisioni finiscono in `progetto.md`, e una richiesta come "rifai l'intro" porta direttamente alla fase giusta.
- **Racconta con la camera:** una scaletta con piani alternati (LS, MS, CU, ECU, POV) e, ogni poche scene, una ripresa spettacolare: slow-mo e speed ramp, camera che segue il pezzo, traiettorie da braccio robotico, contromovimento, da esploso a sezione in un'unica ripresa.
- **Mostra quello che una telecamera non può:** sezioni, esplosi, materiali e texture realistici, qualsiasi ambiente.
- **Mostra l'ingegneria (facoltativo):** un calcolo di resistenza vero diventa un'animazione, con il pezzo che si piega sotto carico passando dal blu al rosso, e la tavola quotata diventa il modello 3D.
- **Extra AI (facoltativo):** con Higgsfield MCP, il pezzo dentro la fabbrica o in un mondo più grande (mondo generato, prodotto vero da Blender sopra), persone, grafiche ed effetti più spettacolari con il testo esatto messo da HyperFrames, upscale dei render, nuovi formati. Mai sulla geometria del prodotto, sui numeri o sui loghi.
- **Render su GPU Metal** con controllo anti-blocco, render ripartibili e la possibilità di rifare solo i frame cambiati.

### Il percorso

| # | Fase | Cosa ottieni |
|---|---|---|
| 0 | **Brief** | formato, durata, ambiente e atmosfera, palette delle infografiche, salvati in `progetto.md` |
| 1 | **Il pezzo** | modello in scala reale, materiali e ambientazione, mostrati in viste statiche |
| 2 | **Le scene** | per ognuna: storyboard 1 fps, poi anteprima a 24, 12 o 6 fps |
| 3 | **Montaggio** | tutte le scene in un'anteprima unica, con i tempi in `timings.json` |
| 4 | **Grafiche e testo** | titoli, callout, misure e sottotitoli in [HyperFrames](https://github.com/heygen-com/hyperframes); nel 9:16 rispetta le zone sicure di Reels, Stories e TikTok, così l'interfaccia delle app non copre mai i testi importanti |
| 5 | **Audio** | voce, musica ed effetti con [ElevenLabs](https://elevenlabs.io/mcp); scene adattate alla voce |
| 6 | **Visione d'insieme** | il video completo in bozza, da approvare |
| 7 | **Render finale** | Cycles su GPU Metal, con stima dei tempi e notifica a fine render |
| 8 | **Rifare un pezzo** | solo i frame cambiati |
| 9 | **Consegna** | `master.mp4` a −14 LUFS, `light.mp4` sotto i 28 MB, `sottotitoli.srt`; pagina 3D interattiva facoltativa |

I dettagli di ogni fase, gli script e l'elenco di montaggio (EDL) sono nella [documentazione completa](blender-product-video/README.md).

### Installazione

**1. La skill**

```bash
git clone https://github.com/mariomele/blender-product-video.git
cp -r blender-product-video/blender-product-video ~/.claude/skills/
```

Riavvia Claude Code: la skill si attiva da sola quando chiedi un video 3D di un prodotto.

**2. Le dipendenze**

Sistema: macOS con Apple Silicon (provato su M1 Pro). Python 3 è già incluso in macOS. Tutti i comandi sono qui sotto, pronti da incollare.

| Vuoi… | Installa |
|---|---|
| una prova veloce, uno storyboard | le necessarie |
| un video finito con testi e voce | + HyperFrames, ElevenLabs |
| codice più snello e veloce da Claude | + Ponytail |
| partire da uno STEP, un disegno o uno schizzo | + text-to-cad |
| partire da un DWG di AutoCAD | + LibreDWG |
| partire dalla pagina web del prodotto | + Firecrawl |
| mostrare la resistenza o una tavola tecnica | + text-to-cad |
| muovere un robot o una macchina entro i fine corsa veri dei giunti | + text-to-cad |
| mostrare in 3D una scheda elettronica KiCad | + text-to-cad |
| la fabbrica, un mondo più grande, persone, grafiche più spettacolari | + Higgsfield |
| anche una pagina 3D interattiva | + Machine |

**Necessarie**

- **[Homebrew](https://brew.sh)**: installa gli altri strumenti. *Quando:* una volta, prima di tutto (saltalo se `brew -v` risponde).

  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

- **[Claude Code](https://claude.com/claude-code)**: l'assistente con cui parli: legge la skill e guida tutti gli strumenti. *Quando:* sempre.

  ```bash
  curl -fsSL https://claude.ai/install.sh | bash
  ```

- **[Blender 5.1+](https://www.blender.org/download/)**: modello, materiali, scene, render Cycles su Metal. *Quando:* sempre (in `/Applications`, oppure imposta la variabile `BLENDER`).

  ```bash
  brew install --cask blender
  ```

- **[Blender MCP (Blender Lab)](https://www.blender.org/lab/mcp-server/)**: fa vedere e modificare a Claude il file Blender aperto, dal vivo. *Quando:* quando lavori con Blender aperto; i render in background non ne hanno bisogno.

  ```bash
  brew install uv
  git clone https://projects.blender.org/lab/blender_mcp.git ~/blender_mcp
  claude mcp add blender -- uv --directory ~/blender_mcp/mcp run blender-mcp
  ```

  ```bash
  curl -L -o ~/Downloads/blender-mcp-addon.zip "https://projects.blender.org/lab/blender_mcp/releases/download/v1.0.3/mcp-1.0.3.zip"
  ```

  Poi in Blender: *Edit → Preferences → Get Extensions → Install from Disk*, scegli lo zip.

- **[FFmpeg](https://ffmpeg.org)**: anteprime, montaggio, mix audio, file di consegna. *Quando:* sempre.

  ```bash
  brew install ffmpeg
  ```

- **[Blender skills](https://github.com/arjun988/blender-skills)**: **obbligatorie.** La skill le pilota: a ogni passo carica quella giusta (blender-director e hard-surface per il modello, materials e lookdev per i materiali, lighting, camera-cinematography, animation, rendering). All'avvio lancia `scripts/check_skills.sh` e si ferma se ne manca una. *Quando:* fasi 1, 2 e 7.

  ```bash
  git clone https://github.com/arjun988/blender-skills.git /tmp/blender-skills
  cp -r /tmp/blender-skills/.claude/skills/* ~/.claude/skills/
  ```


**Per il video finito**

- **[Node.js 22+ and HyperFrames](https://github.com/heygen-com/hyperframes)**: titoli, callout, misure, sottotitoli, logo finale, con testo esatto nella tua palette. *Quando:* fase 4; saltalo solo per un video senza testo.

  ```bash
  brew install node
  claude plugin marketplace add heygen-com/hyperframes
  claude plugin install hyperframes@hyperframes
  ```

- **[ElevenLabs MCP](https://elevenlabs.io/mcp)**: voce fuori campo, musica, effetti; scene allungate per la voce. *Quando:* fase 5, se il video ha l'audio; serve un account con crediti, chiesti ogni volta.

  ```bash
  claude mcp add --transport http elevenlabs https://api.elevenlabs.io/v1/mcp
  ```

  Poi `/mcp` in Claude Code per accedere.


- **[Ponytail](https://github.com/DietrichGebert/ponytail)**: fa scrivere a Claude il codice più corto che funziona e riusare prima gli script della skill: meno token, meno errori, anteprime più veloci; `/ponytail-review` controlla gli script del progetto. *Quando:* in ogni fase in cui Claude scrive script, più un controllo prima del render finale.

  ```bash
  claude plugin marketplace add DietrichGebert/ponytail
  claude plugin install ponytail@ponytail
  ```

**Facoltative, in base all'uso**

- **[text-to-cad (with build123d and bd_warehouse)](https://github.com/earthtojake/text-to-cad)**: apre gli STEP con le parti separate in scala reale; CAD parametrico con [build123d](https://github.com/gumyr/build123d); viti, cuscinetti, ingranaggi ISO veri da [bd_warehouse](https://github.com/gumyr/bd_warehouse); calcoli di resistenza e tavole quotate; assi e fine corsa dei giunti di robot e macchine; schede KiCad esportate in 3D. *Quando:* hai uno STEP, un disegno o uno schizzo; una sezione ha bisogno di interni veri; vuoi mostrare la resistenza o una tavola; un robot deve muoversi come quello vero; il prodotto ha una scheda elettronica da mostrare.

  ```bash
  curl -fsSL https://texttocad.dev/install.sh | sh
  ```

- **[LibreDWG](https://www.gnu.org/software/libredwg/)**: legge i disegni DWG di AutoCAD, solo 2D, in scala reale. *Quando:* la sorgente è un `.dwg`.

  ```bash
  brew install libredwg
  ```

- **[Firecrawl MCP](https://docs.firecrawl.dev/mcp-server)**: legge pagine prodotto e schede tecniche, ricava la palette da un sito. *Quando:* parti da un link (altrimenti Claude usa il browser integrato).

  ```bash
  claude mcp add --transport http firecrawl https://mcp.firecrawl.dev/v2/mcp-oauth
  ```

  Poi `/mcp` per accedere.

- **[Higgsfield MCP](https://higgsfield.ai/mcp)**: AI sopra Blender: il pezzo nella fabbrica o in un mondo più grande, persone, effetti spettacolari sotto il testo esatto di HyperFrames, upscale, cambi di formato. *Quando:* video social e di lancio che hanno bisogno di scala; mai su sezioni, esplosi, numeri o loghi; crediti chiesti prima.

  ```bash
  claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp
  ```

  Poi `/mcp` per accedere.

- **[Teardown skill](https://github.com/elvarofficial/teardown)**: alternativa veloce senza Blender: ricostruisce la macchina in three.js e registra un video del tour in pochi minuti, o crea una pagina interattiva. Le forme sono approssimate. *Quando:* un video veloce di "come funziona" o un pitch, dove la fedeltà al prodotto vero non conta.

  ```bash
  npx skills add elvarofficial/teardown -g -a claude-code
  ```
  Poi, una volta, nella cartella installata: `npm install && npx playwright install chromium`.

- **[Machine skill](https://github.com/AirsupHQ/machine-skill)**: una pagina web 3D interattiva del prodotto. *Quando:* vuoi anche una pagina per il sito o per uno schermo in fiera.

  ```bash
  git clone https://github.com/AirsupHQ/machine-skill.git ~/.claude/skills/machine
  cd ~/.claude/skills/machine && npm i -D playwright && npx playwright install chromium
  ```


**3. Verifica rapida**

```bash
/Applications/Blender.app/Contents/MacOS/Blender --version
ffmpeg -version | head -1
node -v
claude mcp list
```

### Come si usa

Basta chiederlo a Claude Code, per esempio:

- "Fammi un video 3D di questo prodotto, ti allego il CAD"
- "Ho queste foto della macchina, voglio un video per Instagram"
- "Rifai l'intro con la camera più bassa"
- "Aggiungi voce fuori campo e musica"
- "Prepara i file da consegnare"

### Struttura del repo

```
blender-product-video/      la skill (da copiare in ~/.claude/skills/)
  SKILL.md                  istruzioni per Claude
  README.md                 documentazione completa
  scripts/                  import, anteprime, render, voce, sottotitoli, consegna
  evals/                    casi di prova del comportamento
docs/                       pagina del progetto (GitHub Pages), logo, immagini di esempio
```

### Licenza

Ideata da Mario Mele. [MIT](LICENSE)
