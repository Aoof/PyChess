import sys
import os
import math

import numpy as np

import pygame
pygame.init()

from Settings import Settings


class ChessGame():
    def __init__(self, size=64):
        """ The Game client side """
        self.settings = Settings(size) # Import settings

        self.window = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) # Use settings to create a window
        pygame.display.set_caption("Chess")

        self.board = np.zeros([8, 8], dtype=Piece)
        self.selected = None
    
    def setup(self):
        self.checker = np.zeros([8, 8], dtype="i2")
        for y, xList in enumerate(self.checker):
            for x, data in enumerate(xList):
                if x % 2 != 0:
                    if y % 2 == 0: self.checker[y, x] = 1
                    else: self.checker[y, x-1] = 1

    def select(self, piece):
        for y in self.board:
            for p in y:
                if p == piece:
                    self.selected = p

    def deselect(self, piece):
        if self.selected == piece:
            self.selected = None

    def validate_movement(self, piece):
        movement = []
        if piece.logic == 0:
            movement = [[1, 0], [0, 1], [1, 1], [-1, -1], [0, -1], [-1, 0], [1, -1], [-1, 1]]
        elif piece.logic == 1:
            for i in range(8):
                movement.append([i, i])
                movement.append([-i, -i])
                movement.append([-i, i])
                movement.append([i, -i])
            for i in range(8):
                movement.append([i, 0])
                movement.append([0, i])
                movement.append([-i, 0])
                movement.append([0, -i])
        elif piece.logic == 2:
            for i in range(8):
                movement.append([i, i])
                movement.append([-i, -i])
                movement.append([-i, i])
                movement.append([i, -i])
        elif piece.logic == 3:
            movement = [[2, 1], [1, 2], [-2, 1], [2, -1], [-1, 2], [1, -2], [-2, -1], [-1, -2]]
        elif piece.logic == 4:
            for i in range(8):
                movement.append([i, 0])
                movement.append([0, i])
                movement.append([-i, 0])
                movement.append([0, -i])
        elif piece.logic == 5:
            if not piece.moved:
                movement.append([0, 2] if piece.color == "white" else [0, -2])
            movement.append([0, 1] if piece.color == "white" else [0, -1])
        
        for i, offsets in enumerate(movement):
            if [piece.x + offsets[0], piece.y + offsets[1]] != [piece.x, piece.y]:
                movement[i] = [piece.x + offsets[0], piece.y + offsets[1]]

                x, y = movement[i]
                if piece.logic == 0:
                    if self.board[y, x].color == piece.color:
                        movement.remove([x, y])
        return movement

    def _update_board(self):
        b = np.zeros([8, 8], dtype=Piece)
        for y in self.board:
            for p in y:
                if p != 0:
                    b[p.y, p.x] = p
        self.board = b

    def _update_screen(self):
        self.window.fill((255, 255, 255))

        for y, xList in enumerate(self.checker):
            for x, data in enumerate(xList):
                if self.board[y, x] != self.selected:
                    pygame.draw.rect(self.window, (232, 235, 239) if data else (125, 135, 150), (x*self.settings.size, y*self.settings.size, self.settings.size, self.settings.size))
                else:
                    pygame.draw.rect(self.window, np.array([232, 235, 239]) - 50 if data else np.array([125, 135, 150]) + 50, (x*self.settings.size, y*self.settings.size, self.settings.size, self.settings.size))
        
        for xList in self.board:
            for piece in xList:
                if piece != 0:
                    piece.draw()
        
        if self.selected:
            for x, y in self.validate_movement(self.selected):
                x = (x * self.settings.size) + self.settings.size//2
                y = (y * self.settings.size) + self.settings.size//2

                pygame.draw.circle(self.window, (173, 216, 230), (x, y), self.settings.size//6)
        
        pygame.display.update()

    def _event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._update_board()
                for y in self.board:
                    for piece in y:
                        if piece != 0:
                            piece._mouse_handler()
        
    def run(self):
        self.running = True
        while self.running:
            self._event_handler()
            self._update_screen()



class Piece():
    def __init__(self):
        """ Represents a chess piece """
        self.image = None
        self.name = ""
        self.color = ""
        self.logic = 0
        self.selected = False
        self.moved = False
        
        self.chessGame = None

        self.x, self.y = 0, 0

    def draw(self):
        self._refresh_details()
        self.chessGame.window.blit(self.image, (self.detailed_x, self.detailed_y))

    def _refresh_details(self):
        self.detailed_x, self.detailed_y = (self.x*self.chessGame.settings.size, self.y*self.chessGame.settings.size)
    
    def _mouse_handler(self):
        """ Returns True if mouse is inside piece sprite and is clicked """
        self._refresh_details()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        first_condition = (mouse_x >= self.detailed_x and mouse_y >= self.detailed_y) # Mouse is inside a huge box starting from the piece's coordinates lines are both positive
        second_condition = (self.detailed_x + self.chessGame.settings.size > mouse_x and self.detailed_y + self.chessGame.settings.size > mouse_y) # Mouse is inside a huge box starting from the piece's coordinates plus the piece size lines are both negative
        
        if first_condition and second_condition:
            self.chessGame.select(self)
        else:
            self.chessGame.deselect(self)


if __name__ == "__main__":
    chessGame = ChessGame(96)

    """ Pieces setup mess """
    
    chess_presets = np.zeros([2, 6], dtype=object)
    names = ["king", "queen", "bishop", "knight", "rook", "pawn"]
    for y, xList in enumerate(chess_presets):
        for x, _ in enumerate(xList):
            if y:
                color = "black"
            else:
                color = "white"
            chess_presets[y, x] = [x, color, names[x], pygame.image.load(os.path.join(os.path.dirname(__file__), "assets\\"+color+"_"+names[x]+".png"))]
        
    
    destribution = np.array([[4], [3], [2, 5], [1, 6], [0, 7]], dtype=object)
    pieces = []
    for i in range(5):
        for x in destribution[i]:
            tmp_piece = Piece()
            tmp_piece.logic, tmp_piece.color, tmp_piece.name, tmp_piece.image = chess_presets[0, i]
            tmp_piece.x = x
            tmp_piece.y = 0 if tmp_piece.color == "white" else 7
            pieces.append(tmp_piece)
            
            tmp_piece = Piece()
            tmp_piece.logic, tmp_piece.color, tmp_piece.name, tmp_piece.image = chess_presets[1, i]
            tmp_piece.x = x
            tmp_piece.y = 0 if tmp_piece.color == "white" else 7
            pieces.append(tmp_piece)

    for i in range(8):
        tmp_piece = Piece()
        tmp_piece.logic, tmp_piece.color, tmp_piece.name, tmp_piece.image = [5, "white", "pawn", pygame.image.load(os.path.join(os.path.dirname(__file__), "assets\\"+"white_pawn.png"))]
        tmp_piece.x = i
        tmp_piece.y = 1
        pieces.append(tmp_piece)
        
        tmp_piece = Piece()
        tmp_piece.logic, tmp_piece.color, tmp_piece.name, tmp_piece.image = [5, "black", "pawn", pygame.image.load(os.path.join(os.path.dirname(__file__), "assets\\"+"black_pawn.png"))]
        tmp_piece.x = i
        tmp_piece.y = 6
        pieces.append(tmp_piece)
    
    for piece in pieces:
        piece.chessGame = chessGame

        resized = pygame.transform.scale(piece.image, (chessGame.settings.size, chessGame.settings.size))
        piece.image = resized

        chessGame.board[piece.y, piece.x] = piece
    
    chessGame.setup()
    chessGame.run()