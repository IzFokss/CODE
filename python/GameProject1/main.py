import pygame as py
import random

py.init()
py.mouse.set_visible(False)

WIDTH, HEIGHT = 800, 600
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Game")

GREY = (225, 225, 225)
clock = py.time.Clock()

MAX_ENEMIES = 40


# -------- PLAYER --------

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15 
        self.color = (0, 0, 255)

    def collide_with(self, x, y, radius):
        dx = x - self.x
        dy = y - self.y
        return dx*dx + dy*dy <= (self.radius + radius) ** 2

    def draw(self):
        py.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


# -------- ENEMY --------

class Enemy:
    def __init__(self, enemies):
        self.radius = 25   
        self.color = (255, 0, 0)
        self.spawn(enemies)

    def spawn(self, enemies):
        while True:
            side = random.choice(["left", "right", "top", "bottom"])

            if side == "left":
                x = -self.radius
                y = random.randint(0, HEIGHT)

            elif side == "right":
                x = WIDTH + self.radius
                y = random.randint(0, HEIGHT)

            elif side == "top":
                x = random.randint(0, WIDTH)
                y = -self.radius

            else:
                x = random.randint(0, WIDTH)
                y = HEIGHT + self.radius

            overlap = False
            for e in enemies:
                dx = x - e.x
                dy = y - e.y
                if dx*dx + dy*dy < (self.radius + e.radius + 10)**2:
                    overlap = True
                    break

            if not overlap:
                self.x = x
                self.y = y
                break

    def move(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist != 0:
            self.x += dx / dist * 2
            self.y += dy / dist * 2

    def update(self, player):
        self.move(player)

    def draw(self):
        py.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


# -------- GAME --------

player = Player(400, 300)
enemies = []

spawn_delay = 3000
min_delay = 500
last_spawn = py.time.get_ticks()

running = True

while running:
    clock.tick(60)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

        if event.type == py.MOUSEMOTION:
            player.x, player.y = event.pos

    # -------- SPAWN SYSTEM --------
    current_time = py.time.get_ticks()

    if current_time - last_spawn > spawn_delay and len(enemies) < MAX_ENEMIES:
        enemies.append(Enemy(enemies))
        last_spawn = current_time

        spawn_delay *= 0.95
        if spawn_delay < min_delay:
            spawn_delay = min_delay

    # -------- UPDATE --------
    for enemy in enemies:
        enemy.update(player)

    # anti overlap en jeu
    for i, e1 in enumerate(enemies):
        for e2 in enemies[i+1:]:
            dx = e2.x - e1.x
            dy = e2.y - e1.y
            dist_sq = dx*dx + dy*dy
            min_dist = e1.radius + e2.radius

            if dist_sq < min_dist**2 and dist_sq != 0:
                dist = dist_sq ** 0.5
                overlap = (min_dist - dist) / 2

                e1.x -= dx / dist * overlap
                e1.y -= dy / dist * overlap
                e2.x += dx / dist * overlap
                e2.y += dy / dist * overlap

    # -------- COLLISIONS --------
    for enemy in enemies:
        if player.collide_with(enemy.x, enemy.y, enemy.radius):
            print("GAME OVER")
            running = False

    # -------- DRAW --------
    screen.fill(GREY)

    player.draw()

    for enemy in enemies:
        enemy.draw()

    py.display.update()

py.quit()