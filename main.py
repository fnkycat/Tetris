import pygame
import sys
import random

pygame.init()

width = 10
height = 20
block_size = 30

field_width = width * block_size
field_height = height * block_size

field_x = (1200 - field_width) // 2
field_y = (800 - field_height) // 2

screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Tetris")
black = (0, 0, 0)
white = (255, 255, 255)
gray = (50, 50, 50)

clock = pygame.time.Clock()

fall_timer = 0
fall_speed = 500

field = []

for y in range(height):
    field.append([0] * width)

figures = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],   # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],   # O
    [(0, 0), (1, 0), (2, 0), (1, 1)],   # T
    [(1, 0), (2, 0), (0, 1), (1, 1)],   # S
    [(0, 0), (1, 0), (1, 1), (2, 1)],   # Z
    [(0, 0), (0, 1), (1, 1), (2, 1)],   # J
    [(2, 0), (0, 1), (1, 1), (2, 1)]    # L
]

score = 0
lines = 0

figure = random.choice(figures)
next_figure = random.choice(figures)

figure_x = width // 2 - 2
figure_y = 0

def can_move(dx, dy, blocks=None):
    if blocks is None:
        blocks = figure

    for block_x, block_y in blocks:
        new_x = figure_x + block_x + dx
        new_y = figure_y + block_y + dy

        if not (0 <= new_x < width and 0 <= new_y < height):
            return False

        if field[new_y][new_x] != 0:
            return False

    return True

def rotate_figure():
    global figure

    rotated = [(-block_y, block_x) for block_x, block_y in figure]
    min_x = min(x for x, y in rotated)
    min_y = min(y for x, y in rotated)
    rotated = [(x - min_x, y - min_y) for x, y in rotated]

    if can_move(0, 0, rotated):
        figure = rotated

def lock_figure():
    global score

    for block_x, block_y in figure:

        x = figure_x + block_x
        y = figure_y + block_y

        field[y][x] = 1
        score += 1

def clear_line():
    global lines
    y = height - 1

    while y >= 0:
        if all(field[y]):
            del field[y]
            field.insert(0, [0] * width)
            lines += 1
        else:
            y -= 1

def spawn_figure():
    global figure
    global next_figure
    global figure_x
    global figure_y

    figure = next_figure
    next_figure = random.choice(figures)

    figure_x = width // 2 - 2
    figure_y = 0

def game_over():
    for block_x, block_y in figure:

        x = figure_x + block_x
        y = figure_y + block_y

        if field[y][x] != 0:
            return True

    return False

def draw_field():
    for y in range(height):
        for x in range(width):

            pygame.draw.rect(
                screen,
                gray,
                (
                    field_x + x * block_size,
                    field_y + y * block_size,
                    block_size,
                    block_size
                ),
                1
            )

            if field[y][x] != 0:
                pygame.draw.rect(
                    screen,
                    white,
                    (
                        field_x + x * block_size,
                        field_y + y * block_size,
                        block_size,
                        block_size
                    )
                )

                pygame.draw.rect(
                    screen,
                    black,
                    (
                        field_x + x * block_size,
                        field_y + y * block_size,
                        block_size,
                        block_size
                    ),
                    2
                )

def draw_figure():
    for block_x, block_y in figure:

        x = figure_x + block_x
        y = figure_y + block_y

        pygame.draw.rect(
            screen,
            white,
            (
                field_x + x * block_size,
                field_y + y * block_size,
                block_size,
                block_size
            )
        )

        pygame.draw.rect(
            screen,
            black,
            (
                field_x + x * block_size,
                field_y + y * block_size,
                block_size,
                block_size
            ),
            2
        )

def draw_next_figure():

    preview_block_size = 20

    start_x = right_x
    start_y = right_y + 130

    draw_text("next:", start_x, start_y)

    for block_x, block_y in next_figure:

        x = start_x + block_x * preview_block_size
        y = start_y + 40 + block_y * preview_block_size

        pygame.draw.rect(
            screen,
            white,
            (x, y, preview_block_size, preview_block_size)
        )

        pygame.draw.rect(
            screen,
            black,
            (x, y, preview_block_size, preview_block_size),
            2)

state = True

while state:
    dt = clock.tick(60)
    fall_timer += dt

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                if can_move(-1, 0):
                    figure_x -= 1

            if event.key in (pygame.K_RIGHT, pygame.K_d):
                if can_move(1, 0):
                    figure_x += 1

            if event.key in (pygame.K_DOWN, pygame.K_s):
                if can_move(0, 1):
                    figure_y += 1

            if event.key == pygame.K_x:
                rotate_figure()

    if fall_timer >= fall_speed:
        fall_timer = 0

        if can_move(0, 1):
            figure_y += 1
        else:
            lock_figure()
            clear_line()
            spawn_figure()

            if game_over():
                state = False

    font = pygame.font.SysFont('Consolas', 17)

    left_x = field_x - 300
    top_y = field_y

    right_x = field_x + field_width + 80
    right_y = field_y

    def draw_text(text, x, y):
        text_surface = font.render(text, True, white)
        screen.blit(text_surface, (x, y))

    screen.fill(black)

    draw_text("controls:", left_x, top_y)
    draw_text("[a] or [←] - move left", left_x, top_y + 40)
    draw_text("[d] or [→] - move right", left_x, top_y + 80)
    draw_text("[s] or [↓] - move down", left_x, top_y + 120)
    draw_text("[x] - rotate", left_x, top_y + 160)

    draw_text(f"score: {score}", right_x, right_y)
    draw_text(f"lines: {lines}", right_x, right_y + 40)

    draw_next_figure()

    draw_field()
    draw_figure()

    pygame.display.flip()

pygame.quit()