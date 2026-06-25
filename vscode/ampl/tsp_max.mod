set NODES;
set ARCS within {NODES, NODES};

param cost{ARCS};
param n := card(NODES);

var x{ARCS} binary;
var u{NODES} >= 0 <= n-1;

maximize TotalCost:
    sum{(i,j) in ARCS} cost[i,j] * x[i,j];

# Ogni nodo ha esattamente un arco uscente
s.t. OutFlow{i in NODES}:
    sum{j in NODES: (i,j) in ARCS} x[i,j] = 1;

# Ogni nodo ha esattamente un arco entrante
s.t. InFlow{j in NODES}:
    sum{i in NODES: (i,j) in ARCS} x[i,j] = 1;

# Vincoli MTZ per eliminare sottocicli
s.t. MTZ{i in NODES, j in NODES: i != j && i != 1 && j != 1 && (i,j) in ARCS}:
    u[i] - u[j] + (n-1)*x[i,j] <= n-2;

# Fissiamo il nodo di partenza
s.t. FixStart:
    u[1] = 0;
