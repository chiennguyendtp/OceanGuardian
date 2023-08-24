import random
import pygame
import pgzrun
# The size of the board in tiles
TILESW = 14
TILESH = 10
# The pixel size of the screen
WIDTH = TILESW * 40
HEIGHT = TILESH * 40

TITLE = "Ocean Guardian"
score = 0
cursor = Actor("selected", topleft=(0, 0))

board = []
for row in range(TILESH):
    # Make a list of 10 random tiles
    tiles = [random.randint(1, 11) for _ in range(TILESW)]
    board.append(tiles)


def draw():
    screen.clear()
    for y in range(TILESH):
        for x in range(TILESW):
            tile = board[y][x]
            if tile == 9:  # if it's a trash tile
                trash_image = pygame.image.load("9.png")
                screen.blit(trash_image, (x * 40, y * 40))
            elif tile:
                screen.blit(str(tile), (x * 40, y * 40))
    cursor.draw()


    # Display the score on the screen
    screen.draw.text("Score: %s" % score, bottomleft=(0, HEIGHT), fontsize=60)


def cursor_tile_pos():
    return (int(cursor.x // 40) -1 , int(cursor.y // 40))


def on_key_up(key):
    x, y = cursor_tile_pos()
    if key == keys.LEFT and x > 0:
        cursor.x -= 40
    if key == keys.RIGHT and x < TILESW - 2:
        cursor.x += 40
    if key == keys.UP and y > 0:
        cursor.y -= 40
    if key == keys.DOWN and y < TILESH - 1:
        cursor.y += 40
    if key == keys.SPACE:
        board[y][x], board[y][x + 1] = board[y][x + 1], board[y][x]
    global score


def check_matches():
    global score
    for y in range(TILESH):
        for x in range(TILESW - 2):
            if board[y][x] == 9 and board[y][x + 1] == 9 and board[y][x + 2] == 9:
                # Trash tile matching for plastic bottle
                board[y][x] = None
                board[y][x + 1] = None
                board[y][x + 2] = None
                score += 75
            if board[y][x] == 10 and board[y][x + 1] == 10 and board[y][x + 2] == 10:
                # Trash tile matching for plastic bag
                board[y][x] = None
                board[y][x + 1] = None
                board[y][x + 2] = None
                score += 100
            if board[y][x] == 11 and board[y][x + 1] == 11 and board[y][x + 2] == 11:
                # Trash tile matching for plastic can
                board[y][x] = None
                board[y][x + 1] = None
                board[y][x + 2] = None
                score += 50
            elif (
                board[y][x] is not None
                and board[y][x] == board[y][x + 1] == board[y][x + 2]
            ):
                # Normal matching tiles
                board[y][x] = None
                board[y][x + 1] = None
                board[y][x + 2] = None
                score += 20


# Develop check gap for the game after match 3 tiles
def check_gaps():
    # Work from the bottom up
    for y in range(TILESH - 1, -1, -1):
        for x in range(TILESW):
            if board[y][x] is None:
                drop_tiles(x, y)


# Develop drop the tile function after have gap
def drop_tiles(x, y):
    # Loop backwards through the rows from x,y to the top
    for row in range(y, 0, -1):
        # Copy the tile above down
        board[row][x] = board[row - 1][x]
    # Finally blank the tile at the top
    board[0][x] = None


def add_new_tiles():
    for x in range(TILESW):
        if board[0][x] is None and random.random() < NEW_TILE_PROB:
            board[0][x] = random.randint(1, 9)


score = 0
NEW_TILE_PROB = 0.1  # 10% chance of adding a new tile each time


def every_second():
    check_matches()
    check_gaps()
    add_new_tiles()


clock.schedule_interval(every_second, 0.5)

pgzrun.go()
