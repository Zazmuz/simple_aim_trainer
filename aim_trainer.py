# Simple pygame program

# Import and initialize the pygame library
import pygame
import random
import time
pygame.init()
start_time = 0
end_time = 0
taps = 0
hits = 0
score = None
levels_passed = -1
game_is_going = True
display_object = pygame.display.Info()
width,height = display_object.current_w, display_object.current_h
current_size = 70
dots_to_shoot = []
mouse_click_pos = None
running = True
dont_append = None
crosshair_img = pygame.image.load('crosshair3.png')
myfont = pygame.font.SysFont('Comic Sans MS', 30)
myfont_big = pygame.font.SysFont('Comic Sans MS', 40)

# Set up the drawing window
#screen = pygame.display.set_mode([width, height])
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
def crosshair(xy):
    screen.blit(crosshair_img, (xy[0],xy[1]))



#for i in range(1,10):
#    dots_to_shoot.append(((random.randint(1,width),random.randint(1,height)),current_size))

# Run until the user asks to quit
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                dots_to_shoot = []
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if game_is_going:
                    taps += 1
                    mouse_click_pos = event.pos
                    if dots_to_shoot != []:
                        for index,dot in enumerate(dots_to_shoot):
                            if ((mouse_click_pos[0]-dot[0][0])**2 + ((mouse_click_pos[1]-dot[0][1]))**2) <= (dot[1]**2):
                                dots_to_shoot.pop(index)
                                hits += 1
                                if start_time == 0:
                                    start_time = time.time()
    if dots_to_shoot == []:
        if current_size > 20:
            current_size -= 5
            levels_passed += 1
        dots_to_shoot.append(((random.randint(100, width-100), random.randint(100, height-100)), current_size))

        while len(dots_to_shoot) != 5:
            dont_append = False
            may_become_dot = ((random.randint(100, width-100), random.randint(100, height-100)), current_size)

            for current_dot in dots_to_shoot:
                if ((may_become_dot[0][0]-current_dot[0][0])**2 + ((may_become_dot[0][1]-current_dot[0][1]))**2) <= ((current_size)**2)*10: #((current_size)**2)*4:
                    dont_append = True

            if not dont_append:
                dots_to_shoot.append(may_become_dot)
            #print(dots_to_shoot)

    if start_time != 0:
        if end_time-start_time < 60:
            end_time = time.time()
        else:
            game_is_going = False


    # Fill the background with white
    screen.fill((0, 0, 0))


    if game_is_going:
        # Draw a circle for each element in dots to shoot
        for dot in dots_to_shoot:
            pygame.draw.circle(screen, (255, 255, 255), dot[0], dot[1])
    else:
        if score == None:
            score = (1000*(levels_passed**1.1))+(100*(5-len(dots_to_shoot)))
            score += score*(hits/taps)
            score = round(score)
        stat_text_surface_2 = myfont_big.render('Score: ' + str(score), False, (255, 0, 255))
        screen.blit(stat_text_surface_2, ((width / 2)-150, height/2))

    # Render stats
    if taps >= 1:
        stat_text_surface_1 = myfont.render('Time: ' + str(round((end_time-start_time),1)) + '           Shots: ' + str(taps) + '           Acc: ' + str(round(((hits/taps)*100),2)) + '%', False, (255, 0, 0))
    else:
        stat_text_surface_1 = myfont.render('Time: 0s           Shots: ' + str(taps) + '           Acc: 0%', False, (255, 0, 0))
    screen.blit(stat_text_surface_1, ((width/2)-200, 0))

    # Render crosshair
    crosshair(pygame.mouse.get_pos())

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()