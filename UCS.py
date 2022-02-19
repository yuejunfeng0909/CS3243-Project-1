# Helper functions to aid in your implementation. Can edit/remove
import copy
import heapq as hq
from Chess import parser, XYtoPos
# import numpy as np

class node:
    
    def __init__(self, path: list, cost: int):
        self.path = path
        self.cost = cost
    
    def __lt__(self, nxt):
        return self.cost < nxt.cost

def search():
    initState = parser()
    nodesExplored = 0
    exploredNodes = []
    frontier = []
    initialRun = True
    while initialRun or len(frontier) != 0:
        nodesExplored+=1
        if not initialRun:
            frontiernode:node = hq.heappop(frontier)
            currentPath:list = frontiernode.path
            currentNode = currentPath[-1][1]
            currentPathCost = frontiernode.cost
        else:
            currentPath = []
            currentPathCost = 0
            initialRun = False
            currentNode = (initState.player_x, initState.player_y)

        initState.setPlayerPiece(initState.player_piece.type, currentNode[0], currentNode[1])

        # goal check
        if initState.goalCheck():
            # print(np.array(initState.board.cost))
            for i in range(len(currentPath)):
                currentPath[i] = [XYtoPos(currentPath[i][0]), XYtoPos(currentPath[i][1])]
            return currentPath, nodesExplored, currentPathCost

        newDests = initState.possibleNewDestination(exploredNodes)
        for newDest in newDests:
            exploredNodes.append(newDest)
            if len(currentPath) == 0:
                newPath = [[currentNode, newDest]]
            else:
                newPath:list = copy.copy(currentPath)
                newPath.append([currentNode, newDest])
            hq.heappush(frontier, node(newPath, currentPathCost + initState.board.cost[newDest[0]][newDest[1]]))
    return [], 0


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_UCS():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored, pathCost= search() #For reference
    return moves, nodesExplored, pathCost #Format to be returned
    
# print(run_UCS())