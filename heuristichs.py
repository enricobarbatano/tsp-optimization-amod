import numpy as np
# importo numpy per eseguire calcoli matematici efficienti

# come per lo script tsp_to_dat leggo il file tsp.lib nella directory di input e inserisco le coordinate in una lista (coord),
# successivamente trasformo la lista in un array numpy per rendere i calcoli molto più efficienti.
def read_tsplib(filename):
    """
    Legge un file TSPLIB (.tsp o .tsp.gz) e restituisce la matrice dei costi euclidei.
    """
    coords = []
    in_coords = False  # flag che indica quando iniziare a leggere le coordinate

    with open(filename, "rt") as f:
        for line in f:
            line = line.strip()

            # se troviamo la sezione delle coordinate, attiviamo il flag
            if "NODE_COORD_SECTION" in line:
                in_coords = True
                continue

            # se raggiungiamo la fine del file, interrompiamo la lettura
            if "EOF" in line:
                break

            # se non siamo ancora nella sezione delle coordinate, saltiamo la riga
            if not in_coords:
                continue

            parts = line.split()
            # verifichiamo che la riga inizi con un indice numerico e contenga almeno 3 colonne
            if len(parts) >= 3 and parts[0].isdigit():
                try:
                    coords.append((float(parts[1]), float(parts[2])))
                except ValueError:
                    # ignoro righe non numeriche (come COMMENT o TYPE)
                    continue

    coords = np.array(coords)
    n = len(coords)

    cost = np.zeros((n, n))
    # creo una matrice dei costi NxN

    for i in range(n): 
        for j in range(n):
            if i != j:
                # per ogni coppia (i,j) con i != j, calcolo la distanza euclidea e la arrotondo a due decimali
                cost[i, j] = round(np.linalg.norm(coords[i] - coords[j]), 2)
                
    return cost 
    # ritorno la matrice dei costi



# funzione che usiamo per trovare una soluzione approssimata del tour a costo maggiore
def max_diversity(cost):
    
    n = len(cost)
    # definiamo n = numero di nodi
    
    i, j = divmod(np.argmax(cost), n)   
    # trova la coppia più distante tramite argmax(cost) e converte l'indice lineare in coordinate (i, j)
    
    tour = [i, j, i]
    # inizializzo il tour iniziale con i nodi più distanti
    
    remaining = set(range(n)) - {i, j}
    # definisco l'insieme dei nodi rimanenti
    
    while remaining:
        # cicla finché remaining non è vuoto
        
        best_node = max(remaining, key=lambda node: np.mean([cost[node, v] for v in tour[:-1]]))
        # sceglie il nodo con distanza media maggiore tra quelli rimasti
        
        best_pos = max(
            range(len(tour)-1),
            key=lambda k: cost[tour[k], best_node] + cost[best_node, tour[k+1]] - cost[tour[k], tour[k+1]]
        )
        # calcola in quale posizione inserire il nodo per massimizzare il costo totale
        
        tour.insert(best_pos+1, best_node)
        remaining.remove(best_node)
        # inserisce il nodo nella best_pos trovata nel tour e lo rimuove dall'insieme dei nodi rimanenti

    return tour



def tour_cost(cost, tour):
    # funzione che calcola il costo del tour trovato sommando i singoli costi tra nodi consecutivi nel tour
    return sum(cost[tour[i], tour[i + 1]] for i in range(len(tour) - 1))



def two_opt(cost, tour):
    # definisce la funzione two_opt che tenta di migliorare la soluzione trovata
    
    best = tour
    # inizializzo come best_tour il tour base che abbiamo passato in input
    
    improved = True 
    # flag che ci permette di entrare nel while alla prima iterazione: serve per ripetere l'iterazione finché si trova un miglioramento
    
    while improved:
        # se improved alla fine delle iterazioni è ancora False significa che non ha trovato miglioramenti, quindi esce dal ciclo
        improved = False
        
        for i in range(1, len(best) - 2): 
            # ciclo sui nodi i (non partendo dal primo per fissare il nodo iniziale)
            
            for j in range(i + 2, len(best) - 1): 
                # salto i+1 per evitare archi consecutivi
                
                new_tour = best[:i] + best[i:j][::-1] + best[j:] 
                # creo il nuovo tour: [tour prima di i] + [segmento (i,j) invertito] + [tour dopo j]
                
                if tour_cost(cost, new_tour) > tour_cost(cost, best):
                    best, improved = new_tour, True
                    # se il nuovo tour ha costo maggiore del best_tour, aggiorna il best_tour e continua a cercare
                
        tour = best
        # dopo aver ciclato tutti gli (i,j), aggiorno tour con l'ultima soluzione migliore
        
    return best



# con questo idioma Python possiamo eseguire lo script direttamente per testarlo su un'istanza (nel nostro caso berlin52.tsp)
if __name__ == "__main__":
    
    filename = "C:/Users/User/OneDrive/Desktop/Progetti_Uni/Progetto_Amod/.vscode/tsplib/berlin52.tsp"
    
    cost = read_tsplib(filename)

    tour = max_diversity(cost)
    tour = two_opt(cost, tour)

    print("Tour trovato:", tour)
    print("Costo:", tour_cost(cost, tour))
