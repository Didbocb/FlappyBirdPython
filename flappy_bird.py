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

    def update(self):

        #handle the animation
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy)




run = True
while run:

    clock.tick(fps)

    screen.blit(background_img, (0, 0))
    screen.blit(background_img, (288, 0))

    bird_group.draw(screen)
    bird_group.update()

    screen.blit(ground_img, (ground_scroll, 512))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 48:
        ground_scroll = 0

    screen.blit(ground_img, (ground_scroll2, 512))
    ground_scroll2 -= scroll_speed
    if ground_scroll2 < 288:
        ground_scroll2 = 336

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()