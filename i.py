from pygame import *
from random import randint

clock = time.Clock()

print("Управление на WASD, q - ускорить перемещение, e - замедлить, лкм - телепортироваться вперед")

life = 3

start_time = time.get_ticks() # заменил метод объекта
cur_time = start_time

font.init()
font2 = font.SysFont(None, 36)
font1 = font.SysFont(None, 80)
win = font1.render('You win!', True, (255,25,255))
lose = font1.render('You lose!', True, (255,25,255))

mixer.init()
mixer.music.load('musica.ogg')
mixer.music.play()

img_back = "background.jpg" 
img_hero = "noletmediem.png" 
img_enemy = "derevo.png"
img_kamen = "led.png"

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 30:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 45:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 30:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 30:
            self.rect.y += self.speed
        if keys[K_q] and self.speed == 10:
            self.speed = self.speed + 10
        if keys[K_e] and self.speed == 20:
            self.speed = self.speed - 10
        


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(5, win_width - 5)
            self.rect.y = -150

class Led(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(5, win_width - 5)
            self.rect.y = -100

win_width = 700
win_height = 500
display.set_caption("challenge")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

hero = Player(img_hero, 5, win_height - 100, 10, 10, 10)


monsters = sprite.Group()
for i in range(1,20):
    monster = Enemy(img_enemy, randint(5, win_width - 5), -40, 40,150, randint(10,13))
    monsters.add(monster)

leds = sprite.Group()
for i in range(1,13):
    led = Led(img_kamen, randint(5, win_width - 5), -40, 50, 100, randint(10,13))
    leds.add(led)

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if hero.rect.y > 200:
                    hero.rect.y = hero.rect.y - 175

    if not finish:
        new_time = time.get_ticks()

        if new_time - start_time >= 60:
            window.blit(win,(250,250))
            finish = True
        if life == 3:
            life_color = (0,150,0)

        if life == 2:
            life_color = (150,150,0)
        
        if life == 1:
            life_color = (150,0,0)

        window.blit(background,(0,0))

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        hero.update()
        monsters.update()
        leds.update()


        hero.reset()
        monsters.draw(window)
        leds.draw(window)

        if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero, leds, False):
            sprite.spritecollide(hero, monsters, True)
            sprite.spritecollide(hero, leds, True)
            life = life - 1

        if sprite.spritecollide(hero, monsters, False):
            finish = True
            window.blit(lose,(200,200))

        if sprite.spritecollide(hero, leds, False):
            finish = True
            window.blit(lose,(200,200))

        if life <= 0:
            finish = True
            window.blit(lose,(200,200))

        display.update()

    else:
        finish = False
        life = 3
        for b in monsters:
            b.kill()
        for b in leds:
            b.kill()

        time.delay(2000)
        for i in range(1,20):
            monster = Enemy(img_enemy, randint(5, win_width - 5), -40, 40,150, randint(10,13))
            monsters.add(monster)

        for i in range(1,13):
            led = Led(img_kamen, randint(5, win_width - 5), -40, 50, 100, randint(10,13))
            leds.add(led)

    clock.tick(40)
