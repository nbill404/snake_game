# A* algorithm for pathfinding
import heapq
from math import dist

from snakegame import SnakeGame

class Node:

    def __init__(self, pos, f,  predecessor = None):
        self.pos = pos
        self.f = f
        self.predecessor = predecessor      
    
    def __lt__(self, other) -> bool:
        return self.f < other.f

    def __eq__(self, other) -> bool:
        return self.pos[0] == other.pos[0] and self.pos[1] == other.pos[1]

def search(matrix, start, end):
    nodes_open = []
    nodes_closed = []

    heapq.heappush(nodes_open, Node(start, 0))

    while nodes_open:
        current = heapq.heappop(nodes_open)
        nodes_closed.append(current)  

        if current.pos[0] == end[0] and current.pos[1] == end[1]:
            return current
        
        for d in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            i = current.pos[0] + d[0]
            j = current.pos[1] + d[1]

            if not(0 <= i and i < len(matrix) and 0 <= j and j < len(matrix[0])):
                continue
            
            # 0 represents open space
            if matrix[i][j] != 0 or Node([i, j], 0) in nodes_closed:
                continue
            
            g = current.f + dist(current.pos, [i, j])
            h = dist(end, [i, j])
            f = g + h

            new_node = Node([i, j], f, current)


            try:
                # Node already exists
                i = nodes_open.index(new_node)
                
                if new_node.f < nodes_open[i].f:
                    nodes_open[i] = new_node 
                    heapq.heapify(nodes_open)
            except ValueError:
                # Node doesn't exist
                heapq.heappush(nodes_open, new_node)
    
    return None

def get_next(matrix, start, end):
    end = search(matrix, start, end)
    
    if end:
        l = [end.pos]

        while end is not None:
            l.append(end.pos)
            end = end.predecessor

        if len(l) < 2:
            return None

        return l[-2]
    else:
        return None


def get_ai_move(game: SnakeGame) -> tuple[int]:
    # A* algorithm
    next = get_next(game.matrix, game.snake[0], game.apple)
    if next:
        return (next[0] - game.snake[0][0], next[1] - game.snake[0][1])
    else:
        # Picks direction if path is not found

        next = game.snake[0]
        for d in SnakeGame.directions:
            if game.is_inbounds((next[0] + d[0], next[1] + d[1])):
                if game.matrix[next[0] + d[0]][next[1] + d[1]] == 0:
                    
                    return d
        
        print("test")
        return (0 , -1)

if __name__ == "__main__":

    m = [[0 for _ in range(8)] for __ in range(10)]

    for j in range(1, 8):
        m[4][j] = 1

    




