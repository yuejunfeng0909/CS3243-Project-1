class Piece:
    pieces = ["King", "Rook", "Bishop", "Queen", "Knight", "Obstacle"]

    def __init__(self, pieceType) -> None:
        self.type = pieceType


class Board:

    def __init__(self, x: int, y: int) -> None:
        self.board_size_x = x
        self.board_size_y = y
        self.enemy_type = [[0] * y] * x
        self.threatened = [[0] * y] * x # Threatened position is 1
        self.blocked = [[0] * y] * x
        self.cost = [[1] * y] * x

    def isValidMovePosition(self, x, y):
        # Check out of range
        if (0 > x or x >= self.board_size_x) and (0 > y or y >= self.board_size_y):
            return False
        
        # Check Threatened
        if self.threatened[x][y] == 1 or self.blocked[x][y] == 1:
            return False

        return True


class State:

    def __init__(self, board:Board, player_type, player_x: int, player_y: int) -> None:
        self.board = board
        self.player_type = player_type
        self.player_x = player_x
        self.player_y = player_y

    def __eq__(self, __o: object) -> bool:
        return self.player_x == __o.player_x and self.player_y == __o.player_y

    # def available_moves(self):
    #     moves = []
    #     if self.player_type == "King":
    #         # around
    #         for x in range(-1, 2):
    #             for y in range(-1, 2):
    #                 if x == y == 0 or self.board.isValidMovePosition(self.player_x + x, self.player_y + y) == False:
    #                     continue
    #                 moves.append([self.player_x + x, self.player_y + y])
                    
    #     elif self.player_type == "Rook":
    #         # horizontal and verticle
    #         for x_offset in range(0, self.board.board_size_x):
    #             new_x = self.player_x + x_offset
    #             new_y = self.player_y
    #             if self.board.blocked[new_x][new_y] == 1:
    #                 break
    #             if self.board.isValidMovePosition(new_x, new_y) == False:
    #                 continue
    #             moves.append([new_x, new_y])
            
    #         for x_offset in range(0, self.board.board_size_x):
    #             new_x = self.player_x - x_offset
    #             new_y = self.player_y
    #             if self.board.blocked[new_x][new_y] == 1:
    #                 break
    #             if self.board.isValidMovePosition(new_x, new_y) == False:
    #                 continue
    #             moves.append([new_x, new_y])

    #     elif self.player_type == "Bishop":
    #         # diagnals
    #         max_steps = min(self.board.board_size_x, self.board.board_size_y)

    #         for x_sign in [-1, 1]:
    #             for y_sign in [-1, 1]:
    #                 for step in range(1, max_steps):
    #                     new_x = self.player_x + x_sign * step
    #                     new_y = self.player_y + y_sign * step
    #                     if self.board.blocked[new_x][new_y] == 1:
    #                         break
    #                     if self.board.isValidMovePosition(new_x, new_y) == False:
    #                         continue
    #                     moves.append([new_x, new_y])

    #     elif self.player_type == "Queen":
    #         # horizontal and verticle
    #         for x_offset in range(0, self.board.board_size_x):
    #             new_x = self.player_x + x_offset
    #             new_y = self.player_y
    #             if self.board.blocked[new_x][new_y] == 1:
    #                 break
    #             if self.board.isValidMovePosition(new_x, new_y) == False:
    #                 continue
    #             moves.append([new_x, new_y])
            
    #         for x_offset in range(0, self.board.board_size_x):
    #             new_x = self.player_x - x_offset
    #             new_y = self.player_y
    #             if self.board.blocked[new_x][new_y] == 1:
    #                 break
    #             if self.board.isValidMovePosition(new_x, new_y) == False:
    #                 continue
    #             moves.append([new_x, new_y])

    #         # do the same for y
    #         for y_offset in range(0, self.board.board_size_y):
    #             new_x = self.player_x
    #             new_y = self.player_y + y_offset
    #             if self.board.blocked[new_x][new_y] == 1:
    #                 break
    #             if self.board.isValidMovePosition(new_x, new_y) == False:
    #                 continue
    #             moves.append([new_x, new_y])
            
    #         for y_offset in range(0, self.board.board_size_y):
    #             new_x = self.player_x
    #             new_y = self.player_y - y_offset
    #             if self.board.blocked[new_x][new_y] == 1:
    #                 break
    #             if self.board.isValidMovePosition(new_x, new_y) == False:
    #                 continue
    #             moves.append([new_x, new_y])
            
    #         # diagnals
    #         max_steps = min(self.board.board_size_x, self.board.board_size_y)

    #         for x_sign in [-1, 1]:
    #             for y_sign in [-1, 1]:
    #                 for step in range(1, max_steps):
    #                     new_x = self.player_x + x_sign * step
    #                     new_y = self.player_y + y_sign * step
    #                     if self.board.blocked[new_x][new_y] == 1:
    #                         break
    #                     if self.board.isValidMovePosition(new_x, new_y) == False:
    #                         continue
    #                     moves.append([new_x, new_y])
        
    #     elif self.player_type == "Knight":
    #         for x_sign in [-1, 1]:
    #             for y_sign in [-1, 1]:
    #                 new_x = self.player_x + x_sign * 1
    #                 new_y = self.player_y + y_sign * 2
    #                 if self.board.isValidMovePosition(new_x, new_y):
    #                     moves.append([new_x, new_y])
                    
    #                 new_x = self.player_x + x_sign * 2
    #                 new_y = self.player_y + y_sign * 1
    #                 if self.board.isValidMovePosition(new_x, new_y):
    #                     moves.append([new_x, new_y])
        
    #     return moves

def letterToX(character):
    return ord(character) - ord('a')