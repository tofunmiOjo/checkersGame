import pygame
from checkers.constants import WIDTH, HEIGHT, BOXSIZE, BROWN, WHITE, MAINMENU
from checkers.gamepiece import GamePiece
from checkers.gameLogic import GameLogic
from minimax import minimaxAlgo, getMoveList
import random

FRAMES_PER_SEC = 60

# Receive imported constants and set the width and height 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Welcome to our checkers gameLogic!')

def useMouse(location):
    x, y = location
    row = int(y // BOXSIZE)
    column = int(x // BOXSIZE)
    return row, column

#displays options when game has ended 
def showGameOverScreen(winner):
    font = pygame.font.SysFont('comicsansms', 36)
    if winner == BROWN:
        text = font.render("GAME OVER !!", True, WHITE)
        text2 = font.render("Brown player wins!", True, WHITE)
    elif winner == WHITE:
        text = font.render("GAME OVER !!", True, WHITE)
        text2 = font.render("White player wins!", True, WHITE)
    else:
        text = font.render("GAME OVER !!", True, WHITE)
        text2 = font.render("It's a draw!", True, WHITE)

    play_again_text = font.render("Play Again", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    WINDOW.fill((0, 0, 0))
    WINDOW.blit(text, text_rect)
    WINDOW.blit(text2, text2_rect)
    pygame.draw.rect(WINDOW, (0, 0, 255), play_again_rect, border_radius=5)
    pygame.draw.rect(WINDOW, (0, 0, 255), quit_rect, border_radius=5)
    WINDOW.blit(play_again_text, play_again_rect)
    WINDOW.blit(quit_text, quit_rect)
    pygame.display.update()

#gameLoop for advanced mode 
def twoPlayer():
    run = True
    clock = pygame.time.Clock()
    gameLogic = GameLogic(WINDOW)

    while run:
        clock.tick(FRAMES_PER_SEC)

        if gameLogic.getWinner() != None:
            print(gameLogic.getWinner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                row, column = useMouse(location)
                gameLogic.choose(row, column)

        gameLogic.update()
    
    pygame.quit()

#game loop for hard mode 
def hardMode():
    run = True
    clock = pygame.time.Clock()
    gameLogic = GameLogic(WINDOW)
    pygame.display.set_caption('Welcome to our checkers gameLogic -> hard mode')


    while run:
        clock.tick(FRAMES_PER_SEC)

        if gameLogic.turn == WHITE:
            v, newBoard = minimaxAlgo(gameLogic.getBoard(), 4, WHITE, gameLogic)
            gameLogic.aiMove(newBoard)

        if gameLogic.getWinner() != None:
            showGameOverScreen(gameLogic.getWinner()) 
            if playAgain() == True:
                run = playAgain()
                gameLogic.reset()
                mainMenu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                row, column = useMouse(location)
                gameLogic.choose(row, column)

        gameLogic.update()

    pygame.quit()

#game loop for easy mode 
def easyMode():
    run = True
    clock = pygame.time.Clock()
    gameLogic = GameLogic(WINDOW)
    pygame.display.set_caption('Welcome to our checkers gameLogic -> easy mode')


    while run:
        clock.tick(FRAMES_PER_SEC)

        if gameLogic.turn == WHITE:
            moves = getMoveList(gameLogic.getBoard(), WHITE, gameLogic)
            if moves:
                move = random.choice(moves)
                gameLogic.aiMove(move)

        gameLogic.update()

        if gameLogic.getWinner() != None:
            showGameOverScreen(gameLogic.getWinner()) 
            if playAgain() == True:
                run = playAgain()
                gameLogic.reset()
                mainMenu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                row, column = useMouse(location)
                gameLogic.choose(row, column)

        gameLogic.update()

    pygame.quit()

#resart game funtion
def playAgain():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                if WIDTH // 2 - 100 <= location[0] <= WIDTH // 2 + 100:
                    if HEIGHT // 2 + 50 <= location[1] <= HEIGHT // 2 + 100:
                        return True
                    elif HEIGHT // 2 + 100 <= location[1] <= HEIGHT // 2 + 150:
                        return False

#main selection menu
def mainMenu():
    pygame.init()
    
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(FRAMES_PER_SEC)
        WINDOW.fill((0, 0, 0))  # Fill the window with black color
        
        # Draw menu options
        font = pygame.font.SysFont('comicsansms', 36)

        intro = font.render("WELCOME TO OUR CHECKERS GAME", True, WHITE)
        easy_mode = font.render("1. Easy Mode", True, WHITE)
        start_text = font.render("2. Hard mode", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)
        two_player = font.render("3. Multiplayer", True, WHITE)

        WINDOW.blit(MAINMENU, (0,0))
        WINDOW.blit(intro, (WIDTH // 2 - intro.get_width() // 2, HEIGHT // 2 - 200))
        WINDOW.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))
        WINDOW.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 250))
        WINDOW.blit(easy_mode, (WIDTH // 2 - easy_mode.get_width() // 2, HEIGHT // 2 - 50))
        WINDOW.blit(two_player, (WIDTH // 2 - easy_mode.get_width() // 2, HEIGHT // 2 + 150))

            
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

                if WIDTH // 2 - two_player.get_width() // 2 <= location[0] <= WIDTH // 2 + two_player.get_width() // 2:
                    if HEIGHT // 2 + 150 <= location[1] <= HEIGHT // 2 + 150 + two_player.get_height():
                        twoPlayer()
                
                if WIDTH // 2 - quit_text.get_width() // 2 <= location[0] <= WIDTH // 2 + quit_text.get_width() // 2:
                    if HEIGHT // 2 + 250 <= location[1] <= HEIGHT // 2 + 250 + quit_text.get_height():
                        print("Thank you for playing!")
                        run = False
        
    pygame.quit()


mainMenu()
