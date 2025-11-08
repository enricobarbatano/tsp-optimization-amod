import os 
#libreria che ci serve per utilizzare il filesystem

import numpy as np 
#libreria cdhe ci implementa le operazioni numeriche (ci serve per calcolare le distanze)

def tsp_to_dat(tsplib_file, dat_file):
    
    coords = [] 
    #lista che conterrà le coordinate del file TSPLIB (x,y)
    
    with open(tsplib_file, "rt") as f: 
        #apre il file in modalità testo per la lettura 
        
        read_coords = False 
        #flag che ci segnala quando entriamo nella sezione NODE_COORF_SECTION
        
        for line in f:   
            #scorre il file riga per riga
            
            line = line.strip()  
            # .strip() ci elimina spazi bianchi e newline
            
            if line.startswith("NODE_COORD_SECTION"): 
                
                #se la riga comincia con NODE_COORD_SECTION, si imposta la precedente flag a true e iniziamo a leggere le righe che contengono le coordinate
                
                read_coords = True
                continue
            
            if line.startswith("EOF"):  
                #se incontriamo "EOF" usciamo dal ciclo perchè rappresenta la fine dell'istanza .tsp
                break
            
            if read_coords:  
                # se la flag è attiva entriamo nell'if.
                
                parts = line.split()  
                #.split() ci divide la riga in token separati da spazi.
                
                coords.append((float(parts[1]), float(parts[2])))  
                #la riga di coords ha 3 token (i,x(i),y(i)),  inseriamo nella tupla i della lista x e y come float

    coords = np.array(coords)  
    #convertiamo la lista di tuple in un array nunpy con n righe e 2 colonne (rappresentano x e y)
    
    n = len(coords)   
    # calcolo il numero di nodi

    D = np.sqrt(((coords[:, None, :] - coords[None, :, :])**2).sum(axis=2)) 
    #calcoliamo la matrice delle distanze euclidee e la assegniamo a D
    
    np.fill_diagonal(D, 0.0)
    # imposto a 0 la diagonale, che corrisponde alla distanza di un nodo da se stesso.

   
    with open(dat_file, "w", encoding="utf-8") as f: 
        #apro il file di output in scrittura con encoding utf-8.
        
        f.write("set NODES := " + " ".join(map(str, range(1, n+1))) + ";\n\n") 
        #scrivo la dichiarazione del set NODES (genero gli indici a partire da 1, convertendo gli interi in stringhe (str))
        
        f.write("set ARCS :=\n" + "\n".join(f"{i+1} {j+1}" for i in range(n) for j in range(n) if i!=j) + ";\n\n") 
        #costruisce gli archi nel file .dat per ogni i e j (ovviamente con i!=j)
        
        f.write("param cost :=\n" + "\n".join(f"[{i+1},{j+1}] {D[i,j]:.2f}" for i in range(n) for j in range(n) if i!=j) + ";\n") 
        #scrive il parametro param cost nel formato [i,j] e D[i,j] per ogni i,j (con i !=j)


# questo codice viene eseguito solo se lo script è eseguito direttamente 
if __name__ == "__main__":
    
    tsplib_dir = r"C:\Users\User\OneDrive\Desktop\Progetti_Uni\Progetto_Amod\.vscode\tsplib" 
    # definisco la directory di input
    
    ampl_dir   = r"C:\Users\User\OneDrive\Desktop\Progetti_Uni\Progetto_Amod\.vscode\ampl" 
    # definisco la directory di output
    
    os.makedirs(ampl_dir, exist_ok=True) 
    #comando che serve a creare la directory di output se non esoiste

    for file in os.listdir(tsplib_dir): 
        # ciclo i file all'interno della directory di input
        
        if file.endswith(".tsp"): 
            #se il file è del tipo .tsp entro nell'if (in questo caso succede sempre) chiamando la funzione tsp_to_dat.
            
            tsp_to_dat(
                os.path.join(tsplib_dir, file),
                # metood che costruisce l'intero path del file di input quando lo passa alla funzione
                
                os.path.join(ampl_dir, os.path.splitext(file)[0] + ".dat")
                # metodo che sostituisce l'estenzione originale.tsp e la sostituisce con .dat
            )
