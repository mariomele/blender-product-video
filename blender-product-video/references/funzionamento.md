# Funzionamento: scheda, cinematica, verifica

Leggila alla fase 1a, prima di modellare, e ogni volta che verifichi il moto di una scena.

## Scheda (`funzionamento.md` del progetto)

Ricavala da tutte le sorgenti:
- **CAD**: parti mobili e i loro assi (con **text-to-cad:robot-simulation**: link, giunti, `cad model ranges <id>` per i fine corsa), accoppiamenti, numero di denti di ingranaggi e pulegge, passo di viti e cremagliere;
- **PDF** (scheda tecnica, manuale, catalogo): corse, velocità, giri/min, cicli/min, portate, sequenza delle fasi, schemi cinematici;
- **descrizione a parole** dell'utente o del cliente: trascrivila in righe misurabili e chiedi i numeri che mancano;
- **sito**: `firecrawl_scrape` delle pagine prodotto e dei video incorporati;
- **video di riferimento**: `$K/contact_sheet.sh <video> preview/ref.jpg 0.25` (un frame ogni 0,25 s) e guarda i frame: verso di rotazione, ordine dei movimenti, tempo del ciclo misurato fra due istanti uguali. Segna i tempi in secondi del video.

Una riga per parte mobile:

| parte | moto (rotazione / traslazione) | asse e verso | corsa o limiti | velocità | mossa da | fase del ciclo | fonte |
|---|---|---|---|---|---|---|---|

Poi il **ciclo** in ordine, con i tempi (es. "0–1,2 s pinza chiude, 1,2–3 s braccio ruota di 90°…"), i **flussi** (materiale, fluido, prodotto: da dove entrano, dove escono, in che verso) e i **vincoli** (parti che non devono mai toccarsi). Ogni riga ha la sua **fonte** (file e pagina, link, secondo del video, "detto dall'utente"); quello che deduci tu è segnato "dedotto" e va confermato; quello che non si ricava si chiede, non si inventa.

La scheda serve anche al modello (fase 1b): ogni parte della scheda deve essere un oggetto a sé, con il perno sul suo asse.

## Cinematica coerente

- Ingranaggi esterni `giri2 = giri1 · z1/z2` con verso opposto (interni: stesso verso).
- Cinghie e catene: stessa velocità lineare sulle pulegge.
- Vite: `avanzamento = giri · passo`. Pignone e cremagliera: `v = ω · r`.
- Anima tutto da una sola variabile di tempo (la proprietà `t` letta dai driver, fase 2) e scrivi i rapporti nei driver: così restano esatti anche con lo slow-mo e gli `extra`.
- **Velocità vere o leggibili**: una macchina vera può essere troppo veloce per l'occhio. Si può rallentare, ma uguale per tutte le parti della scena (i rapporti restano veri) e dicendolo a schermo ("rallentato ×4").

## Verifica su ogni scena

Dopo l'animazione e prima dello storyboard da approvare:

`"$B" -b <scena.blend> --python $K/motion_probe.py -- preview/<n>_moto.json [step] [first last]`

Stampa una riga `PROBE` per ogni oggetto che si muove: rotazione totale e range per asse in gradi, giri/min medi, escursione in metri (moto relativo al genitore, con vincoli e driver). Confronta con la scheda: assi, versi, rapporti fra parti collegate, corse dentro i limiti, ordine e tempi del ciclo; nel JSON hai il valore frame per frame. Per il rapporto fra due ingranaggi confronta gli rpm di parti con lo stesso genitore, o porta i valori nello stesso riferimento.

Scrivi il risultato nella tabella **Verifica** in fondo a `funzionamento.md` (voce · atteso con fonte · misurato · ok/no) e correggi gli scarti prima di andare avanti. In agentica lo fa l'agente del funzionamento.

Checkpoint (guidata): la scheda con le righe dedotte da confermare, poi la tabella Verifica di ogni scena insieme al suo storyboard.
