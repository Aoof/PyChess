# Game.py
The Game class is responsible for running the chess game. It is initialized with default values for the game window, settings, and board. The Update method is responsible for updating the game window, and the Events method handles user input and events such as mouse clicks and window closing. The run method is the main game loop that continuously updates the game window and handles events.

The findPieceByPos method takes in a position and returns the piece located at that position, if any. The move_piece method handles moving a piece to a new position, including taking a piece if one is located at the new position.


# Board.py
This file contains the `Board` class which is responsible for drawing the chessboard, updating the pieces on the board, keeping track of the current turn, and drawing the taken pieces.

The `Board` class has the following attributes:

- `piece_list`: A 2D list representing the current state of the board. Each element in the list is a string representing a chess piece or "--" if the spot is empty.
- `taken`: A dictionary containing the number of pieces taken by each player. The keys are "white" and "black" and the values are default dictionaries mapping each piece type (e.g. "p" for pawn) to the number of that type of piece taken.
- `pieces`: A list of `Piece` objects representing the pieces on the board.
notation: A 2D list of strings representing the notation for each square on the board.
- `checker`: A 2D numpy array containing 1s and 0s representing the checkerboard pattern for the board.
- `settings`: An object containing the size and theme of the board.
- `selected`: A list containing the indices of the currently selected piece.
- `turn`: A string representing the current turn, either "white" or "black".

The `Board` class has the following methods:

- `__init__(self, settings)`: The constructor for the class which initializes all of the attributes described above.
- `draw_board(self, window)`: Draws the board and pieces on the given window.
- `draw_cell_labels(self, window, row_index, column_index, piece)`: Draws the notation for each square on the board.
- `update_turn(self)`: Changes the current turn to the other player.
- `isValidMove(self, piece, pos)`: Returns whether the given move is a valid move for the given piece.
The `Board` class is used in `Game.py` to draw the board and update the pieces on the board.

# Piece.py
This module contains the Piece class which represents a single chess piece on the board. The Piece class has the following attributes:

- `sprite (pygame.image)`: A pygame loaded image for chess piece sprites.
- `color (string)`: Color of the piece, either `'black'` or `'white'`.
- `type (string)`: Type of the piece, one of `'rook'`, `'knight'`, `'bishop'`, `'queen'`, `'king'`, or `'pawn'`.
- `position (list of int)`: Position of the piece on the board, represented as a 2D array index `[row, column]`.
This class is used in the `Board` class to keep track of all pieces on the board, as well as their positions and attributes.


# Latest updates
General notes per commit
- `TODO Jan 13 16:54` Keep valid moves as it is but instead deny the user from making a move if user was in check. 
- `DONE Jan 13 16:54` Modified Board.py because it's formatted brilliantly and totally won't need a full rewrite.