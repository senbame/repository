import pygame

pygame.init()
screen = pygame.display.set_mode((600,300))
done = True
is_red = True
x  ,y = 25,25
clock = pygame.time.Clock()
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_red = not is_red
        
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y-=3
    if pressed[pygame.K_DOWN]: y+=3
    if pressed[pygame.K_LEFT]: x -= 3
    if pressed[pygame.K_RIGHT]: x += 3

    x = max(25 , min(x , 600 - 25))
    y = max(25 , min(y , 300 - 25))
    screen.fill((255,255,255))
    if is_red: color = (255,0,0)
    else:color = (255,100,0)
    pygame.draw.circle(screen , color , (x,y) , 25)
    pygame.display.flip()
    clock.tick(60)
