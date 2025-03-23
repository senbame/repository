import pygame
def drawRect(screen, start_point, end_point, color):
    rect = pygame.Rect(start_point, (end_point[0] - start_point[0], end_point[1] - start_point[1]))
    pygame.draw.rect(screen, color, rect, 2)

def drawLine(screen , start_point , end_point , rad , color):
    pygame.draw.line(screen , color , start_point , end_point , rad)

def drawCircle(screen, start_point, end_point, color):
    radius = int(((end_point[0] - start_point[0]) ** 2 + (end_point[1] - start_point[1]) ** 2) ** 0.5)  
    pygame.draw.circle(screen, color, start_point, radius, 2)  

def colorPicker(mode):
    if mode == 'blue':
        return (0,0,255)
    elif mode == 'red':
        return (255,0,0)
    elif mode == 'green':
        return (0,255,0)
    elif mode == 'white':
        return (255,255,255)
    elif mode == 'yellow':
        return (255,255,0)
    elif mode == 'orange':
        return (255,128,0)
def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    FramPerSec = pygame.time.Clock()
    FPS = 60
    
    font = pygame.font.Font(None, 36)
    radius = 10
    mode = 'red'
    prev_mode = mode
    initial_points = []

    done = True
    eraser = False
    rectangle = False
    input_active = True
    drawing_rect = False
    paint_mode = False
    drawing_circle = False
    circle = False

    rects = []
    rect_start = None
    circles = []
    circle_start = None
    while done:
        mouse_pos = pygame.mouse.get_pos()
        pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_F4 and (pressed[pygame.K_LALT] or pressed[pygame.K_RALT]):
                    done = False
                elif event.key == pygame.K_ESCAPE:
                    done = False
                elif event.key == pygame.K_r:
                    mode = 'red' 
                elif event.key == pygame.K_b:
                    mode = 'blue' 
                elif event.key == pygame.K_g:
                    mode  = 'green' 
                elif event.key == pygame.K_e:
                    eraser = not eraser
                    if eraser:
                        prev_mode = mode
                        mode = 'white'
                    else:
                        mode = prev_mode
                elif event.key == pygame.K_y:
                    mode  = 'yellow' 
                elif event.key == pygame.K_o:
                    mode = 'orange' 
                elif event.key == pygame.K_q:
                    rectangle = not rectangle
                elif event.key == pygame.K_p:
                    paint_mode = not paint_mode
                elif event.key == pygame.K_c:
                    circle = not circle
                elif event.key == pygame.K_DELETE:
                    initial_points.clear()
                    rects.clear()
                    circles.clear()    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    radius = min(200 , radius+1)
                    if rectangle:
                        if not drawing_rect:
                            rect_start = mouse_pos
                            drawing_rect = True
                        else:
                            rects.append((rect_start,mouse_pos))
                            drawing_rect = False
                    elif circle:
                        if not drawing_circle:
                            circle_start = mouse_pos
                            drawing_circle = True
                        else:
                            circles.append((circle_start,mouse_pos))
                            drawing_circle = False
                    else:
                        initial_points.append((mouse_pos,mode))
                elif event.button == 3:
                    radius = max(1,radius - 1)

            if event.type == pygame.MOUSEMOTION and paint_mode:
                position = event.pos
                initial_points.append((position,mode))
    
        
        screen.fill((255,255,255))
        i = 0
        length = len(initial_points)
        if paint_mode:
            while i < length-1:
                color = colorPicker(initial_points[i][1])
                drawLine(screen ,initial_points[i][0] , initial_points[i+1][0] , radius , color)
                i += 1
        for rect in rects:
            drawRect(screen, rect[0], rect[1], (0,0,0))

        for circ in circles:
            drawCircle(screen, circ[0], circ[1], (0,0,0))

        if eraser:
            pygame.mouse.set_visible(False)
            pygame.draw.circle(screen, (0, 0, 0), mouse_pos, radius, 2)  
            pygame.draw.circle(screen, colorPicker(mode), mouse_pos, radius - 2)  
        else:
            pygame.mouse.set_visible(True)
        

        if rectangle:
            pygame.mouse.set_visible(False)
            cross_size = radius * 2  
            color = (0, 0, 0)  
            # Горизонтальная линия
            pygame.draw.line(screen, color, (mouse_pos[0] - cross_size, mouse_pos[1]),
                             (mouse_pos[0] + cross_size, mouse_pos[1]), 2)
            # Вертикальная линия
            pygame.draw.line(screen, color, (mouse_pos[0], mouse_pos[1] - cross_size),
                             (mouse_pos[0], mouse_pos[1] + cross_size), 2)
        else:
            pygame.mouse.set_visible(True)
        if circle:
            pygame.mouse.set_visible(False)
            cross_size = radius * 2  
            color = (0, 0, 0)  
            # Горизонтальная линия
            pygame.draw.line(screen, color, (mouse_pos[0] - cross_size, mouse_pos[1]),
                             (mouse_pos[0] + cross_size, mouse_pos[1]), 2)
            # Вертикальная линия
            pygame.draw.line(screen, color, (mouse_pos[0], mouse_pos[1] - cross_size),
                             (mouse_pos[0], mouse_pos[1] + cross_size), 2)
        else:
            pygame.mouse.set_visible(True)

        if drawing_rect and rect_start:
            drawRect(screen, rect_start, mouse_pos, (0, 0, 0))
        
        if drawing_circle and circle_start:
            drawCircle(screen , circle_start , mouse_pos,(0,0,0))

        status_text = f"Mode: {'Eraser' if eraser else mode} | Paint: {'ON' if paint_mode else 'OFF'} | Rect: {'ON' if rectangle else 'OFF'} | Circle: {'ON' if circle else 'OFF'}"
        text_surface = font.render(status_text, True, (0, 0, 0))
        screen.blit(text_surface, (10, 10))
        pygame.display.flip()
        FramPerSec.tick(FPS)

main()
