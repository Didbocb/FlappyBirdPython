import pygame
from pygame.locals import *
from pygame.sprite import Group
import random

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
pipe_gap = 150
pipe_frequency = 1000 #milliseconds
last_pipe = pygame.time.get_ticks()

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

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/pipe-green.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

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

    #draw pipe
    pipe_group.draw(screen)

    #draw the ground
    screen.blit(ground_img, (ground_scroll, 512))
    screen.blit(ground_img, (ground_scroll2, 512))

    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over =  True

    #check if bird hits ground
    if flappy.rect.bottom >= 512:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #scroll the ground
        screen.blit(ground_img, (ground_scroll, 512))
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 48:
            ground_scroll = 0
        screen.blit(ground_img, (ground_scroll2, 512))
        ground_scroll2 -= scroll_speed
        if ground_scroll2 < 288:
            ground_scroll2 = 336
        
        pipe_group.update()

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        
    pygame.display.update()

pygame.quit()