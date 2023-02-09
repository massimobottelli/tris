import pygame
import random

HUMAN = "X"
AI = "O"

def initialize():
    global count, running, screen, width, height, cell_width, cell_height, board, values, current_player

    # Initialize constants and variables
    width, height = 500, 500
    cell_width = width // 3
    cell_height = height // 3
    current_player = AI 
    board = [["", "", ""] for i in range(3)]
    values = [[1, 1, 1] for i in range(3)]
    count = 0
    running = True

    # Initialize the game engine
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("TRIS")

    # Draw the game board
    for i in range(1, 3):
        pygame.draw.line(
            screen, (255, 255, 255), (i * cell_width, 0), (i * cell_width, height), 2
        )
        pygame.draw.line(
            screen, (255, 255, 255), (0, i * cell_height), (width, i * cell_height), 2
        )
    pygame.display.update()


def display_symbol(i,j):
    font_size = min(cell_width, cell_height)
    font = pygame.font.Font(None, font_size)
    text = font.render(board[i][j], True, (255, 255, 255))
    text_rect = text.get_rect(
        center=(
            j * cell_width + cell_width // 2,
            i * cell_height + cell_height // 2,
        )
    )
    screen.blit(text, text_rect)


def human_move():
    global current_player, count, running
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False
        # Detect click on board
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            i = mouse_y // cell_height
            j = mouse_x // cell_width

            if board[i][j] == "":
                board[i][j] = current_player
                values[i][j] = 3
                for i in range(3):
                    for j in range(3):
                        if board[i][j] != "":
                            display_symbol(i,j)
                current_player = HUMAN if current_player == AI else AI
                count += 1
                pygame.display.update()


def computer_move():
    global current_player, count

    # calculate winning move
    result = find_winning_move(values, 25)
    if result is not None:
        i = result[0]
        j = result[1]
        print("Winning move: ", str(i), ",", str(j))
    else:
        result = find_winning_move(values, 9)
        if result is not None:
            i = result[0]
            j = result[1]
            print("Blocking move: ", str(i), ",", str(j))
        else:
            # select target position
            i = random.randint(0, 2)
            j = random.randint(0, 2)

    pygame.time.wait(500)

    if board[i][j] == "":
        board[i][j] = current_player
        values[i][j] = 5
        display_symbol(i,j)
        current_player = HUMAN if current_player == AI else AI
        count += 1
        pygame.display.update()


def find_winning_move(values, check):
    row_product = [1] * 3
    col_product = [1] * 3
    diagonal1_product = 1
    diagonal2_product = 1

    for i in range(3):
        for j in range(3):
            row_product[i] *= values[i][j]
            col_product[j] *= values[i][j]
            if i == j:
                diagonal1_product *= values[i][j]
            if i + j == 2:
                diagonal2_product *= values[i][j]

    if check in row_product:
        row = row_product.index(check)
        for col in range(3):
            if values[row][col] == 1:
                return (row, col)
    elif check in col_product:
        col = col_product.index(check)
        for row in range(3):
            if values[row][col] == 1:
                return (row, col)
    elif diagonal1_product == check:
        for i in range(3):
            if values[i][i] == 1:
                return (i, i)
    elif diagonal2_product == check:
        for i in range(3):
            if values[i][2-i] == 1:
                return (i, 2-i)
    else:
        return None

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    return None


def display_winner(current_player):
    player = current_player
    player = HUMAN if player == AI else AI
    font_size = min(cell_width, cell_height) // 2
    font = pygame.font.Font(None, font_size)
    winner = "You win!" if player == HUMAN else "AI wins!"
    display_text(
        "{}".format(winner), font, screen, width // 2, height // 2
    )
    pygame.display.update()
    pygame.time.wait(3000)
    initialize()


def display_tie():
    font_size = min(cell_width, cell_height) // 2
    font = pygame.font.Font(None, font_size)
    display_text("No winner!", font, screen, width // 2, height // 2)
    pygame.display.update()
    pygame.time.wait(3000)
    initialize()


def display_text(text, font, screen, x, y):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x, y))
    screen.fill((0, 0, 0), text_rect)
    screen.blit(text_surface, text_rect)


# Run the game loop
initialize()

while running:

    if current_player == HUMAN:
        human_move()
    else:
        computer_move()

    if check_winner():
        display_winner(current_player)

    if count == 9:
        display_tie()


pygame.quit()
