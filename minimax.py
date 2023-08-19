from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)

def minimaxAlgo(location, depth, maxPlayer, gameLogic):
    # Check if the maximum depth is reached or if there is a winner
    if depth == 0 or location.getWinner() is not None:
        return location.evaluate(), location

    moveSet = getMoveList(location, maxPlayer, gameLogic)
    bestMove = None
    if maxPlayer:
        maxEval = float('-inf')
        # Evaluate all possible moves for the maximizing player
        for move in moveSet:
            # Recursively call minimax algorithm for the next depth level
            evaluation = minimaxAlgo(move, depth - 1, False, gameLogic)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                bestMove = move
    else:
        minEval = float('inf')
        # Evaluate all possible moves for the minimizing player
        for move in moveSet:
            # Recursively call minimax algorithm for the next depth level
            evaluation = minimaxAlgo(move, depth - 1, True, gameLogic)[0]
            if evaluation < minEval:
                minEval = evaluation
                bestMove = move

    # Return the best evaluation value and the corresponding best move
    return maxEval if maxPlayer else minEval, bestMove


def performMove(piece, move, board, gameLogic, skip):
    # Create a deep copy of the board to perform the move
    newBoard = deepcopy(board)
    new_piece = newBoard.getPiece(piece.row, piece.column)
    # Move the piece to the new position
    newBoard.movePiece(new_piece, move[0], move[1])
    if skip:
        # If there is a capture move, delete the skipped piece
        newBoard.delete(skip)

    return newBoard


def getMoveList(board, maxPlayer, gameLogic):
    moveSet = []
    jumpMoves = []

    color = WHITE if maxPlayer else RED
    for piece in board.getAllPieces(color):
        # Get legal moves for the current piece
        legalMoves = board.getLegalMoves(piece)
        displayMove(gameLogic, board, piece, legalMoves)
        for move, skip in legalMoves.items():
            # Perform the move and create a new board state
            newBoard = performMove(piece, move, board, gameLogic, skip)
            if skip:  # If there is a capture move, prioritize it
                jumpMoves.append(newBoard)
            else:
                moveSet.append(newBoard)

    # If there are any capturing moves, return them first
    if jumpMoves:
        return jumpMoves
    else:
        return moveSet


def displayMove(gameLogic, board, piece, legalMoves):
    # Draw the game board, highlighted piece, and legal moves
    board.drawBoard(gameLogic.window)
    pygame.draw.circle(gameLogic.window, (0, 255, 0), (piece.x, piece.y), 50, 5)
    gameLogic.drawLegalMoves(legalMoves.keys())
    pygame.display.update()
    # pygame.time.delay(100)
