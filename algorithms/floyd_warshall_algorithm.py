from graph import Graph, GraphError

def floyd_warshall(graph: Graph) -> dict:
    if not graph.weighted:
        raise GraphError("Алгоритм Флойда-Уоршелла применим только к взвешенным графам.")

    vertices = list(graph.adjacency_list.keys())
    dist = {u: {v: float('inf') for v in vertices} for u in vertices}

    for v in vertices:
        dist[v][v] = 0

    for u in graph.adjacency_list:
        for v, w in graph.adjacency_list[u]:
            if w is None:
                continue
            dist[u][v] = w

    for k in vertices:
        for i in vertices:
            for j in vertices:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Проверка наличия отрицательных циклов
    for v in vertices:
        if dist[v][v] < 0:
            raise GraphError("Обнаружен цикл отрицательного веса. Алгоритм Флойда-Уоршелла не может быть применён.")

    return dist
