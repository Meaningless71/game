#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1

class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > 500:
                self.rect.x = randint(80, 620)
                self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
window = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

ship = Player('rocket.png', 5, 400, 80, 100, 10)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(5):
    monser = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 3))
    monsters.add(monser)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroids('asteroid.png', randint(30, 670), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

font.init()
font2 = font.Font(None, 36)

font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


run = True
finish = False
life = 3
rel_time = False
num_fire = 0
while run:
                              
    for e in event.get():
        if e.type == QUIT:
            run = False 

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if finish == False:
        window.blit(background, (0, 0))

        ship.update()
        ship.reset()

        text = font2.render('Счёт: ' + str(score),  1, (255, 255, 255))
        window.blit(text, (10, 10))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        monsters.draw(window)
        monsters.update()

        asteroids.update()
        asteroids.draw(window)

        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        for b in bullets:
            b.kill()
        for b in monsters:
            b.kill()
        for b in asteroids:
            b.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    
    if life <= 0:
        finish = True
        window.blit(lose, (200, 200))

    if lost == 3:
        finish = True
        window.blit(lose, (200, 200))

    if score >= 10:
        finish = True
        window.blit(win, (200, 200))

    display.update()
    time.delay(50)