# TASK 2 ############################################################
def in_out_degree(graph):
    in_degree = {}
    out_degree = {}
    for vertex in graph:
        out_degree[vertex] = 0
        in_degree[vertex] = 0
            
    for vertex in graph:
        out_degree[vertex] = len(graph[vertex])  # out_degree[v] = len(graph[v])
            
        for neighbor in graph[vertex]:
            in_degree[neighbor] += 1
                
    return in_degree, out_degree

def dfs(graph, start):
    visited = [start]
    stack = [start]   # es el camino actual, su ultimo elemento es el vertice en el que se esta

    while stack:
        vertex = stack[-1]
        smallest = None
        for neighbor in graph[vertex]:
            if neighbor not in visited and (smallest is None or neighbor < smallest):
                smallest = neighbor

        if smallest is None:
            stack.pop()              # no quedan vecinos: retrocedemos
        else:
            visited.append(smallest)
            stack.append(smallest)

    return visited

def connected_components(graph):
    components = []
    found = []  # vértices ya asignados a algún componente

    for vertex in graph:
        if vertex not in found:
            reachable = dfs(graph, vertex)
            components.append(set(reachable))  # la salida debe ser una lista de sets
            found.extend(reachable)

    return components

def is_weakly_connected(graph):
    # Construir la "sombra" no dirigida
    shadow = {vertex: [] for vertex in graph}
    for u in graph:
        for v in graph[u]:
            shadow[u].append(v)
            shadow[v].append(u)

    return len(connected_components(shadow)) == 1

def eulerian_type(graph, directed = True):
    if directed == False:       # undirected
        if len(connected_components(graph)) != 1:
            return "None" 

        odd = 0
        for vertex in graph:
            if len(graph[vertex]) % 2 == 1:  # grado impar
                odd += 1

        if odd == 0:  # si no hay ningun grado impar (son todos pares): circuito
            return "Circuit"
        
        if odd == 2:  # si hay dos vértices que tienen grado impar: camino
            return "Path"
        return "None"

    else:        # directed
        if is_weakly_connected(graph) == False:
            return "None"    

        in_degree, out_degree = in_out_degree(graph)
        start = 0
        end = 0
        for vertex in graph:
            excess = out_degree[vertex] - in_degree[vertex]
            if excess == 1:
                start += 1
            elif excess == -1:
                end += 1
            elif excess != 0:
                return "None"

        if start == 0 and end == 0:
            return "Circuit"

        if start == 1 and end == 1:
            return "Path"

        return None


def kmer_composition(text, k):
    list_windows = []
    l = len(text)
    for i in range(l-k+1):
        window = text[i:i + k]
        list_windows.append(window)
    return list_windows

# Example:
# print(kmer_composition("GATTACA", 4))    # `["GATT", "ATTA", "TTAC", "TACA"]`

# Self check:
# print(kmer_composition("GATTACA", 4))    # list has 4 elements
# print(kmer_composition("ACTGATGTTTACA", 6))   # list has 8 elements
    # Checked: the length of the list is len(text)-k+1


def debruijn_graph(kmers):   # kmers is a list of strings with the same length k>=2
    graph = {}  # clave: nodo de origen;   valor: nodos de destino
    for km in kmers:
        prefix = km[:-1]
        suffix = km[1:]

        if prefix not in graph:
            graph[prefix] = []
        if suffix not in graph:
            graph[suffix] = []

        graph[prefix].append(suffix)
    return graph

# print(debruijn_graph(["CATCATCAT"]))

def spell_path(nodes):   # nodes: lista de strings de longitud k
    k = len(nodes[0])
    walk = nodes[0]   # se empieza por el primer nodo, que es el único entero
    for node in nodes[1:]:   # empezamos el bucle por el segundo nodo
        walk += node[(k-1):]   # añadimos a la lista la ultima letra de cada nodo
    return walk

# Example:
# print(spell_path(["GAT", "ATT", "TTA"]))     # GATTA
# SELF-CHECK:
# print(spell_path(kmer_composition("ACCTGGAGC", 4)))   # == text: TRUE
# print(spell_path(kmer_composition("AGTCGTGAACTG", 5)))   # == text: TRUE
    # Checked: the result is the text itself

print(spell_path(kmer_composition("CATCATCAT", 3)))

toyA = {"ACT": ["CTG"], "AGA": ["GAC", "GAA"], "CAG": ["AGA"], 
        "CCA": ["CAG"], "CTG": ["TGA"], "GAA": [], "GAC": ["ACT"], 
        "GGT": ["GTC"], "GTC": ["TCC"], "TCC": ["CCA"], "TGA": ["GAC", "GAA"]}
print(eulerian_type(toyA, True))


# TASK 3 ##########################################################3
def hierholzer(graph, start, verbose=False):
    unused = {}
    for node in graph:
        unused[node] = sorted(graph[node])

    # Primer recorrido (reemplaza a walk_from(start))
    path = [start]
    current = start
    while len(unused[current]) > 0:
        next_node = unused[current].pop(0)
        path.append(next_node)
        current = next_node

    n_walk = 1
    if verbose:
        print(f"walk 1: {path}")

    while True:
        restart = None
        i = 0
        while i < len(path) and restart is None:
            if len(unused[path[i]]) > 0:
                restart = i
            i += 1

        # Si no quedan aristas libres, devolvemos el camino con return
        if restart is None:
            return path

        restart_node = path[restart]

        # Nuevo recorrido desde el nodo de reinicio (reemplaza a walk_from(restart_node))
        new_walk = [restart_node]
        current = restart_node
        while len(unused[current]) > 0:
            next_node = unused[current].pop(0)
            new_walk.append(next_node)
            current = next_node

        n_walk += 1
        if verbose:
            print(f"walk {n_walk} (restarted at {restart_node}): {new_walk}")

        path = path[:restart] + new_walk + path[restart + 1:]
        if verbose:
            print(f"after splice: {path}")


from collections import Counter

def eulerian_path(graph, verbose=False):
    in_degree = {}
    for node in graph:
        if node not in in_degree:
            in_degree[node] = 0
        for neighbor in graph[node]:
            if neighbor not in in_degree:
                in_degree[neighbor] = 0
            in_degree[neighbor] += 1

    start = None
    for node in sorted(graph.keys()):
        out_deg = len(graph[node])
        in_deg = in_degree.get(node, 0)
        if out_deg - in_deg == 1 and start is None:
            start = node

    if start is None:
        start = min(graph)

    return hierholzer(graph, start, verbose)


# TASK 4 ##########################################################
toyC = {"AT": ["TC"], "TC": ["CT"], "CC": ["CT"], "CT": ["TT"], "TT": ["TG"],
         "GG": ["GT"], "GT": ["TG", "TA"], "TA": ["AT"], "TG": ["GT", "GG"]}

print(eulerian_path(toyC, verbose=True))   # it returns the second Eularian path

def contigs(graph):
    in_degree, out_degree = in_out_degree(graph)
    seen = set()     
    result = []

    nodes = list(graph)
    nodes.sort()

    for vertex in nodes:
        if in_degree[vertex] == 1 and out_degree[vertex] == 1:
            continue

        neighbors = list(graph[vertex])
        neighbors.sort()
        for neighbor in neighbors:       
            path = [vertex, neighbor]
            current = neighbor
            while in_degree[current] == 1 and out_degree[current] == 1:
                seen.add(current)
                current = graph[current][0]
                path.append(current)
            result.append(spell_path(path))

    for vertex in nodes:
        if in_degree[vertex] == 1 and out_degree[vertex] == 1 and vertex not in seen:
            cycle = [vertex]
            seen.add(vertex)
            current = graph[vertex][0]
            while current != vertex:
                cycle.append(current)
                seen.add(current)
                current = graph[current][0]

            first = cycle[0]             
            for node in cycle:
                if node < first:
                    first = node
            position = cycle.index(first)

            rotated = cycle[position:] + cycle[:position]
            rotated.append(first)         # cerrar el ciclo
            result.append(spell_path(rotated))

    result.sort()
    return result


# SELF-CHECK 1: every edge of the graph lies in exactly one contig
kmers = kmer_composition("GATTACAGATTACA", 3)
all_kmers = []
for contig in contigs(debruijn_graph(kmers)):
     all_kmers += kmer_composition(contig, 3)
kmers.sort()
all_kmers.sort()
print(all_kmers == kmers)   # TRUE
    # Checked: the k-mers of all contigs together are exactly the k-mers of the graph

# SELF-CHECK 2: no (k-1)-mer occurs twice -> exactly one contig, the string itself
print(contigs(debruijn_graph(kmer_composition("ACGTAGC", 3))))   # == ['ACGTAGC']
    # Checked: the only contig is the text itself

# SELF-CHECK 3: first k-1 letters == last k-1 letters, no other (k-1)-mer repeats
print(contigs(debruijn_graph(kmer_composition("ACGTTGCAAC", 3))))   # == ['AACGTTGCAA']
    # Checked: one contig of the same length as the text, a rotation of it

# SELF-CHECK 4: toy C
print(contigs(toyC))   

# SELF-CHECK 5: the result does not depend on the order of the input k-mers
print(contigs(debruijn_graph(["GAT", "ATT", "TTA"])) == contigs(debruijn_graph(["TTA", "GAT", "ATT"])))   # TRUE
    # Checked: same list of contigs with the k-mers in a different order