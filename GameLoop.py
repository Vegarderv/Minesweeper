"""
MineSweeper made by Vegard
"""
import pygame as pg
from GameBoard import GameBoard, ClickBoard

# Game Settings
height = 12
width = 10
number_of_bombs = 15

# initiating Game Board
game_board = GameBoard(number_of_bombs, width, height)
board_clicked = ClickBoard(width, height, game_board)
board_clicked.initiate_board()

# PyGame elements
clock = pg.time.Clock()
running = True
window_width = width * 30 + 1
window_height = height * 30 + 51
window = pg.display.set_mode((window_width, window_height))
LEFT = 1
RIGHT = 3

# Font
pg.font.init()
my_font = pg.font.SysFont('Arial', 30)
my_font_2 = pg.font.SysFont('Arial', 60)

# Colors
magenta = (203, 79, 219)
black = (0, 0, 0)
light_magenta = (216, 142, 225)

def start_screen():
    run = True
    while run:
        clock.tick(60)
        pg.display.flip()

while running:

    # Getting game inputs
    events = pg.event.get()
    mouse = pg.event.poll()
    for event in events:
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:  # Left Click
            pos = pg.mouse.get_pos()
            x_pos = pos[0] // 30
            # Checks if mouse is over game board
            if pos[1] > 50 and not board_clicked.is_finished():
                y_pos = (pos[1] - 50) // 30
                if game_board.get_field(x_pos, y_pos) == -1:
                    running = False
                board_clicked.click_board(x_pos, y_pos)
            else:  # Checking for restart
                if (window_width / 2 - 15) < pos[0] < (window_width / 2 + 15) and 10 < pos[1] < 40:  # that's a restart
                    game_board = GameBoard(number_of_bombs, width, height)
                    board_clicked = ClickBoard(width, height, game_board)
        elif event.type == pg.MOUSEBUTTONUP and event.button == 3 and not board_clicked.is_finished():  # Right click
            pos = pg.mouse.get_pos()
            x_pos = pos[0] // 30
            # Checks if mouse is over game board
            if pos[1] > 50:
                y_pos = (pos[1]-50) // 30
                board_clicked.right_click_board(x_pos, y_pos)
        if event.type == pg.QUIT:  # if x is pressed
            running = False

    window.fill(magenta)

    # Drawing the restart button
    pg.draw.rect(window, light_magenta, (0, 0, window_width, 50))
    pg.draw.rect(window, magenta, (window_width / 2 - 15, 10, 30, 30))
    text = my_font.render("R", False, black)

    # Centering the text
    text_rect = text.get_rect(center=((window_width / 2), 25))
    window.blit(text, text_rect)

    # Drawing Game Board
    for x in range(game_board.get_width()):
        for y in range(game_board.get_height()):
            clicked = board_clicked.is_clicked(x, y)
            if clicked == 1:
                number = game_board.get_field(x, y)
                if number == -1:
                    number = "X"
                elif number == 0:
                    number = ""
                else:
                    number = str(int(number))

                # Drawing the numbers
                pg.draw.rect(window, magenta, (30 * x + 1, 30 * y + 51, 29, 29))
                text = my_font.render(number, False, black)
                # Centering the text
                text_rect = text.get_rect(center=((30 * x + 16), (30 * y + 16 + 51)))
                window.blit(text, text_rect)
            elif not clicked:  # If tile is not clicked
                pg.draw.rect(window, black, (30 * x + 1, 30 * y + 51, 29, 29))
            else:  # If tile is right clicked
                pg.draw.rect(window, light_magenta, (30 * x + 1, 30 * y + 51, 29, 29))

    if board_clicked.is_finished():  # If finished
        text = my_font_2.render("YOU WIN!", False, black)

        # Centering the text
        text_rect = text.get_rect(center=((window_width / 2), window_height / 2))
        window.blit(text, text_rect)
    clock.tick(60)
    pg.display.flip()
