"""
MiniMax Algorithm Implementation
"""

from typing import List, Tuple, Optional
from enum import Enum


class PlayerType(Enum):
    """Enum to represent player types."""
    MAX = "MAX"  # Our agent (wants maximum utility)
    MIN = "MIN"  # Adversary (wants minimum utility for us)


class GameNode:
    """Represents a node in the game tree."""
    def __init__(self, name: str, player: PlayerType = PlayerType.MAX, 
                 utility: Optional[int] = None):
        self.name = name
        self.player = player
        self.children: List['GameNode'] = []
        self.utility = utility
        self.is_terminal = utility is not None
    
    def add_child(self, child: 'GameNode') -> None:
        """Add a child node."""
        self.children.append(child)
    
    def __str__(self) -> str:
        if self.is_terminal:
            return f"{self.name} (utility={self.utility})"
        return f"{self.name} ({self.player.value}'s turn, {len(self.children)} children)"


class MiniMaxResult:
    """Result of MiniMax search."""
    def __init__(self, best_value: int, best_path: List[str], 
                 decision_tree: str = ""):
        self.best_value = best_value
        self.best_path = best_path
        self.decision_tree = decision_tree
    
    def __str__(self) -> str:
        return (f" MiniMax Result:\n"
                f"   Best achievable utility: {self.best_value}\n"
                f"   Optimal path: {' → '.join(self.best_path)}\n"
                f"\n{self.decision_tree}")


class MiniMax:
    """
    MiniMax algorithm implementation.
    """
    
    def __init__(self):
        """Initialize MiniMax solver."""
        self.nodes_evaluated = 0
        self.decision_log: List[str] = []
    
    def search(self, root: GameNode, verbose: bool = True) -> MiniMaxResult:
        
        self.nodes_evaluated = 0
        self.decision_log = []
        
        if verbose:
            print(f" MiniMax Search Starting from {root.name}")
            print("=" * 50)
        
        best_value, best_path = self._minimax(root, [], 0, verbose)
        
        decision_tree = self._build_decision_tree(root, 0)
        
        if verbose:
            print(f" Total nodes evaluated: {self.nodes_evaluated}")
        
        return MiniMaxResult(best_value, best_path, decision_tree)
    
    def _minimax(self, node: GameNode, path: List[str], depth: int, 
                 verbose: bool) -> Tuple[int, List[str]]:
        """
        Recursive MiniMax implementation.
        """
        self.nodes_evaluated += 1
        current_path = path + [node.name]
        indent = "  " * depth
        
        # Terminal node: return utility
        if node.is_terminal:
            if verbose:
                print(f"{indent}🍃 Terminal: {node.name} = {node.utility}")
            return node.utility, current_path
        
        if verbose:
            player_emoji = "🔵" if node.player == PlayerType.MAX else "🔴"
            print(f"{indent}{player_emoji} {node.player.value}: {node.name}")
        
        if node.player == PlayerType.MAX:
            # MAX wants to maximize
            best_value = float('-inf')
            best_path = current_path
            
            for child in node.children:
                value, child_path = self._minimax(child, current_path, depth + 1, verbose)
                if value > best_value:
                    best_value = value
                    best_path = child_path
            
            if verbose:
                print(f"{indent}   → MAX chooses {best_value} (path to {best_path[-1] if best_path else '?'})")
            
            return best_value, best_path
        
        else:  # MIN player
            # MIN wants to minimize (from MAX's perspective)
            best_value = float('inf')
            best_path = current_path
            
            for child in node.children:
                value, child_path = self._minimax(child, current_path, depth + 1, verbose)
                if value < best_value:
                    best_value = value
                    best_path = child_path
            
            if verbose:
                print(f"{indent}   → MIN chooses {best_value} (path to {best_path[-1] if best_path else '?'})")
            
            return best_value, best_path
    
    def _build_decision_tree(self, node: GameNode, depth: int) -> str:
        """
        Build a string visualization of the decision tree.
        """
        indent = "    " * depth
        
        if node.is_terminal:
            return f"{indent}└── {node.name} [utility: {node.utility}]\n"
        
        player_marker = "[MAX]" if node.player == PlayerType.MAX else "[MIN]"
        result = f"{indent}├── {node.name} {player_marker}\n"
        
        for child in node.children:
            result += self._build_decision_tree(child, depth + 1)
        
        return result


def create_ethiopia_adversarial_game() -> GameNode:
    
    root = GameNode("Addis Ababa", PlayerType.MAX)

    gedo = GameNode("Gedo", PlayerType.MAX)
    root.add_child(gedo)
    
    nekemete = GameNode("Nekemete", PlayerType.MIN)
    gedo.add_child(nekemete)
    
    shambu = GameNode("Shambu", utility=4)
    nekemete.add_child(shambu)
    
    fincha = GameNode("Fincha", utility=5)
    nekemete.add_child(fincha)
    
    gimbi_limu = GameNode("Gimbi-Limu", PlayerType.MIN)
    gedo.add_child(gimbi_limu)
    
    gimbi = GameNode("Gimbi", utility=8)
    gimbi_limu.add_child(gimbi)
    
    limu = GameNode("Limu", utility=8)
    gimbi_limu.add_child(limu)
    
    ambo = GameNode("Ambo", PlayerType.MAX)
    root.add_child(ambo)
    
    buta_jirra = GameNode("Buta Jirra", PlayerType.MIN)
    ambo.add_child(buta_jirra)
    
    worabe = GameNode("Worabe", PlayerType.MAX)
    buta_jirra.add_child(worabe)
    
    hossana = GameNode("Hossana", utility=6)
    worabe.add_child(hossana)
    
    durame = GameNode("Durame", utility=5)
    worabe.add_child(durame)
    
    wolkite = GameNode("Wolkite", PlayerType.MAX)
    buta_jirra.add_child(wolkite)
    
    bench_naji = GameNode("Bench Naji", utility=5)
    wolkite.add_child(bench_naji)
    
    tepi = GameNode("Tepi", utility=6)
    wolkite.add_child(tepi)
    
    kaffa = GameNode("Kaffa", utility=7)
    wolkite.add_child(kaffa)
    
    adama = GameNode("Adama", PlayerType.MIN)  
    root.add_child(adama)
    
    mojo = GameNode("Mojo", PlayerType.MAX)
    adama.add_child(mojo)
    
    dilla = GameNode("Dilla", utility=9)
    mojo.add_child(dilla)
    
    diredawa = GameNode("Diredawa", PlayerType.MIN)
    adama.add_child(diredawa)
    
    chiro = GameNode("Chiro", utility=6)
    diredawa.add_child(chiro)
    
    harar = GameNode("Harar", utility=10)
    diredawa.add_child(harar)
    
    return root



if __name__ == "__main__":
    game_tree = create_ethiopia_adversarial_game()
    minimax = MiniMax()
    result = minimax.search(game_tree, verbose=False)
    
    print(f"Best coffee quality: {result.best_value}")
    print(f"Optimal path: {' -> '.join(result.best_path)}")

