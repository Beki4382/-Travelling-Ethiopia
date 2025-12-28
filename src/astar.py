"""
A* Search Algorithm Implementation 
"""

import heapq
from typing import List, Dict
from graph import WeightedGraph, create_weighted_ethiopia_graph, HEURISTICS_TO_MOYALE


class AStarResult:
    def __init__(self, path: List[str] = None, total_cost: float = 0, success: bool = False):
        self.path = path or []
        self.total_cost = total_cost
        self.success = success
    
    def __str__(self) -> str:
        if self.success:
            return (f"Path Found: {' -> '.join(self.path)}\n"
                    f"Total Cost: {self.total_cost}\n"
                    f"Path Length: {len(self.path)} cities")
        return "No path found"


class AStarSearch:
    """
    A* Search implementation.
    Uses f(n) = g(n) + h(n) to find optimal path.
    
    Takes the SAME WeightedGraph as UCS + heuristics dictionary.
    """
    
    def __init__(self, graph: WeightedGraph, heuristics: Dict[str, float]):
        self.graph = graph
        self.heuristics = heuristics
    
    def get_heuristic(self, node: str) -> float:
        return self.heuristics.get(node, 0)
    
    def search(self, initial: str, goal: str) -> AStarResult:
        if initial not in self.graph.weighted_adjacency:
            return AStarResult(success=False)
        if goal not in self.graph.weighted_adjacency:
            return AStarResult(success=False)
        if initial == goal:
            return AStarResult(path=[initial], total_cost=0, success=True)
        
        h_initial = self.get_heuristic(initial)
        counter = 0
        
        pq = [(h_initial, 0, counter, initial, [initial])]
        g_scores: Dict[str, float] = {initial: 0}
        
        while pq:
            f_value, g_value, _, current, path = heapq.heappop(pq)
            
            if current in g_scores and g_value > g_scores[current]:
                continue
            
            if current == goal:
                return AStarResult(path=path, total_cost=g_value, success=True)
            
            for neighbor, edge_cost in self.graph.get_weighted_neighbors(current):
                tentative_g = g_value + edge_cost
                
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    h_neighbor = self.get_heuristic(neighbor)
                    f_neighbor = tentative_g + h_neighbor
                    new_path = path + [neighbor]
                    counter += 1
                    heapq.heappush(pq, (f_neighbor, tentative_g, counter, neighbor, new_path))
        
        return AStarResult(success=False)


if __name__ == "__main__":
    print("=== A* Search Algorithm ===")
    print("Available cities: Addis Ababa, Moyale, Gondar, Lalibela, Axum, Bahir Dar, etc.")
    print("(Heuristics are optimized for reaching Moyale)")
    print()
    
    start = input("Enter start city (default: Addis Ababa): ").strip()
    if not start:
        start = "Addis Ababa"
    
    goal = input("Enter goal city (default: Moyale): ").strip()
    if not goal:
        goal = "Moyale"
    
    graph = create_weighted_ethiopia_graph()
   
    astar = AStarSearch(graph, HEURISTICS_TO_MOYALE)
    result = astar.search(start, goal)
    print(f"\nA* Result:")
    print(result)
