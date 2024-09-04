import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Initialize variables
score = 0
lives = 3
level = 1
ball_speed = [0, 0]
paddle_speed = 0
game_started = False

# Create the paddle
paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create the ball
ball = pygame.Rect(paddle.centerx - BALL_RADIUS, paddle.top - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Create bricks
bricks = []
for row in range(5):
    for col in range(10):
        brick = pygame.Rect(col * (BRICK_WIDTH + 5) + 30, row * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_started:
                if event.key == pygame.K_SPACE:
                    game_started = True
                    ball_speed = [5, -5]  # Start moving the ball upwards
            if event.key == pygame.K_LEFT:
                paddle_speed = -5
            elif event.key == pygame.K_RIGHT:
                paddle_speed = 5
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                paddle_speed = 0

    # Move the paddle
    paddle.x += paddle_speed
    if paddle.left < 0:
        paddle.left = 0
    elif paddle.right > WIDTH:
        paddle.right = WIDTH

    # Move the ball if the game has started
    if game_started:
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

    # Check for collisions with walls
    if ball.left < 0 or ball.right > WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top < 0:
        ball_speed[1] = -ball_speed[1]
    elif ball.bottom > HEIGHT:
        ball_speed = [0, 0]
        lives -= 1
        if lives == 0:
            game_over_text = pygame.font.Font(None, 50).render("GAME OVER", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()
        else:
            # Reset ball position to paddle center and start moving upward again
            ball.center = paddle.center
            ball_speed = [5, -5]
            game_started = False  # Reset game state

    # Check for collision with paddle
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]

    # Check for collision with bricks
    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] = -ball_speed[1]
            score += 1

    # Draw everything
    pygame.draw.rect(screen, BLACK, paddle)
    pygame.draw.circle(screen, BLACK, ball.center, BALL_RADIUS)

    for brick in bricks:
        pygame.draw.rect(screen, BLACK, brick)

    # Display score and lives
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    lives_text = pygame.font.Font(None, 36).render(f"Lives: {lives}", True, BLACK)
    screen.blit(lives_text, (WIDTH - 120, 10))

    if not game_started:
        start_text = pygame.font.Font(None, 50).render("PRESS SPACE TO START", True, BLACK)
        screen.blit(start_text, (WIDTH // 2 - 250, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)