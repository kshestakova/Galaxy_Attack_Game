import pygame
import random
import os

WIDTH = 480
HEIGHT = 600
FPS = 60

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Игра и окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("!!!GALAXY ATTACK!!!")
clock = pygame.time.Clock()

# Загрузка всей игровой графики
main = os.path.dirname(__file__)
img_folder = os.path.join(main, "img")

background = pygame.image.load(os.path.join(img_folder, "starfield.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, "playerShip1_orange.png")).convert()
meteor_img = pygame.image.load(os.path.join(img_folder, "meteorBrown_med1.png")).convert()
bullet_img = pygame.image.load(os.path.join(img_folder, "laserRed07.png")).convert()

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 40)) 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT-25
        self.speedx = 0
        

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speedx = -8
        if keys[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        

# Класс моба
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.85//2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-2, 2)
            self.speedy = random.randrange(1, 8)

# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        # Убить, если  пуля заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for _ in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Цикл игры
GAME = True
while GAME:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Проверка, не ударил ли моб игрока
    hit_with_player = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hit_with_player:
        GAME = False

    # Проверка столкновений пуль и мобов
    hits_with_bullets = pygame.sprite.groupcollide(bullets, mobs, True, True)
    for hit in hits_with_bullets:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # Обновление спрайтов
    all_sprites.update()

    # Рендеринг
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    # Обновление дисплея
    pygame.display.flip()

pygame.quit()


