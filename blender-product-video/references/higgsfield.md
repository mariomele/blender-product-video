# Extra AI con Higgsfield MCP (facoltativo, costa crediti)

Leggila quando proponi scene AI nella scaletta o lo stile "effetti Higgsfield + testo HyperFrames" in fase 4. Il render Blender resta la base, e l'AI si usa solo dove migliora qualcosa senza cambiare il prodotto. Prima di ogni generazione controlla i crediti con `balance`, di' quanto costa e chiedi l'ok. Controlla ogni risultato fotogramma per fotogramma: l'AI può cambiare forme, loghi, scritte e numero di pezzi.

Usi consigliati:
- **Upscale** (`upscale_video`, `upscale_image`): render a risoluzione più bassa e poi upscale. Si risparmiano ore di GPU, ma va provato su uno shot prima.
- **Il pezzo in un mondo più grande**: la fabbrica dove lavora, la linea intera, la città o il cantiere che la usa, il prodotto finito che esce dalla macchina e arriva al cliente. Due modi, in ordine di fedeltà:
  1. **Composito**: Higgsfield genera solo il mondo (`generate_video` o `generate_image`, senza il prodotto, con camera e prospettiva descritte come la scena Blender), poi il prodotto renderizzato in Blender con sfondo trasparente (`film_transparent`, PNG RGBA) ci va sopra, con ombre da un piano shadow catcher. Allinea altezza della camera, lunghezza focale e direzione della luce al plate generato.
  2. **Video da frame Blender**: si parte (o si arriva) su un frame Blender e l'AI fa il resto, per esempio la camera che si allontana dal pezzo fino a mostrare tutta la fabbrica. Il prodotto deve diventare piccolo in fretta. Il taglio torna su Blender per ogni dettaglio.
- **Persone** (`generate_video` / `generate_image` da un frame Blender): un operatore alla macchina, mani che montano un pezzo, il prodotto in uso. Il prodotto deve restare piccolo nell'inquadratura o fuori fuoco.
- **Intro e chiusure d'atmosfera**: fumo, luce, ambiente, che partono da un frame Blender o finiscono su un frame Blender, così il passaggio è invisibile.
- **Formati** (`reframe`, `outpaint_image`): da 16:9 a 9:16 o 1:1 senza ri-renderizzare, solo se il prodotto non viene tagliato.
- **Ambiente**: sfondi, backplate o texture generati (cemento, capannone) da usare in Blender.
- **Effetti sotto le grafiche**: transizioni, flussi di energia o di fluido, particelle, luci, sfondi animati per i titoli, sempre senza testo e senza numeri, con i colori della palette nel prompt. I modelli AI sbagliano le lettere e inventano cifre: il testo lo mette sempre HyperFrames. Prima prova un effetto solo. Vanno in `hyperframes/assets/` e si usano come video di sfondo o in fusione (`screen`, `add`) sopra il render.

Mai su sezioni, esplosi, FEA, quote, loghi, scritte o primi piani del prodotto: lì servono la geometria vera e i numeri veri, solo Blender. Segna in `progetto.md` quali scene contengono AI. Nella scaletta proponi tu dove una scena AI farebbe la differenza (apertura nel mondo, chiusura sul prodotto in uso), perché l'utente spesso non sa che si può fare.
