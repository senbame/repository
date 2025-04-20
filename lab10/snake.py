import pygame
import random
import time
import psycopg2
from config import load_config
def create_users_table():
    commands = [
        """ 
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS user_score (
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            score INTEGER NOT NULL,
            level INTEGER NOT NULL,
            speed INTEGER NOT NULL,
            PRIMARY KEY (user_id)
        );
        """
    ]
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при создании таблиц:", error)
def list_of_user():
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users ")
                cur.execute("SELECT * FROM user_score")
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                
    except(psycopg2.DatabaseError,Exception) as error:
        print("Error: ", error)
def existance_of_user(username):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE username = %s" , (username,))
                user = cur.fetchone()
                rows = cur.fetchall()
                if user:
                    return True
                else:
                    return False
    except(psycopg2.DatabaseError,Exception) as error:
        print("Error: ", error)
        return False
def get_user(username):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id,username from users WHERE username = %s" , (username,))
                user = cur.fetchone()
                if user:
                    return user
                else:
                    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
                    user_id = cur.fetchone()[0]
                    return (user_id, username)
    except(psycopg2.DatabaseError , Exception) as error:
        print("Ошибка при получении или создании игрока: ",error)
def get_user_score(user_id):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT score, level, speed FROM user_score WHERE user_id = %s;", (user_id,))
                score = cur.fetchone()
                if score:
                    return score
                else:
                    return (0,1,10) # Начальный счёт, уровень и скорость
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Ошибка при получении счёта: {error}")
        return (0, 1, 10)
def save_score(user_id, score, level, speed):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO user_score (user_id, score, level, speed)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE
                    SET score = EXCLUDED.score, level = EXCLUDED.level, speed = EXCLUDED.speed;
                """, (user_id, score, level, speed))
                print("Текущий счёт сохранён!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Ошибка при сохранении счёта: {error}")
def game(username):
    pygame.init()

    # Настройки экрана
    WIDTH, HEIGHT, CELL = 600, 400, 20
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка")
    WIDTH_OF_FIELD, HEIGHT_OF_FIELD = 500, 300

    # Цвета
    WHITE, GREEN, RED, BLACK, DARK_GREEN = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0), (1, 50, 32)

    # Картинки
    bg = pygame.image.load(r"C:\KBTU\githowto\PP2\lab8\elements_of_snake\bg.jpg")
    bg_changed = pygame.transform.scale(bg, (500, 300))
    head_of_snake = pygame.image.load(r"C:\KBTU\githowto\PP2\lab8\elements_of_snake\2469829.png")
    head_of_snake_changed = pygame.transform.scale(head_of_snake, (20, 20))
    head_of_snake_changed = pygame.transform.rotate(head_of_snake_changed, 90)
    gameover = pygame.image.load(r"C:\KBTU\githowto\PP2\lab8\elements_of_snake\gameover.jpg")

    #Информация про пользователя
    user = get_user(username)
    if not user:
        return
    user_id, _ = user
    score,level,speed = get_user_score(user_id)
    # Переменные игры
    snake = [(WIDTH_OF_FIELD // 2, HEIGHT_OF_FIELD // 2)]
    direction = (CELL, 0)
    food = (random.randrange(50, WIDTH_OF_FIELD + 50, CELL), random.randrange(50, HEIGHT_OF_FIELD + 50, CELL))
    dir_of_head = "RIGHT"
    paused = False

    font = pygame.font.Font(r"C:\KBTU\githowto\PP2\lab8\elements_of_racing\fontik.ttf", 24)
    game_over = pygame.font.Font(r"C:\KBTU\githowto\PP2\lab8\elements_of_racing\fontik.ttf", 46)
    first_game_over = pygame.font.Font(r"C:\KBTU\githowto\PP2\lab8\elements_of_snake\Serati.ttf", 46)
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(DARK_GREEN)
        screen.blit(bg_changed, (50, 50))
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_HOME:
                    save_score(user_id,score,level,speed)

                if event.key == pygame.K_q:
                    save_score(user_id,score,level,speed)
                    running = False
                if event.key == pygame.K_DELETE:
                    save_score(user_id,0,1,10)


        if paused:
            screen.blit(first_game_over.render("Game is Paused", True, BLACK), (150, 150))
            pygame.display.flip()
            continue
        # Управление движением змеи
        
        if keys[pygame.K_w] and direction != (0, CELL):
            direction = (0, -CELL)
            dir_of_head = "UP"
        if keys[pygame.K_s] and direction != (0, -CELL):
            direction = (0, CELL)
            dir_of_head = "DOWN"
        if keys[pygame.K_a] and direction != (CELL, 0):
            direction = (-CELL, 0)
            dir_of_head = "LEFT"
        if keys[pygame.K_d] and direction != (-CELL, 0):
            direction = (CELL, 0)
            dir_of_head = "RIGHT"

        # Новый ход змеи
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Проверка на столкновение
        if new_head in snake or not (50 <= new_head[0] < WIDTH_OF_FIELD + 50 and 50 <= new_head[1] < HEIGHT_OF_FIELD + 50):
            screen.blit(first_game_over.render("Game Over :(", True, BLACK), (170, 150))
            pygame.display.flip()
            time.sleep(2)
            screen.blit(gameover, (-950, -400))
            screen.blit(game_over.render(f"Your Final Score: {score}", True, BLACK), (10, 10))
            screen.blit(game_over.render(f"Your Final Level: {level}", True, BLACK), (10, 60))
            pygame.display.flip()
            time.sleep(1)
            break

        # Поворот головы змеи в зависимости от направления
        if dir_of_head == "UP":
            head_snake = pygame.transform.rotate(head_of_snake_changed, 90)
        elif dir_of_head == "LEFT":
            head_snake = pygame.transform.rotate(head_of_snake_changed, 180)
        elif dir_of_head == "DOWN":
            head_snake = pygame.transform.rotate(head_of_snake_changed, -90)
        elif dir_of_head == "RIGHT":
            head_snake = pygame.transform.rotate(head_of_snake_changed, 0)

        snake.insert(0, new_head)

        # Если змейка съела еду
        if new_head == food:
            score += 1
            food = (random.randrange(50, WIDTH_OF_FIELD + 50, CELL), random.randrange(50, HEIGHT_OF_FIELD + 50, CELL))
            if score % 3 == 0:
                level += 1
                speed += 2
        else:
            snake.pop()

        # Отображение змеи
        for i, (x, y) in enumerate(snake):
            if i == 0:
                screen.blit(head_snake, (x, y))  # Рисуем голову змеи
            else:
                pygame.draw.rect(screen, GREEN, (x, y, CELL, CELL))  # Остальная часть тела — зеленые квадраты

        # Отображение еды
        x, y = food
        pygame.draw.rect(screen, RED, (x, y, CELL, CELL))

        # Вывод счёта и уровня
        screen.blit(font.render(f"Score: {score}", True, BLACK), (300, 1))
        screen.blit(font.render(f"Level: {level}", True, BLACK), (200, 1))

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()

def main():
    create_users_table()
    while True:
        print("\nChoose your option")
        print("1. Play")
        print("2. See Results")
        print("3. Quit")
        choice = int(input("Choose your option: "))
        if choice == 1:
            username = input("Enter a username: ")
            if existance_of_user(username):
                print("\nYou are already in database")
                user_id, _ = get_user(username)
                score, level, speed = get_user_score(user_id)
                print(f"Your score: {score}")
                print(f"Your level: {level}")
                print(f"Your speed: {speed}")
                time.sleep(3)
                game(username)
            else:
                game(username)
        elif choice == 2:
            name = input("Enter the username: ")
            user_id , _ = get_user(name)
            score, level, speed = get_user_score(user_id)
            print(f"Your score: {score}")
            print(f"Your level: {level}")
            print(f"Your speed: {speed}")
            print("Do you wanna reset it? (yes/no)")
            reset = input()
            if reset == "yes":
                user_id,_ = get_user(name)
                save_score(user_id , 0 , 1 , 10)
        elif choice == 3:
            break
if __name__ == '__main__':
    main()
    
            


