#Создание Шутерa!

from pygame import *
from random import randint
#Подключение фоновой музыки

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_bullet = 'bullet.png'
img_enemy ='ufo.png'
img_asteroid = 'asteroid.png'

#Создание окна
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
background = transform.scale(image.load(img_back), (win_width, win_height))

font.init()
font1 = font.SysFont('Arial', 40)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.SysFont('Arial', 36)

#Создание заготовки
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (60, 60))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x , self.rect.y))

#Создание класса ракеты
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        #Управление вправо и влево
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)
        asteroid = Enemy('asteroid.png', randint(30, win_width- 30), -40, randint(1, 10))
        asteroids.add(asteroids)

score = 0
lost = 0
goal = 10
max_lost = 10
finish = False

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(60, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png', randint(60, win_width- 80), -40, randint(1, 5))
    monsters.add(monster)

ship = Player('rocket.png', 20, win_height - 100, 7)#ракета

for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(30, win_width- 30), -40, randint(1, 10))
    asteroids.add(asteroid)

rel_time = False
num_fire = 0

game = True
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        #Выход при нажатии на 'Закрыть окно'
        if e.type == QUIT:
            game = False

        #Событие на нажатие на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                fire_sound.play()
                ship.fire()

                #if num_fire >= 5 and rel_time == False:
                    #last_time = timer()
                    #rel_time == True
        
    window.blit(background , (0,0))

    if finish != True:
        if rel_time == True:
            now_time = timer()

            #if now_time = last_time < 3:
                #reload = font2.render('Walt, reload...', 1, (150, 0, 0))
                #window.blit(reload, (260, 480))

            #else:
                #num_fire = 0
                #rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(10, win_width - 80), -40, randint(1, 5))
            monsters.add(monster)

        collides = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides:
            score += 1
            asteroid = Enemy('asteroid.png', randint(10, win_width - 80), -40, randint(1, 5))
            asteroids.add(asteroid)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render('Счет: ' + str(score), 8, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), 9, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        #'Показание' всех созданных объектов
        ship.reset()        
        ship.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        
        display.update()
        

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(60, win_width - 80), -40, randint(1, 7))
            monsters.add(monster)

        for i in range(1, 3):
            asteroid = Enemy('asteroid.png', randint(60, win_width - 80), -40, randint(1, 10))
            asteroids.add(asteroid)

    time.delay(50)
    clock.tick(FPS)
