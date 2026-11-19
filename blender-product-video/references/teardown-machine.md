# Alternativa veloce e pagina interattiva (`/teardown`, `/machine`)

Leggila quando nel brief serve un video "come funziona" in pochi minuti senza fedeltà al prodotto vero, o quando l'utente vuole una pagina 3D interattiva.

## Alternativa veloce con `/teardown` (se è installata)

Quando la fedeltà al prodotto vero non conta (idea, pitch, spiegazione di un principio), proponila al posto di Blender. `/teardown` ricostruisce la macchina a codice in three.js e registra un tour in mp4 con il suo sonoro: minuti invece di ore di render, ma forme e proporzioni sono approssimate e la resa non è quella di Cycles. Non usarla se servono misure, loghi o materiali veri, né mescolarla con scene Blender nello stesso video. Se l'utente la sceglie, segui la sua skill; da questa riprendi la domanda del render (risoluzione e durata; fps e qualità se `/teardown` li supporta), le zone sicure del 9:16 per i testi (`hyperframes.md`) e la consegna (fase 9).

## Pagina interattiva (fase 9)

Solo se chiesta nel brief e se `/machine` o `/teardown` è installata; con tutte e due chiedi quale. Usa la skill scelta per creare `delivery/<nome>.html`: un file unico in three.js, da aprire nel browser o mettere in un iframe, con esploso, sezione, radiografia e numeri calcolati. Passale le misure, la distinta dei pezzi con i materiali e i dati tecnici raccolti in `progetto.md` e `funzionamento.md`. Avvisa che la skill ricostruisce il pezzo con forme proprie: è una versione semplificata, non carica il modello Blender e ha una resa diversa da Cycles. Per questo non va montata dentro il video. Mostrala con uno screenshot e falla approvare a parte.
