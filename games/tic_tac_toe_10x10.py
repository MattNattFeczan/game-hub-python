import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

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


def launch_tictactoe(screen):
    # getting the size of a screen
    w, h = screen.get_size()
    square_size = w // COLS
    
    # init the start values
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    running = True
    current_player = 1
    error_message = ""

    # set the font
    font = pygame.font.SysFont(None, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT" 
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if make_move(x, y, board, square_size, current_player):
                    error_message = ""
                else:
                    error_message = "Niepoprawny ruch! Pole zajęte."
                pass

        screen.fill(WHITE)
        draw_grid(screen, w, h, square_size)
        draw_figures(screen, board, square_size)

        if error_message != "":
            text_surface = font.render(error_message, True, RED)
            
            text_rect = text_surface.get_rect(center=(w // 2, h // 2)) 
            bg_rect = text_rect.inflate(20, 20)             
            pygame.draw.rect(screen, BLACK, bg_rect)
            pygame.draw.rect(screen, RED, bg_rect, 3) 
            screen.blit(text_surface, text_rect) 

        pygame.display.update()

    return
