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

    def __init__(self, pieceType, isPlayer: bool) -> None:
        self.type = pieceType
        self.isPlayer = isPlayer

    def isEmpty(self) -> bool:
        return self.type != "Empty"
    
    def possibleMovement(self):
        return self.movement[self.type]



class Board:

    def __init__(self, x: int, y: int) -> None:
        self.board_size_x = x
        self.board_size_y = y
        self.pieces = [[Piece("Empty", False)] * y] * x
        self.threatened = [[False] * y] * x  # Threatened position is True
        self.blocked = [[False] * y] * x
        self.cost = [[1] * y] * x

    def isWithinBoard(self, x, y) -> bool:
        if (0 > x or x >= self.board_size_x) and (0 > y or y >= self.board_size_y):
            return False
        return True
    
    def isThreatened(self, x, y) -> bool:
        return self.threatened[x][y] or self.isBlocked(x, y)

    def isBlocked(self, x, y) -> bool:
        return self.pieces[x][y].isEmpty()

class transitionModel():

    def __init__(self, board: Board, x: int, y: int, piece_movements):
        self.x = x
        self.y = y
        self.board = board
        self.movements = piece_movements

    def getNewPosition(self, x_change: int, y_change: int):
        return (self.x + x_change, self.y + y_change)

    def moveToDirection(self, x_change: int, y_change: int):
        new_x, new_y = self.getNewPosition(x_change, y_change)
        if (self.board.isWithinBoard(new_x, new_y)):
            x, y = new_x, new_y
            return (x, y)
    
    def getAllPossibleMovementToDirection(self, x_change: int, y_change: int, max_steps = 0):
        if max_steps == 0:
            max_steps == max(self.board.board_size_x, self.board.board_size_y)
        steps = []
        for i in range(max_steps):
            new_pos = self.moveToDirection(x_change, y_change)
            if new_pos == None or self.board.isBlocked(new_pos[0], new_pos[1]):
                break
            if self.board.isThreatened(new_pos[0], new_pos[1]):
                continue
            steps.append(new_pos)
        return steps
    
    def getAllPossibleNewUserPos(self):
        steps = []
        for movement in self.movements:
            for xChange, yChange, maxSteps in movement:
                steps.extend(self.getAllPossibleMovementToDirection(xChange, yChange, maxSteps))


class State:
    def __init__(self, x: int, y: int) -> None:
        self.board = Board(x, y)
    
    # for generating new states
    def __init__(self, presetBoard: Board, playerType, playerX, playerY) -> None:
        self.board = presetBoard

    def __eq__(self, __o: object) -> bool:
        return self.player_x == __o.player_x and self.player_y == __o.player_y

    def addEnemyPiece(self, piece: Piece, x: int, y: int) -> None:
        self.board.pieces[x][y] = piece

    def updateThreatened(self):
        for x in range(self.board.board_size_x):
            for y in range(self.board.board_size_y):
                piece = self.board.pieces[x][y]
                if piece.type == "Empty":
                    continue
                if piece.type == "Knight":
                    for twoSteps in [-2, 2]:
                        for oneStep in [-1, 1]:
                            self.setThreatened(x+twoSteps, y+oneStep)
                            self.setThreatened(x+oneStep, y+twoSteps)
                else:
                    transModel = transitionModel(self.board, x, y, piece.possibleMovement())
                    for possibleX, possibleY in transModel.getAllPossibleNewUserPos:
                        self.setThreatened(possibleX, possibleY)

    def setThreatened(self, x, y) -> None:
        self.board.threatened[x][y] = True
                    

    def setUserPiece(self, pieceType, x: int, y: int) -> None:
        self.player_piece = Piece(pieceType, True)
        self.player_x = x
        self.player_y = y
        self.transModel = transitionModel(self.board, x, y, self.player_piece.possibleMovement())

    def updateThreatened(self, piece: Piece, x: int, y: int) -> None:
        self.addEnemyPiece(piece, x, y)

    def possibleNewStates(self, ):
        newStates = []
        for movements in transitionModel.getAllPossibleNewUserPos():
            if self.board.isThreatened(movements[0], movements[1]) == False:
                newStates.append(State(self.board, self.player_piece.type, self.player_x, self.player_y))
        
        

def letterToX(character):
    return ord(character) - ord('a')
