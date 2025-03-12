import pygame
import time
pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

main_clock = pygame.image.load(r"lab7\clock_images\clock.png")
main_clock = pygame.transform.scale(main_clock , (800,600))

minutes_arrow = pygame.image.load(r"lab7\clock_images\rightarm.png")
seconds_arrow = pygame.image.load(r"lab7\clock_images\leftarm.png")

minutes_arrow = pygame.transform.scale(minutes_arrow , (1000,800))
seconds_arrow = pygame.transform.scale(seconds_arrow,(50,782))
def blitRotateCenter(surf, image, center, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center)
    surf.blit(rotated_image, new_rect)

done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    current_time = time.localtime()
    second_angle = -current_time.tm_sec * 6
    minute_angle = -current_time.tm_min * 6 - current_time.tm_sec * 0.1

    screen.fill((255,255,255))
    screen.blit(main_clock, (0,0))

    blitRotateCenter(screen , minutes_arrow , (400,300) , minute_angle)
    blitRotateCenter(screen , seconds_arrow , (400,300) , second_angle)

    pygame.display.flip()
    clock.tick(30)
pygame.quit()