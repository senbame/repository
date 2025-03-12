import pygame
import os
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800,600))
bg = pygame.image.load(r"lab7\mp3_images\background.jpg")
bg = pygame.transform.scale(bg, (800,600))

play_button = pygame.image.load(r"lab7\mp3_images\play.png")
play_button = pygame.transform.scale(play_button, (100,100))

pause_button = pygame.image.load(r"lab7\mp3_images\pause.png")
pause_button = pygame.transform.scale(pause_button, (100,100))

next_button = pygame.image.load(r"lab7\mp3_images\next.png")
next_button = pygame.transform.scale(next_button, (100,100))

back_button = pygame.image.load(r"lab7\mp3_images\back.png")
back_button = pygame.transform.scale(back_button, (100,100))

mus = "lab7\songs"
album = [os.path.join(mus, file) for file in os.listdir(mus) if file.endswith(".mp3")]
index = 0
font = pygame.font.Font(r"lab7\mp3_images\tihana.otf", 29)
def load(index):
    pygame.mixer.music.load(album[index])
    trackname = os.path.basename(album[index])
    return trackname.rsplit(".",1)[0]


track = load(index)

done = True
playing = False
paused = True

while done:
    screen.blit(bg, (0,0))
    screen.blit(next_button,(175,50))
    screen.blit(back_button,(25,50))

    text = font.render(f"Now Playing: {track}", True, (0,0,0))
    screen.blit(text, (25,25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    playing = False
                    paused = True
                else:
                    pygame.mixer.music.play()
                    playing = True
                    paused = False
            elif event.key == pygame.K_RIGHT:
                paused = not playing
                index = (index + 1) % len(album)
                track = load(index)
                if not paused:
                    pygame.mixer.music.play()
                    playing = True
            elif event.key == pygame.K_LEFT:
                paused = not playing
                index = (index - 1) % len(album)
                track = load(index)
                if not paused:
                    pygame.mixer.music.play()
                    playing = True
    pressed = pygame.key.get_pressed() 

    screen.blit(next_button,(175,50))
    screen.blit(back_button,(25,50))

    if playing:
        screen.blit(pause_button,(100,50))
    else:
        screen.blit(play_button, (100,50))
    if pressed[pygame.K_RIGHT]:
        press_next_button = pygame.transform.scale(next_button,(130,130))
        screen.blit(press_next_button,(160,35))
    if pressed[pygame.K_LEFT]:
        press_back_button = pygame.transform.scale(back_button,(130,130))
        screen.blit(press_back_button,(10,35)) 
        
    pygame.display.flip()
pygame.quit()