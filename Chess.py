import numpy as np
import sys


class Piece:

    pieces = ["King", "Rook", "Bishop", "Queen", "Knight", "Obstacle", "Empty"]

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

    def isWithinBoard(self, x, y) -> bool:
        if (0 > x or x >= self.board_size_x) or (0 > y or y >= self.board_size_y):
            return False
        return True

    def isThreatened(self, x, y) -> bool:
        return self.threatened[x][y] or self.isBlocked(x, y)

    def isBlocked(self, x, y) -> bool:
        return self.isWithinBoard(x, y) == False or self.pieces[x][y].isEmpty() == False


class transitionModel():

    def __init__(self, board: Board, x: int, y: int, piece_movements):
        self.x = x
        self.y = y
        self.board = board
        self.movements = piece_movements

    def moveToDirection(self, x_change: int, y_change: int):
        new_x, new_y = self.x + x_change, self.y + y_change
        if (self.board.isWithinBoard(new_x, new_y)):
            return (new_x, new_y)

    def getAllPossibleMovementToDirection(self, x_change: int, y_change: int, max_steps=0):
        if max_steps == 0:
            max_steps == max(self.board.board_size_x, self.board.board_size_y)
        steps = []
        for i in range(max_steps):
            new_pos = self.moveToDirection((i+1) * x_change, (i+1) * y_change)
            if new_pos == None or self.board.isBlocked(new_pos[0], new_pos[1]):
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

    def __init__(self, x: int, y: int) -> None:
        self.board = Board(x, y)

    def __eq__(self, __o: object) -> bool:
        return self.player_x == __o.player_x and self.player_y == __o.player_y

    def addEnemyPiece(self, piece: str, x: int, y: int) -> None:
        self.board.pieces[x][y] = Piece(piece)
        self.board.blocked[x][y] = True
        # self.board.threatened[x][y] = True

    def updateThreatened(self):
        for x in range(self.board.board_size_x):
            for y in range(self.board.board_size_y):
                piece: Piece = self.board.pieces[x][y]
                if piece.isEmpty() or piece.type == "Obstacle":
                    continue
                if piece.type == "Knight":
                    for twoSteps in [-2, 2]:
                        for oneStep in [-1, 1]:
                            self.setThreatened(x+twoSteps, y+oneStep)
                            self.setThreatened(x+oneStep, y+twoSteps)
                else:
                    transModel = transitionModel(
                        self.board, x, y, piece.possibleMovement())
                    for possibleX, possibleY in transModel.getAllPossibleNewPos():
                        self.setThreatened(possibleX, possibleY)

    def setThreatened(self, x, y) -> None:
        if self.board.isWithinBoard(x, y) == False:
            return
        self.board.threatened[x][y] = True

    def setUserPiece(self, pieceType, x: int, y: int) -> None:
        self.player_piece = Piece(pieceType)
        self.player_x = x
        self.player_y = y
        self.transModel = transitionModel(
            self.board, x, y, self.player_piece.possibleMovement())

    def addGoal(self, x: int, y: int) -> None:
        self.goals.append((x, y))

    def possibleNewStates(self):
        newStates = []
        for movements in transitionModel.getAllPossibleNewPos():
            if self.board.isThreatened(movements[0], movements[1]) == False:
                newStates.append(
                    State(self.board, self.player_piece.type, self.player_x, self.player_y))


def letterToX(character) -> int:
    return ord(character) - ord('a')


def PosToXY(pos):
    return (letterToX(pos[0]), int(pos[1:]))


def parser() -> State:
    f = open(sys.argv[1], "r")

    def input():
        line = f.readline().strip("\n")
        return line
    rows = int(input().split(":")[1])
    cols = int(input().split(":")[1])
    game = State(rows, cols)
    input()  # ignore
    posOfObstacles = input().split(":")[1].split(" ")
    for obstacle in posOfObstacles:
        x, y = PosToXY(obstacle)
        game.addEnemyPiece("Obstacle", x, y)
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
        game.addEnemyPiece(enemyType, enemyX, enemyY)
    game.updateThreatened()
    input()
    input()
    playerType, playerPos = input()[1:][:-1].split(",")
    playerX, playerY = PosToXY(playerPos)
    game.setUserPiece(playerType, playerX, playerY)
    goals = input().split(":")[1].split(" ")
    for goal in goals:
        x, y = PosToXY(goal)
        game.addGoal(x, y)
    f.close()
    return game


initState = parser()
print("Blocked")
print(np.array(initState.board.blocked))
print("Threatened")
print(np.array(initState.board.threatened))
print("cost")
print(np.array(initState.board.cost))
