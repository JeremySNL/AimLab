import pygame
import random
pygame.init()

pygame.display.set_caption("AimLab")

class target(object):
    def __init__(self, x, y, rad, color, start_vel, minus_vel):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.start_vel = start_vel
        self.minus_vel = minus_vel

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.rad)

    def getClicked(self):
        self.x = random.randint((self.rad), (screenWidth - self.rad))
        self.y = random.randint((self.rad), (screenHeight - self.rad))

#Funcion para que se dibuje todos los eventos
def redraw(screen):
    screen.fill((0, 0, 0))
    if not(pause) and not(win):
        target_1.draw(screen)
        scoreText = scoreFont.render("Acertados: " + str(score), 1, (0, 0, 255))
        missText = scoreFont.render("Errados: " + str(miss), 1, (255, 0, 0))
        screen.blit(scoreText, ((screenWidth/2 - scoreText.get_size()[0] - 20), 20))
        screen.blit(missText, ((screenWidth/2 + 20), 20))
    elif pause and not(win):
        scoreText = scoreFont.render("Press space bar to continue", 1, (255, 255, 255))
        text_x, text_y = scoreText.get_size()
        screen.blit(scoreText, ((screenWidth/2 - text_x/2), screenHeight/2 - text_y/2))
        pygame.draw.rect(screen, (255, 255, 255), ((screenWidth/2 - text_x/2 - 10), (screenHeight/2 - text_y/2), (text_x + 20), (text_y+5)), 1)
    else:
        winText = scoreFont.render("You Win!", 1, (255, 255, 255))
        exitText = scoreFont.render("Press ESC to exit", 1, (255, 255, 255))
        winText_x, winText_y = winText.get_size()
        exitText_x, exitText_y = exitText.get_size()
        screen.blit(winText, (screenWidth/2 - winText_x/2, screenHeight/2 - winText_y/2))
        screen.blit(exitText, (screenWidth/2 - exitText_x/2, screenHeight/2 - exitText_y/2 + 100))
    pygame.display.update()

#Variables
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screenWidth, screenHeight = pygame.display.get_window_size()
target_1 = target(screenWidth/2, screenHeight/2, 30, (255, 0, 0), 2000, 50)
scoreFont = pygame.font.SysFont("comicsans", 25, True, False)
score = 0
miss = 0
win = False
pause = True
spaceCD = -1000
spawnCD = 0

run = True
while run:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()

    if (current_time - spaceCD) <= 1000:
        pygame.time.delay(1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        distance = int((((mouse_x - target_1.x)**2) + ((mouse_y - target_1.y)**2))**(0.5))
        if distance <= target_1.rad and event.type == pygame.MOUSEBUTTONDOWN and not(pause):
            target_1.getClicked()
            spawnCD = pygame.time.get_ticks()
            score += 1
            target_1.start_vel -= target_1.minus_vel
        elif event.type == pygame.MOUSEBUTTONDOWN and not(pause):
            miss += 1
    
    keys = pygame.key.get_pressed()
    #Si presiona ESC se cerrará el juego 
    if keys[pygame.K_ESCAPE]:
        run = False

    if keys[pygame.K_SPACE] and pause and (current_time - spaceCD) >= 1000:
        spawnCD = pygame.time.get_ticks()
        pause = False
        spaceCD = pygame.time.get_ticks()
        
    elif keys[pygame.K_SPACE] and not(pause) and (current_time - spaceCD) >= 1000:
        pause = True
        spaceCD = pygame.time.get_ticks()

    if (current_time - spawnCD) >= target_1.start_vel and not(pause):
        target_1.x = random.randint((target_1.rad),(screenWidth - target_1.rad))
        target_1.y = random.randint((target_1.rad), (screenHeight - target_1.rad))
        spawnCD = pygame.time.get_ticks()

    if score >= 35:
        win = True

    redraw(screen)
pygame.QUIT