import pygame
pygame.init()
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(r"Assets\spaceship.png"),(90,90))
        self.rect = self.img    