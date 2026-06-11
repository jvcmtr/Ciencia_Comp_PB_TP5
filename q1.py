from graph import Graph
from math import inf
from q1_data import CONEXOES, NUM_CIDADES

def kruskal(edges, get_weight_fn=None):
    if not get_weight_fn:
        get_weight_fn = lambda a: 1
    if not edges:
        raise ValueError("Cant apply kruskal algorithm, no edges available.")
    if len(edges[0]) < 3:
        raise ValueError("Cant apply kruskal algorithm. Edges list is not in the correct format [(nodeA, nodeB, weight)]")

    edges = sorted(edges, key=get_weight_fn)
    subtrees = []
    mst = []

    for e in edges:
        # Encontra em quais subgrafos nodeA e nodeB estão
        a, b = None, None
        for t in subtrees:
            if e[0] in t:
                a = t
            if e[1] in t:
                b = t
        # Se esse edge causa um loop, pula para a proxima iteracao
        if a == b and a is not None:
            continue
        
        # Adiciona o edge a MST e atualiza os dados de apoio
        mst.append(e)
        if a and not b:
            a.add(e[1])
        elif b and not a:
            b.add(e[0])
        elif not a and not b:
            subtrees.append({e[0], e[1]})
        else:
            a.update(b)
            subtrees.remove(b)

    return mst


def djikstra(graph, start, end, get_weight_fn=None):
    if not get_weight_fn:
        get_weight_fn = lambda a: 1

    nodes = graph.get_all_nodes()

    if start not in nodes or end not in nodes:
        return None, inf

    seen_nodes = {node: (inf, None) for node in nodes}
    seen_nodes[start] = (0, None)
    not_seen = set(nodes)
    
    while len(not_seen) > 0:
        current = min(not_seen, key=lambda n: seen_nodes[n][0])
        
        # if seen_nodes[current][0]==inf or current == end:
        if current == end:
            break
            
        not_seen.remove(current)
        
        for edge in graph.get_edges_from(current):
            n, weight = edge[1], get_weight_fn(edge)
            # Se não tivermos analisado esse nó ainda, pulamos
            if not n in not_seen:
                continue
            # Atualiza o custo para chegar aquele node se encontrarmos um menor
            cost = seen_nodes[current][0] + weight
            if cost < seen_nodes[n][0]:
                seen_nodes[n] = (cost, current)
                    

    path, cost = [], seen_nodes[end][0]
    while seen_nodes[end][1] is not None:
        path.append(end)
        end = seen_nodes[end][1]
    
    return path, cost


if __name__ == "__main__":
    CIDADE_0 = 0
    edges = [ (x[0], x[1], (x[2], x[3])) for x in CONEXOES ]
    line_cost = lambda e: e[2][0]
    line_latency = lambda e: e[2][1]


    min_spanning_tree = kruskal(edges, line_cost)
    custo_total = 0
    for e in min_spanning_tree:
        custo_total += line_cost(e)
    graph = Graph(min_spanning_tree)


    latencia_cidades = {}
    for node in graph.get_all_nodes():
        if node != CIDADE_0:
            caminho, custo = djikstra(graph, CIDADE_0, node, line_latency)
            latencia_cidades[node] = custo


    latencias = sorted( latencia_cidades.items(), key=lambda i: i[1])
    maior = latencias[-1]
    avg = 0
    for k, v in latencia_cidades.items():
        avg += v
        if v > maior[1]:
            maior = (k, v)
    avg = avg/len(latencias)


    print(f"_________________________________________")
    print(f"RESUMO:")
    print(f" Linhas totais entre cidades : \t {len(min_spanning_tree)}")
    print(f" N Cidades conectadas        : \t {NUM_CIDADES}")
    print(f" Custo total das linhas      : \t {custo_total}")
    print(f" Latencia media*             : \t {avg:.2f}")
    print(f" Maior latencia*             : \t {maior[1]} (Cidade {maior[0]})")
    print(f"\n* - Latencias calculadas em relacao a cidade 0")

    print(f"_________________________________________")
    print(f"LINHAS DE FIBRA OTICA:")
    graph.print_from(CIDADE_0, prefix="Cidade:")

    print(f"_________________________________________")
    print(f"LATENCIAS \t (com relação a cidade 0)")
    for k, v in latencias:
        print(f"  - Cidade {k}\t: {v}")
