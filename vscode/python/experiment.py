
import os, time, csv 
# os per operazioni con il filesystem, time per misurare i tempi, csv per scrivere i risultati nel file di oytput
import numpy as np, matplotlib.pyplot as plt
# numpy lo usiamo per operazioni numeriche, matplolib lo utilizziamo plottare i risultati
from amplpy import AMPL
# importo la classe AMPL che ci permette di comunicare con il modello AMPL (caricare modelli, dati, risolvere)
from heuristichs import read_tsplib, max_diversity, two_opt, tour_cost
#importiamo le funzioni definite nello script heuristichs.py 
import tsp_to_dat
#importo il modulo che consente la trasformazione del file .tsp in file .dat.






def reconstruct_tour_from_ampl(ampl, n_nodes):
    # questa funzione restituisce una lista di nodi 0-based che rappresentano il ciclo
    try:
        # in questa porzione di codice proviamo a leggere le variabili x[i,j] dal modello AMPL (trasformiamole da 1-based a 0-based)
        edges = [(int(i)-1, int(j)-1)
                 for (i,j),val in ampl.getVariable("x").getValues().toDict().items()
                 if val and val > 0.5]
        #edge non è altro che la lista di archi selezionati con coppie (i,j) in 0-based
    except Exception:
        return None
    if not edges:
        return None
    #se la lettura degli archi fallisce o nella lista non ci sono archi, ritorna NONE (nessun tour trovato)

    succ = {i: j for i, j in edges}
    #definiamo il dizionario che mappa ogni nodo i al successivo nodo j
    tour = [0]
    # la costruzione del tour inizia come convenzione dal nodo 0
    
    while len(tour) < n_nodes:
        #finchè il tour non contiene ogni nodo, continua a ciclare
        
        next = succ.get(tour[-1])
        #con questa riga prendiamo il nodo successivo in next
        
        if next is None or next in tour:
            return None
        #se next è già nel tour o manca l'arco uscente la funzione fallisce e ritorna NONE
        
        tour.append(next)
        #se tutto ok si aggiunge next al tour
        
    return tour + [0]
    #alla fine ci viene restituita la lista (tour) chiusa aggiungendo il ritorno al nodo [0]






def plot_tours(coords, tour_ampl, tour_heur, name, folder, costo_a, costo_h):
    #questa funzione che plotta i tour prende in input: la lista delle coppie con le coordinate dei nodi, 
    #le liste di nodi per ampl e heuristchs, il nome dell'istanza, la cartela e i rispettivi costi
    
    coords = np.array(coords)
    #converte la lista coords in un array NumPy utile per le performance delle operazioni
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    #creo la figura con due subplot (1 riga, 2 colonne) e imposto la dimensione dell'immagine 
    
    for ax, tour, title, color in [
        (axes[0], tour_ampl, "AMPL", "green"),
        (axes[1], tour_heur, "Euristica", "red"),
    ]:
    #ciclo su due tuple, associando il primo subplot al tour AMPL e il secondo subplot all'euristica,
    #rendo tutto più compatto grazie al for.
    
        if tour:
            xs, ys = [coords[i][0] for i in tour], [coords[i][1] for i in tour]
            #se il tour esisto creo due liste con le coordinate xs e ys per ogni tour 
            
            ax.plot(xs, ys, "-o", color=color, markersize=4)
            #disegno il percorso nel piano: collego ogni punto (xs[k], ys[k]) a (xs[k+1], ys[k+1])
            
        for idx, (x, y) in enumerate(coords):
            #per ogni nodo presente in coords, scrivo il suo indice 1-based vicino alla coordinata del garfico
            ax.text(x, y, str(idx + 1), fontsize=7, ha="right", va="bottom")
        ax.set_title(title)
        #imposto il titolo del subplot: AMPL o Euristica 
        ax.axis("equal")

    fig.suptitle(
        f"Confronto tour — {name}\nAMPL={costo_a:.2f} | Eur={costo_h:.2f}",
        fontsize=12,
    )
    #titolo generale della figura dove mostro nome dell'istanza, e costi delle due istanze
    
    plt.tight_layout()
    #ottimizzo le figure per evitare sovrapposizioni
    
    plt.savefig(os.path.join(folder, f"tour_{name}.png"), dpi=200)
    # salvo la figura in formato PNG nella cartella folder (data in input)
    
    plt.close()
    #chiudo la figura






def run_experiments(
    
    tsplib_folder=r"C:\Users\User\OneDrive\Desktop\Progetti_Uni\Progetto_Amod\.vscode\tsplib",
    ampl_folder=r"C:\Users\User\OneDrive\Desktop\Progetti_Uni\Progetto_Amod\.vscode\ampl",
    results_folder=r"C:\Users\User\OneDrive\Desktop\Progetti_Uni\Progetto_Amod\.vscode\result",
    #dichiariamo le cartelle dove si trovano i file tsp, dat e quella dove salvare i risultati
    
    timeout=2400,
    #impostiamo un tempo limite per il solver (20 minuti in questo caso)
):
    
    os.makedirs(results_folder, exist_ok=True)
    #creo  la cartella dei risultati se non esiste, la flag exist_ok evita l'eccezione.
    
    results = []
    #definisco la lista dei risultati

    instances = [
        f for f in os.listdir(tsplib_folder) if f.endswith((".tsp", ".tsp.gz"))
    ]
    #inserisco nella lista istanze, tutti i file nella cartella TSPLIB_FOLDER che finiscono per .tsp o .tsp.gz
    
    instances.sort()
    #li riodino alfabeticamente

    for fname in instances:
        #inizio il ciclo per ogni file presente nekla lista istances
        
        base = fname.replace(".tsp", "").replace(".gz", "")
        #calcolo il nome base dell'istanza rimuovwndo le esetnsioni
        
        tsp_file, dat_file = os.path.join(tsplib_folder, fname), os.path.join(
            ampl_folder, base + ".dat"
        )
        #costruisco i percorsi per tsp sorgente e dat corrispondente
        
        print(f"\n {fname}")
        #stampo il nome dell'istanza per avvisare il fatto che sta per essere processata

        
        if not os.path.exists(dat_file):
            tsp_to_dat.tsp_to_dat(tsp_file, dat_file)
        #richiamo il metodo tsp_to_dat nel caso in cui la conversione in .dat non esiste


        if os.path.exists(dat_file):
            size_ampl_mb = os.path.getsize(dat_file) / (1024 * 1024)  # MB
        else:
            size_ampl_mb = 0.0
        #determino la dimensione su disco in MB del file .dat, se il file non esiste, assegno 0 MB
        
        #CALCOLO TSP TRAMITE EURISTICA
        cost_matrix = read_tsplib(tsp_file)
        #prendo la matrice dei costi dell'istanza tsp tramite la funzione read_tsplib in heuristichs
        n = len(cost_matrix)
        #segno il numero di nodi dell'istanza
        
        size_heur_mb = cost_matrix.nbytes / (1024 * 1024)
        #definisco il peso dell'euristica (in MB), considerando il peso in RAM della matrice dei costi

        
        t0 = time.time()
        #segno il tempo di inizio per il calcolo
        
        tour_heur = two_opt(cost_matrix, max_diversity(cost_matrix))
        #calcolo il best tour con max-diversity -> two-opt
        
        th = time.time() - t0
        #calcolo il tempo totale come tempo finale-tempo iniziale (in secondi)
        
        costo_h = tour_cost(cost_matrix, tour_heur)
        #calcolo il costo totale del tour euristico
        
        if tour_heur[-1] != tour_heur[0]:
            tour_heur.append(tour_heur[0])
        #controllo che il tour sia chiuso, in cso contrario lo chiudo io.
        
        
        #CALCOLO TSP TRAMITE AMPL
        
        ampl = AMPL()
        #creo un istanza dell'oggetto AMPL
        
        ampl.read(os.path.join(ampl_folder, "tsp_max.mod"))
        #carico il file del modello  AMPL tsp_max.mod
        
        ampl.readData(dat_file)
        #carico il file .dat
        
        ampl.option["solver"], ampl.option["cbc_options"] = "cbc", f"timelimit={timeout}"
        #imposto le opzioni AMPL come il solver e il timeout
        
        t0 = time.time()
        #segno il tempo di inizio del calcolo
        
        ampl.solve()
        #eseguo il calcolo
        
        ta = time.time() - t0
        #calcolo il tempo impiegato come tempo finale-tempo iniziale
        
        costo_a = ampl.getObjective("TotalCost").value()
        #memorizzo il costo del modello 
        
        tour_ampl = reconstruct_tour_from_ampl(ampl, n)
        if not tour_ampl:
            print("Nessun tour AMPL, uso euristica")
            tour_ampl, costo_a, ta = tour_heur[:], costo_h, 0.0
        #richiamo la funzione definita sopra per ricostruire il tour a partire dalle variabili x del modello AMPl

        #LETTURA DELLE COORDINATE PER IL PLOTTING
        
        coords = []
        
        #estrazione delle coordinate da TSPLIB come già fatto in tsp_to_dat
        with open(tsp_file, "rt") as f:
            in_coord = False
            for line in f:
                if "NODE_COORD_SECTION" in line:
                    in_coord = True
                    continue
                if "EOF" in line:
                    break
                if in_coord:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        coords.append((float(parts[1]), float(parts[2])))

        #RICHIAMO LA FUNZIONE PLOT_TOUR PER CREARE E SALVARE LA FIGURA COMPARATIVA TRA EURISTICA E AMPL
        plot_tours(coords, tour_ampl, tour_heur, base, results_folder, costo_a, costo_h)
        
        gap = (costo_a - costo_h) / costo_a * 100 if costo_a else 0
        #calcolo il gap tra euristica e ampl

        n_archi = len(tour_ampl) - 1 if tour_ampl else 0
        #calcolo il numero di archi  (metto il -1 perchè l'ultimo elemento è uguale al primo)
        
        msg = (
            f"AMPL={costo_a:.2f} ({ta:.2f}s, {n_archi} archi) | "
            f"Eur={costo_h:.2f} ({th:.2f}s) | Gap={gap:.2f}% | "
            f"Peso_AMPL={size_ampl_mb:.3f}MB | Peso_Euristica={size_heur_mb:.3f}MB"
        )
        #costruisco una stringa msg formattata con: costo e tempo AMPL e euristica, gap percentuale, peso file .dat e peso euristica  

        if n_archi != n:
            msg += f"Attesi {n}, trovati {n_archi}"
        # se il numero di archi trovati è diverso dal numero di nodi, aggiunge un avviso alla stringa.    
        
        print(msg)
        #stampo il messaggio per l'istanza corrente
        
        results.append([
            fname, n, costo_a, costo_h, gap, ta, th, n_archi,
            size_ampl_mb, size_heur_mb
        ])
        #aggiungo una riga alla lista result, con i valoeri da salvare successivamente nel csv


    # SALVO I RISULTATI OTTENUTI NEL FILE CSV ALLA FINE DELLA FUNZIONE RUN_EXPERIMENT CHE CICLA TITTE LE ISTANZE
    with open(os.path.join(results_folder, "comparison.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        
        writer.writerow([
            "Istanza",
            "Nodi",
            "Costo_AMPL",
            "Costo_Euristica",
            "Gap(%)",
            "Tempo_AMPL(s)",
            "Tempo_Euristica(s)",
            "Archi_AMPL",
            "Peso_AMPL(MB)",
            "Peso_Euristica(MB)",
        ])
        #scrivo la riga di intestazione con i nomi delle colonne

        writer.writerows(results)
        #scrivo le righe accumulate nella lista results sul CSV
        
# Eseguo la funzione principale se lo script viene lanciato direttamente
if __name__ == "__main__":
    run_experiments()
