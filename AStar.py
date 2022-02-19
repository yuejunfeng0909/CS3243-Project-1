# Helper functions to aid in your implementation. Can edit/remove
import copy
import heapq as hq
from Chess import parser, XYtoPos
# import numpy as np

class node:
    
    def __init__(self, path: list, cost: int, heuristics: int):
        self.path = path
        self.cost = cost
        self.heuristics = heuristics
    
    def __lt__(self, nxt):
        return self.cost + self.heuristics < nxt.cost + nxt.heuristics

def search():
    initState = parser()
    # threaten = []
    # for i in range(initState.board.board_size_x):
    #     row = []
    #     for j in range(initState.board.board_size_y):
    #         row.append(1 if initState.board.threatened[i][j] else 0)
    #     threaten.append(row)
    # print(np.array(threaten))
    nodesExplored = 0
    exploredNodes = []
    frontier = []
    initialRun = True
    while initialRun or len(frontier) != 0:
        if not initialRun:
            frontiernode:node = hq.heappop(frontier)
            currentPath:list = frontiernode.path
            currentNode = currentPath[-1]
            currentPathCost = frontiernode.cost
        else:
            currentNode = (initState.player_x, initState.player_y)
            currentPath = [currentNode]
            currentPathCost = 0
            initialRun = False
        
        if currentNode in exploredNodes:
            continue

        exploredNodes.append(currentNode)
        nodesExplored+=1

        initState.setPlayerPiece(initState.player_piece.type, currentNode[0], currentNode[1])

        # goal check
        if initState.goalCheck():
            # print(np.array(initState.board.threatened))
            moves = []
            for i in range(len(currentPath) - 1):
                moves.append([XYtoPos(currentPath[i]), XYtoPos(currentPath[i+1])])
            return moves, nodesExplored, currentPathCost
        
        # print(currentPath)
        newDests = initState.possibleNewDestination(exploredNodes)
        for newDest in newDests:
            newPath:list = copy.copy(currentPath)
            newPath.append(newDest)
            initState.setPlayerPiece(initState.player_piece.type, newDest[0], newDest[1])
            heuristics = initState.manhattanDistanceToClosestGoal()
            hq.heappush(frontier, node(newPath, currentPathCost + initState.board.cost[newDest[0]][newDest[1]], heuristics))
    return [], 0, 0


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_AStar():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored, pathCost= search() #For reference
    return moves, nodesExplored, pathCost #Format to be returned
    
# print(run_AStar())