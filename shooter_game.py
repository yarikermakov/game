from pygame import *
from random import *
from time import time as timer
win_width = 1000
win_hight =700
window = display.set_mode((win_width,win_hight))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_hight))

mixer.init()
mixer.music.load("space.ogg")
#mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(1)

font.init()
font1 = font.Font(None, 50)
win = font1.render('YOU WIN!', True, (255, 255, 0))
lose = font1.render('YOU LOSE!', True, (255, 0, 0))



font2 = font.Font(None, 36)


# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -=self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x +=self.speed           
        if keys [K_UP] and self.rect.y > 5:
            self.rect.y -=self.speed
        if keys[K_DOWN] and self.rect.y < win_hight-80:
            self.rect.y +=self.speed


        


    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_hight:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = -50
            self.speed = randint(1,6)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y<-10:
            self.kill()

bullets = sprite.Group()






class Anim(sprite.Sprite):
    def __init__(self,nameDirAnim,pos_x,pos_y,countSprite):
        sprite.Sprite.__init__(self)
        self.animation_set = [image.load(f"{nameDirAnim}/{i}.png") for i in range(1, countSprite)]
        self.i = 0
        self.x = pos_x
        self.y = pos_y
    
    def update(self):
        window.blit(self.animation_set[self.i], (self.x, self.y))
        self.i += 1
        if self.i > len(self.animation_set) -1:
            self.kill()

animsHit = sprite.Group()

animsHit = sprite.Group()

run = True # 
finish = False

score = 0
lost = 0
num_fire = 0
life = 5
rel_time = False
ship = Player("rocket.png",5, win_hight-100, 80,100,10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png",randint(80,win_width-80),-50,80,50,randint(1,5))
    monsters.add(monster)

while run:
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == MOUSEBUTTONDOWN :
            if e.button == 1:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire>= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    
    if finish != True:
        window.blit(background,(0,0))

        text = font2.render("Рахунок: "+str(score),True,(255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("Пропущено: "+str(lost),True,(255,255,255))
        window.blit(text_lose,(10,50))

        
        ship.reset()
        ship.update()

        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        animsHit.update()

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload= font2.render("Wait, reload...",1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False    

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
        ###
            x, y = c.rect.x , c.rect.y 
            hit = Anim("anim2",x,y,9)
            animsHit.add(hit)
            ###
            score += 1
            monster = Enemy("ufo.png",randint(80,win_width-80),-50,80,50,randint(1,5))
            monsters.add(monster)






        
        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship,monsters, True)
            life -= 1

        #умова перемоги
        if score >= 10:
            finish = True
            window.blit(win,(win_width/1000,win_hight/10))

        #умова програшу
        if life < 1 or lost >= 5:
            finish = True  
            window.blit(lose,(370,300))


        if life > 4:
            fill_color = (0,150,0)
        elif life > 2:
            fill_color = (150,150,0)
        else:
            ill_color= (150,0,0)
                
        text_life = font1.render(str(life),1,fill_color)
        window.blit(text_life,(640,20))

    display.update()
    time.delay(50)
