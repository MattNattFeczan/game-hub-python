import pygame
import sys
from tic_tac_toe_10x10_bot import najlepszy_ruch

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BLUE = (70, 130, 180)
ORANGE = (255, 165, 0)

ROWS = 10
COLS = 10

def draw_grid(screen, width, height, square_size):
    for i in range(COLS+1):
        pygame.draw.line(screen, BLACK, [i * square_size, 0], [i * square_size, height], 5)

    for i in range(ROWS+1):
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
    col = int(x/square_size)
    row = int(y/square_size)

    if row >= ROWS or col >= COLS:
        return False

    if(board[row][col]):
        return False
    board[row][col] = current_player
    return True
def is_win_possible(board, gracz):

    oponent = 2 if gracz == 1 else 1

    #poziom
    for r in range(ROWS):
        for c in range(COLS - 4):
            block = False
            for k in range(5):
                if board[r][c+k] == oponent:
                    block = True
                    break
            if not block: return True

    #pion
    for r in range(ROWS - 4):
        for c in range(COLS):
            block = False
            for k in range(5):
                if board[r+k][c] == oponent:
                    block = True
                    break
            if not block: return True

    #skos \
    for r in range(ROWS - 4):
        for c in range(COLS - 4):
            block = False
            for k in range(5):
                if board[r+k][c+k] == oponent:
                    block = True
                    break
            if not block: return True

    #skos /
    for r in range(ROWS - 4):
        for c in range(4, COLS):
            block = False
            for k in range(5):
                if board[r+k][c-k] == oponent:
                    block = True
                    break
            if not block: return True

    return False


def check_draw(board):

    empty = False
    for r in range(ROWS):
        if 0 in board[r]:
            empty = True
            break

    if not empty:
        return True 

    player1 = is_win_possible(board, 1)
    bot2 = is_win_possible(board, 2)

    if not player1 and not bot2:
        return True

    return False

def end_game(board):
    for row in range(10):
        for col in range(10):
            player = board[row][col]
            if player == 0:
                continue

            if col + 4 < 10:
                if (board[row][col + 1] == player and
                        board[row][col + 2] == player and
                        board[row][col + 3] == player and
                        board[row][col + 4] == player):
                    return player

            if row + 4 < 10:
                if (board[row + 1][col] == player and
                        board[row + 2][col] == player and
                        board[row + 3][col] == player and
                        board[row + 4][col] == player):
                    return player

            if row + 4 < 10 and col + 4 < 10:
                if (board[row + 1][col + 1] == player and
                        board[row + 2][col + 2] == player and
                        board[row + 3][col + 3] == player and
                        board[row + 4][col + 4] == player):
                    return player

            if row + 4 < 10 and col - 4 >= 0:
                if (board[row + 1][col - 1] == player and
                        board[row + 2][col - 2] == player and
                        board[row + 3][col - 3] == player and
                        board[row + 4][col - 4] == player):
                    return player
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
    error_timer = 0

    # set the font
    font = pygame.font.SysFont(None, 40)
    big_font = pygame.font.SysFont(None, 60)

    # button presetes
    btn_again_rect = pygame.Rect(w//4, h//2, w//2, 50)
    btn_menu_rect = pygame.Rect(w//4, h//2 + 70, w//2, 50)

    while running:

        screen.fill(WHITE)
        draw_grid(screen, w, h, square_size)
        draw_figures(screen, board, square_size)

        if error_message != "" and winner == 0:
            current_time = pygame.time.get_ticks()
            time_passed = current_time - error_timer

            czas_widocznosci = 2000
            czas_zanikania = 1000
            calkowity_czas = czas_widocznosci + czas_zanikania

            if time_passed < calkowity_czas:
                if time_passed < czas_widocznosci:
                    alpha = 255
                else:
                    czas_w_zanikaniu = time_passed - czas_widocznosci
                    procent_zaniku = czas_w_zanikaniu / czas_zanikania
                    alpha = int(255 * (1 - procent_zaniku))

                error_surface = pygame.Surface((w, h), pygame.SRCALPHA)

                text_surface = font.render(error_message, True, RED)
                text_rect = text_surface.get_rect(center=(w // 2, h // 2))
                bg_rect = text_rect.inflate(20, 20)

                pygame.draw.rect(error_surface, (*BLACK, alpha), bg_rect)
                pygame.draw.rect(error_surface, (*RED, alpha), bg_rect, 3)

                text_surface.set_alpha(alpha)
                error_surface.blit(text_surface, text_rect)

                screen.blit(error_surface, (0, 0))
            else:
                error_message = ""

        winner = end_game(board);

        if winner == 0 and check_draw(board):
            winner = 3

        if winner:
            overlay = pygame.Surface((w, h))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0,0))
            announcement = ""
            if(winner == 1):
                announcement = "Congratulations! You won!"
                text_color = GREEN
            elif(winner == 2):
                announcement = "Sorry, You have lost."
                text_color = YELLOW
            elif winner == 3:
                announcement = "It's a draw!"
                text_color = ORANGE

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

        if current_player == 2 and not winner:
            pygame.event.pump()
            ruch = najlepszy_ruch(board)
            if ruch:
                r, k = ruch
                make_move(k * square_size + 1, r * square_size + 1, board, square_size, current_player)
                current_player = 1
                error_message = ""
            continue

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
                    if current_player == 1:
                        if make_move(x, y, board, square_size, current_player):
                            error_message = ""
                            current_player = 2
                        else:
                            error_message = "Niepoprawny ruch! Pole zajęte."
                            error_timer = pygame.time.get_ticks()
    return


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Tic Tac Toe 10x10")
    launch_tictactoe(screen)
    pygame.quit()
    sys.exit()
