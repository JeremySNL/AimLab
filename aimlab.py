import pygame
import random
pygame.init()

pygame.display.set_caption("AimLab")

class target(object):
    def __init__(self, x, y, rad, color):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = (255, 0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.rad)

    def getClicked(self):
        self.x = random.randint((self.rad), (screenWidth - self.rad))
        self.y = random.randint((self.rad), (screenHeight - self.rad))

#Funcion para que se dibuje todos los eventos
def redraw(screen):
    screen.fill((0, 0, 0))
    if not(pause):
        target_1.draw(screen)
        scoreText = scoreFont.render("Score: " + str(score), 1, (0, 0, 255))
        screen.blit(scoreText, ((screenWidth * 0.90), 20))
    else:
        scoreText = scoreFont.render("Press space bar to continue", 1, (255, 255, 255))
        text_x, text_y = scoreText.get_size()
        screen.blit(scoreText, ((screenWidth/2 - text_x/2), screenHeight/2 - text_y/2))
        pygame.draw.rect(screen, (255, 255, 255), ((screenWidth/2 - text_x/2 - 10), (screenHeight/2 - text_y/2), (text_x + 20), (text_y+5)), 1)
    pygame.display.update()

#Variables
vel_resta = 50
vel = 2000
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screenWidth, screenHeight = pygame.display.get_window_size()
target_1 = target(screenWidth/2, screenHeight/2, 30, (255, 0, 0))
scoreFont = pygame.font.SysFont("comicsans", 25, True, False)
score = 1
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
            vel -= vel_resta
    
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

    if (current_time - spawnCD) >= vel and not(pause):
        target_1.x = random.randint((target_1.rad),(screenWidth - target_1.rad))
        target_1.y = random.randint((target_1.rad), (screenHeight - target_1.rad))
        print(str(current_time), str(spawnCD))
        spawnCD = pygame.time.get_ticks()

    redraw(screen)
pygame.QUIT