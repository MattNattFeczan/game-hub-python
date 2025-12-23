import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BLUE = (70, 130, 180)

ROWS = 10
COLS = 10

def draw_grid(screen, width, height, square_size):
    for i in range(COLS):
        pygame.draw.line(screen, BLACK, [i * square_size, 0], [i * square_size, height], 5)

    for i in range(ROWS):
        pygame.draw.line(screen, BLACK, [0, i * square_size], [width, i * square_size], 5)

def draw_figures(screen, board, square_size):

    COLOR_P1 = GREEN 
    COLOR_P2 = YELLOW 
    LINE_WIDTH = 10 
    OFFSET = square_size // 4 
    RADIUS = square_size // 4  

    rows = len(board)
    cols = len(board[0])

    for row in range(rows):
        for col in range(cols):
            
            # if player 1 is inside
            if board[row][col] == 1:
                # calculate the middle of the cross
                start_x = col * square_size + OFFSET
                start_y = row * square_size + OFFSET
                end_x = col * square_size + square_size - OFFSET
                end_y = row * square_size + square_size - OFFSET

                pygame.draw.line(screen, COLOR_P1, (start_x, start_y), (end_x, end_y), LINE_WIDTH)
                pygame.draw.line(screen, COLOR_P1, (start_x, end_y), (end_x, start_y), LINE_WIDTH)

            # if player 2 is inside
            elif board[row][col] == 2:
                center_x = int(col * square_size + square_size // 2)
                center_y = int(row * square_size + square_size // 2)

                pygame.draw.circle(screen, COLOR_P2, (center_x, center_y), RADIUS, LINE_WIDTH)


def make_move(x, y, board, square_size, current_player):
    col = int(y/square_size)
    row = int(x/square_size)

    if row >= ROWS or col >= COLS:
        return False

    if(board[col][row]):
        return False
    board[col][row] = current_player
    return True

def end_game(board):
    for row in range(ROWS):
        for col in range(COLS):
            if (col >= 4 and board[col][row] 
                and board[col][row] == board[col-1][row] == board[col-2][row] == board[col-3][row] == board[col-4][row]):
                return board[col][row]
            if (row >= 4 and board[col][row] 
                and board[col][row] == board[col][row-1] == board[col][row-2] == board[col][row-3] == board[col][row-4]):
                return board[col][row]
            if (row >= 4 and col >= 4 and board[col][row] 
                and board[col][row] == board[col-1][row-1] == board[col-2][row-2] == board[col-3][row-3] == board[col-4][row-4]):
                return board[col][row]
            if (row + 4 <= ROWS and col >= 4 and board[col][row]
                and board[col][row] == board[col-1][row+1] == board[col-2][row+2] == board[col-3][row+3] == board[col-4][row+4]):
                return board[col][row]

    return 0

def launch_tictactoe(screen):
    # getting the size of a screen
    w, h = screen.get_size()
    square_size = w // COLS
    
    # init the start values
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    running = True
    current_player = 1
    winner = 0
    error_message = ""

    # set the font
    font = pygame.font.SysFont(None, 40)
    big_font = pygame.font.SysFont(None, 60)

    # button presetes
    btn_again_rect = pygame.Rect(w//4, h//2, w//2, 50) 
    btn_menu_rect = pygame.Rect(w//4, h//2 + 70, w//2, 50)

    while running:
        winner = end_game(board);
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT" 
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check if we are still playing 
                if winner:
                    if btn_menu_rect.collidepoint((x, y)):
                        return
                    if btn_again_rect.collidepoint((x, y)):
                        board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                        winner = 0
                        current_player = 1
                        error_message = ""
                # if we have ended the game
                else:
                    if make_move(x, y, board, square_size, current_player):
                        error_message = ""
                    else:
                        error_message = "Niepoprawny ruch! Pole zajęte."

        screen.fill(WHITE)
        draw_grid(screen, w, h, square_size)
        draw_figures(screen, board, square_size)

        if error_message != "" and winner == 0:
            text_surface = font.render(error_message, True, RED)
            
            text_rect = text_surface.get_rect(center=(w // 2, h // 2)) 
            bg_rect = text_rect.inflate(20, 20)             
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, RED, bg_rect, 3) 
            screen.blit(text_surface, text_rect) 

        if winner:
            overlay = pygame.Surface((w, h))
            overlay.set_alpha(180) 
            overlay.fill(BLACK)
            screen.blit(overlay, (0,0))
            announcement = ""
            if(winner == 1):
                announcement = "Congratulations! You won!"
                text_color = GREEN
            else:
                announcement = "Sorry, You have lost."
                text_color = YELLOW
            
            # Display announcement
            text_surf = big_font.render(announcement, True, text_color)
            text_rect = text_surf.get_rect(center=(w//2, h//3))
            screen.blit(text_surf, text_rect)

            # Play again button 
            pygame.draw.rect(screen, BLUE, btn_again_rect)
            pygame.draw.rect(screen, WHITE, btn_again_rect, 3)
            msg_again = font.render("Play Again", True, WHITE)
            msg_again_rect = msg_again.get_rect(center=btn_again_rect.center)
            screen.blit(msg_again, msg_again_rect)

            # Menu button
            pygame.draw.rect(screen, DARK_GRAY, btn_menu_rect)
            pygame.draw.rect(screen, WHITE, btn_menu_rect, 3)
            msg_menu = font.render("Back to menu", True, WHITE)
            msg_menu_rect = msg_menu.get_rect(center=btn_menu_rect.center)
            screen.blit(msg_menu, msg_menu_rect)

            
        pygame.display.update()

    return
