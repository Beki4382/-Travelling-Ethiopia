#Uniform Cost Search (UCS) Implementation

import heapq
from typing import List, Dict

try:
    from .graph import WeightedGraph, create_weighted_ethiopia_graph
except ImportError:
    from graph import WeightedGraph, create_weighted_ethiopia_graph


class UCSResult:
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


class UniformCostSearch:
    """
    Finds the lowest cost path using a priority queue.
    """
    
    def __init__(self, graph: WeightedGraph):
        self.graph = graph
    
    def search(self, initial: str, goal: str) -> UCSResult:
        if initial not in self.graph.weighted_adjacency:
            return UCSResult(success=False)
        if goal not in self.graph.weighted_adjacency:
            return UCSResult(success=False)
        if initial == goal:
            return UCSResult(path=[initial], total_cost=0, success=True)
        
        counter = 0
        pq = [(0, counter, initial, [initial])]
        visited: Dict[str, float] = {}
        
        while pq:
            current_cost, _, current_city, path = heapq.heappop(pq)
            
            if current_city in visited and visited[current_city] <= current_cost:
                continue
            
            visited[current_city] = current_cost
            
            if current_city == goal:
                return UCSResult(path=path, total_cost=current_cost, success=True)
            
            for neighbor, edge_cost in self.graph.get_weighted_neighbors(current_city):
                if neighbor not in visited:
                    new_cost = current_cost + edge_cost
                    new_path = path + [neighbor]
                    counter += 1
                    heapq.heappush(pq, (new_cost, counter, neighbor, new_path))
        
        return UCSResult(success=False)


class MultiGoalUCS:
    """
    Multi-goal UCS 
    Visits all goal cities using greedy nearest-first approach.
    """
    
    def __init__(self, graph: WeightedGraph):
        self.graph = graph
        self.ucs = UniformCostSearch(graph)
    
    def search(self, initial: str, goals: List[str]) -> Dict:
        unvisited_goals = set(goals)
        current_location = initial
        complete_path = [initial]
        total_cost = 0
        visit_order = []
        
        while unvisited_goals:
            best_result = None
            best_goal = None
            best_cost = float('inf')
            
            for goal in unvisited_goals:
                result = self.ucs.search(current_location, goal)
                if result.success and result.total_cost < best_cost:
                    best_cost = result.total_cost
                    best_goal = goal
                    best_result = result
            
            if best_result is None:
                return {
                    "complete_path": complete_path,
                    "total_cost": total_cost,
                    "visit_order": visit_order,
                    "success": False
                }
            
            complete_path.extend(best_result.path[1:])
            total_cost += best_cost
            visit_order.append(best_goal)
            unvisited_goals.remove(best_goal)
            current_location = best_goal
        
        return {
            "complete_path": complete_path,
            "total_cost": total_cost,
            "visit_order": visit_order,
            "success": True
        }


if __name__ == "__main__":
    print("=== Uniform Cost Search (UCS) ===")
    print("Available cities: Addis Ababa, Gondar, Lalibela, Axum, Bahir Dar, Moyale, etc.")
    print()
    
    choice = input("Choose mode: [1] single goal or [2] multi-goal (default=1): ").strip().lower()
    
    graph = create_weighted_ethiopia_graph()
    
    if choice in ("2", "multi", "m"):
        # Multi-goal mode
        start = input("Enter start city (default: Addis Ababa): ").strip()
        if not start:
            start = "Addis Ababa"
        
        print("Default goals: Axum, Gondar, Lalibela, Babile, Jimma, Bale, Sof Oumer, Arba Minch")
        goals_input = input("Enter goals (comma-separated) or press Enter for default: ").strip()
        
        if goals_input:
            goals = [g.strip() for g in goals_input.split(",")]
        else:
            goals = ["Axum", "Gondar", "Lalibela", "Babile", "Jimma", "Bale", "Sof Oumer", "Arba Minch"]
        
        multi_ucs = MultiGoalUCS(graph)
        result = multi_ucs.search(start, goals)
        print(f"\nVisit Order: {' -> '.join([start] + result['visit_order'])}")
        print(f"Total Cost: {result['total_cost']}")
    else:
        # Single goal mode
        start = input("Enter start city (default: Addis Ababa): ").strip()
        if not start:
            start = "Addis Ababa"
        
        goal = input("Enter goal city (default: Lalibela): ").strip()
        if not goal:
            goal = "Lalibela"
        
        ucs = UniformCostSearch(graph)
        result = ucs.search(start, goal)
        print(f"\nUCS Result:")
        print(result)
