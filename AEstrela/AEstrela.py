import heapq

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

# Heurística: distância em linha reta (em km)
heuristic = {
    "Stuttgart": 6200,
    "Paris": 5900,
    "Berlin": 6100,
    "London": 5600,
    "Reykjavik": 3900,
    "New York": 300,
    "Boston": 0
}

def a_star_search(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))  # (f_score, city)

    came_from = {}  # Para reconstruir o caminho
    g_score = {city: float("inf") for city in graph}
    g_score[start] = 0

    f_score = {city: float("inf") for city in graph}
    f_score[start] = heuristic[start]

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruir o caminho
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            print("Caminho encontrado:")
            for step in path:
                print(f"-> {step}", end=" ")
            print("\nDistância total:", g_score[goal], "km")
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

# Executa a busca
a_star_search("Stuttgart", "Boston")
