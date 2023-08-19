import pygame
from checkers.constants import WIDTH, HEIGHT, BOXSIZE, BROWN, WHITE, MAINMENU
from checkers.gamepiece import GamePiece
from checkers.gameLogic import GameLogic
from minimax import minimaxAlgo, getMoveList
import random

FRAMES_PER_SEC = 60

# Receive imported constants and set the width and height 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Welcome to our checkers game!')

def useMouse(location):
    x, y = location
    row = int(y // BOXSIZE)
    column = int(x // BOXSIZE)
    return row, column

def hardMode():
    run = True
    clock = pygame.time.Clock()
    gameLogic = GameLogic(WINDOW)
    pygame.display.set_caption('Welcome to our checkers game -> hard mode')


    while run:
        clock.tick(FRAMES_PER_SEC)

        if gameLogic.turn == BROWN:
            v, newBoard = minimaxAlgo(gameLogic.getBoard(), 4, WHITE, gameLogic)
            gameLogic.aiMove(newBoard)

        if gameLogic.getWinner() is not None:
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                row, column = useMouse(location)
                gameLogic.choose(row, column)

        gameLogic.update()

    pygame.time.wait(3000)  # Wait for 3 seconds before quitting
    pygame.quit()

def easyMode():
    run = True
    clock = pygame.time.Clock()
    gameLogic = GameLogic(WINDOW)
    pygame.display.set_caption('Welcome to our checkers game -> easy mode')


    while run:
        clock.tick(FRAMES_PER_SEC)

        if gameLogic.turn == WHITE:
            moves = getMoveList(gameLogic.getBoard(), WHITE, gameLogic)
            if moves:
                move = random.choice(moves)
                gameLogic.aiMove(move)

        gameLogic.update()

        if gameLogic.getWinner() is not None:
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                row, column = useMouse(location)
                gameLogic.choose(row, column)

        gameLogic.update()

    pygame.time.wait(3000)  # Wait for 3 seconds before quitting
    pygame.quit()

def mainMenu():
    pygame.init()
    
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(FRAMES_PER_SEC)
        WINDOW.fill((0, 0, 0))  # Fill the window with black color
        
        # Draw menu options
        font = pygame.font.SysFont('comicsansms', 36)

        intro = font.render("WELCOME TO OUR CHECKERS GAME", True, (255, 255, 255))
        easy_mode = font.render("1. Easy Mode", True, (255, 255, 255))
        start_text = font.render("2. Hard mode", True, (255, 255, 255))
        quit_text = font.render("Quit", True, WHITE)
        WINDOW.blit(MAINMENU, (0,0))
        WINDOW.blit(intro, (WIDTH // 2 - intro.get_width() // 2, HEIGHT // 2 - 200))
        WINDOW.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 50))
        WINDOW.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 200))
        WINDOW.blit(easy_mode, (WIDTH // 2 - easy_mode.get_width() // 2, HEIGHT // 2 + 50))
            
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                if WIDTH // 2 - start_text.get_width() // 2 <= location[0] <= WIDTH // 2 + start_text.get_width() // 2:
                    if HEIGHT // 2 - 50 <= location[1] <= HEIGHT // 2 - 50 + start_text.get_height():
                        hardMode()
                    
                if WIDTH // 2 - easy_mode.get_width() // 2 <= location[0] <= WIDTH // 2 + easy_mode.get_width() // 2:
                    if HEIGHT // 2 + 50 <= location[1] <= HEIGHT // 2 + 50 + easy_mode.get_height():
                        easyMode()
                
                if WIDTH // 2 - quit_text.get_width() // 2 <= location[0] <= WIDTH // 2 + quit_text.get_width() // 2:
                    if HEIGHT // 2 + 200 <= location[1] <= HEIGHT // 2 + 200 + quit_text.get_height():
                        print("Thank you for playing!")
                        run = False
        
    pygame.quit()


mainMenu()

