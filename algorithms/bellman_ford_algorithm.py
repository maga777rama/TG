from graph import Graph, GraphError

def bellman_ford(graph: Graph, start: str) -> dict:
    if not graph.weighted:
        raise GraphError("Алгоритм Форда-Беллмана применим только к взвешенным графам.")

    if start not in graph.adjacency_list:
        raise GraphError(f"Начальная вершина '{start}' не найдена в графе.")

    distances = {vertex: float('inf') for vertex in graph.adjacency_list}
    distances[start] = 0

    for _ in range(len(graph.adjacency_list) - 1):
        updated = False
        for u in graph.adjacency_list:
            for v, weight in graph.adjacency_list[u]:
                if weight is None:
                    continue
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    updated = True
        if not updated:
            break

    # Проверка на наличие цикла отрицательного веса
    for u in graph.adjacency_list:
        for v, weight in graph.adjacency_list[u]:
            if weight is None:
                continue
            if distances[u] + weight < distances[v]:
                raise GraphError("Обнаружен цикл отрицательного веса. Алгоритм Форда-Беллмана не может быть применён.")

    return distances
