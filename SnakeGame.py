# Game of Snake
# Author: Dhruv Patel
# Purpose: Fun side project to explore PyGame and practice programming in Python

import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    rows = 15
    w = 450

    def __init__(self, start, dirnx = -1, dirny = 0, color = (0, 230, 255)):
        self.pos = start
        self.dirnx = -1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False):
        dist = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i*dist+1, j*dist+1, dist-2, dist-2))
        if eyes:
            center = dist // 2
            radius = 3
            circleMid = (i*dist+center-radius, j*dist+6)
            circleMid2 = (i*dist+dist-radius*2, j*dist+6)
            pygame.draw.circle(surface, (0, 0, 0), circleMid, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMid2, radius)

class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = -1
        self.dirny = 0

    def move(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # Rather than error, we shall reset the snek
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)


    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = -1
        self.dirny = 0

    def add_cube(self):
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def draw_grid(w, row, surface):
    size = w // row
    x = 0
    y = 0
    for i in range(row):
        x += size
        y += size
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redraw_window(surface):
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()

def random_apple(rows, snek):
    pos = snek.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), pos))) > 0:
            continue
        else:
            break

    return x, y

def msg_box(situation, msg):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(situation, msg)
    try:
        root.destroy()
    except:
        print("It ain't getting destroy")

def main():
    global width, rows, s, snack
    width = 450
    rows = 15
    s = Snake((0, 255, 0), (8, 8))
    snack = Cube(random_apple(rows, s), color=((30, 255, 30)))
    win = pygame.display.set_mode((width, width))
    clock = pygame.time.Clock()

    f = True
    while f:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_apple(rows, s), color=((30, 255, 30)))
        for i in range(len(s.body)):
            if s.body[i].pos in list(map(lambda z:z.pos, s.body[i+1:])):
                msg_box("Game Over!", "Score: %d\nPlay Again" % len(s.body))
                s.reset((8, 8))
                break

        redraw_window(win)

if __name__ == "__main__":
    main()