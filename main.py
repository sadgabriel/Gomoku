import pygame
import board as bd

pygame.init()

# constants
WIDTH, HEGIHT = 720, 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
board = bd.Board()
turn = 1
winner = 0
running = True

while running:
    # event handling phase
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            board = bd.Board()
            winner = 0
            turn = 1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and winner == 0: # left click
            raw_x, raw_y = event.pos
            
            # calculate x, y index
            x = (raw_x - 22) // 45
            y = (raw_y - 22) // 45
            
            if board.put_stone(x, y, turn):
                # stone putted successfully
                
                if board.check_end(x, y, turn):
                    # game end
                    if turn % 2 == 1:
                        winner = 1
                    else:
                        winner = 2
                
                turn += 1
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # testing
            pass
    
    # rendering phase
    screen.fill(WHITE)
    board.render(screen, turn)
    
    if winner:
        font = pygame.font.SysFont(None, 60)
        message = [None, "Black Win!", "White Win!"][winner]
        
        text_surface = font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH/2, HEGIHT/2))
        screen.blit(text_surface, text_rect)
    
    pygame.display.flip()

    # fps control
    clock.tick(60)

pygame.quit()