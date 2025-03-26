import pygame
import random
import time
import sys

# Инициализация Pygame
pygame.init()
pygame.font.init()

# FPS
FPS = 60
FramesPerSec = pygame.time.Clock()

# Размеры
width, height = 400, 600
SPEED = 5
SCORE = 0
COIN = 0
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Don't Need for Speed")

# Цвета
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255 , 0)
pink = (254,0 ,254)

# Шрифты
font = pygame.font.Font(r"lab8\elements_of_racing\fontik.ttf", 60)
font_first = pygame.font.Font(r"lab8\elements_of_racing\Serati.ttf", 40) 
font_small = pygame.font.Font(r"lab8\elements_of_racing\fontik.ttf", 20)
game_over = font.render("Game Over", True, black)

# Элементы
mycar = pygame.image.load(r"lab8\elements_of_racing\mycar.png")
enemycar = pygame.image.load(r"lab8\elements_of_racing\othercar.png")

mycar_resized = pygame.transform.scale(mycar, (100, 100))
enemycar_resized = pygame.transform.scale(enemycar, (100, 100))

background = pygame.image.load(r"lab8\elements_of_racing\road.png")
background_changed = pygame.transform.scale(background , (400,600))

coin = pygame.image.load(r"lab8\elements_of_racing\coin.png")
coin_changed = pygame.transform.scale(coin , (50,50))

gameover = pygame.image.load(r"lab8\elements_of_racing\game_over.jpg")
gameover_changed = pygame.transform.scale(gameover,(400,600))
# Классы
class EnemyCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemycar_resized
        self.rect = self.image.get_rect(center=(random.randint(40, width - 40), -100))  # Старт выше экрана
        self.mask = pygame.mask.from_surface(self.image)

    def movement(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > height:
            self.rect.top = -100
            self.rect.center = (random.randint(40, width - 40), -100)
            SCORE += 1

class MyCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mycar_resized
        self.rect = self.image.get_rect(center=(160, 520))  # Начальное положение игрока
        self.mask = pygame.mask.from_surface(self.image)

    def movement(self):
        pressed_k = pygame.key.get_pressed()
        if pressed_k[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_k[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.move_ip(5, 0)
class Coins(pygame.sprite.Sprite):
    def __init__(self , x = None):
        super().__init__()
        if x is None:
            x = random.randint(40,width-40)
        self.image = coin_changed
        self.rect = self.image.get_rect(center= (x , -100))
        self.mask = pygame.mask.from_surface(self.image)

    def movement(self):
        self.rect.move_ip(0, 3)
        if self.rect.top > height:
            self.rect.top = -100
            self.rect.center = (random.randint(40 , width-40),-100)
        
def spawn_coins():
    x = random.randint(40,width - 40)
    random_coins = random.randint(1,3)
    for _ in range(random_coins):
        new_coin = Coins(x)
        group_of_coins.add(new_coin)
        all_sprites.add(new_coin)
        

# Спрайты
me = MyCar()
enemy = EnemyCar()
coins = Coins()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(me)
group_of_coins = pygame.sprite.Group()

enemies.add(enemy)

all_sprites.add(enemy)
all_sprites.add(me)
all_sprites.add(coins)

group_of_coins.add(coins)

# Событие ускорения
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Цикл игры
done = True
while done:
    #Проверям сбор монет
    collided_coin = pygame.sprite.spritecollide(me, group_of_coins, True, pygame.sprite.collide_mask)
    if collided_coin:  
        COIN += len(collided_coin)
    
        spawn_coins()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        if event.type == INC_SPEED:
            if COIN > 0 and COIN % 5 == 0:
                SPEED += 1 

    screen.fill(white)  # Сначала заливаем экран, затем рисуем фон
    screen.blit(background_changed, (0, 0))

    # Отображаем счёт
    scores = font_small.render(str(SCORE), True, red)
    screen.blit(scores, (10, 10))
    #Отображаем счетчик монет
    Coin_counter = font_small.render(str(COIN), True , yellow)
    screen.blit(Coin_counter,(380,10)) 
    # Двигаем машины
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.movement()

    
   
    #Проверяем столкновение
    if COIN == 1:
        coin_stat = font_small.render(f"You have {COIN} coin" , True , black)
    else:
        coin_stat = font_small.render(f"You have {COIN} coins" , True , black)
    score_stat = font_small.render(f"Your score is {SCORE}",True,black)
    if pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask):
        screen.blit(font_first.render("Game Over :(",True ,pink ),(80,250))
        pygame.display.flip()
        time.sleep(2)
        screen.blit(gameover_changed,(0,0))
        screen.blit(game_over, (90,20))
        screen.blit(score_stat,(90,100))
        screen.blit(coin_stat, (90,80))
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramesPerSec.tick(FPS)
