add_library('minim')
import os
import random, math

path = os.getcwd()
RESOLUTION_W = 1280
RESOLUTION_H = 720
GROUND = 585
player = Minim(this)

class Creature:
    def __init__(self, x, y, r, g, img, img_w, img_h, num_slices):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.vy = 1
        self.vx = 0
        self.img = loadImage(path + "/images/" + img)
        self.img_w = img_w
        self.img_h = img_h
        self.num_slices = num_slices
        self.slice = 0
        self.dir = RIGHT
    
    def gravity(self):
        
        for platform in game.platforms:
            if self.y + self.r <= platform.y and self.x >= platform.x and self.x <= platform.x + platform.w:
                self.g = platform.y
                break
            else:
                self.g = game.g
        
        
        if self.y + self.r >= self.g:
            self.vy = 0
        else:
            self.vy += 0.4
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
            
    def update(self):
        self.gravity()
        
        self.y += self.vy
        self.x += self.vx
    
    def display(self):
        self.update()

        if self.dir == RIGHT:
            image(self.img, self.x-self.img_w//2 - game.x_shift, self.y-self.img_h//2, self.img_w, self.img_h, self.slice * self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT:
            image(self.img, self.x-self.img_w//2 - game.x_shift, self.y-self.img_h//2, self.img_w, self.img_h, (self.slice + 1) * self.img_w, 0, self.slice * self.img_w, self.img_h)
            
class Mario(Creature):
    
    def __init__(self, x, y, r, g):
        Creature.__init__(self, x, y, r, g, "mario.png", 100, 70, 11)
        self.key_handler = {LEFT:False, RIGHT:False, UP:False}
        self.alive = True
        self.jump_sound = player.loadFile(path + "/sounds/jump.mp3")
        self.kill_sound = player.loadFile(path + "/sounds/kill.mp3")
        self.coin_sound = player.loadFile(path + "/sounds/coin.mp3")
    
    def update(self):
        self.gravity()
        
        if self.key_handler[LEFT] == True:
            self.vx = -7
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True:
            self.vx = 7
            self.dir = RIGHT
        else:
            self.vx = 0
        
        if self.key_handler[UP] == True and self.y + self.r == self.g:
            self.vy = -10
            self.jump_sound.rewind()
            self.jump_sound.play()
        
        if frameCount % 5 == 0 and self.vx != 0 and self.vy == 0:
            self.slice = (self.slice + 1) % self.num_slices
        elif self.vx == 0:
            self.slice = 3  
        
        for gomba in game.gombas:
            if self.distance(gomba) <= self.r + gomba.r:
                if self.vy > 0:
                    game.gombas.remove(gomba)
                    self.kill_sound.rewind()
                    self.kill_sound.play()
                else:
                    self.alive = False
                    game.platforms = []
                    game.gombas = []
                    self.vy = -15
                    self.g = 900
        
        for coin in game.coins:
            if self.distance(coin) <= self.r + coin.r:
                game.points += 1
                game.coins.remove(coin)
                self.coin_sound.rewind()
                self.coin_sound.play()
        
        self.y += self.vy
        self.x += self.vx
        
        if self.x - self.r < 0:
            self.x = self.r
        
        if self.x >= game.w//2:
            game.x_shift += self.vx
        elif self.x < game.w//2:
            game.x_shift = 0

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
    
class Gomba(Creature):
    
    def __init__(self, x, y, r, g, x_left, x_right):
        Creature.__init__(self, x, y, r, g, "gomba.png", 60, 60, 5)
        self.x_left = x_left
        self.x_right = x_right
        self.vx = random.randint(1,5)
    
    def update(self):
        self.gravity()
    
        if self.x >= self.x_right:
            self.vx *= -1
            self.dir = LEFT
        elif self.x <= self.x_left:
            self.vx *= -1 
            self.dir = RIGHT
                
        if frameCount % 5 == 0:
            self.slice = (self.slice + 1) % self.num_slices
            
        self.y += self.vy
        self.x += self.vx
    
class Coin(Creature):

    def __init__(self, x, y, r, g):
        Creature.__init__(self, x, y, r, g, "coin.png", 30, 40, 4)

    def update(self):
        # self.gravity()
        if frameCount % 10 == 0:
            self.slice = (self.slice + 1) % self.num_slices
            
class Platform:
    
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = loadImage(path + "/images/platform.png")
        
    def display(self):
        image(self.img, self.x - game.x_shift, self.y)

class Game:
    def __init__(self):
        self.w = RESOLUTION_W
        self.h = RESOLUTION_H
        self.g = GROUND
        self.x_shift = 0
        self.mario = Mario(100, 100, 35, self.g)
        self.platforms = []
        for i in range(3):
            self.platforms.append(Platform(200 + i*300, 500 - i*100, 200, 50))
            self.platforms.append(Platform(1200 + i*300, 500 - i*100, 200, 50))
            
        self.gombas = []
        for i in range(5):
            self.gombas.append(Gomba(random.randint(230, 770), 100, 30, self.g, 200, 800))
            self.gombas.append(Gomba(random.randint(1230, 1770), 100, 30, self.g, 1200, 1800))
    
        self.coins = []
        for i in range(4):
            self.coins.append(Coin(830 + i*50, 270, 20, 0))
        self.points = 0
    
        self.bg_imgs = []
        for i in range(5, 0, -1):
            self.bg_imgs.append(loadImage(path + "/images/layer_0" + str(i) + ".png"))
    
        self.bg_sound = player.loadFile(path + "/sounds/background.mp3")
        self.bg_sound.loop()
    
    def display(self):
        fill(0, 125, 0)
        noStroke()
        rect(0, self.g, self.w, self.h - self.g)
        
        x_shift = self.x_shift
        cnt = 0
        for bg_img in self.bg_imgs:
            if cnt == 0:
                x_shift = self.x_shift//4
            elif cnt == 1:
                x_shift = self.x_shift//3
            elif cnt == 2:
                x_shift = self.x_shift//2
            else:
                x_shift = self.x_shift
            
            width_right = x_shift % self.w
            width_left = self.w - width_right
            
            image(bg_img, 0 ,0, width_left, self.h, width_right, 0, self.w, self.h)
            
            image(bg_img, width_left, 0, width_right, self.h, 0, 0, width_right, self.h)
            cnt += 1
        
        for platform in self.platforms:
            platform.display()
        
        for coin in self.coins:
            coin.display()
        
        for gomba in self.gombas:
            gomba.display()
    
        fill(0,0,0,)
        textSize(22)
        text(str(self.points), self.w - 50, 30)
        self.mario.display()

def setup():
    size(RESOLUTION_W, RESOLUTION_H)
    background(255,255,255)

def draw():
    background(255,255,255)
    game.display()

def keyPressed():
    if keyCode == LEFT:
        game.mario.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.mario.key_handler[RIGHT] = True
    elif keyCode == UP:
        game.mario.key_handler[UP] = True
    elif keyCode == 32:
        if game.bg_sound.isPlaying() == True:
            game.bg_sound.pause()
            noLoop()
        else:
            game.bg_sound.play()
            loop()

def keyReleased():
    if keyCode == LEFT:
        game.mario.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.mario.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.mario.key_handler[UP] = False


def mouseClicked():
    global game
    player.stop()
    if game.mario.alive == False:
        game = Game()

        
game = Game()
