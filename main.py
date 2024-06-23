import os
from random import randint
import pygame
from pygame.font import Font

pygame.init()
WIDTH, HEIGHT = 1200,675
FPS = 60
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

class Ship(pygame.sprite.Sprite):
    """
    Is the class that models the behaviour of the space ship. Inhreits the functionality of a sprite
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Assets\spaceship.png"),(100,100)).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (600,665))

    def move_spaceship(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_w]:
            self.rect.y -= 7
        if keys_pressed[pygame.K_s]:
            self.rect.y += 7
        if keys_pressed[pygame.K_a]:
            self.rect.x -= 8
        if keys_pressed[pygame.K_d]:
            self.rect.x += 8
        # keeps ship in window
        if self.rect.right >= 1200: self.rect.right = 1200
        if self.rect.left <= 0: self.rect.left = 0 
        if self.rect.bottom >= 675: self.rect.bottom =675
        if self.rect.top <= 0: self.rect.top = 0
    def update(self):
        self.move_spaceship()
        if not game_active:
            self.rect.midbottom = (600,665)
        
class Rock(pygame.sprite.Sprite):
    def __init__(self,ship) -> None:
        super().__init__()
        ship_xpos = ship.rect.x
        difficulty = 500 - (level * 30)
        if difficulty >= 300:
            self.upper, self.lower = ship_xpos + 300, ship_xpos - 300
        self.speed = 2
        self.image = pygame.transform.rotozoom(pygame.image.load(os.path.join('Assets','asteroid.png')).convert_alpha(),0,0.3)
        self.rect = self.image.get_rect(center = (randint(self.lower,self.upper),-100))
    def destroy(self):
        if self.rect.y > 665 : self.kill()
    def update(self):
        self.destroy()
        self.rect.y += self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, ship):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(os.path.join('Assets','bullet.png')).convert_alpha(),90,0.05)
        self.rect = self.image.get_rect(midbottom = (ship.rect.centerx,ship.rect.centery))
    def update(self):
        self.rect.y -= 7
        if self.rect.bottom <= 0: self.kill()

            
def bullet_collision():
    for bullet in bullets:
        if pygame.sprite.spritecollide(bullet,rocks,True):
            bullet.kill()
        
def rock_collision():
    if pygame.sprite.spritecollide(ship.sprite,rocks,dokill=True):
        rocks.empty()
        bullets.empty()
        return False
    return True
bullets = pygame.sprite.Group()
rocks = pygame.sprite.Group()
ship = pygame.sprite.GroupSingle()
ship.add(Ship())

def display_score():
    score_int = pygame.time.get_ticks() //1000 - start_time
    score_str = font.render(str(score_int),False,'White')
    score_rect = score_str.get_rect(midbottom=(1150,665))
    screen.blit(score_str,score_rect)
    return score_int
level = 0
start_time = 0
score = 0
font = pygame.font.Font(os.path.join('Assets','font.ttf'),25)

rock_timer = pygame.USEREVENT +1
pygame.time.set_timer(rock_timer,500)
game_active = False

run = True
while run:
    keys_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and len(bullets)<1:
                bullets.add(Bullet(ship.sprite))                
            if event.type == rock_timer:
                rocks.add(Rock(ship.sprite))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_time = int(pygame.time.get_ticks() // 1000)
                    game_active = True
    
    if game_active:
        screen.fill('Blue')
        rocks.draw(screen)
        rocks.update()
        game_active = rock_collision()
        ship.draw(screen)
        ship.update()
        bullets.draw(screen)
        bullets.update()
        score = display_score()
        level = score // 10 if score % 10 == 0 else level
        bullet_collision()
    else:
        screen.fill('White')
        intro = font.render('Welcome to game, press space to start',False,'Black')
        intro_rect = intro.get_rect(center=(600,335))
        game_over = font.render(f'your score was {score}, space to replay',False,'Black')
        game_over_rect = game_over.get_rect(center=(600,335))
        
        if score == 0:
            screen.blit(intro,intro_rect)
        else:screen.blit(game_over,game_over_rect)
    
    clock.tick(FPS)
    pygame.display.update() 
pygame.quit()