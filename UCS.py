# Helper functions to aid in your implementation. Can edit/remove
import copy
import heapq as hq
import sys

class Piece:

    movement = {"King": [(1, 1, 1), (1, 0, 1), (1, -1, 1), (0, -1, 1), (-1, -1, 1), (-1, 0, 1), (-1, 1, 1), (0, 1, 1)],
                "Rook": [(1, 0, 0), (0, -1, 0), (-1, 0, 0), (0, 1, 0)],
                "Bishop": [(1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)],
                "Queen": [(1, 0, 0), (0, -1, 0), (-1, 0, 0), (0, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)],
                "Knight": [],
                "Obstacle": [],
                "Empty": [],
                }

    def __init__(self, pieceType: str) -> None:
        self.type = pieceType

    def isEmpty(self) -> bool:
        return self.type == "Empty"

    def possibleMovement(self):
        return self.movement[self.type]

class Board:

    enemyPos = []

    def __init__(self, x: int, y: int) -> None:
        self.board_size_x = x
        self.board_size_y = y

        self.pieces = []
        for i in range(x):
            row = []
            for j in range(y):
                row.append(Piece("Empty"))
            self.pieces.append(row)

        self.threatened = []  # Threatened position is True
        for i in range(x):
            self.threatened.append([False, ] * y)

        self.blocked = []
        for i in range(x):
            self.blocked.append([False, ] * y)

        self.cost = []
        for i in range(x):
            self.cost.append([1, ] * y)
    

    def addEnemyPiece(self, piece: str, x: int, y: int) -> None:
        self.pieces[x][y] = Piece(piece)
        self.blocked[x][y] = True
        self.threatened[x][y] = True
        self.enemyPos.append((x, y))
    
    def addObstaclePiece(self, x: int, y: int) -> None:
        self.pieces[x][y] = Piece("Obstacle")
        self.threatened[x][y] = True
        self.blocked[x][y] = True

    def isWithinBoard(self, x, y) -> bool:
        if (0 > x or x >= self.board_size_x) or (0 > y or y >= self.board_size_y):
            return False
        return True

    def isThreatened(self, x, y) -> bool:
        return self.threatened[x][y] or self.isBlocked(x, y)

    def isBlocked(self, x, y) -> bool:
        return self.isWithinBoard(x, y) == False or self.pieces[x][y].isEmpty() == False
    
    def updateThreatened(self):
        for x, y in self.enemyPos:
            piece: Piece = self.pieces[x][y]
            if piece.type == "Knight":
                for twoSteps in [-2, 2]:
                    for oneStep in [-1, 1]:
                        self.setThreatened(x+twoSteps, y+oneStep)
                        self.setThreatened(x+oneStep, y+twoSteps)
            else:
                transModel = transitionModel(
                    self, x, y, piece.possibleMovement())
                for possibleX, possibleY in transModel.getAllPossibleNewPos():
                    self.setThreatened(possibleX, possibleY)

    def setThreatened(self, x, y) -> None:
        if self.isWithinBoard(x, y) == False:
            return
        self.threatened[x][y] = True


class transitionModel():

    def __init__(self, board: Board, x: int, y: int, piece_movements):
        self.x = x
        self.y = y
        self.board = board
        self.movements = piece_movements

    def moveToDirection(self, x_change: int, y_change: int):
        new_x = self.x + x_change
        new_y = self.y + y_change
        return (new_x, new_y)

    def getAllPossibleMovementToDirection(self, x_change: int, y_change: int, max_steps=0):
        if max_steps == 0:
            max_steps = max(self.board.board_size_x, self.board.board_size_y)
        steps = []
        for i in range(max_steps):
            new_pos = self.moveToDirection((i+1) * x_change, (i+1) * y_change)
            if self.board.isBlocked(new_pos[0], new_pos[1]):
                break
            if self.board.isThreatened(new_pos[0], new_pos[1]):
                continue
            steps.append(new_pos)
        return steps

    def getAllPossibleNewPos(self):
        steps = []
        for movement in self.movements:
            xChange, yChange, maxSteps = movement
            steps.extend(self.getAllPossibleMovementToDirection(
                xChange, yChange, maxSteps))
        return steps


class State:
    goals = []

    def __eq__(self, __o: object) -> bool:
        return self.player_x == __o.player_x and self.player_y == __o.player_y

    def initBoard(self, x: int, y: int) -> Board:
        self.board = Board(x, y)

    def setBoard(self, board: Board) -> None:
        self.board = board

    def setPlayerPiece(self, pieceType, x: int, y: int) -> None:
        self.player_piece = Piece(pieceType)
        self.player_x = x
        self.player_y = y
        self.transModel = transitionModel(
            self.board, x, y, self.player_piece.possibleMovement())

    def addGoal(self, x: int, y: int) -> None:
        self.goals.append((x, y))

    def setGoal(self, goals:list) -> None:
        self.goals = goals
    
    def goalCheck(self):
        return (self.player_x, self.player_y) in self.goals
    
    def manhattanDistanceToClosestGoal(self):
        dist = self.board.board_size_x + self.board.board_size_y
        selectedGoal = None
        for goal in self.goals:
            manhattanDist = abs(self.player_x - goal[0]) + abs(self.player_y - goal[1])
            if manhattanDist < dist:
                dist = manhattanDist
                selectedGoal = goal
        # print("manhat dist from", (self.player_x, self.player_y), "to", selectedGoal, "is", dist)
        return dist

    def possibleNewDestination(self, visited):
        newDestination = []
        for newDest in self.transModel.getAllPossibleNewPos():
            newPos = (newDest[0], newDest[1])
            if (not newPos in visited) and not self.board.isThreatened(newDest[0], newDest[1]):
                newDestination.append(newPos)
        return newDestination


def letterToX(character) -> int:
    return ord(character) - ord('a')


def PosToXY(pos) -> tuple:
    return (letterToX(pos[0]), int(pos[1:]))

def XYtoPos(xy: tuple) -> tuple:
    xCharVal:int = xy[0]+ord('a')
    return (chr(xCharVal), xy[1])


def parser() -> State:
    f = open(sys.argv[1], "r")

    def input():
        line = f.readline().strip("\n")
        return line
    rows = int(input().split(":")[1])
    cols = int(input().split(":")[1])
    game = State()
    game.initBoard(cols, rows)
    input()  # ignore
    posOfObstacles = input().split(":")[1].split(" ")
    for obstacle in posOfObstacles:
        x, y = PosToXY(obstacle)
        game.board.addObstaclePiece(x, y)
    input()

    # cost
    selectedGrid = input()
    while selectedGrid[0] == "[":
        costtogrid = selectedGrid[1:][:-1]  # remove bracket
        costtogrid = costtogrid.split(",")
        x, y = PosToXY(costtogrid[0])
        cost = int(costtogrid[1])
        game.board.cost[x][y] = cost
        selectedGrid = input()

    # enemies
    numOfEachEnemies = selectedGrid.split(":")[1].split(" ")
    numOfEnemies = 0
    for num in numOfEachEnemies:
        numOfEnemies += int(num)
    input()
    for i in range(numOfEnemies):
        enemyType, enemyPos = input()[1:][:-1].split(",")
        enemyX, enemyY = PosToXY(enemyPos)
        game.board.addEnemyPiece(enemyType, enemyX, enemyY)
    game.board.updateThreatened()
    input()
    input()
    playerType, playerPos = input()[1:][:-1].split(",")
    playerX, playerY = PosToXY(playerPos)
    game.setPlayerPiece(playerType, playerX, playerY)
    goals = input().split(":")[1].split(" ")
    for goal in goals:
        x, y = PosToXY(goal)
        game.addGoal(x, y)
    f.close()
    return game

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
            moves = []
            for i in range(len(currentPath) - 1):
                moves.append([XYtoPos(currentPath[i]), XYtoPos(currentPath[i+1])])
            return moves, nodesExplored, currentPathCost
        
        newDests = initState.possibleNewDestination(exploredNodes)
        for newDest in newDests:
            newPath:list = copy.copy(currentPath)
            newPath.append(newDest)
            initState.setPlayerPiece(initState.player_piece.type, newDest[0], newDest[1])
            hq.heappush(frontier, node(newPath, currentPathCost + initState.board.cost[newDest[0]][newDest[1]]))
    return [], 0, 0


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_UCS():
    # You can code in here but you cannot remove this function or change the return type

    moves, nodesExplored, pathCost= search() #For reference
    return moves, nodesExplored, pathCost #Format to be returned
    
# print(run_UCS())