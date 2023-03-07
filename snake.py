import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0] # i stands for row
        j = self.pos[1]    # j stands for column

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:
            centre = dis // 2
            radius = 3
            circle_Middle = (i*dis+centre-radius, j*dis+8)
            circle_Middle_2 = (i*dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_Middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_Middle_2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

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



    def reset (self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_Cube (self):
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny
        if dx == 1 and dy == 0:    # all this is checking where snake is going and where to add new cube
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate (self.body):
            if i == 0 :
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_Grid(w, rows, surface):
    size_Between = w // rows   # width / rows, // division = answer rounded

    x = 0
    y = 0
    for l in range(rows):
        x = x + size_Between
        y = y + size_Between

        pygame.draw.line(surface, (255, 255, 255), (x,0), (x, w)) # vertical line with start and end position
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y)) # horizontal line with start and end position


def redraw_Window(surface):
    global row, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    draw_Grid(width, rows, surface)
    pygame.display.update()


def random_Snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:   # checkig to not put snack on the snake
            continue
        else:
            break
    return (x, y)


def message_Box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(random_Snack(rows, s), color = (0, 255, 0))
    clock = pygame.time.Clock()
    flag = True

    while flag:
        pygame.time.delay(50)        #delaying everything by 50 ms (the lower this goes, the faster its going to be)
        clock.tick(10)    #clock.tick (10) means 10fps (the lower this goes, the slower its going to be)
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_Cube()
            snack = cube(random_Snack(rows, s), color = (0, 255, 0))

        for x in range(len(s.body)) :
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1: ])):
                print('Score: ', len(s.body))
                message_Box('YOU LOST ! ', 'Play again :)')
                s.reset((10, 10))
                break

        redraw_Window(win)


    pass

rows = 20
width = 500
height = 500



main()















