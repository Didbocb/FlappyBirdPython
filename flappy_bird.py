import pygame
from pygame.locals import *
from pygame.sprite import Group

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 576
screen_height = 624

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define game variables
ground_scroll = 0
ground_scroll2 = 336
scroll_speed = 4
flying = False
game_over = False

#load images
background_img = pygame.image.load('sprites/background-day.png')
ground_img = pygame.image.load('sprites/base.png')

pygame_icon = pygame.image.load('favicon.ico')
pygame.display.set_icon(pygame_icon)

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        img = pygame.image.load('sprites/yellowbird-downflap.png')
        self.images.append(img)
        img = pygame.image.load('sprites/yellowbird-midflap.png')
        self.images.append(img)
        img = pygame.image.load('sprites/yellowbird-upflap.png')
        self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 512:
                self.rect.y += int(self.vel)
        
        if game_over == False:
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)




run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(background_img, (0, 0))
    screen.blit(background_img, (288, 0))

    #draw bird
    bird_group.draw(screen)
    bird_group.update()

    #draw the ground
    screen.blit(ground_img, (ground_scroll, 512))
    screen.blit(ground_img, (ground_scroll2, 512))

    #check if bird hits ground
    if flappy.rect.bottom > 512:
        game_over = True
        flying = False

    if game_over == False:
        #scroll the ground
        screen.blit(ground_img, (ground_scroll, 512))
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 48:
            ground_scroll = 0
        screen.blit(ground_img, (ground_scroll2, 512))
        ground_scroll2 -= scroll_speed
        if ground_scroll2 < 288:
            ground_scroll2 = 336

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        
    pygame.display.update()

pygame.quit()