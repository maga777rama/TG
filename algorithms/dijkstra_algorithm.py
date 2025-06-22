import heapq
from graph import Graph, GraphError

def dijkstra(graph: Graph, start: str, track_steps: bool = False):
    if not graph.weighted:
        raise GraphError("Алгоритм Дейкстры применим только к взвешенным графам.")

    for u in graph.adjacency_list:
        for v, weight in graph.adjacency_list[u]:
            if weight is not None and weight < 0:
                raise GraphError("Алгоритм Дейкстры не работает с отрицательными весами рёбер.")

    if start not in graph.adjacency_list:
        raise GraphError(f"Начальная вершина '{start}' не найдена в графе.")

    distances = {vertex: float('inf') for vertex in graph.adjacency_list}
    distances[start] = 0
    visited = set()
    steps = []

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex in visited:
            continue
        visited.add(current_vertex)

        updated_edges = set()

        for neighbor, weight in graph.adjacency_list[current_vertex]:
            if weight is None:
                continue
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor))
                updated_edges.add((current_vertex, neighbor))

        if track_steps:
            steps.append({
                'current': current_vertex,
                'distances': distances.copy(),
                'visited': visited.copy(),
                'updated_edges': updated_edges.copy(),
            })

    if track_steps:
        return distances, steps
    return distances


