# Automatica e agentica: percorso, controlli, squadra

Leggila all'inizio di un progetto in automatica o in agentica, e a ogni sessione che ne riprende uno.

## Percorso in automatica (quattro soste)

1. **Sosta 1, brief e scaletta.** Prima del riepilogo leggi le sorgenti e scrivi la scheda di funzionamento (fase 1a): nel riepilogo metti le sue righe dedotte e le domande su quelle che non si ricavano. Metti anche la scaletta, con le riprese vere già al loro posto (b-roll, split, passaggio vero→3D): costruita dall'idea di storia dell'utente (la quarta domanda del brief) o, con "Decidi tu", generata da te dal racconto, con le regole della fase 2. Una riga per scena.
2. **Da solo fino al video muto**: modello, materiali, ambiente, verifica del funzionamento di ogni scena (`motion_probe.py`), storyboard e anteprime, montaggio e render del montaggio con il codice di bozza (`preview_jpg/final.mp4`), senza testi né audio. Se ci sono riprese vere, il video muto le contiene già (`riprese-vere.md`). Durante il lavoro scrivi già, scena per scena, i testi a schermo e la frase della voce in `storyboard.json` (circa 2,5 parole al secondo, entro la durata della scena).
3. **Sosta 2, i testi.** Completa `storyboard.json` (frame, piano, testo a schermo e voce di ogni scena, nelle lingue del brief) e lancia `python3 $K/storyboard_pdf.py storyboard.json delivery/storyboard`: escono lo storyboard in PDF, i `vo_<lingua>.md` e i `vo_<lingua>.txt`. Manda il video muto, il PDF e i `.md`, e chiedi le correzioni. Le correzioni dell'utente sui `.md` le riporti tu in `storyboard.json` e rilanci lo script: i file derivati non si correggono a mano. Se il cliente approva lo storyboard a parte, aspetta il suo ok.
4. **Da solo, video più testi**: grafiche HyperFrames sopra il video muto con i testi approvati (fase 4), con i loro controlli. Bozza: `npx hyperframes render --quality draft -o preview/testi.mp4`.
5. **Sosta 3, video con i testi e ok al finale.** Manda il video e chiedi in una domanda sola: l'ok al video, l'ok alla voce (con la stima dei crediti) e l'ok al render finale con il suo codice di qualità (proposta `4-4-3`) e la stima delle ore. Se crediti o ore superano il budget del brief, dillo nella domanda. La risposta va in `progetto.md`, riga `Ok render finale`. Le correzioni tornano alla fase giusta, poi rifai questa sosta.
6. **Da solo, voce e video finale**: voce con ElevenLabs dai `vo_<lingua>.txt` approvati (fase 5), musica e SFX, `fit_vo.py` per adattare le scene alla voce, render finale con il codice approvato (fase 7), grafiche riallineate su `final_jpg/timings.json` e ricontrollate (fase 5, "Dopo fit_vo"), file di consegna (fase 9).
7. **Sosta 4, consegna.** Mandi il video finale e i file di consegna, con il riepilogo dei controlli fatti.

Dopo un "rifai" o una richiesta nuova riprendi il percorso dal punto in cui eri, e dillo in una riga. Se la richiesta tocca qualcosa già approvato a una sosta (testi, video con i testi), ripassa da quella sosta.

## Controlli in automatica

Al posto di ogni checkpoint guardi tu il risultato (`Read` sui JPG e sui PNG di snapshot) e lo correggi prima di passare oltre. Ogni controllo va in `progetto.md`, sotto Decisioni: cosa hai visto, cosa hai corretto. Se dopo due correzioni un problema resta, è una sosta: mostralo e chiedi. Alle soste mostra anche il riepilogo dei controlli.

| Fase | Controlla |
|---|---|
| 1a funzionamento | ogni riga di `funzionamento.md` ha la sua fonte; quello che non si ricava è una sosta, non una scelta tua |
| 1b modello | proporzioni e colori contro le foto di riferimento, scala reale (una misura nota), nessuna parte mancante o capovolta, normali e materiali senza nero o rosa |
| 2 scene | il moto misurato con `motion_probe.py` torna con `funzionamento.md` (assi, versi, rapporti, corse, ordine del ciclo); il soggetto resta in quadro, nessuna compenetrazione, i giunti dentro i limiti, la camera non attraversa oggetti, il movimento si legge |
| 3 montaggio | le regole del montaggio della fase 2, durata totale entro ±10% del brief |
| 3 riprese vere | stessa macchina e stessa versione del 3D, nello split lo stesso istante del ciclo (±2 frame), colore e contrasto vicini al render, niente tremolio né rotazione sbagliata |
| 4 testi | le regole di "Scrivere voce e testi" (fase 4), ogni numero con la sua fonte |
| 4 grafiche | le regole di "Grafiche animate" (fase 4), zone sicure (`hyperframes.md`), solo colori della palette, misure uguali alla sorgente |
| 5 audio | ogni scena dura quanto la sua voce più il margine (`fit_vo.py`), pronuncia di nomi e sigle, musica sotto la voce |

## Modalità agentica

Stesso percorso, stesse soste e stesse regole di budget dell'automatica. In più il lavoro si divide fra **subagenti** (strumento `Agent`, in background), come in una piccola casa di produzione. Tu sei il **produttore**: parli con l'utente, tieni `progetto.md`, `storyboard.json`, il budget, le soste e i render, e scegli fra le proposte degli agenti; il racconto lo decidono regista e sceneggiatore. Ogni agente riceve un compito stretto, i file da leggere e quello che deve rendere; scrive solo nei suoi file e ti torna un rapporto breve. Il suo rapporto è un'indicazione, non una prova: controlla il risultato prima di segnarlo fatto.

| Agente | Quando parte | Cosa fa | Rende |
|---|---|---|---|
| **Regista** | dopo il brief, poi su storyboard, anteprime e montaggio | scrive il **trattamento** (la storia in 5 righe: chi guarda, il problema, la svolta, la prova, come finisce), da lì la scaletta con piani, movimenti e ritmo (fase 2); sulle bozze giudica il racconto: si capisce, tiene l'attenzione, il ritmo respira | `trattamento.md`, la scaletta, note di regia per scena |
| **Sceneggiatore** | insieme al regista, poi dopo ogni cambio di scaletta | scrive voce e testi a schermo come racconto, con le regole della fase 4; propone 2–3 agganci diversi | `testi.md` (per scena e lingua: voce e testo a schermo), `agganci.md`; tu li copi in `storyboard.json` |
| **Funzionamento** (il più importante) | prima del modello (1a), poi su ogni anteprima e sul montaggio | legge le sorgenti senza vedere il tuo lavoro, scrive o controlla `funzionamento.md`, poi misura il moto delle scene con `motion_probe.py` e lo confronta riga per riga | la tabella Verifica di `funzionamento.md`, con ogni scarto e la scena e i frame dove sta |
| **Revisore tecnico** | storyboard, anteprime, montaggio | guarda solo i frame (griglie, provini, snapshot) con la scaletta e la scheda: compenetrazioni, camera che attraversa oggetti, materiali neri o rosa, scatti, continuità | elenco dei problemi con scena, frame e gravità (blocca / da sistemare / gusto) |
| **Motion designer** | dopo la sosta 2, sui testi approvati | progetta e costruisce le grafiche animate HyperFrames e le controlla in movimento, con le regole della fase 4; dopo `fit_vo.py` le riallinea sui nuovi tempi | `hyperframes/` con `check` pulito, snapshot a più istanti per scena, `grafiche.md` con i tempi di ogni elemento |
| **Audio** | dopo la sosta 2, sui testi approvati | solo suono: scaletta degli SFX con i loro istanti, brief e prompt della musica, piano del mix sotto la voce; non spende crediti | `audio/sfx.md`, `audio/musica.md`, `audio/mix.md` |
| **Riprese vere** | appena arrivano i video | analizza le riprese (durata, fps, rotazione, stabilità, pezzi buoni con in e out, istanti del ciclo) | `source/video/riprese.md` e un provino per ripresa |
| **Spettatore** | sulla bozza completa, prima della sosta 3 (e prima della consegna) | guarda il video senza sapere niente del progetto, né brief né scaletta: dice in una frase cosa ha capito, dove si è perso, quale testo non ha fatto in tempo a leggere, cosa ricorda | `spettatore.md`; lo confronti tu con "Cosa deve capire chi guarda" del brief |

**Come si passano il lavoro.**
1. Prima di ogni render: funzionamento (la scheda), regista e sceneggiatore (trattamento, scaletta e testi in bozza). La scaletta segue la storia, non il contrario. Trattamento e agganci vanno nel riepilogo della sosta 1.
2. Durante i render delle scene e del montaggio: funzionamento e revisore tecnico; il regista guarda storyboard e anteprime per il racconto.
3. Dopo la sosta 2: il motion designer fa le grafiche sui testi approvati, l'audio prepara SFX, musica e mix.
4. Prima della sosta 3: lo spettatore. Se la sua frase non coincide con "Cosa deve capire chi guarda", regista e sceneggiatore correggono prima che il video arrivi all'utente.

Regole:
- **Una GPU sola**: i render Blender li lanci solo tu, uno alla volta. Gli agenti lavorano sul resto, ed è lì che si guadagna tempo.
- **Indipendenza dei controlli**: revisore tecnico, funzionamento e spettatore non ricevono le tue conclusioni, solo i materiali (lo spettatore nemmeno quelli: solo il video); altrimenti trovano giusto quello che hai già trovato giusto tu. Un problema "blocca" torna alla fase giusta; dopo due giri senza soluzione è una sosta.
- **Mai due agenti sugli stessi file.** `storyboard.json` e `progetto.md` li scrivi solo tu. Al massimo quanti ne dice la riga `Agenti` (di default 3 insieme): gli agenti si alternano per fase, non partono tutti insieme. Gli agenti consumano token: dillo nel brief, con la modalità.
- Le generazioni a pagamento (voce, musica, SFX, AI) le lanci tu, dentro il budget, non gli agenti.

## Soste sul telefono

In agentica, e anche in automatica se l'utente lo chiede. I render lunghi girano con Bash `run_in_background`. A ogni sosta manda il file da guardare con `SendUserFile` (status `proactive`: il video leggero, il PDF, il provino) e una domanda di una riga; l'utente può rispondere dal telefono ("ok", "rifai la scena 3", "stop"). Se `SendUserFile` non c'è, scrivi il percorso completo del file. Il render finale di notte funziona così: parte con l'ok della sosta 3 e la consegna arriva sul telefono alla sosta 4.

## Senza soste

Riga `Modalità: agentica senza soste`, solo se l'utente lo chiede. Va dal brief alla consegna senza fermarsi: trattamento, scaletta, aggancio, testi e voce li scelgono regista e sceneggiatore e li approvi tu come produttore; la voce si genera dentro il budget; il render finale parte con il codice e il tetto di ore scritti nel brief (riga `Budget`, voce `finale ≤ N h`; senza quella voce ti fermi prima del finale). Nella consegna metti lo storyboard in PDF e i `vo_<lingua>.md` segnati "da approvare".

Restano le fermate per una spesa fuori budget, una cancellazione, un dato che non si inventa e un problema di funzionamento che non si risolve dopo due giri (lì ti fermi e lo mandi sul telefono: un video che si muove male non va consegnato). Se invece è lo spettatore a non capire dopo due giri di correzioni, non fermarti: consegna, e scrivi in testa al riepilogo cosa ha capito lui e cosa doveva capire, come primo punto da rivedere.

Consigliala solo per prove interne o per varianti di un video già approvato, mai per un primo video da mandare al cliente.
