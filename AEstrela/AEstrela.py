import heapq
import networkx as nx
import matplotlib.pyplot as plt
import math

# Grafo com distâncias reais aproximadas entre cidades conectadas (em km)
graph = {
    "Stuttgart": {"Paris": 500, "Berlin": 635},
    "Paris": {"London": 344, "New York": 5830},
    "Berlin": {"London": 930, "Reykjavik": 2500},
    "London": {"Reykjavik": 1900, "New York": 5570},
    "Reykjavik": {"New York": 4200},
    "New York": {"Boston": 300},
    "Boston": {}
}

# Coordenadas aproximadas (latitude, longitude) de cada cidade
coordinates = {
    "Stuttgart": (48.78, 9.18),
    "Paris": (48.85, 2.35),
    "Berlin": (52.52, 13.40),
    "London": (51.50, -0.12),
    "Reykjavik": (64.13, -21.90),
    "New York": (40.71, -74.01),
    "Boston": (42.36, -71.05)
}

# Posições no plano para visualização
city_positions = {
    "Stuttgart": (1, 3),
    "Paris": (0, 2),
    "Berlin": (2, 4),
    "London": (0, 3),
    "Reykjavik": (-1, 5),
    "New York": (-3, 2),
    "Boston": (-4, 1)
}

def straight_line_distance(coord1, coord2):
    # Distância euclidiana entre pontos no globo, multiplicada por 111 km (1 grau de latitude = 111 km)
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 111

def build_heuristic(goal):
    heuristic = {}
    for city in coordinates:
        heuristic[city] = straight_line_distance(coordinates[city], coordinates[goal])
    return heuristic

def draw_graph(graph, path=None):
    G = nx.DiGraph()
    for city, neighbors in graph.items():
        for neighbor, distance in neighbors.items():
            G.add_edge(city, neighbor, weight=distance)

    pos = city_positions  # posições fixas para visualização

    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10, arrows=True)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red')

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

    plt.title("Grafo de cidades com melhor caminho (A*)")
    plt.axis("off")
    plt.show()

def a_star_search(start, goal):
    heuristic = build_heuristic(goal)

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {city: float("inf") for city in graph}
    g_score[start] = 0

    f_score = {city: float("inf") for city in graph}
    f_score[start] = heuristic[start]

    caminho_percorrido = []

    while open_set:
        _, current = heapq.heappop(open_set)
        caminho_percorrido.append(current)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()

            print("\nCaminho percorrido até encontrar o objetivo:")
            for step in caminho_percorrido:
                print(f"-> {step}", end=" ")
            print("\n\nCaminho final encontrado:")
            for step in path:
                print(f"-> {step}", end=" ")
            print("\n\nDistância total:", g_score[goal], "km")
            return path

        for neighbor, distance in graph[current].items():
            tentative_g_score = g_score[current] + distance
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic[neighbor]
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    print("Caminho não encontrado.")
    return None


inicio = "Stuttgart"
fim = "Boston"

draw_graph(graph)
path = a_star_search(inicio, fim)
if path:
    draw_graph(graph, path)
