from .constants import BROWN, WHITE, BOXSIZE, MAROON, CROWN
import pygame

class GamePiece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.getPosition()

    def getPosition(self):
        self.x = BOXSIZE * self.column + BOXSIZE // 2
        self.y = BOXSIZE * self.row + BOXSIZE // 2

    def setKing(self):
        self.king = True
    
    def drawPiece(self, window):
        radius = BOXSIZE//2 - self.PADDING
        pygame.draw.circle(window, MAROON, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)

        #DRAW CROWN IN THE MIDDLE OF KING PEICE
        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height() // 2))
       
    def movePiece(self, row, column):
        self.row = row
        self.column = column
        
        #recalc position after moving peice 
        self.getPosition()