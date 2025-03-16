#Imports
import pygame
import random 
import time
#FPS
FPS = 60
FramesPerSec = pygame.time.Clock()

#elements that are needed
mycar = pygame.image.load(r"lab8\elements_of_racing\mycar.png")
enemycar = pygame.image.load(r"lab8\elements_of_racing\othercar.png")

mycar_resized  = pygame.transform.scale(mycar , (100,100))
enemycar_resized = pygame.transform.scale(enemycar , (100,100))

#basic colors
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

#classes
class EnemyCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemycar_resized
        self.rect = self.image.get_rect()
#screen showing
width = 400
height = 600
screen = pygame.display.set_mode((width,height))
screen.fill(white)
pygame.display.set_caption("Don't Need for Speed")

#main part
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    pygame.display.flip()
    FramesPerSec.tick(FPS)