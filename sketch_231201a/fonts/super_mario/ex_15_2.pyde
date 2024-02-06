import random

class Particle:
    
    def __init__(self, cx, cy, d, r):
        self.x = 0
        self.y = 0
        self.d = d
        self.cx = cx
        self.cy = cy
        self.r = r
        self.theta = 0
    
    def update(self):
        self.r -= 0.2
        self.theta = (self.theta + 0.1) % 6.28
        self.x = self.cx + self.r * cos(self.theta)
        self.y = self.cy + self.r * sin(self.theta)
    
    def display(self):
        if self.r > 0:
            fill(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            ellipse(self.x, self.y, self.d, self.d)
    
def setup():
    size(600, 600)
    strokeWeight(0)
    background(255)

def draw():
    for particle in particles:
        particle.update()
        particle.display()
    
def mouseClicked():
    particles.append(Particle(mouseX, mouseY, 10, 100))

particles = []
