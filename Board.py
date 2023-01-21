import numpy as np 
import string
import pygame
import collections
import os
from Piece import Piece

FONT = "Albertus"
TAKEN_SIZES = 65

class Board():
    def __init__(self, settings):
        self.piece_list = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]

        self.taken = {
            "black": collections.defaultdict(int),
            "white": collections.defaultdict(int)
        }

        self.inCheck = [False, False] # [whiteInCheck, blackInCheck]
        chars = np.array([i for i in string.ascii_uppercase][:8])
        numbers = np.array([i + 1 for i in range(8)][::-1])
        self.notation = []

        for num in numbers:
            self.notation.append([])
            for char in chars: self.notation[-1].append(char + str(num))

        self.notation = np.array(self.notation)
        self.checker = np.zeros([8, 8], int)
        self.settings = settings
        self.selected = []
        self.turn = "white"

        for y, li in enumerate(self.checker):
            for x, _ in enumerate(li):
                if x % 2 != 0:
                    if y % 2 == 0: self.checker[y, x] = 1
                    else: self.checker[y, x-1] = 1
        self.pieces = [*self.get_pieces(self.piece_list)]
        print(self.pieces)

    def get_pieces(self, notationBoard):
        types = {"r": "rook", "n":"knight", "b":"bishop", "q":"queen", "k":"king", "p":"pawn"}
        for r in range(8):
            for c in range(8):
                piece = notationBoard[r][c]
                if piece != "--":
                    color, type = piece[0], piece[1]
                    color = "white" if color == "w" else "black"
                    type = types[type]
                    sprite_loc = os.path.join(os.path.dirname(__file__), f"assets/{color}_{type}.png")
                    sprite = pygame.image.load(sprite_loc)
                    sprite = pygame.transform.scale(sprite, (self.settings.size, self.settings.size))
                    position = [r, c]
                    yield Piece(sprite, color, type, position)

    def draw_board(self, window):
        # Draw the board cells
        for row_index, row in enumerate(self.checker):
            for column_index, piece in enumerate(row):
                cell_color = self.settings.theme[0] if piece else self.settings.theme[1]
                if [row_index,column_index] == self.selected:
                    cell_color = self.settings.theme[0] - 50 if piece else self.settings.theme[1] + 50
                cell_rect = (column_index * self.settings.size, row_index * self.settings.size, self.settings.size, self.settings.size)
                pygame.draw.rect(window, cell_color, cell_rect)
                self.draw_cell_labels(window, row_index, column_index, piece)
        
        # Draw the turn indicator
        font = pygame.font.SysFont(FONT, 40)
        text = font.render("Turn: " + self.turn, True, (0, 0, 0))
        window.blit(text, (self.settings.width//2 - text.get_width()//2, self.settings.height - text.get_height()))
        
        # Draw taken pieces
        font = pygame.font.SysFont(FONT, 30)
        text = font.render(" ".join([f"{str.upper(x[0])}: {self.taken['white'][x]}" for x in self.taken["white"].keys()]), True, (0, 0, 0))
        window.blit(text, (0, self.settings.height - text.get_height()))

        text = font.render(" ".join([f"{str.upper(x[0])}: {self.taken['black'][x]}" for x in self.taken["black"].keys()]), True, (0, 0, 0))
        window.blit(text, (self.settings.width - text.get_width(), self.settings.height - text.get_height()))
        
        # Draw the pieces
        for piece in self.pieces:
            sprite_pos = (piece.position[1] * self.settings.size + self.settings.size / 2 - piece.sprite.get_height() / 2,
                        piece.position[0] * self.settings.size + self.settings.size / 2 - piece.sprite.get_width() / 2)
            window.blit(piece.sprite, sprite_pos)
        
        # Draw available moves
        sPiece = self.findPieceByPos(self.selected, self.pieces)
        if sPiece: self.draw_moves(window, sPiece)

    def draw_cell_labels(self, window, row_index, column_index, piece):
        label_color = self.settings.theme[1] if piece else self.settings.theme[0] 
        font = pygame.font.SysFont(FONT, 20)
        if row_index == 0:
            label = font.render(self.notation[row_index][column_index][0], True, label_color)
            window.blit(label, (column_index * self.settings.size, row_index * self.settings.size))
        if column_index == 0:
            label = font.render(self.notation[row_index][column_index][1], True, label_color)
            window.blit(label, (column_index * self.settings.size, row_index * self.settings.size + self.settings.size - label.get_height()))

    def update_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def get_moves(self, piece, notationBoard):
        for row_index, row in enumerate(notationBoard):
            for column_index, _ in enumerate(row):
                if self.isValidMove(piece, [row_index, column_index]):
                    yield [row_index, column_index]

    def draw_moves(self, window, piece):
        for row_index, column_index in self.get_moves(piece, self.piece_list):
            r = self.settings.size // 8
            x, y = column_index * self.settings.size, row_index * self.settings.size
            x += self.settings.size // 2
            y += self.settings.size // 2 
            pygame.draw.circle(window, (100, 100, 100), (x, y), r)
    
    def isValidMove(self, piece : Piece, newPosition):
        if newPosition[0] > 8 or newPosition[0] < 0 or newPosition[1] > 8 or newPosition[1] < 0:
            return False

        if self.piece_list[newPosition[0]][newPosition[1]] != "--" and self.piece_list[newPosition[0]][newPosition[1]][0] == piece.color[0]:
            return False

        if piece.type == "pawn":
            if piece.color == "white" and newPosition[0] >= piece.position[0]:
                return False
            if piece.color == "black" and newPosition[0] <= piece.position[0]:
                return False

            if abs(piece.position[1] - newPosition[1]) == 1 and \
               abs(piece.position[0] - newPosition[0]) == 1 and \
               self.piece_list[newPosition[0]][newPosition[1]] != "--":
                return True
            
            if abs(piece.position[0] - newPosition[0]) == 1 and \
               piece.position[1] == newPosition[1] and \
               self.piece_list[newPosition[0]][newPosition[1]] == "--":
                return True

            if self.piece_list[newPosition[0] + (1 if piece.color == "white" else -1)][newPosition[1]] == "--" and \
                piece.position[0] in (1, 6) and newPosition[0] in (3, 4) and \
                abs(piece.position[0] - newPosition[0]) == 2 and \
                piece.position[1] == newPosition[1] and \
                self.piece_list[newPosition[0]][newPosition[1]] == "--":
                return True

            return False
        if piece.type == "knight":
            if abs(newPosition[0] - piece.position[0]) == 2 and \
               abs(newPosition[1] - piece.position[1]) == 1:
                return True
            if abs(newPosition[0] - piece.position[0]) == 1 and \
               abs(newPosition[1] - piece.position[1]) == 2:
                return True
            return False
        if piece.type == "bishop":
            if abs(newPosition[0] - piece.position[0]) != abs(newPosition[1] - piece.position[1]):
                return False
            if self.pathIsBlockedB(piece, newPosition):
                return False
            return True
        if piece.type == "rook":
            if newPosition[0] != piece.position[0] and newPosition[1] != piece.position[1]:
                return False
            if self.pathIsBlockedR(piece,newPosition):
                return False
            return True
        if piece.type == "queen":
            if abs(newPosition[0] - piece.position[0]) == abs(newPosition[1] - piece.position[1]):
                if self.pathIsBlockedB(piece, newPosition):
                    return False
            elif newPosition[0] == piece.position[0] or newPosition[1] == piece.position[1]:
                if self.pathIsBlockedR(piece, newPosition):
                    return False
            else:
                return False
            return True
        if piece.type == "king":
            if abs(newPosition[0] - piece.position[0]) > 1 or abs(newPosition[1] - piece.position[1]) > 1:
                return False
            return True
        return False

    def pathIsBlockedB(self, piece : Piece, dest):
        if abs(dest[0] - piece.position[0]) != abs(dest[1] - piece.position[1]):
            return True
        
        x_dir = 1 if dest[0] > piece.position[0] else -1
        y_dir = 1 if dest[1] > piece.position[1] else -1
        x = piece.position[0] + x_dir
        y = piece.position[1] + y_dir
        while [x, y] != dest:
            if self.piece_list[x][y] != "--":
                return True
            x += x_dir
            y += y_dir

        if self.piece_list[dest[0]][dest[1]][0] != piece.color[0]:
            return False
        return True

    def pathIsBlockedR(self, piece : Piece, dest):
        if piece.position[0] != dest[0] and piece.position[1] != dest[1]:
            return True

        x_dir = 1 if dest[0] > piece.position[0] else -1
        y_dir = 1 if dest[1] > piece.position[1] else -1

        if piece.position[0] == dest[0]:
            y = piece.position[1] + y_dir
            while y != dest[1]:
                if self.piece_list[piece.position[0]][y] != "--":
                    return True
                y += y_dir
        else:
            x = piece.position[0] + x_dir
            while x != dest[0]:
                if self.piece_list[x][piece.position[1]] != "--":
                    return True
                x += x_dir

        if self.piece_list[dest[0]][dest[1]][0] != piece.color[0]:
            return False
        return True


    def findPieceByPos(self, pos, pieces):
        for piece in pieces:
            if piece.position == pos:
                return piece
        return None


    def move_piece(self, piece : Piece, pos):
        if self.isValidMove(piece, pos) and self.turn == piece.color:
            piece_list = self.piece_list.copy()
            piece_list[pos[0]][pos[1]] = piece_list[piece.position[0]][piece.position[1]]
            piece_list[piece.position[0]][piece.position[1]] = "--"
            futureBoardPieces = [*self.get_pieces(piece_list)]
            for futurePiece in futureBoardPieces:
                for futureMove in self.get_moves(futurePiece, piece_list):
                    target = self.findPieceByPos(futureMove, futureBoardPieces)
                    if target and target.color != futurePiece.color and target.type == "king":
                        print(target.color + " threatened by " + futurePiece.color)

            target = self.findPieceByPos(pos, self.pieces)
            if target and target.color != piece.color:
                self.taken[piece.color][target.type] += 1 
                self.pieces.remove(target)

            self.piece_list[pos[0]][pos[1]] = self.piece_list[piece.position[0]][piece.position[1]]
            self.piece_list[piece.position[0]][piece.position[1]] = "--"
            piece.position = pos
            self.update_turn()
