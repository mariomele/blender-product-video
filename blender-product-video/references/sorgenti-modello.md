# Sorgenti del modello: formati, foto, CAD parametrico

Leggila quando arriva un file da importare, quando l'utente chiede cosa mandare, o quando modelli da foto, disegno o schizzo.

## Formati accettati

Quando l'utente chiede cosa mandare: **STEP** è il migliore (misure esatte, parti separate con il loro nome, pronto per esplosi e sezioni), poi **GLB**.

| Formato | Entra con `import_model.py` | Serve | Unità |
|---|---|---|---|
| **STEP / STP** | sì | **text-to-cad** (comando `cad`) | automatica: le parti restano separate con il loro nome |
| **3MF** | sì | **text-to-cad** | automatica |
| **GLB / glTF** | sì | niente | `m` (tiene colori e parti) |
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

## Altre sorgenti

| Sorgente | Come procedere |
|---|---|
| **Disegno raster o schizzo** | Leggilo, trascrivi le quote in una tabella dentro `progetto.md` e modella in **build123d** (sotto) con quelle quote come parametri. Le quote mancanti si chiedono, non si inventano. Senza `cad`, modella in Blender in Python (bmesh / geometry nodes). |
| **Foto** | Vedi sotto. |
| **Link** | Pagina prodotto → leggila (`firecrawl_scrape` o il browser integrato) per foto, misure, schede tecniche, codici colore; poi procedi come per foto/disegni. Link a un modello (GrabCAD, TraceParts, produttore, Sketchfab) → chiedi l'ok, controlla la licenza, poi `import_model.py`. Salva tutto in `source/`. |

## Da foto

È la sorgente più lenta e la meno precisa: dillo subito.
- Foto che servono: fronte, retro, due lati, alto, una o due 3/4, primi piani di giunzioni, loghi, etichette, comandi. Luce diffusa, niente grandangolo spinto, possibilmente un metro o un oggetto di misura nota nell'inquadratura.
- Almeno **una misura reale** (lunghezza totale o altezza): senza, la scala è inventata.
- Monta le foto come riferimento (`bpy.ops.image.import_as_mesh_planes` o Empty immagine sugli assi) e modella a blocchi, poi dettaglia. Skill: **blender-director**, **hard-surface**, **prop-artist**.
- L'image-to-3D con AI (Higgsfield `generate_3d`, Magnific `models3d_generate`) serve solo per una bozza o per oggetti di contorno, mai per parti tecniche. Costa crediti: chiedi.

## CAD parametrico (build123d)

Se è installato text-to-cad: per le parti meccaniche è più preciso e più veloce che modellare in Blender. Vale per disegni, schizzi, foto con misure e per le parti interne di una sezione.
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
