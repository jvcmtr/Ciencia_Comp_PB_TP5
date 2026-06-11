from q2_data import CAPACIDADE_SERVIDOR, VMS_SOLICITADAS

def next_fit(items, capacity):
    bins = []
    
    if not items:
        return bins

    current = []
    soma = 0
    
    for i in items:
        if soma + i <= capacity:
            current.append(i)
            soma += i
        else:
            bins.append(current)
            current = [i]
            soma = i
            
    if current:
        bins.append(current)
        
    return bins

def first_fit(items, capacity, decreasing=True):
    items = sorted(items, reverse=decreasing)
    bins = [] #{'items': [5, 3], 'remaining': 2}

    for i in items:
        placed = False
        for b in bins:
            if b['remaining'] >= i:
                b['items'].append(i)
                b['remaining'] -= i
                placed = True
                break
        if not placed:
            bins.append({'items': [i], 'remaining': capacity - i})

    return [b['items'] for b in bins]


def test(data, capacity):
    a = next_fit(data, capacity)
    a_free = sum([ capacity-sum(x) for x in a ])
    a_avg = sum([ sum(x) for x in a ]) / len(a)
    a_percent = (a_avg/capacity)*100
    b = first_fit(data, capacity)
    b_free = sum([ capacity-sum(x) for x in b ])
    b_avg = sum([ sum(x) for x in b ]) / len(b)
    b_percent = (b_avg/capacity)*100

    print(f"""
        === RESULTADO DA ALOCAÇÃO (HEURÍSTICAS) ===

        [Heurística Next-Fit]
        - Servidores utilizados: {len(a)} servidores
        - Exemplo de ocupação do Servidor 1: {a[0]} (Total: {sum(a[0])}/{capacity} GB)
        - Ocupação media de cada servidor: {a_avg:.1f}/{capacity} GB ({a_percent:.1f}% ocupado)
        - Percentual de espaço livre não utilizado: {(100-a_percent):.2f}% 

        [Heurística First-Fit Decreasing]
        - Servidores utilizados: {len(b)} servidores
        - Exemplo de ocupação do Servidor 1: {b[0]} (Total: {sum(b[0])}/{capacity} GB)
        - Ocupação media de cada servidor: {b_avg:.1f}/{capacity} GB ({b_percent:.1f}% ocupado)
        - Percentual de espaço livre não utilizado: {(100-b_percent):.2f}% 

        Conclusão: A heurística First-Fit Decreasing: 
        - Economizou {len(a) - len(b)} servidores em relação à Next-Fit.
        - Reduziu em {a_free - b_free} GB ({((a_free - b_free)/a_free)*100:.1f}%) o espaço não utilizado nos servidores em relação à Next-Fit.""".replace("    ", " ")
    )

if __name__ == "__main__":
    test(VMS_SOLICITADAS, CAPACIDADE_SERVIDOR)
