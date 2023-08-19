import pygame

# Relative import
from .constants import BLACK, ROWS, BROWN, BOXSIZE, COLUMNS, WHITE
from .gamepiece import GamePiece

class Gameboard:

    def __init__(self):
        # Initialize the game board and game statistics
        self.board = []  # 2D list representing the game board
        self.brownLeft = self.whiteLeft = 12  # Number of remaining pieces for each player
        self.brownKings = self.whiteKings = 0  # Number of kings for each player
        self.setBoard()  # Set up the initial game board configuration
    
    def drawBoxes(self, window):
        # Draw the boxes on the game board
        window.fill(BLACK)  # Fill the window with black color
        for row in range(ROWS):
            for column in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(window, BROWN, (row*BOXSIZE, column *BOXSIZE, BOXSIZE, BOXSIZE))

    def evaluate(self):
        # Evaluate the current game state (heuristic evaluation)
        return self.whiteLeft - self.brownLeft + (self.whiteKings * 0.5 - self.brownKings * 0.5)

    def getAllPieces(self, color):
        # Get all the game pieces of the specified color
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def movePiece(self, piece, row, column):
        # Move a game piece to the specified position
        self.board[piece.row][piece.column], self.board[row][column] = self.board[row][column], self.board[piece.row][piece.column]
        piece.movePiece(row, column)  # Update the piece's position

        if row == ROWS - 1 or row == 0:
            # If the piece reaches the last row, promote it to a king
            piece.setKing()
            if piece.color == WHITE:
                self.whiteKings += 1
            else:
                self.brownKings += 1 

    def getPiece(self, row, column):
        # Get the piece at the specified position
        return self.board[row][column]

    def setBoard(self):
        # Set up the initial game board configuration
        for row in range(ROWS):
            self.board.append([])
            for column in range(COLUMNS):
                if column % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(GamePiece(row, column, WHITE))  # Add a white game piece
                    elif row > 4:
                        self.board[row].append(GamePiece(row, column, BROWN))  # Add a brown game piece
                    else:
                        self.board[row].append(0)  # Empty space
                else:
                    self.board[row].append(0)  # Empty space
        
    def drawBoard(self, window):
        # Draw the game board and game pieces on the window
        self.drawBoxes(window)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.drawPiece(window)

    def delete(self, pieces):
        # Delete the specified pieces from the game board
        for piece in pieces:
            self.board[piece.row][piece.column] = 0  # Set the position as empty
            if piece != 0:
                if piece.color == BROWN:
                    self.brownLeft -= 1  # Decrease the count of remaining brown pieces
                else:
                    self.whiteLeft -= 1  # Decrease the count of remaining white pieces
    
    def getWinner(self):
        # Check if there is a winner in the game
        if self.brownLeft <= 0:
            return WHITE  # White player wins
        elif self.whiteLeft <= 0:
            return BROWN  # Brown player wins
        
        return None  # No winner yet
    
    def getLegalMoves(self, piece):
        # Get all the legal moveSet for the specified piece
        moveSet = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row

        if piece.color == BROWN or piece.king:
            moveSet.update(self.traverseLeft(row -1, max(row-3, -1), -1, piece.color, left))
            moveSet.update(self.traverseRight(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moveSet.update(self.traverseLeft(row +1, min(row+3, ROWS), 1, piece.color, left))
            moveSet.update(self.traverseRight(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moveSet

    def traverseLeft(self, startPos, stopPos, step, color, left, jumped=[]):
        # Recursively traverse left to find all legal moveSet
        moveSet = {}
        last = []
        for r in range(startPos, stopPos, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if jumped and not last:
                    break
                elif jumped:
                    moveSet[(r, left)] = last + jumped
                else:
                    moveSet[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moveSet.update(self.traverseLeft(r+step, row, step, color, left-1,jumped=last))
                    moveSet.update(self.traverseRight(r+step, row, step, color, left+1,jumped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moveSet

    def traverseRight(self, startPos, stopPos, step, color, right, jumped=[]):
        # Recursively traverse right to find all legal moveSet
        moveSet = {}
        last = []
        for r in range(startPos, stopPos, step):
            if right >= COLUMNS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if jumped and not last:
                    break
                elif jumped:
                    moveSet[(r,right)] = last + jumped
                else:
                    moveSet[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moveSet.update(self.traverseLeft(r+step, row, step, color, right-1,jumped=last))
                    moveSet.update(self.traverseRight(r+step, row, step, color, right+1,jumped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moveSet
