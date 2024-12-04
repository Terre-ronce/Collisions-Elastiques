import pygame

# classe Etincelle pour gérer les étincelles
class Etincelle:
    def __init__(self, x, y, color, lifespan, velocity):
        self.x = x
        self.y = y
        self.color = color
        self.lifespan = lifespan
        self.velocity = velocity

    def update(self):
        # Déplace la particule selon sa vitesse
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        # Réduit la durée de vie
        self.lifespan -= 1

    def draw(self, surface):
        if self.lifespan > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 1)