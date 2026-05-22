import json
from collections import deque


# =========================
# NODE
# =========================
class GraphNode:
    def __init__(self, name):
        if not name.strip():
            raise ValueError("Имя вершины не может быть пустым.")

        self.name = name

    def __str__(self):
        return self.name


# =========================
# EDGE
# =========================
class Edge:
    def __init__(self, from_node, to_node, weight=1):
        if weight < 0:
            raise ValueError("Вес не может быть отрицательным.")

        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight


# =========================
# ABSTRACT GRAPH
# =========================
class Graph:
    def __init__(self):
        self.adjacency_list = {}

    # Добавление вершины
    def add_node(self, node):
        if not node.strip():
            raise ValueError("Имя вершины пустое.")

        if node in self.adjacency_list:
            raise Exception("Вершина уже существует.")

        self.adjacency_list[node] = []

    # Удаление вершины
    def remove_node(self, node):
        if node not in self.adjacency_list:
            raise Exception("Вершина не найдена.")

        del self.adjacency_list[node]

        for edges in self.adjacency_list.values():
            edges[:] = [e for e in edges if e.to_node != node]

    # Добавление ребра
    def add_edge(self, from_node, to_node, weight=1):
        raise NotImplementedError

    # Удаление ребра
    def remove_edge(self, from_node, to_node):
        if from_node not in self.adjacency_list:
            raise Exception("Вершина не найдена.")

        self.adjacency_list[from_node] = [
            e for e in self.adjacency_list[from_node]
            if e.to_node != to_node
        ]

    # Вывод графа
    def print_graph(self):
        for node, edges in self.adjacency_list.items():
            print(f"{node}: ", end="")

            for edge in edges:
                print(f"-> {edge.to_node}(w:{edge.weight}) ", end="")

            print()


# =========================
# DIRECTED GRAPH
# =========================
class DirectedGraph(Graph):
    def add_edge(self, from_node, to_node, weight=1):
        if from_node not in self.adjacency_list or \
           to_node not in self.adjacency_list:
            raise Exception("Одна из вершин отсутствует.")

        self.adjacency_list[from_node].append(
            Edge(from_node, to_node, weight)
        )


# =========================
# UNDIRECTED GRAPH
# =========================
class UndirectedGraph(Graph):
    def add_edge(self, from_node, to_node, weight=1):
        if from_node not in self.adjacency_list or \
           to_node not in self.adjacency_list:
            raise Exception("Одна из вершин отсутствует.")

        self.adjacency_list[from_node].append(
            Edge(from_node, to_node, weight)
        )

        self.adjacency_list[to_node].append(
            Edge(to_node, from_node, weight)
        )


# =========================
# WEIGHTED GRAPH
# =========================
class WeightedGraph(Graph):
    def add_edge(self, from_node, to_node, weight=1):
        if weight < 0:
            raise Exception("Вес не может быть отрицательным.")

        if from_node not in self.adjacency_list or \
           to_node not in self.adjacency_list:
            raise Exception("Одна из вершин отсутствует.")

        self.adjacency_list[from_node].append(
            Edge(from_node, to_node, weight)
        )


# =========================
# FACTORY
# =========================
class GraphFactory:
    @staticmethod
    def create_graph(graph_type):
        graph_type = graph_type.lower()

        if graph_type == "directed":
            return DirectedGraph()

        elif graph_type == "undirected":
            return UndirectedGraph()

        elif graph_type == "weighted":
            return WeightedGraph()

        else:
            raise Exception("Неизвестный тип графа.")


# =========================
# BFS
# =========================
class BFS:
    @staticmethod
    def traverse(graph, start):
        if start not in graph.adjacency_list:
            raise Exception("Стартовая вершина отсутствует.")

        visited = set()
        queue = deque()
        result = []

        visited.add(start)
        queue.append(start)

        while queue:
            current = queue.popleft()

            result.append(current)

            for edge in graph.adjacency_list[current]:
                if edge.to_node not in visited:
                    visited.add(edge.to_node)
                    queue.append(edge.to_node)

        return result


# =========================
# DFS
# =========================
class DFS:
    @staticmethod
    def traverse(graph, start):
        if start not in graph.adjacency_list:
            raise Exception("Стартовая вершина отсутствует.")

        visited = set()
        result = []

        DFS._dfs_recursive(graph, start, visited, result)

        return result

    @staticmethod
    def _dfs_recursive(graph, current, visited, result):
        visited.add(current)
        result.append(current)

        for edge in graph.adjacency_list[current]:
            if edge.to_node not in visited:
                DFS._dfs_recursive(
                    graph,
                    edge.to_node,
                    visited,
                    result
                )


# =========================
# DIJKSTRA
# =========================
class Dijkstra:
    @staticmethod
    def find_shortest_paths(graph, start):
        if start not in graph.adjacency_list:
            raise Exception("Стартовая вершина отсутствует.")

        distances = {
            node: float("inf")
            for node in graph.adjacency_list
        }

        distances[start] = 0

        visited = set()

        while len(visited) < len(graph.adjacency_list):

            current = min(
                (
                    node for node in distances
                    if node not in visited
                ),
                key=lambda node: distances[node]
            )

            visited.add(current)

            for edge in graph.adjacency_list[current]:

                new_distance = (
                    distances[current] + edge.weight
                )

                if new_distance < distances[edge.to_node]:
                    distances[edge.to_node] = new_distance

        return distances


# =========================
# JSON SERIALIZER
# =========================
class GraphSerializer:

    @staticmethod
    def save(graph, path):
        data = {}

        for node, edges in graph.adjacency_list.items():
            data[node] = []

            for edge in edges:
                data[node].append({
                    "to": edge.to_node,
                    "weight": edge.weight
                })

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def load(path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)


# =========================
# PROGRAM
# =========================
def main():

    print("=== GRAPH NAVIGATOR ===")

    try:

        # Создание графа через Factory
        graph = GraphFactory.create_graph("weighted")

        # Добавление вершин
        graph.add_node("A")
        graph.add_node("B")
        graph.add_node("C")
        graph.add_node("D")
        graph.add_node("E")

        # Добавление рёбер
        graph.add_edge("A", "B", 4)
        graph.add_edge("A", "C", 2)
        graph.add_edge("B", "D", 5)
        graph.add_edge("C", "D", 1)
        graph.add_edge("D", "E", 3)

        # Вывод графа
        print("\nГРАФ:")
        graph.print_graph()

        # BFS
        print("\nBFS:")
        bfs_result = BFS.traverse(graph, "A")
        print(" -> ".join(bfs_result))

        # DFS
        print("\nDFS:")
        dfs_result = DFS.traverse(graph, "A")
        print(" -> ".join(dfs_result))

        # Дейкстра
        print("\nКРАТЧАЙШИЕ ПУТИ (ДЕЙКСТРА):")

        distances = Dijkstra.find_shortest_paths(graph, "A")

        for node, distance in distances.items():
            print(f"До {node}: {distance}")

        # Сохранение JSON
        print("\nСОХРАНЕНИЕ В JSON...")
        GraphSerializer.save(graph, "graph.json")

        print("Граф сохранён в graph.json")

        # Загрузка JSON
        print("\nЗАГРУЗКА ИЗ JSON:")

        loaded = GraphSerializer.load("graph.json")

        print(json.dumps(
            loaded,
            indent=4,
            ensure_ascii=False
        ))

        print("\nПрограмма завершена.")

    except Exception as error:
        print(f"Ошибка: {error}")


# =========================
# START
# =========================
if __name__ == "__main__":
    main()
