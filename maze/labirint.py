import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import networkx as nx
from queue import Queue
import copy


class MazeSolver:
    def __init__(self, filename):

        self.maze, self.start, self.end = self.read_maze(filename)
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.graph = self.build_graph()
        self.history = []
        self.reset()

    def read_maze(self, filename):

        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        maze = []
        start = end = None
        for i, line in enumerate(lines):
            row = []
            for j, ch in enumerate(line):
                if ch == 'S':
                    start = (i, j)
                elif ch == 'E':
                    end = (i, j)
                row.append(ch)
            maze.append(row)
        return maze, start, end

    def build_graph(self):
        G = nx.Graph()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] != '#':
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < self.rows and 0 <= nj < self.cols:
                            if self.maze[ni][nj] != '#':
                                G.add_edge((i, j), (ni, nj))
        return G

    def reset(self):
        # Сброс состояния поиска до начального
        self.visited = set()
        self.queue = Queue()
        self.queue.put(self.start)
        self.visited.add(self.start)
        self.parent = {}
        self.path_found = False
        self.history = []

    def save_state(self):
        state = {
            'visited': copy.deepcopy(self.visited),
            'queue': copy.deepcopy(list(self.queue.queue)),
            'parent': copy.deepcopy(self.parent),
            'path_found': self.path_found
        }
        self.history.append(state)

    def load_prev_state(self):
        if not self.history:
            return
        state = self.history.pop()
        self.visited = state['visited']
        self.queue = Queue()
        for item in state['queue']:
            self.queue.put(item)
        self.parent = state['parent']
        self.path_found = state['path_found']

    def bfs_step(self):

        if self.queue.empty() or self.path_found:
            return

        self.save_state()
        current = self.queue.get()

        if current == self.end:
            self.path_found = True
            return

        for neighbor in self.graph.neighbors(current):
            if neighbor not in self.visited:
                self.queue.put(neighbor)
                self.visited.add(neighbor)
                self.parent[neighbor] = current

    def reconstruct_path(self):
        path = []
        if not self.path_found:
            return path
        node = self.end
        while node != self.start:
            path.append(node)
            node = self.parent[node]
        path.append(self.start)
        return list(reversed(path))

    def draw(self):
        plt.clf()

        pos = {node: (node[1], -node[0]) for node in self.graph.nodes()}
        nx.draw(self.graph, pos, node_size=500, node_color='lightgray', with_labels=False)

        labels = {}
        for (i, j), ch in [((i, j), self.maze[i][j]) for i in range(self.rows) for j in range(self.cols)]:
            if ch != '#':
                labels[(i, j)] = ch
        nx.draw_networkx_labels(self.graph, pos, labels)


        nx.draw_networkx_nodes(self.graph, pos, nodelist=list(self.visited), node_color='yellow')


        if self.path_found:
            path = self.reconstruct_path()
            nx.draw_networkx_nodes(self.graph, pos, nodelist=path, node_color='green')
            nx.draw_networkx_edges(self.graph, pos, edgelist=list(zip(path, path[1:])), edge_color='green', width=2)

        plt.title("Maze Solver - BFS")
        plt.pause(0.01)


class MazeApp:
    def __init__(self, root, filename):
        self.root = root
        self.solver = MazeSolver(filename)
        self.root.title("Maze Visualizer")


        self.canvas = tk.Canvas(root, width=600, height=100)
        self.canvas.pack()


        self.step_btn = tk.Button(root, text="→ Следующий шаг", command=self.next_step)
        self.step_btn.pack(side=tk.LEFT, padx=10, pady=10)


        self.back_btn = tk.Button(root, text="← Назад", command=self.prev_step)
        self.back_btn.pack(side=tk.LEFT, padx=10, pady=10)


        self.reset_btn = tk.Button(root, text="⟳ Сброс", command=self.reset)
        self.reset_btn.pack(side=tk.LEFT, padx=10, pady=10)


        plt.ion()
        self.solver.draw()

    def next_step(self):

        self.solver.bfs_step()
        self.solver.draw()

    def prev_step(self):

        self.solver.load_prev_state()
        self.solver.draw()

    def reset(self):

        self.solver.reset()
        self.solver.draw()


if __name__ == "__main__":
    filename = "input.txt"
    root = tk.Tk()
    app = MazeApp(root, filename)
    root.mainloop()
