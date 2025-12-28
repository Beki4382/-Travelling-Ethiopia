from typing import Dict, List, Tuple, Optional, Set


# Basic unweighted graph for BFS and DFS
class Graph:
    
    def __init__(self):
        # Store city connections as adjacency list
        self.adjacency_list: Dict[str, List[str]] = {}
    
    def add_node(self, node: str) -> None:
        # Add city if not exists
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []
    
    def add_edge(self, node1: str, node2: str) -> None:
        # Ensure both nodes exist
        self.add_node(node1)
        self.add_node(node2)
        # Add bidirectional connection (undirected graph)
        if node2 not in self.adjacency_list[node1]:
            self.adjacency_list[node1].append(node2)
        if node1 not in self.adjacency_list[node2]:
            self.adjacency_list[node2].append(node1)
    
    def get_neighbors(self, node: str) -> List[str]:
        # Return list of connected cities
        return self.adjacency_list.get(node, [])
    
    def get_all_nodes(self) -> List[str]:
        # Return all cities in graph
        return list(self.adjacency_list.keys())
    
    def __str__(self) -> str:
        result = "Graph:\n"
        for node, neighbors in sorted(self.adjacency_list.items()):
            result += f"  {node} -> {neighbors}\n"
        return result


# Weighted graph for UCS and A* (adds edge costs)
class WeightedGraph(Graph):
    
    def __init__(self):
        super().__init__()
        # Store (neighbor, cost) tuples
        self.weighted_adjacency: Dict[str, List[Tuple[str, float]]] = {}
    
    def add_weighted_edge(self, node1: str, node2: str, cost: float) -> None:
        # Add to basic adjacency list
        self.add_edge(node1, node2)
        # Initialize weighted adjacency if needed
        if node1 not in self.weighted_adjacency:
            self.weighted_adjacency[node1] = []
        if node2 not in self.weighted_adjacency:
            self.weighted_adjacency[node2] = []
        # Add edge with cost (avoid duplicates)
        if not any(neighbor == node2 for neighbor, _ in self.weighted_adjacency[node1]):
            self.weighted_adjacency[node1].append((node2, cost))
        if not any(neighbor == node1 for neighbor, _ in self.weighted_adjacency[node2]):
            self.weighted_adjacency[node2].append((node1, cost))
    
    def get_weighted_neighbors(self, node: str) -> List[Tuple[str, float]]:
        # Return list of (neighbor, cost) tuples
        return self.weighted_adjacency.get(node, [])
    
    def get_cost(self, node1: str, node2: str) -> Optional[float]:
        # Get cost between two connected cities
        neighbors = self.weighted_adjacency.get(node1, [])
        for neighbor, cost in neighbors:
            if neighbor == node2:
                return cost
        return None
    
    def __str__(self) -> str:
        result = "Weighted Graph:\n"
        for node, neighbors in sorted(self.weighted_adjacency.items()):
            result += f"  {node} -> {neighbors}\n"
        return result


# Heuristic graph extends WeightedGraph (adds h(n) values for A*)
class HeuristicGraph(WeightedGraph):
    
    def __init__(self):
        super().__init__()
        # Store heuristic values h(n) for each city
        self.heuristics: Dict[str, float] = {}
    
    def set_heuristic(self, node: str, h_value: float) -> None:
        # Set estimated distance to goal
        self.heuristics[node] = h_value
    
    def get_heuristic(self, node: str) -> float:
        # Get heuristic value (default 0)
        return self.heuristics.get(node, 0)
    
    def __str__(self) -> str:
        result = "Heuristic Graph:\n"
        result += "Connections:\n"
        for node, neighbors in sorted(self.weighted_adjacency.items()):
            h = self.heuristics.get(node, "?")
            result += f"  {node} (h={h}) -> {neighbors}\n"
        return result


# City name aliases for consistency
FIGURE_1_NAME_ALIASES: Dict[str, str] = {
    "Asmera": "Asmara",
    "Nekemte": "Nekemete",
    "Mizan Teferi": "Mezan Teferi",
    "Gonder": "Gondar",
}


def _normalize_city_name(name: str) -> str:
    # Normalize city names for consistency
    name = (name or "").strip()
    return FIGURE_1_NAME_ALIASES.get(name, name)


# Unweighted adjacency list for BFS/DFS
FIGURE_1_ADJACENCY: Dict[str, List[str]] = {
    "Addis Ababa": ["Debre Birhan", "Ambo", "Adama"],
    "Adama": ["Addis Ababa", "Matahara", "Asella", "Batu"],
    "Adigrat": ["Asmera", "Adwa", "Mekelle"],
    "Adwa": ["Axum", "Adigrat", "Mekelle"],
    "Alamata": ["Mekelle", "Woldia", "Samara", "Sekota"],
    "Ambo": ["Nekemte", "Addis Ababa", "Wolkite"],
    "Arba Minch": ["Wolaita Sodo", "Basketo", "Konso"],
    "Asella": ["Adama", "Assasa"],
    "Asmera": ["Adigrat", "Axum"],
    "Assasa": ["Asella", "Dodolla"],
    "Assosa": ["Metekel", "Dembi Dollo"],
    "Awash": ["Matahara", "Chiro", "Gabi Rasu"],
    "Axum": ["Asmera", "Adwa", "Shire"],
    "Azezo": ["Gondar", "Metema", "Bahir Dar"],
    "Babile": ["Harar", "Jigjiga"],
    "Bahir Dar": ["Azezo", "Debre Tabor", "Finote Selam", "Metekel", "Injibara"],
    "Bale": ["Dodolla", "Liben", "Goba", "Sof Oumer"],
    "Basketo": ["Dawro", "Mizan Teferi", "Bench Maji", "Arba Minch"],
    "Batu": ["Adama", "Buta Jirra", "Shashemene"],
    "Bedelle": ["Nekemte", "Gore", "Jimma"],
    "Bench Maji": ["Basketo", "Juba"],
    "Bonga": ["Tepi", "Jimma", "Dawro", "Mizan Teferi"],
    "Bule Hora": ["Dilla", "Yabello"],
    "Buta Jirra": ["Worabe", "Batu"],
    "Chiro": ["Awash", "Dire Dawa"],
    "Dawro": ["Bonga", "Wolaita Sodo", "Basketo"],
    "Debarke": ["Shire", "Gondar"],
    "Debre Birhan": ["Debre Sina", "Addis Ababa"],
    "Debre Markos": ["Finote Selam", "Debre Sina"],
    "Debre Sina": ["Kemise", "Debre Birhan", "Debre Markos"],
    "Debre Tabor": ["Bahir Dar", "Lalibela"],
    "Dega Habur": ["Jigjiga", "Kebri Dehar", "Goba"],
    "Dembi Dollo": ["Assosa", "Gambella", "Gimbi"],
    "Dessie": ["Woldia", "Kemise"],
    "Dilla": ["Hawassa", "Bule Hora"],
    "Dire Dawa": ["Chiro", "Harar"],
    "Dodolla": ["Assasa", "Shashemene", "Bale"],
    "Dollo": ["Gode"],
    "Fanti Rasu": ["Kilbet Rasu", "Samara"],
    "Finote Selam": ["Injibara", "Bahir Dar", "Debre Markos"],
    "Gabi Rasu": ["Samara", "Awash"],
    "Gambella": ["Dembi Dollo", "Gore"],
    "Gimbi": ["Dembi Dollo", "Nekemte"],
    "Goba": ["Bale", "Sof Oumer"],
    "Gode": ["Kebri Dehar", "Dollo", "Mokadisho"],
    "Gondar": ["Humera", "Debarke", "Azezo", "Metema"],
    "Gore": ["Gambella", "Bedelle", "Tepi"],
    "Harar": ["Dire Dawa", "Babile"],
    "Hawassa": ["Shashemene", "Dilla"],
    "Hossana": ["Worabe", "Wolaita Sodo", "Shashemene"],
    "Humera": ["Kartum", "Shire", "Gondar"],
    "Injibara": ["Bahir Dar", "Finote Selam"],
    "Jigjiga": ["Babile", "Dega Habur"],
    "Jimma": ["Bedelle", "Bonga", "Wolkite"],
    "Juba": ["Bench Maji"],
    "Kartum": ["Metema", "Humera"],
    "Kebri Dehar": ["Dega Habur", "Werder", "Gode", "Sof Oumer"],
    "Kemise": ["Dessie", "Debre Sina"],
    "Kilbet Rasu": ["Fanti Rasu"],
    "Konso": ["Arba Minch", "Yabello"],
    "Lalibela": ["Debre Tabor", "Woldia"],
    "Liben": ["Bale"],
    "Matahara": ["Awash", "Adama"],
    "Mekelle": ["Adigrat", "Sekota", "Alamata", "Adwa"],
    "Metema": ["Kartum", "Azezo", "Gonder"],
    "Metekel": ["Bahir Dar", "Assosa"],
    "Mizan Teferi": ["Tepi", "Basketo", "Bonga"],
    "Mokadisho": ["Gode"],
    "Moyale": ["Yabello", "Nairobi"],
    "Nairobi": ["Moyale"],
    "Nekemte": ["Gimbi", "Bedelle", "Ambo"],
    "Samara": ["Alamata", "Woldia", "Fanti Rasu", "Gabi Rasu"],
    "Sekota": ["Mekelle", "Lalibela", "Alamata"],
    "Shashemene": ["Batu", "Hawassa", "Dodolla", "Hossana"],
    "Shire": ["Humera", "Axum", "Debarke"],
    "Sof Oumer": ["Goba", "Kebri Dehar", "Bale"],
    "Tepi": ["Gore", "Mizan Teferi", "Bonga"],
    "Werder": ["Kebri Dehar"],
    "Wolaita Sodo": ["Hossana", "Dawro", "Arba Minch"],
    "Woldia": ["Lalibela", "Alamata", "Samara", "Dessie"],
    "Wolkite": ["Ambo", "Jimma", "Worabe"],
    "Worabe": ["Wolkite", "Buta Jirra", "Hossana"],
    "Yabello": ["Konso", "Bule Hora", "Moyale"],
}


# Weighted adjacency list for UCS and A* {city: [(neighbor, cost), ...]}
FIGURE_2_WEIGHTED_ADJACENCY = {
    "Addis Ababa": [("Debre Birhan", 5), ("Ambo", 5), ("Adama", 3)],
    "Adama": [("Addis Ababa", 3), ("Matahara", 3), ("Asella", 4), ("Batu", 4)],
    "Adigrat": [("Asmara", 6), ("Adwa", 4), ("Mekelle", 4)],
    "Adwa": [("Axum", 1), ("Adigrat", 4), ("Mekelle", 5)],
    "Alamata": [("Mekelle", 5), ("Woldia", 3), ("Samara", 11), ("Sekota", 6)],
    "Ambo": [("Nekemte", 9), ("Addis Ababa", 5), ("Wolkite", 6)],
    "Arba Minch": [("Wolaita Sodo", 4), ("Basketo", 10), ("Konso", 4)],
    "Asella": [("Adama", 4), ("Assasa", 4)],
    "Asmara": [("Adigrat", 6), ("Axum", 5)],
    "Assasa": [("Asella", 4), ("Dodolla", 3)],
    "Assosa": [("Metekel", 8), ("Dembi Dollo", 12)],
    "Awash": [("Matahara", 1), ("Chiro", 4), ("Gabi Rasu", 5)],
    "Axum": [("Asmara", 5), ("Adwa", 1), ("Shire", 2)],
    "Azezo": [("Gondar", 1), ("Metema", 7), ("Bahir Dar", 7)],
    "Babile": [("Harar", 2), ("Jigjiga", 3)],
    "Bahir Dar": [("Azezo", 7), ("Debre Tabor", 4), ("Finote Selam", 6), ("Metekel", 11), ("Injibara", 4)],
    "Bale": [("Dodolla", 13), ("Liben", 11), ("Goba", 18), ("Sof Oumer", 23)],
    "Basketo": [("Dawro", 5), ("Mizan Teferi", 4), ("Bench Maji", 5), ("Arba Minch", 10)],
    "Batu": [("Adama", 4), ("Buta Jirra", 2), ("Shashemene", 3)],
    "Bedelle": [("Nekemte", 6), ("Gore", 6), ("Jimma", 7)],
    "Bench Maji": [("Basketo", 5), ("Juba", 22)],
    "Bonga": [("Tepi", 8), ("Jimma", 4), ("Dawro", 10), ("Mizan Teferi", 4)],
    "Bule Hora": [("Dilla", 4), ("Yabello", 3)],
    "Buta Jirra": [("Worabe", 5), ("Batu", 2)],
    "Chiro": [("Awash", 4), ("Dire Dawa", 8)],
    "Dawro": [("Bonga", 10), ("Wolaita Sodo", 10), ("Basketo", 5)],
    "Debarke": [("Shire", 9), ("Gondar", 4)],
    "Debre Birhan": [("Debre Sina", 2), ("Addis Ababa", 5)],
    "Debre Markos": [("Finote Selam", 3), ("Debre Sina", 17)],
    "Debre Sina": [("Kemise", 6), ("Debre Birhan", 2), ("Debre Markos", 17)],
    "Debre Tabor": [("Bahir Dar", 4), ("Lalibela", 8)],
    "Dega Habur": [("Jigjiga", 5), ("Kebri Dehar", 6), ("Goba", 25)],
    "Dembi Dollo": [("Assosa", 12), ("Gambella", 4), ("Gimbi", 6)],
    "Dessie": [("Woldia", 6), ("Kemise", 4)],
    "Dilla": [("Hawassa", 3), ("Bule Hora", 4)],
    "Dire Dawa": [("Chiro", 8), ("Harar", 4)],
    "Dodolla": [("Assasa", 3), ("Shashemene", 3), ("Bale", 13)],
    "Dollo": [("Gode", 17)],
    "Fanti Rasu": [("Kilbet Rasu", 6), ("Samara", 7)],
    "Finote Selam": [("Injibara", 2), ("Bahir Dar", 6), ("Debre Markos", 3)],
    "Gabi Rasu": [("Samara", 9), ("Awash", 5)],
    "Gambella": [("Dembi Dollo", 4), ("Gore", 5)],
    "Gimbi": [("Dembi Dollo", 6), ("Nekemte", 4)],
    "Goba": [("Bale", 18), ("Sof Oumer", 23)],
    "Gode": [("Kebri Dehar", 5), ("Dollo", 17), ("Mokadisho", 50)],
    "Gondar": [("Humera", 9), ("Debarke", 4), ("Azezo", 1), ("Metema", 7)],
    "Gore": [("Gambella", 5), ("Bedelle", 6), ("Tepi", 9)],
    "Harar": [("Dire Dawa", 4), ("Babile", 2)],
    "Hawassa": [("Shashemene", 1), ("Dilla", 3)],
    "Hossana": [("Worabe", 2), ("Wolaita Sodo", 7), ("Shashemene", 5)],
    "Humera": [("Kartum", 21), ("Shire", 8), ("Gondar", 9)],
    "Injibara": [("Bahir Dar", 4), ("Finote Selam", 2)],
    "Jigjiga": [("Babile", 3), ("Dega Habur", 5)],
    "Jimma": [("Bedelle", 7), ("Bonga", 4), ("Wolkite", 8)],
    "Juba": [("Bench Maji", 22)],
    "Kartum": [("Metema", 19), ("Humera", 21)],
    "Kebri Dehar": [("Dega Habur", 6), ("Werder", 6), ("Gode", 5), ("Sof Oumer", 23)],
    "Kemise": [("Dessie", 4), ("Debre Sina", 6)],
    "Kilbet Rasu": [("Fanti Rasu", 6)],
    "Konso": [("Arba Minch", 4), ("Yabello", 3)],
    "Lalibela": [("Debre Tabor", 8), ("Woldia", 7)],
    "Liben": [("Bale", 11)],
    "Matahara": [("Awash", 1), ("Adama", 3)],
    "Mekelle": [("Adigrat", 4), ("Sekota", 9), ("Alamata", 5), ("Adwa", 5)],
    "Metema": [("Kartum", 19), ("Azezo", 7), ("Gondar", 7)],
    "Metekel": [("Bahir Dar", 11), ("Assosa", 8)],
    "Mizan Teferi": [("Tepi", 4), ("Basketo", 4), ("Bonga", 4)],
    "Mokadisho": [("Gode", 50)],
    "Moyale": [("Yabello", 6), ("Nairobi", 22)],
    "Nairobi": [("Moyale", 22)],
    "Nekemte": [("Gimbi", 4), ("Bedelle", 6), ("Ambo", 9)],
    "Samara": [("Alamata", 11), ("Woldia", 8), ("Fanti Rasu", 7), ("Gabi Rasu", 9)],
    "Sekota": [("Mekelle", 9), ("Lalibela", 6), ("Alamata", 6)],
    "Shashemene": [("Batu", 3), ("Hawassa", 1), ("Dodolla", 3), ("Hossana", 5)],
    "Shire": [("Humera", 8), ("Axum", 2), ("Debarke", 9)],
    "Sof Oumer": [("Goba", 23), ("Kebri Dehar", 23), ("Bale", 23)],
    "Tepi": [("Gore", 9), ("Mizan Teferi", 4), ("Bonga", 8)],
    "Werder": [("Kebri Dehar", 6)],
    "Wolaita Sodo": [("Hossana", 7), ("Dawro", 10), ("Arba Minch", 4)],
    "Woldia": [("Lalibela", 7), ("Alamata", 3), ("Samara", 8), ("Dessie", 6)],
    "Wolkite": [("Ambo", 6), ("Jimma", 8), ("Worabe", 2)],
    "Worabe": [("Wolkite", 2), ("Buta Jirra", 5), ("Hossana", 2)],
    "Yabello": [("Konso", 3), ("Bule Hora", 3), ("Moyale", 6)],
}


# Create unweighted graph from Figure 1 for BFS/DFS
def create_ethiopia_graph() -> Graph:
    graph = Graph()
    for city, neighbors in FIGURE_1_ADJACENCY.items():
        city_n = _normalize_city_name(city)
        for neighbor in neighbors:
            neighbor_n = _normalize_city_name(neighbor)
            if city_n and neighbor_n and city_n != neighbor_n:
                graph.add_edge(city_n, neighbor_n)
    return graph


# Heuristic values h(n) = estimated distance to Moyale (for A*)
HEURISTICS_TO_MOYALE = {
    "Moyale": 0,
    "Yabello": 6,
    "Konso": 9,
    "Bule Hora": 8,
    "Arba Minch": 13,
    "Dilla": 12,
    "Liben": 11,
    "Bale": 22,
    "Robe": 22,
    "Goba": 40,
    "Sof Oumer": 45,
    "Dollo": 18,
    "Gode": 35,
    "Hawassa": 15,
    "Wolaita Sodo": 17,
    "Shashemene": 16,
    "Assasa": 18,
    "Dodolla": 19,
    "Dawro": 23,
    "Basketo": 23,
    "Bench Maji": 28,
    "Juba": 50,
    "Addis Ababa": 26,
    "Adama": 23,
    "Batu": 19,
    "Assella": 22,
    "Buta Jirra": 22,
    "Debre Birhan": 31,
    "Debre Sina": 33,
    "Kemise": 40,
    "Jimma": 33,
    "Wolkite": 25,
    "Worabe": 21,
    "Hossana": 21,
    "Bonga": 37,
    "Tepi": 41,
    "Gore": 46,
    "Bedelle": 40,
    "Mizan Teferi": 37,
    "Nekemte": 39,
    "Gimbi": 43,
    "Dembi Dollo": 49,
    "Gambella": 51,
    "Assosa": 51,
    "Ambo": 31,
    "Matahara": 26,
    "Awash": 27,
    "Chiro": 31,
    "Dire Dawa": 37,
    "Harar": 35,
    "Babile": 35,
    "Jigjiga": 40,
    "Dega Habur": 45,
    "Kebri Dehar": 40,
    "Werder": 46,
    "Gabi Rasu": 32,
    "Dessie": 44,
    "Woldia": 50,
    "Lalibela": 57,
    "Debre Tabor": 52,
    "Bahir Dar": 48,
    "Gondar": 56,
    "Debarke": 60,
    "Azezo": 55,
    "Metema": 62,
    "Humera": 65,
    "Kartum": 81,
    "Shire": 67,
    "Axum": 66,
    "Adwa": 65,
    "Adigrat": 62,
    "Mekelle": 58,
    "Sekota": 59,
    "Alamata": 53,
    "Samara": 42,
    "Fanti Rasu": 49,
    "Kilbet Rasu": 55,
    "Asmara": 68,
    "Injibara": 44,
    "Finote Selam": 42,
    "Debre Markos": 39,
    "Metekel": 59,
    "Nairobi": 22,
    "Mokadisho": 40,
}


# Create weighted graph from Figure 2 for UCS and A*
def create_weighted_ethiopia_graph() -> WeightedGraph:
    graph = WeightedGraph()
    for city, neighbors in FIGURE_2_WEIGHTED_ADJACENCY.items():
        for neighbor, weight in neighbors:
            graph.add_weighted_edge(city, neighbor, weight)
    return graph


# Create heuristic graph (weighted + heuristics) for A*
def create_heuristic_ethiopia_graph() -> HeuristicGraph:
    graph = HeuristicGraph()
    # Add weighted edges
    for city, neighbors in FIGURE_2_WEIGHTED_ADJACENCY.items():
        for neighbor, weight in neighbors:
            graph.add_weighted_edge(city, neighbor, weight)
    # Add heuristic values
    for city, h_value in HEURISTICS_TO_MOYALE.items():
        graph.set_heuristic(city, h_value)
    return graph

