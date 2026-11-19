# Scene con text-to-cad: resistenza, giunti, tavola tecnica

Leggila quando il brief chiede calcoli, una tavola quotata o il movimento vero di un robot. Servono il comando `cad` e il pezzo in STEP.

## Resistenza (FEA)

Il pezzo che si piega sotto carico mentre si colora dal blu al rosso, dove regge e dove è al limite. Con la skill **text-to-cad:fea**: scegli le facce bloccate e caricate (`cad step solve <pezzo>.step` le elenca), e prendi carico e materiale dal cliente: non si inventano. Poi `cad step solve <pezzo>.step --study study.json --out fea/`, e da lì:

```
cad run --with meshio $K/fea_surface.py fea/result.vtu fea/surface.npz
"$B" -b --factory-startup --python $K/fea_to_blend.py -- fea/surface.npz fea/fea.blend <snervamento_MPa> [scala|auto] [first] [last]
```

Il .blend contiene l'oggetto `FEA`. Fra `first` e `last` il carico entra: il pezzo si deforma e passa dal metallo ai colori. Il rosso corrisponde allo snervamento, quindi rosso vuol dire "qui cede". Aggiungi camera e luci come in ogni scena, o collega l'oggetto (`Append`) nella scena del prodotto. In sovrimpressione, con HyperFrames, metti la scala colori, il carico in N o kg e il coefficiente di sicurezza da `result.json`. La deformazione è esagerata (il fattore lo stampa lo script): dillo in un testo a schermo. Fai approvare i numeri al cliente prima del render.

## Movimento vero di un robot o di una macchina con giunti

Con la skill **text-to-cad:robot-simulation**, partendo dallo STEP del costruttore (la sua ricetta "from a vendor STEP": raggruppa le parti in link e trova gli assi dalla geometria). `cad model ranges <id>` trova i fine corsa di ogni giunto dove le parti si toccano; se il cliente ha la scheda tecnica con le escursioni degli assi, valgono quelle. In Blender metti il perno di ogni parte sull'asse del giunto e un vincolo `Limit Rotation` (o `Limit Location` per gli assi lineari) con quei limiti, poi anima dentro i limiti: il braccio si muove come quello vero, senza compenetrazioni. Assi e limiti vanno in `funzionamento.md`. URDF e MJCF servono solo se il cliente li vuole per la simulazione.

## Tavola tecnica

Con la skill **text-to-cad:engineering-drawing** crea il PDF quotato dal modello, e convertilo in immagine con `sips -s format png`. Usi nel video: la tavola che si dissolve nel pezzo 3D con la camera allineata alla vista frontale, oppure la tavola come piano in scena, con le linee che si accendono. Il PDF si consegna anche in fase 9 (`delivery/<nome>_tavola.pdf`).
