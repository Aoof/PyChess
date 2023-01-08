import pygame, numpy as np, sys, os
from Settings import Settings
from Board import Board
from Piece import Piece

WIDTH = 900
HEIGHT = 960
SIZES = 113
THEME_COLOR1 = [232, 235, 239]
THEME_COLOR2 = [125, 135, 150]
pygame.init()

class Game():
    def __init__(self):

        self.cur_win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess by Aoof")
        pygame.display.set_icon(pygame.image.load(os.path.join(os.path.dirname(__file__), "assets/white_king.png")))
        self.settings = Settings(
                SIZES,
                [np.array(THEME_COLOR1), np.array(THEME_COLOR2)],
                (WIDTH, HEIGHT)
            )
        self.board = Board(self.settings)

    def Update(self):
        self.cur_win.fill((255, 255, 255))
        self.board.draw_board(self.cur_win)
        
        pygame.display.update()

    def Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for piece in self.board.pieces:
                    piece_y = piece.position[0] * self.settings.size
                    piece_x = piece.position[1] * self.settings.size
                    if (piece_x <= mouse_x < piece_x + self.settings.size) and \
                       (piece_y <= mouse_y < piece_y + self.settings.size) and \
                       self.board.turn == piece.color:
                        if self.board.selected != piece.position:
                            self.board.selected = piece.position
                        else:
                            self.board.selected = []
                mouse_x = mouse_x // self.settings.size
                mouse_y = mouse_y // self.settings.size
                piece = self.board.findPieceByPos(self.board.selected)
                if piece: self.board.move_piece(piece, [mouse_y, mouse_x])
                
    def run(self):
        self.running = True
        while self.running:
            self.Events()
            self.Update()


if __name__ == "__main__":
    game = Game()
    types = {"r": "rook", "n":"knight", "b":"bishop", "q":"queen", "k":"king", "p":"pawn"}
    for r in range(8):
        for c in range(8):
            piece = game.board.piece_list[r][c]
            if piece != "--":
                color, type = piece[0], piece[1]
                color = "white" if color == "w" else "black"
                type = types[type]
                sprite_loc = os.path.join(os.path.dirname(__file__), f"assets/{color}_{type}.png")
                sprite = pygame.image.load(sprite_loc)
                sprite = pygame.transform.scale(sprite, (game.settings.size, game.settings.size))
                position = [r, c]
                game.board.pieces.append(Piece(sprite, color, type, position))
                print(f"loaded {sprite_loc}")
    game.run()