# Helper functions to aid in your implementation. Can edit/remove
import copy
from Chess import parser, XYtoPos
# import numpy as np

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
        nodesExplored+=1
        if not initialRun:
            # print("Frontier", frontier)
            currentPath:list = frontier.pop(0)
            currentNode = currentPath[-1][1]
        else:
            currentPath = []
            initialRun = False
            currentNode = (initState.player_x, initState.player_y)

        initState.setPlayerPiece(initState.player_piece.type, currentNode[0], currentNode[1])

        # goal check
        if initState.goalCheck():
            for i in range(len(currentPath)):
                currentPath[i] = [XYtoPos(currentPath[i][0]), XYtoPos(currentPath[i][1])]
            return currentPath, nodesExplored

        newDests = initState.possibleNewDestination(exploredNodes)
        for newDest in newDests:            
            exploredNodes.append(newDest)
            if len(currentPath) == 0:
                newPath = [[currentNode, newDest]]
            else:
                newPath:list = copy.copy(currentPath)
                newPath.append([currentNode, newDest])
            frontier.insert(0, newPath)
    return [], 0


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_DFS():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored = search() #For reference
    return moves, nodesExplored #Format to be returned
    

# print(run_DFS())