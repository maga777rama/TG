import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.widgets as widgets

def visualize_steps(graph, steps, draw_step_fn, pos=None):
    G = nx.DiGraph() if graph.directed else nx.Graph()
    for u in graph.adjacency_list:
        for v, w in graph.adjacency_list[u]:
            G.add_edge(u, v, weight=w)

    if pos is None:
        pos = nx.spring_layout(G)

    fig, ax = plt.subplots(figsize=(8, 6))
    step_index = [0]

    def draw():
        ax.clear()
        draw_step_fn(ax, G, pos, steps[step_index[0]], step_index[0], len(steps))
        fig.canvas.draw()

    def next_step(event):
        if step_index[0] < len(steps) - 1:
            step_index[0] += 1
            draw()

    def prev_step(event):
        if step_index[0] > 0:
            step_index[0] -= 1
            draw()

    axprev = plt.axes([0.25, 0.01, 0.2, 0.05])
    axnext = plt.axes([0.55, 0.01, 0.2, 0.05])
    bnext = widgets.Button(axnext, '→ Вперёд')
    bprev = widgets.Button(axprev, '← Назад')
    bnext.on_clicked(next_step)
    bprev.on_clicked(prev_step)

    draw()
    plt.show()

def draw_dijkstra_step(ax, G, pos, step, index, total):
    labels = {}
    node_colors = []

    for node in G.nodes():
        dist = step['distances'].get(node, float('inf'))
        labels[node] = f"{node}\n{dist if dist != float('inf') else '∞'}"

        if node == step['current']:
            node_colors.append('orange')
        elif node in step['visited']:
            node_colors.append('lightgreen')
        else:
            node_colors.append('lightgray')

    edge_colors = []
    for u, v in G.edges():
        if (u, v) in step.get('updated_edges', set()):
            edge_colors.append('red')
        else:
            edge_colors.append('black')

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=1200)
    nx.draw_networkx_labels(G, pos, ax=ax, labels=labels)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    ax.set_title(f"Шаг {index + 1} из {total}")
    ax.axis('off')

    legend_elements = [
        Patch(facecolor='lightgray', label='Непосещённая'),
        Patch(facecolor='lightgreen', label='Посещённая'),
        Patch(facecolor='orange', label='Текущая'),
        Line2D([0], [0], color='red', lw=2, label='Обновлённое ребро')
    ]
    ax.legend(handles=legend_elements, loc='upper left')
