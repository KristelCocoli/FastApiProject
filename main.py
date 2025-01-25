import pygame
import sys
import random

# Colors
BACKGROUND_COLOR = (30, 30, 30)
PLAYER_COLOR = (0, 255, 128)
BALL_COLOR = (255, 69, 105)
LINE_COLOR = (200, 200, 200)
SCORE_COLOR = (255, 255, 255)

# Initialization
pygame.init()
pygame.font.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 450
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Revamped!")
clock = pygame.time.Clock()
SCORE_FONT = pygame.font.SysFont('arial', 24)

# Player and ball setup
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20

player1 = pygame.Rect(10, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(SCREEN_WIDTH - 20, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect((SCREEN_WIDTH // 2) - (BALL_SIZE // 2), (SCREEN_HEIGHT // 2) - (BALL_SIZE // 2), BALL_SIZE, BALL_SIZE)

ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))
player1_score, player2_score = 0, 0
game_active = False

# Functions
def reset_ball():
    """Reset the ball to the center."""
    global ball_speed_x, ball_speed_y, game_active
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))
    game_active = False

def move_ball():
    """Move the ball and handle collisions."""
    global ball_speed_x, ball_speed_y, player1_score, player2_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Wall collision
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Player collision
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1

    # Scoring
    if ball.left <= 0:
        player2_score += 1
        reset_ball()
    elif ball.right >= SCREEN_WIDTH:
        player1_score += 1
        reset_ball()

def move_players():
    """Move players based on key presses."""
    keys = pygame.key.get_pressed()
    # Player 1 (W, S)
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= 5
    if keys[pygame.K_s] and player1.bottom < SCREEN_HEIGHT:
        player1.y += 5
    # Player 2 (UP, DOWN)
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= 5
    if keys[pygame.K_DOWN] and player2.bottom < SCREEN_HEIGHT:
        player2.y += 5

def draw_elements():
    """Draw all game elements."""
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, PLAYER_COLOR, player1)
    pygame.draw.rect(screen, PLAYER_COLOR, player2)
    pygame.draw.ellipse(screen, BALL_COLOR, ball)
    pygame.draw.aaline(screen, LINE_COLOR, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Draw scores
    p1_score_text = SCORE_FONT.render(str(player1_score), True, SCORE_COLOR)
    p2_score_text = SCORE_FONT.render(str(player2_score), True, SCORE_COLOR)
    screen.blit(p1_score_text, (SCREEN_WIDTH // 4, 10))
    screen.blit(p2_score_text, (SCREEN_WIDTH * 3 // 4, 10))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_active and event.type == pygame.KEYDOWN:
            game_active = True

    if game_active:
        move_ball()
        move_players()

    draw_elements()
    pygame.display.update()
    clock.tick(60)
