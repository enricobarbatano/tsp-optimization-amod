# TSP Optimization Project – Modelli PLI ed Euristici

## Descrizione

Questo progetto, sviluppato per il corso di **Algoritmi e Modelli per l'Ottimizzazione Discreta (AMOD)**, analizza e confronta diversi approcci di **ottimizzazione combinatoria** per la risoluzione del **Travelling Salesman Problem (TSP)**.

Il TSP consiste nel determinare un ciclo di costo minimo che visiti ogni nodo esattamente una volta e ritorni al nodo di partenza. Nel progetto vengono confrontati due approcci principali:

1. **Modello PLI (Programmazione Lineare Intera)** implementato in AMPL, utilizzato per ottenere soluzioni esatte tramite solver di ottimizzazione.
2. **Algoritmo euristico personalizzato** implementato in Python, progettato per ridurre i tempi computazionali mantenendo una buona qualità della soluzione.

Il progetto include inoltre script Python per convertire istanze TSPLIB in file `.dat` compatibili con AMPL, eseguire esperimenti e generare risultati comparativi.

---

## Obiettivi

Gli obiettivi principali del progetto sono:

- confrontare il comportamento di metodi esatti ed euristici nella risoluzione del TSP;
- analizzare il trade-off tra **costo computazionale** e **qualità della soluzione**;
- testare le soluzioni su istanze simmetriche di diversa dimensione;
- automatizzare la conversione delle istanze TSPLIB in formato `.dat` per AMPL;
- confrontare graficamente e tabellarmente i risultati ottenuti;
- valutare l'efficienza dell'euristica rispetto alla soluzione prodotta dal modello esatto.

---

## Tecnologie e strumenti utilizzati

- Python 3.x
- NumPy
- Matplotlib
- AMPL
- amplpy
- Solver compatibili con AMPL, ad esempio CPLEX, Gurobi, HiGHS o CBC
- File `.mod`, `.dat` e `.run` per la modellazione e l'esecuzione in AMPL

---

## Installazione

Per eseguire la parte Python del progetto è necessario installare le dipendenze presenti nel file `requirements.txt`.

Clonare il repository:

```bash
git clone <https://github.com/enricobarbatano/tsp-optimization-amod.git>
```

Entrare nella cartella del progetto:

```bash
cd <vscode>
```

Installare le librerie Python richieste:

```bash
pip install -r requirements.txt
```

Su Windows, se il comando `pip` non viene riconosciuto, è possibile usare:

```bash
py -m pip install -r requirements.txt
```

Il comando installa le librerie Python necessarie per eseguire gli script, tra cui `numpy`, `matplotlib` e `amplpy`.


---

## Nota su AMPL

Il file `requirements.txt` installa solo le dipendenze Python del progetto.

Per eseguire il modello esatto è necessario avere anche **AMPL** configurato correttamente sul proprio sistema, insieme a un solver compatibile.

La cartella AMPL del progetto contiene i file necessari per la modellazione e l'esecuzione, ad esempio:

- file `.mod` per la definizione del modello matematico;
- file `.dat` contenenti i dati delle istanze;
- file `.run` per automatizzare l'esecuzione del modello AMPL.

Se si utilizza `amplpy`, è possibile interfacciare Python con AMPL direttamente dagli script Python. Tuttavia, AMPL e il solver devono essere disponibili e configurati correttamente nell'ambiente di esecuzione.

---

## Esecuzione

Il progetto può essere eseguito seguendo questi passaggi:

1. Installare le dipendenze Python:

```bash
pip install -r requirements.txt
```

2. Preparare o inserire le istanze TSP nella cartella dedicata.

3. Convertire eventuali file `.tsp` in file `.dat` compatibili con AMPL usando lo script:

```bash
python tsp_to_dat.py
```

Su Windows, se necessario:

```bash
py tsp_to_dat.py
```

4. Eseguire gli esperimenti tramite lo script principale:

```bash
python experiment.py
```

Oppure su Windows:

```bash
py experiment.py
```

5. Analizzare i risultati prodotti, inclusi grafici, tempi computazionali e confronto tra soluzione esatta ed euristica.

---

## Struttura del progetto

```text
.
├── ampl/
│   ├── *.mod
│   ├── *.dat
│   └── *.run
├── results/
├── experiment.py
├── heuristichs.py
├── tsp_to_dat.py
├── requirements.txt
└── README.md
```

### Descrizione dei file principali

- `experiment.py`  
  Script principale per l'esecuzione degli esperimenti, l'interazione con AMPL tramite `amplpy`, la raccolta dei risultati e la generazione dei grafici comparativi.

- `heuristichs.py`  
  Contiene le funzioni euristiche per la costruzione e il miglioramento delle soluzioni TSP, inclusa la valutazione del costo del tour.

- `tsp_to_dat.py`  
  Script per convertire istanze TSPLIB `.tsp` in file `.dat` utilizzabili dal modello AMPL.

- `ampl/`  
  Cartella contenente i file AMPL del progetto, come modelli `.mod`, dati `.dat` e script `.run`.

- `results/`  
  Cartella destinata al salvataggio di output, grafici e risultati degli esperimenti.

- `requirements.txt`  
  File contenente le dipendenze Python necessarie per eseguire il progetto.

---

## Risultati

Il progetto permette di valutare:

- il tempo di esecuzione del modello esatto rispetto all'euristica;
- la qualità della soluzione euristica rispetto alla soluzione ottenuta tramite AMPL;
- l'impatto della dimensione dell'istanza sui tempi computazionali;
- la differenza tra approccio esatto e approccio approssimato;
- l'efficacia dell'euristica in termini di rapidità e qualità della soluzione.

I risultati vengono analizzati tramite tabelle e grafici comparativi generati dagli script Python.

---

## Note

Il progetto utilizza AMPL per la formulazione esatta del problema e Python per l'automazione degli esperimenti, la gestione delle istanze e l'analisi dei risultati.

La parte Python può essere installata tramite `requirements.txt`, mentre AMPL e il solver devono essere installati o configurati separatamente.

---

## Autore

**Enrico Barbatano**
