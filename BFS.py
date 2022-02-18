# Helper functions to aid in your implementation. Can edit/remove
from Chess import State, parser, XYtoPos

def search():
    initState = parser()
    board = initState.board
    goals = initState.goals
    moves, nodesExplored = [], 0
    exploredNodes = []
    frontier = []
    initialRun = True
    while initialRun or len(frontier) != 0:
        nodesExplored+=1
        if not initialRun:
            # print("Frontier", frontier)
            currentMove = frontier.pop(0)
            moves.append([XYtoPos(currentMove[0]), XYtoPos(currentMove[1])])
            currentNode = (currentMove[1][0], currentMove[1][1])
        else:
            initialRun = False
            currentNode = (initState.player_x, initState.player_y)
        exploredNodes.append(currentNode)

        currentState = State()
        currentState.setBoard(board)
        currentState.setGoal(goals)
        currentState.setPlayerPiece(initState.player_piece.type, currentNode[0], currentNode[1])

        # goal check
        if currentState.goalCheck():
            break

        newDests = initState.possibleNewDestination()
        for newDest in newDests:
            if newDest in exploredNodes:
                continue
            frontier.append([currentNode, newDest])
    return moves, nodesExplored

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_BFS():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored = search() #For reference
    return moves, nodesExplored #Format to be returned

print(run_BFS())