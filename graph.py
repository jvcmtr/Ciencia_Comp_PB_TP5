# Adaptado a partir da questão 3 do TP4 da disciplina de proojeto de bloco
# A principal alteração com relação a classe original é a remoção das funções
# _optimize(), bfs(), dfs() e outras que eram especificas da questão;
#
# Outra alteração importante é a inclusão de logica especifica para lidar
# com o peso de cada edge.  
class Graph:
    def __init__(self, edges):
        """
        'node' aqui pode ser qualquer tipo hasheavel.
        'edges' deve ser uma lista de tuplas seguindo o formato: (node1, node2, metadata)
        """
        self.data = {}
        self.add_edges(edges)
    
    def get_edges_from(self, node):
        return [ (node, *x) for x in self.data[node]]

    def add_edges(self, edges):
        for e in edges:
            self.add_edge(e)

    def add_edge(self, e):
        if not self.data.get(e[0]):
            self.data[e[0]] = set()
        if not self.data.get(e[1]):
            self.data[e[1]] = set()

        self.data[e[0]].add((e[1], e[2]))
        self.data[e[1]].add((e[0], e[2]))

    def get_all_edges(self, complement=False):
        e = {}
        for k, v in self.data.items():
            for node, meta in v:
                if e.get((node, k, meta)) and not complement:
                    continue
                e[(k, node, meta)] = True
 
        return [ k for k, v in e.items()]

    def get_all_nodes(self):
        return [k for k,v in self.data.items() ]


    def print_from(self, start, prefix="", sufix="", depth=0, last_son={0:True}, seen=[]):
        seen.append(start)

        child = [x for x in self.data[start] if x[0] not in seen]

        spacer = ""
        for i in range(depth):
            spacer += "    " if last_son.get(i) else "│   "

        head = "└" if last_son.get(depth) else "├" #─ 
        expand = "─" # if len(child) == 0 else "┬"
        
        print(f"{spacer}{head}{expand}⏵ {prefix}{start}{sufix}")

        for e in child:
            last_son[depth+1] = (e == child[-1])
            self.print_from(e[0], prefix, sufix, depth+1, last_son, seen)