#funciones de los algoritmos solicitados para recorrer los grafos resultantes en los municipios
#Se utiliza los algoritmos BFS y DFS 


#ALGORITMO BFS 
def algBFS(grafo, inicio):
   
    visitados = set([inicio])      # Evitar visitar nodos repetidos
    cola = [inicio]                # Cola para mantener el orden de visita
    orden_visita = []             # Lista que guarda el orden final del recorrido

    while cola:
        actual = cola.pop(0)
        orden_visita.append(actual)

        for vecino in grafo.get(actual, {}):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

    return orden_visita

#ALGORITMO DFS 
def algDFS(grafo, inicio, visitados=None, orden_visita=None):
    
    if visitados is None:
        visitados = set()
        orden_visita = []

    visitados.add(inicio)
    orden_visita.append(inicio)

    for vecino in grafo.get(inicio, {}):
        if vecino not in visitados:
            algDFS(grafo, vecino, visitados, orden_visita)

    return orden_visita
