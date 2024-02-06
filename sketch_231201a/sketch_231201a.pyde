add_library('video')
import os
import time 
from processing.video import Movie

add_library('minim')
path = os.getcwd()
width = 600
height = 400
MENU, GAME, TUTORIAL = range(3)
shootSound, explosionSound, playerDestroyedSound, alienMoveSound, backgroundSound, menuSound = None, None, None, None, None, None


class SpaceShip:# class of generating spaceship
    def __init__(self, posx, posy, img, img_w, img_h):
        self.posx = posx
        self.posy = posy
        self.img = loadImage(path + "/images/" + img)
        self.img_w = img_w
        self.img_h = img_h
        self.speed = 5
        self.bullets = []
        self.shooting = False  # Flag to indicate shooting
        self.shootInterval = 500 # setting the interval of shooting, flexible to change
        self.lastShotTime = 0
        self.key_handler = {LEFT:False, RIGHT:False, UP:False}
        self.life = 3
        self.score = 0
        self.lifePrinted = False

    def move(self): # the function to move spaceship(certain limitation of coordinate so it's not gonna go out)
        if keyPressed:
            
            if self.key_handler[LEFT] == True:
                self.key_handler[RIGHT] = False
                if 0 < self.posx:
                    self.posx -= self.speed
            elif self.key_handler[RIGHT] == True:
                self.key_handler[LEFT] = False
                if self.posx < 570:
                    self.posx += self.speed
            
        if not keyPressed:
            self.shooting = False  # Reset shooting flag when no keys are pressed

    def shoot(self): # shooting mechanism of spaceship
        if key == ' ' and self.shooting and millis() - self.lastShotTime > self.shootInterval:  # 500 milliseconds delay
            self.shooting = False
            self.bullets.append(Bullet(self.posx + 15, self.posy - self.img_h))
            self.lastShotTime = millis()
            shootSound.rewind()
            shootSound.play()

        

    def display(self):
        image(self.img, self.posx, self.posy, self.img_w, self.img_h)

class Bullet:# class for generating bullets
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
            

    def move(self):
        self.y -= self.speed

    def display(self):
        ellipse(self.x, self.y, 5, 10)
            
class Enemy:# class for generating normal enemies
    def __init__(self, x, y, img, img_w, img_h):
        self.x = x
        self.y = y
        self.img = loadImage(path + "/images/" + img)
        self.img_w = img_w
        self.img_h = img_h
        self.special_enemy = False

    def move(self, dx, dy):
        alienMoveSound.rewind()
        alienMoveSound.play()
        self.x += dx
        self.y += dy
        
    def display(self):
        image(self.img, self.x, self.y, self.img_w, self.img_h)
        
class Special_Enemy:#class for generating special enemy(power-up)
    def __init__(self, x, y, img, img_w, img_h):
        self.x = x
        self.y = y
        self.special_enemy = True
        self.img = loadImage(path + "/images/" + img)
        self.img_w = img_w
        self.img_h = img_h
        
    def move(self, dx, dy):
        self.x += 5 * dx
        self.y += dy
        
    def display(self):
        image(self.img, self.x, self.y, self.img_w, self.img_h)
    

class Shield:# class for generating shield
    def __init__(self, x, y, img, img_w, img_h):
        self.x = x
        self.y = y
        self.img = loadImage(path + "/images/" + img)
        self.img_w = img_w
        self.img_h = img_h
        self.health = 15

    def display(self):
        fill(0, 255, 0)
        if self.health > 0:  # Only draw if shield is not destroyed
            image(self.img, self.x, self.y, self.img_w, self.img_h)

class Game: 
    def __init__(self):
        self.spaceship = SpaceShip(width / 2, height - 30, "spaceship.png", 30, 30)
        self.enemies = self.createEnemies()
        self.shields = self.createShields()
        self.enemyBullets = []
        self.enemySpeed = 5
        self.enemyDirection = 1  # 1 for right, -1 for left
        self.enemyDownShift = 2.5  # Amount to move down when changing direction
        self.maxEnemyY = height - 120  # Adjust as needed
        self.explosionFrames = [loadImage(path + "/particles/explosion" + str(i) + ".gif") for i in range(5)]  # Adjust range based on the number of frames
        self.explosions = []  # List to store active explosionsdd
        self.state = MENU  # Start with the menu
        self.enemyRows = self.createEnemyRows()
        self.enemyMoveInterval = 10  # Intervalo de movimiento en milisegundos
        self.lastEnemyMoveTime = 10
        self.power_up_active = False # power-up condition
        self.power_up_start_time = 0
        self.power_up_duration = 8000
        self.gameover = False # quitting game conditions
        self.game_win = False
        self.level = 1  # Add a level attribute to keep track of the game level
        self.baseEnemySpeed = 5  # Base speed of enemies
        self.baseAttackFrequency = 120  # Base attack frequency
        self.menuVideo = None  # Initialize as None here
        self.backgroundimage=loadImage(path + "/images/tutorial.png")
        
    def setupMenuVideo(self):
        '''
        We encounter that reproducing the video in the constructure can lead
        to reproduction problems or buffering, therefore it should be loaded
        in a different class in order to work.
        '''
        self.menuVideo = Movie(this, path + "/video/background1.mp4")
        self.menuVideo.loop()
        
    def drawMenu(self):
        if self.menuVideo.available():
            self.menuVideo.read()
        image(self.menuVideo, 0, 0, width, height)  # Draw the video as background
        fill(255)  # White text
        textSize(32)
        textAlign(CENTER, CENTER)
        text("Space Invaders", width / 2, height / 3)
        textSize(16)
        text("Click to Start", width / 2, height / 2)
        text("Tutorial", width / 2, height / 2 + 30)
        
    def drawTutorial(self):
        fill(255)
        textSize(20)
        text("Tutorial:\nUse A/D to move, Space to shoot.\nClick to return to menu.", width / 2, height / 2, 200, 200)
        image(self.backgroundimage, 0, 0, width, height)
        
    def createEnemyRows(self):
        rows = []
        numAliensY = 5  # Número de filas de enemigos
        for i in range(numAliensY):
            row = {
                'enemies': [enemy for enemy in self.enemies if enemy.y == 40 + i * 40],
                'speed': 0.2 + i * 0.05,  # Velocidad incremental por fila
                'delay': i * 30,  # Retraso incremental por fila
                'moveTime': millis()  # Tiempo inicial para empezar a moverse
            }
            rows.append(row)
        return rows

    def createEnemies(self):
        enemies = []
        numAliensX = 11  # Number of aliens horizontally
        numAliensY = 5   # Number of aliens vertically
        alienSpacingX = 40  # Horizontal spacing between aliens
        alienSpacingY = 40  # Vertical spacing between aliens

        # Calculate total width and starting x-coordinate
        totalAlienWidth = numAliensX * alienSpacingX
        startX = (width - totalAlienWidth) / 2
        
        # Create aliens in rows and columns
        
        enemies_png_list = ["alien4.png", "alien3.png", "alien2.png", "alien1.png"]
        for i in range(numAliensX):
            for j in range(numAliensY):
                x = startX + i * alienSpacingX
                y = 40 + j * alienSpacingY
                if j == 0 or j == 1:
                    enemies.append(Enemy(x, y, enemies_png_list[0], 20, 20))
                else:
                    enemies.append(Enemy(x, y, enemies_png_list[j-1], 20, 20))
            
        enemies.append(Enemy(x,y, enemies_png_list[0], 20, 20))     
        enemies[-1] = Special_Enemy(300,5,"special_enemy.png", 20, 20)

        return enemies
        
    def createShields(self):
        shields = []
        for i in range(4):
            shieldX = 50 + i * 150
            shields.append(Shield(shieldX, height - 100, "shield.png", 60, 45))
        return shields

    def display(self):
        if self.state == MENU:
            if not menuSound.isPlaying():
                menuSound.rewind()
                menuSound.play()
            self.drawMenu()
            
        elif self.state == GAME:
            menuSound.pause()
            background(0)
            self.spaceship.move()
            self.spaceship.shoot()
            self.spaceship.display()
            self.moveEnemies()
    
            self.handleBullets()
            self.drawEnemies()
            self.drawShields()
            self.checkCollisions()
            game.updatePowerUp()
            self.enemyAttack()
            fill(255, 255, 255)
            textSize(10)
            text("The life:" + str(self.spaceship.life), 520, 10)
        
            fill(255, 255, 255)
            textSize(10)
            text("The score:" + str(self.spaceship.score), 520, 30)
                    
            for explosion in self.explosions:
                if explosion['frame'] < len(self.explosionFrames):
                    
                    explosionSound.play()
                    explosionSound.rewind()
                    image(self.explosionFrames[explosion['frame']], explosion['x'] + 20/2 - self.explosionFrames[explosion['frame']].width / 2, explosion['y'] + 20/2 - self.explosionFrames[explosion['frame']].height / 2)

                    explosion['frame'] += 1            

                else:
                    self.explosions.remove(explosion)
                    
        elif self.state == TUTORIAL:
            self.drawTutorial()   
        
        # change the statement that will be printed depending on the game condition
        if self.gameover == True:
            fill(255, 255, 255)
            textSize(20)
            text("Game Over!!", width / 2, height / 2 - 50)
            text("Your Final Score:" + str(self.spaceship.score), width/2, height/2)
            text("Click to go back to menu", width/2, height/2 + 50)
        
        if self.game_win == True:
            fill(255, 255, 255)
            textSize(20)
            text("You won!! \n", width / 2, height / 2 - 50)
            text("Your Final Score:" + str(self.spaceship.score), width/2, height/2)
            text("Click to go back to menu", width/2, height/2 + 50)
            
    def moveEnemies(self):
        current_time = millis()
        if current_time - self.lastEnemyMoveTime > self.enemyMoveInterval:
            moveDown = False
            for enemy in self.enemies:
                enemy.move(self.enemySpeed * self.enemyDirection, 0)
                if enemy.x > width - 10 or enemy.x < 10:
                    moveDown = True

            if moveDown:
                self.enemyDirection *= -1
                for enemy in self.enemies:
                    new_y = enemy.y + self.enemyDownShift
                    if new_y < self.maxEnemyY:
                        enemy.move(0, self.enemyDownShift)
                    else:
                        fill(255, 255, 255)
                        text("Game Over!!", width / 2, height / 2 - 50)
                        text("Your Final Score:" + str(self.spaceship.score), width/2, height/2)
                        text("Click to go back to menu", width/2, height/2 + 50)
                        noLoop()

            self.lastEnemyMoveTime = current_time

            # Aumentar la velocidad de los enemigos gradualmente
            self.enemyMoveInterval = max(1000, self.enemyMoveInterval - 10)
    
        
    def handleBullets(self):
        for bullet in self.spaceship.bullets:
            bullet.move()
            bullet.display()
        self.spaceship.bullets = [bullet for bullet in self.spaceship.bullets if bullet.y > 0]

        for bullet in self.enemyBullets:
            bullet[1] += 5  # Enemy bullet speed
            ellipse(bullet[0], bullet[1], 5, 10)  # Draw enemy bullet
        self.enemyBullets = [bullet for bullet in self.enemyBullets if bullet[1] < height]
        
        # Adjust shooting speed and frequency based on power-up state
        if self.power_up_active:
            self.spaceship.shootInterval = 200  # Faster shooting interval during power-up
        else:
            self.spaceship.shootInterval = 500  # Default shooting interval


    def drawEnemies(self):
        for enemy in self.enemies:
            enemy.display()

    def drawShields(self):
        for shield in self.shields:
            shield.display()

    def checkCollisions(self):
        num_rows = len(self.enemyRows)
        for bullet in self.spaceship.bullets:
            for enemy in self.enemies: # checking collision between spaceship's bullet and enemy's one
                if enemy.special_enemy == True and dist(bullet.x, bullet.y, enemy.x, enemy.y) < 20:# when special enemy destroyed
                    self.activatePowerUp()
                    self.spaceship.score += 1000
                    self.enemies.remove(enemy)
                    self.spaceship.bullets.remove(bullet)
                    self.explosions.append({'x': enemy.x, 'y': enemy.y, 'frame': 0})
                    self.activatePowerUp()
                    if len(self.enemies) == 0:# when all enemies destroyed, win the game
                        self.game_win = True
                        
                elif dist(bullet.x, bullet.y, enemy.x, enemy.y) < 20:# when normaly enemy destroyed          
                    row_index = self.get_enemy_row_index(enemy)
                    score_increment = 100 * (num_rows - row_index)  # Reverse scoring logic
                    self.spaceship.score += score_increment
                    self.enemies.remove(enemy)
                    self.spaceship.bullets.remove(bullet)
                    self.explosions.append({'x': enemy.x, 'y': enemy.y, 'frame': 0})
                    if len(self.enemies) == 0:# when all enemies destroyed, win the game
                        self.game_win = True
                    break
                    

            for shield in self.shields:# detect the collision between spaceship's bullet and shield
                if shield.health > 0 and bullet.x > shield.x and bullet.x < shield.x + 60 and bullet.y > shield.y - 5 and bullet.y < shield.y + 5:
                    shield.health -= 1  # Reduce shield health
                    self.spaceship.bullets.remove(bullet)
                    break

        for bullet in self.enemyBullets:
            for shield in self.shields: # checking collision between shield and enemy's bullet
                if shield.health > 0 and (shield.x < bullet[0] < shield.x + 60) and (shield.y - 5 < bullet[1] < shield.y + 5):
                    shield.health -= 1  # Reduce shield health
                    self.enemyBullets.remove(bullet)
                    break
            
            if (self.spaceship.posx < bullet[0] < self.spaceship.posx + 30) and (self.spaceship.posy < bullet[1] < self.spaceship.posy + 30):
                #checking collision between spaceship and enemy's bullet
                playerDestroyedSound.rewind()
                playerDestroyedSound.play()
                self.spaceship.life -= 1
                if 0 < self.spaceship.life < 3:
                    self.player_hit = True
                elif self.spaceship.life == 0:
                    self.gameover = True
                    noLoop()
                    
                if self.player_hit:# pause for 1 second to avoid spaceship losing all life at once.
                    self.enemyBullets.remove(bullet)
                    delay(1000)  # Pause for 1 second (adjust as needed)
                    redraw()  # Redraw the frame
                    self.player_hit = False
            break
        
                    
        for spaceship_bullet in self.spaceship.bullets:#checking collision between spaceship's bullet and enemy's bullet
            for enemy_bullet in self.enemyBullets:
                if dist(spaceship_bullet.x, spaceship_bullet.y, enemy_bullet[0], enemy_bullet[1]) < 10:
                    # Collision detected, remove both bullets
                    self.enemyBullets.remove(enemy_bullet)
                    self.spaceship.bullets.remove(spaceship_bullet)
        
        if len(self.enemies) == 0: # level up and regenerate enemies
            if self.level < 3: # limit the frequency of regenerating to twice
                self.level += 1  # Increase the level
                self.enemies = self.createEnemies()  # Regenerate enemies
                self.enemySpeed = self.baseEnemySpeed * (1 + 0.1 * self.level)  # Increase enemy speed
                self.baseAttackFrequency = max(60, self.baseAttackFrequency - 10 * self.level)  # Increase attack frequency
                self.game_win = False  # Reset the game win state
            elif self.level == 3:# all enemies destroyed for three times
                self.game_win = True
        
    def get_enemy_row_index(self, enemy):
        row_index = 0
        for row in self.enemyRows:
            if enemy in row['enemies']:
                return row_index
            row_index += 1
        return 0  # Default row index if not found                
                                            
    def activatePowerUp(self): #activate temporary power-up
        self.power_up_active = True
        self.power_up_start_time = millis()

    def updatePowerUp(self):# checking how many seconds left for power-up, and update it
        if self.power_up_active and millis() - self.power_up_start_time > self.power_up_duration:
            self.power_up_active = False                
                    
    def enemyAttack(self):#choose random enemy and it will shoot a bullet
        attackFrequency = max(60, 120 - frameCount // 600 * 10)  # Decrease delay over time
        if frameCount % attackFrequency == 0 and len(self.enemies)  > 0:
            attackingEnemy = self.enemies[int(random(len(self.enemies)))]
            if attackingEnemy != None:
                self.enemyBullets.append([attackingEnemy.x, attackingEnemy.y])
                
    # reset a game when mouse clicked
    def reset_game(self):
        self.__init__()
        game.setupMenuVideo()

        loop()
        menuSound.pause()
        background(0)
        self.spaceship.move()
        self.spaceship.shoot()
        self.spaceship.display()
        self.moveEnemies()
        self.handleBullets()
        self.drawEnemies()
        self.drawShields()
        self.checkCollisions()
        self.enemyAttack()
        for explosion in self.explosions:
            if explosion['frame'] < len(self.explosionFrames):
                image(self.explosionFrames[explosion['frame']], explosion['x'] - self.explosionFrames[explosion['frame']].width / 2, explosion['y'] - self.explosionFrames[explosion['frame']].height / 2)
                explosion['frame'] += 1
            else:
                self.explosions.remove(explosion)
            
def mousePressed():
    if game.state == MENU:
        if width / 2 - 50 < mouseX < width / 2 + 50 and height / 2 - 10 < mouseY < height / 2 + 10:
            game.state = GAME
        elif width / 2 - 50 < mouseX < width / 2 + 50 and height / 2 + 20 < mouseY < height / 2 + 40:
            game.state = TUTORIAL
    elif game.state == TUTORIAL:
        game.state = MENU
        
    if game.gameover or game.game_win:
        game.reset_game()

def setup():
    game.setupMenuVideo()
    
    global shootSound, explosionSound, playerDestroyedSound, alienMoveSound, backgroundSound, menuSound
    size(600, 400)
    textAlign(CENTER, CENTER)
    minim = Minim(this)

    # Cargar los sonidos
    #
    shootSound = minim.loadFile(path + "/sounds/shoot.wav")
    explosionSound = minim.loadFile(path + "/sounds/invaderkilled.wav")
    playerDestroyedSound = minim.loadFile(path + "/sounds/explosion.wav")
    alienMoveSound = minim.loadFile(path + "/sounds/fastinvader1.wav")
    menuSound = minim.loadFile(path + "/sounds/spaceinvaders1.mpeg")
    
    global pixelFont
    pixelFont = createFont("8bitfont.ttf", 16)  # Replace '8bitFont.ttf' with your font file
    textFont(pixelFont)
    size(600, 400)


def draw():
    game.display()
    
def keyPressed():
    if keyCode == LEFT:
        game.spaceship.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.spaceship.key_handler[RIGHT] = True
    elif key == ' ':
        game.spaceship.shooting = True  # Set shooting to True when space is pressed
        
def keyReleased():
    if keyCode == LEFT:
        game.spaceship.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.spaceship.key_handler[RIGHT] = False
    elif key == ' ':
        game.spaceship.shooting = False  # Set shooting to True when space is pressed

game = Game()
