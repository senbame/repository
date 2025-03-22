import pygame
import random
import time
pygame.init()

# Настройки экрана
WIDTH, HEIGHT, CELL = 600, 400, 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
WIDTH_OF_FIELD , HEIGHT_OF_FIELD = 500 , 300
#Цвета
WHITE, GREEN, RED, BLACK , DARK_GREEN = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0) ,(1, 50, 32)
#Картинки
bg = pygame.image.load(r"lab8\elements_of_snake\bg.jpg")
bg_changed = pygame.transform.scale(bg , (500,300))

gameover = pygame.image.load(r"lab8\elements_of_snake\gameover.jpg")
#Переменные игры
snake = [(WIDTH_OF_FIELD // 2, HEIGHT_OF_FIELD // 2)]
direction = (CELL, 0)
food = (random.randrange(50, WIDTH_OF_FIELD+50, CELL), random.randrange(50, HEIGHT_OF_FIELD+50, CELL))
score, level, speed = 0, 1, 10

font = pygame.font.Font(r"lab8\elements_of_racing\fontik.ttf", 24)
game_over = pygame.font.Font(r"lab8\elements_of_racing\fontik.ttf", 46)
first_game_over = pygame.font.Font(r"lab8\elements_of_snake\Serati.ttf" , 46)                             
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(DARK_GREEN)
    screen.blit(bg_changed,(50,50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, CELL):
        direction = (0, -CELL)
    if keys[pygame.K_DOWN] and direction != (0, -CELL):
        direction = (0, CELL)
    if keys[pygame.K_LEFT] and direction != (CELL, 0):
        direction = (-CELL, 0)
    if keys[pygame.K_RIGHT] and direction != (-CELL, 0):
        direction = (CELL, 0)
    
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    if new_head in snake or not (50 <= new_head[0] < WIDTH_OF_FIELD+50 and 50 <= new_head[1] < HEIGHT_OF_FIELD+50):
        screen.blit(first_game_over.render("Game Over :(",True , BLACK),(170,150))
        pygame.display.flip()
        time.sleep(2)
        screen.blit(gameover, (-950,-400))
        screen.blit(game_over.render(f"Your Final Score: {score}", True, BLACK), (10, 10))
        screen.blit(game_over.render(f"Your Final Level: {level}", True, BLACK), (10, 60))
        pygame.display.flip()
        time.sleep(3)
        break
    
    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        food = (random.randrange(50, WIDTH_OF_FIELD+50, CELL), random.randrange(50, HEIGHT_OF_FIELD+50, CELL))
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()
    
    for x,y in snake:
        pygame.draw.rect(screen, GREEN, (x,y, CELL, CELL))
    x , y = food
    pygame.draw.rect(screen, RED, (x,y, CELL, CELL))
    
    screen.blit(font.render(f"Score: {score}", True, BLACK), (300, 1))
    screen.blit(font.render(f"Level: {level}", True, BLACK), (200, 1))
    
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
