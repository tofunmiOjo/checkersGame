import pygame
from .constants import BROWN, WHITE, CHOCO, BOXSIZE
from checkers.gameboard import Gameboard

class GameLogic:
    def __init__(self, window):
        # Initialize the game logic
        self.initialize()
        self.window = window
    
    def update(self):
        # Update the game display
        self.gameBoard.drawBoard(self.window)
        self.drawLegalMoves(self.valid_moves)
        pygame.display.update()

    def initialize(self):
        # Initialize the game logic variables
        self.selectedPiece = None  # Currently selected game piece
        self.gameBoard = Gameboard()  # Game board
        self.turn = BROWN  # Current player's turn
        self.valid_moves = {}  # Valid moves for the selected game piece

    def move(self, row, column):
        # Move the selected piece to the specified row and column
        piece = self.gameBoard.getPiece(row, column)
        if self.selectedPiece and piece == 0 and (row, column) in self.valid_moves:
            # If there is a selected piece, the target position is empty, and it's a valid move
            self.gameBoard.movePiece(self.selectedPiece, row, column)  # Move the piece
            skipped = self.valid_moves[(row, column)]  # Get any skipped piece
            if skipped:
                self.gameBoard.delete(skipped)  # Remove the skipped piece from the board
            self.switchTurn()  # Switch to the next player's turn
        else:
            return False

        return True

    def drawLegalMoves(self, moveSet):
        # Draw circles on the legal move positions
        for move in moveSet:
            row, column = move
            pygame.draw.circle(self.window, CHOCO, (column * BOXSIZE + BOXSIZE//2, row * BOXSIZE + BOXSIZE//2), 15)

    def getWinner(self):
        # Get the getWinner of the game
        return self.gameBoard.getWinner()

    def reset(self):
        # Reset the game logic to the initial state
        self.initialize()

    def choose(self, row, column):
        # Handle the selection of a game piece
        if self.selectedPiece:
            result = self.move(row, column)  # Try to move the selected piece
            if not result:
                self.selectedPiece = None
                self.choose(row, column)  # Retry selection if move is invalid
        
        piece = self.gameBoard.getPiece(row, column)
        if piece != 0 and piece.color == self.turn:
            # Select a game piece if it belongs to the current player
            self.selectedPiece = piece
            self.valid_moves = self.gameBoard.getLegalMoves(piece)  # Get valid moves for the selected piece
            return True
            
        return False

    def switchTurn(self):
        # Switch to the next player's turn
        self.valid_moves = {}  # Reset valid moves
        if self.turn == BROWN:
            self.turn = WHITE
        else:
            self.turn = BROWN

    def aiMove(self, gameBoard):
        # Make a move for the AI player
        self.gameBoard = gameBoard  # Update the game board
        self.switchTurn()  # Switch to the next player's turn

    def getBoard(self):
        # Get the current game board
        return self.gameBoard
