from pygame import*
from time import time as t

win_wind = 1380
win_hight = 776
window = display.set_mode(( win_wind, win_hight))
display.set_caption('Maze (Лабиринт)')

class GameSprite(sprite.Sprite):
    def __init__ (self, image_name, x, y, weidht, hight):
        super().__init__()
        img = image.load(image_name)
        self.image = transform.scale(img, (weidht, hight))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def flip(self):
        self.image = transform.flip(self.image, False, True)

    def rotate(self, degree):
        self.image = transform.rotate(self.image, degree)


    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



background = GameSprite ( image_name = 'back.png',
                        x = 0, 
                        y = 0,
                        weidht = win_wind,
                        hight = win_hight)
platform = GameSprite( image_name = 'wall.png',
                        x = 370,
                        y = 315,
                        weidht = 450,
                        hight = 190)

platform2 = GameSprite( image_name = 'wall2.png',
                        x = 700,
                        y = 150,
                        weidht = 140,
                        hight = 690)

platform3 = GameSprite( image_name = 'wall.png',
                        x = 760,
                        y = 480,
                        weidht = 300,
                        hight = 190)

finish = GameSprite ( image_name ='cup.png',
                    x = 850, y = 650,
                    weidht = 70, hight = 70)


platform2.flip()

walls = sprite.Group()
walls.add(platform)
walls.add(platform2)
walls.add(platform3)

bullets = sprite.Group()


class Player (GameSprite):
    def __init__(self, image_name, x, y, weidht, hight, speed_x, speed_y):
        super().__init__( image_name, x, y, weidht, hight)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def move (self):
        #self.rect.x += self.speed_x
        #self.rect.y += self.speed_y 
        if self.rect.x <= win_wind - 75 and self.speed_x > 0 or self.rect.x >= 0 and self.speed_x < 0:
            self.rect.x += self.speed_x
        
        if self.rect.y <= win_hight - 75 and self.speed_y > 0 or self.rect.y >= 0 and self.speed_y < 0:
            self.rect.y += self.speed_y

        platform_touched = sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for platform in platform_touched:
                self.rect.right = min(self.rect.right, platform.rect.left)

        if self.speed_x < 0:
            for platform in platform_touched:
                self.rect.left = max(self.rect.left, platform.rect.right)

        if self.speed_x > 0:
            for platform in platform_touched:
                self.rect.bottom = min(self.rect.bottom, platform.rect.top)

        if self.speed_x < 0:
            for platform in platform_touched:
                self.rect.top = max(self.rect.top, platform.rect.bottom)

    def fire(self):
        bullet = Bullet(image_name = 'bullet.png',
                        x = self.rect.right,
                        y = self.rect.centery,
                        weidht = 40,
                        hight = 40,
                        speed = 5)
        bullets.add(bullet)

class Enemy(GameSprite):
    direction = 'left'
    def __init__( self, image_name, x, y, weidht, hight, speed):
        super().__init__(image_name, x, y , weidht, hight)
        self.speed = speed
    def move(self):
        if self.rect.x >= win_wind - 120:
            self.direction = 'left'
        elif self.rect.x <= win_wind - 570:
            self.direction = 'right'

        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__( self, image_name, x, y, weidht, hight, speed):
        super().__init__(image_name, x, y , weidht, hight)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_wind:
            self.kill()




font.init()
font = font.SysFont('Arial', 60)
def win():
    window.fill((0, 255, 0))
    win_text = font.render('YOU WIN!', True, (0, 0, 0))
    window.blit(win_text, (600, 350))

def lose():
    window.fill((255, 0, 180))
    lose_text = font.render('YOU LOSE!', True, (0, 0, 0))
    window.blit(lose_text, (600, 350))




ggcharatcer = Player (image_name = 'me.png',
                x = 35, y = 400, 
                weidht = 110, hight = 110,
                speed_x =0, speed_y = 0 )
clock = time.Clock()
fps = 60

ghost = Enemy( image_name = 'enemy.png',
                    x = 1000, y = 370,
                    weidht = 100, hight = 100,
                    speed = 5)

ghost2 = Enemy( image_name = 'enemy.png',
                    x = 1000, y = 200,
                    weidht = 100, hight = 100,
                    speed = 6)


run = True
end = False
win_or_lose = 0
cur = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                ggcharatcer.speed_y = -5
            elif e.key == K_s:
                ggcharatcer.speed_y = 5
            elif e.key == K_d:
                ggcharatcer.speed_x = 5
            elif e.key == K_a:
                ggcharatcer.speed_x = -5
            elif e.key == K_SPACE:
                ggcharatcer.fire()
        elif e.type ==  KEYUP:
            if e.key == K_w:
                ggcharatcer.speed_y = 0
            elif e.key == K_s:
                ggcharatcer.speed_y = 0
            elif e.key == K_d:
                ggcharatcer.speed_x = 0
            elif e.key == K_a:
                ggcharatcer.speed_x = 0

    if not end:
        background.draw()
        platform.draw()
        platform2.draw()
        platform3.draw()
        finish.draw()
        ggcharatcer.draw()
        bullets.draw(window)
        bullets.update()
        ghost.draw()
        ghost.move()
        ghost2.draw()
        ghost2.move()
        ggcharatcer.move()

        sprite.groupcollide(bullets, walls, True, False)

        if sprite.spritecollide(ghost, bullets, True):
            ghost.rect.x = win_wind + 50
            ghost.rect.y = win_wind + 50
            ghost.kill()

        if sprite.spritecollide(ghost2, bullets, True):
            ghost2.rect.x = win_wind + 50
            ghost2.rect.y = win_wind + 50
            ghost2.kill()
        
        if ggcharatcer.rect.colliderect(finish.rect):
            end = True
            start = t()
            win_or_lose = 1
        if ggcharatcer.rect.colliderect(ghost.rect):
            end = True
            start = t()
            win_or_lose = 2
        
        if ggcharatcer.rect.colliderect(ghost2.rect):
            end = True
            start = t()
            win_or_lose = 2


    else:
        if win_or_lose == 2:
            if cur - start < 3:
                cur = t()
                lose()
            else:
                run = False
        elif win_or_lose == 1:
            if cur - start < 3:
                win()
            else:
                run = False
    display.update()
    clock.tick(fps)



