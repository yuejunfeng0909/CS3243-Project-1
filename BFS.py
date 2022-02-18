# Helper functions to aid in your implementation. Can edit/remove
import copy
from Chess import State, parser, XYtoPos

def search():
    initState = parser()
    board = initState.board
    goals = initState.goals
    nodesExplored = 0
    moves = []
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

        currentState = State()
        currentState.setBoard(board)
        currentState.setGoal(goals)
        currentState.setPlayerPiece(initState.player_piece.type, currentNode[0], currentNode[1])

        # goal check
        if currentState.goalCheck():
            moves = currentPath
            break

        newDests = currentState.possibleNewDestination()
        for newDest in newDests:
            if newDest in exploredNodes:
                continue
            exploredNodes.append(newDest)
            if len(currentPath) == 0:
                newPath = [[currentNode, newDest]]
            else:
                newPath:list = copy.deepcopy(currentPath)
                newPath.append([currentNode, newDest])
            frontier.append(newPath)
    return moves, nodesExplored

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored = search() #For reference
    return moves, nodesExplored #Format to be returned

print(run_BFS())