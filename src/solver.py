from PIL import Image
from collections import defaultdict, deque
import itertools
import matplotlib.pyplot as plt
import numpy as np
import random

class UnionFind():

    def __init__(self):
        self.parents = {}
        self.children = defaultdict(int)

    def find_set(self, value):
        path = []
        while value in self.parents:
            path.append(value)
            value = self.parents[value]
        for visited in path:
            self.parents[visited] = value
        return value

    def union(self, first, second):
        first_root = self.find_set(first)
        second_root = self.find_set(second)
        if first_root == second_root:
            return
        if self.children[first_root] < self.children[second_root]:
            first_root, second_root = second_root, first_root
        self.parents[second_root] = first_root
        self.children[first_root] += self.children[second_root] + 1

def generate_neighbors(vertex, rows, cols, dist=1):
    offsets = filter(lambda o: 0 < abs(o[0]) + abs(o[1]) <= dist, itertools.product(range(-dist, dist + 1), range(-dist, dist + 1)))
    return filter(lambda c: 0 <= c[0] < rows and 0 <= c[1] < cols, map(lambda o: (vertex[0] + o[0], vertex[1] + o[1]), offsets))

def generate_maze(dim=60):
    vertices = list(itertools.product(range(dim), range(dim)))
    graph_edges = []
    for vertex in vertices:
        for neighbor in generate_neighbors(vertex, dim, dim):
            if vertex[0] < neighbor[0] or vertex[1] < neighbor[1]:
                graph_edges.append((vertex, neighbor))
    random.shuffle(graph_edges)
    union_find = UnionFind()
    edges = set()
    for vertex, neighbor in graph_edges:
        if union_find.find_set(vertex) != union_find.find_set(neighbor):
            union_find.union(vertex, neighbor)
            edges.add((vertex, neighbor))
    return edges

def draw_maze(edges, dim):
    maze = np.zeros((2*dim + 1, 2*dim + 1))
    for i in range(dim + 1):
        maze[2*i, :] = 1
        maze[:, 2*i] = 1
    for fr, to in edges:
        wall = (fr[0] + to[0] + 1, fr[1] + to[1] + 1)
        maze[wall[0], wall[1]] = 0
    maze[-2, 0] = 0
    maze[1, -1] = 0
    padded_maze = np.pad(maze, ((dim, dim), (dim, dim)), mode="constant", constant_values=0)
    plt.imshow(padded_maze, cmap="Greys")
    plt.show()
    return padded_maze

def solve_maze(maze_picture):
    rows, cols = maze_picture.shape
    print(rows, cols)
    top_intersection = np.argmax(maze_picture[:, cols//2])
    bot_intersection = np.argmax(maze_picture[:, cols//2][::-1])
    maze_picture[:top_intersection, cols//2] = 1
    maze_picture[-bot_intersection:, cols//2] = 1
    start = (0, 0)
    end = (rows - 1, cols - 1)
    visited = set([start])
    queue = deque([start])
    parents = {}
    found_solution = False
    while queue and not found_solution:
        # current = queue.pop()
        current = queue.popleft()
        # print(current)
        for neighbor in generate_neighbors(current, rows, cols):
            if neighbor in visited or maze_picture[neighbor] == 1:
                continue
            visited.add(neighbor)
            queue.append(neighbor)
            parents[neighbor] = current
            if neighbor == end:
                print("target found")
                found_solution = True
                break
    current = end
    maze_picture = np.stack([1 - maze_picture]*3, axis=2).astype("uint8")
    print(maze_picture.shape)
    while current != start and current in parents:
        maze_picture[current[0], current[1]] = [1, 0, 0]
        for neighbor in generate_neighbors(current, rows, cols, 5):
            if maze_picture[neighbor[0], neighbor[1], 0] == 1:
                maze_picture[neighbor[0], neighbor[1]] = [1, 0, 0]

        current = parents[current]
    plt.imsave("solution.png", maze_picture*255)
    return found_solution

def load_image_as_maze(fname, threshold=100):
    img = Image.open(fname)
    img.load()
    print(f"Image dimensions are {img.width}x{img.height}")
    filtered = np.mean(np.asarray(img, dtype="int32"), axis=2) < threshold
    rows = np.any(filtered, axis=1)
    cols = np.any(filtered, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    filtered = filtered[rmin-10:rmax+10, cmin-10:cmax+10]
    return filtered
