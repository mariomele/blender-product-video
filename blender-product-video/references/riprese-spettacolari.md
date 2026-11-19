# Riprese spettacolari

Leggila quando scrivi la scaletta (fase 2). Oltre ai piani di presentazione e a quelli classici, ogni video ne ha diverse, circa una scena ogni 2–3: quelle che sembrano impossibili, o fatte con un braccio robotico (motion control) o con un drone FPV. Proponile sempre, anche se l'utente non le chiede, e segnale con ★ nella scaletta.

- **Velocità estreme e speed ramp**: un movimento lentissimo, tipo slow-mo, su un istante chiave (pezzo che si incastra, scintilla, goccia), poi un'accelerazione di colpo; oppure passaggi velocissimi con motion blur. In 3D lo slow-mo è gratis: l'animazione è procedurale, quindi basta rimappare il tempo con una curva (proprietà `t` sull'oggetto, letta dai driver) e campionare più fitto.
- **Follow e POV**: la camera segue un pezzo lungo il percorso, imparentata o con `Follow Path` e `Damped Track` (il prodotto sul nastro, il fluido nel condotto, la catena sugli ingranaggi). Oppure entra dentro la macchina passando da una fessura.
- **Braccio robotico**: traiettorie lunghe e precise che passano a pochi centimetri dalle parti, sfiorano un bordo, si fermano di colpo su un dettaglio e ripartono. Curve Bezier lisce, con accelerazioni nette all'inizio e alla fine.
- **Contromovimento**: mentre la macchina o un pezzo ruota, la camera orbita in verso opposto, così la rotazione sembra doppia. Funziona anche con un carrello laterale contro il nastro.
- **Cambio di vista in continuità**: senza tagli si passa dall'esploso alla sezione, o dal prodotto intero alla sezione, con il cutter che si apre mentre la camera entra. Oppure la camera attraversa un pannello che diventa trasparente.
- **Angolazioni insolite**: da sotto la macchina, da dentro un tubo, dall'alto a piombo con la camera che ruota sull'asse, a filo di pavimento, inclinata (dutch). Anche un dolly zoom (vertigo), o un fuoco che passa da un dettaglio all'altro (rack focus).
- **Raccordo veloce**: una frusta (whip pan) o un passaggio stretto fra due parti, che diventa il taglio verso la scena dopo.

Le scene spettacolari stanno fra piani più calmi, che danno respiro e contesto. Il motion blur e le traiettorie vicine alle parti si controllano nell'anteprima, non nello storyboard: il blur costa tempo di render, quindi attivalo solo nelle scene veloci.
