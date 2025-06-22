from graph import Graph, GraphError
from algorithms.floyd_warshall_algorithm import floyd_warshall
from algorithms.dijkstra_algorithm import dijkstra
from algorithms.bellman_ford_algorithm import bellman_ford
from visualization_utils import visualize_steps, draw_dijkstra_step


def print_menu():
    print("\nМеню:")
    print("1. Показать граф")
    print("2. Добавить вершину")
    print("3. Добавить ребро")
    print("4. Удалить вершину")
    print("5. Удалить ребро")
    print("6. Экспортировать граф в файл")
    print("7. Импортировать граф из файла")
    print("8. Применить алгоритм Дейкстры")
    print("9. Применить алгоритм Форда-Беллмана")
    print("10. Применить алгоритм Флойда-Уоршелла")
    print("11. Выход")

def input_vertex(prompt: str) -> str:
    v = input(prompt).strip()
    if not v:
        raise ValueError("Имя вершины не может быть пустым.")
    return v

def main():
    graph: Graph = None

    print("Создание графа")
    method = input("Создать граф вручную (m) или загрузить из файла (f)? ").strip().lower()
    if method == 'f':
        path = input("Введите путь к файлу: ").strip()
        try:
            graph = Graph.from_file(path)
            print("Граф успешно загружен из файла.")
        except Exception as e:
            print(f"Ошибка при загрузке графа: {e}")
            return
    else:
        directed = input("Ориентированный граф? (y/n): ").lower().startswith('y')
        weighted = input("Взвешенный граф? (y/n): ").lower().startswith('y')
        graph = Graph(directed=directed, weighted=weighted)

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        try:
            if choice == '1':
                print("\nТекущий граф:")
                print(graph)

            elif choice == '2':
                v = input_vertex("Введите имя новой вершины: ")
                graph.add_vertex(v)
                print(f"Вершина '{v}' добавлена.")

            elif choice == '3':
                u = input_vertex("Введите начальную вершину: ")
                v = input_vertex("Введите конечную вершину: ")
                if graph.weighted:
                    weight = float(input("Введите вес ребра: "))
                    graph.add_edge(u, v, weight)
                else:
                    graph.add_edge(u, v)
                print("Ребро добавлено.")

            elif choice == '4':
                v = input_vertex("Введите вершину для удаления: ")
                graph.remove_vertex(v)
                print(f"Вершина '{v}' удалена.")

            elif choice == '5':
                u = input_vertex("Введите начальную вершину: ")
                v = input_vertex("Введите конечную вершину: ")
                graph.remove_edge(u, v)
                print("Ребро удалено.")

            elif choice == '6':
                path = input("Введите путь к файлу для экспорта: ").strip()
                graph.export_to_file(path)
                print(f"Граф экспортирован в '{path}'.")

            elif choice == '7':
                path = input("Введите путь к файлу: ").strip()
                graph = Graph.from_file(path)
                print(f"Граф успешно загружен из '{path}'.")

            elif choice == '8':
                if not graph.weighted:
                    print("Граф невзвешенный. Алгоритм Дейкстры применим только к взвешенным графам.")
                    continue
                try:
                    start = input_vertex("Введите начальную вершину: ")
                    distances, steps = dijkstra(graph, start, track_steps=True)
                    print(f"Кратчайшие расстояния от вершины '{start}':")
                    for vertex, dist in distances.items():
                        print(f"  {vertex}: {dist if dist != float('inf') else 'недостижимо'}")
                    visualize_steps(graph, steps, draw_dijkstra_step)
                except GraphError as e:
                    print(f"Ошибка: {e}")

            elif choice == '9':
                if not graph.weighted:
                    print("Граф невзвешенный. Алгоритм Форда-Беллмана применим только к взвешенным графам.")
                    continue
                try:

                    start = input_vertex("Введите начальную вершину: ")
                    distances = bellman_ford(graph, start)
                    print(f"Кратчайшие расстояния от вершины '{start}':")
                    for vertex, dist in distances.items():
                        print(f"  {vertex}: {dist if dist != float('inf') else 'недостижимо'}")
                except GraphError as e:
                    print(f"Ошибка: {e}")

            elif choice == '10':
                if not graph.weighted:
                    print("Граф невзвешенный. Алгоритм Флойда-Уоршелла применим только к взвешенным графам.")
                    continue
                try:

                    dist = floyd_warshall(graph)
                    print("Кратчайшие расстояния между всеми парами вершин:")
                    vertices = sorted(dist.keys())
                    header = "     " + "  ".join(f"{v:>5}" for v in vertices)
                    print(header)
                    for u in vertices:
                        row = f"{u:>3}:"
                        for v in vertices:
                            d = dist[u][v]
                            val = f"{d:.1f}" if d != float('inf') else "inf"
                            row += f"  {val:>5}"
                        print(row)
                except GraphError as e:
                    print(f"Ошибка: {e}")

            elif choice == '11':
                print("Выход.")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

        except (GraphError, ValueError) as e:
            print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()

