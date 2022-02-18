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
    currentState = State()
    currentState.setBoard(board)
    currentState.setGoal(goals)
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

        currentState.setPlayerPiece(initState.player_piece.type, currentNode[0], currentNode[1])

        newDests = currentState.possibleNewDestination(exploredNodes)
        for newDest in newDests:

            # goal check
            currentState.setPlayerPiece(initState.player_piece.type, newDest[0], newDest[1])
            if currentState.goalCheck():
                currentPath.append([currentNode, newDest])
                for i in range(len(currentPath)):
                    currentPath[i] = [XYtoPos(currentPath[i][0]), XYtoPos(currentPath[i][1])]
                return currentPath, nodesExplored
            

            exploredNodes.append(newDest)
            if len(currentPath) == 0:
                newPath = [[currentNode, newDest]]
            else:
                newPath:list = copy.deepcopy(currentPath)
                newPath.append([currentNode, newDest])
            frontier.append(newPath)
    return None

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored = search() #For reference
    return moves, nodesExplored #Format to be returned

# print(run_BFS())