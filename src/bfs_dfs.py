from collections import deque
from typing import List, Set, Tuple

try:
    from .graph import Graph, create_ethiopia_graph
except ImportError:
    from graph import Graph, create_ethiopia_graph



class SearchResult:
    def __init__(self, path: List[str] = None, success: bool = False):
        self.path = path or []
        self.success = success
    
    def __str__(self) -> str:
        if self.success:
            return (f"Path Found: {' -> '.join(self.path)}\n"
                    f"Path Length: {len(self.path)} cities")
        return "No path found"


class TravelEthiopiaSearch:
    
    def __init__(self, graph: Graph):
        self.graph = graph
    
    def search(self, initial_state: str, goal_state: str, strategy: str = "bfs") -> SearchResult:
        strategy = strategy.lower()
        if strategy == "bfs":
            return self._breadth_first_search(initial_state, goal_state)
        elif strategy == "dfs":
            return self._depth_first_search(initial_state, goal_state)
        else:
            raise ValueError(f"Unknown strategy: {strategy}. Use 'bfs' or 'dfs'.")
    
    def _breadth_first_search(self, initial: str, goal: str) -> SearchResult:
        if initial not in self.graph.adjacency_list:
            return SearchResult(success=False)
        if goal not in self.graph.adjacency_list:
            return SearchResult(success=False)
        if initial == goal:
            return SearchResult(path=[initial], success=True)
        
        queue = deque([(initial, [initial])])
        visited: Set[str] = {initial}
        
        while queue:
            current, path = queue.popleft()
            for neighbor in self.graph.get_neighbors(current):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    if neighbor == goal:
                        return SearchResult(path=new_path, success=True)
                    visited.add(neighbor)
                    queue.append((neighbor, new_path))
        
        return SearchResult(success=False)
    
    def _depth_first_search(self, initial: str, goal: str) -> SearchResult:
        if initial not in self.graph.adjacency_list:
            return SearchResult(success=False)
        if goal not in self.graph.adjacency_list:
            return SearchResult(success=False)
        if initial == goal:
            return SearchResult(path=[initial], success=True)
        
        stack: List[Tuple[str, List[str]]] = [(initial, [initial])]
        visited: Set[str] = set()
        
        while stack:
            current, path = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                return SearchResult(path=path, success=True)
            for neighbor in reversed(self.graph.get_neighbors(current)):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    stack.append((neighbor, new_path))
        
        return SearchResult(success=False)


if __name__ == "__main__":
    print("=== BFS & DFS Search ===")
    print("Available cities: Addis Ababa, Gondar, Lalibela, Axum, Bahir Dar, Mekelle, etc.")
    print()
    
    start = input("Enter start city (default: Addis Ababa): ").strip()
    if not start:
        start = "Addis Ababa"
    
    goal = input("Enter goal city (default: Gondar): ").strip()
    if not goal:
        goal = "Gondar"
    
    strategy = input("Choose strategy [1] BFS [2] DFS [3] Both (default: 3): ").strip()
    
    graph = create_ethiopia_graph()
    searcher = TravelEthiopiaSearch(graph)
    
    if strategy in ("1", "bfs"):
        result = searcher.search(start, goal, "bfs")
        print(f"\nBFS Result:")
        print(result)
    elif strategy in ("2", "dfs"):
        result = searcher.search(start, goal, "dfs")
        print(f"\nDFS Result:")
        print(result)
    else:
        # Run both
        result = searcher.search(start, goal, "bfs")
        print(f"\nBFS Result:")
        print(result)
        
        result = searcher.search(start, goal, "dfs")
        print(f"\nDFS Result:")
        print(result)