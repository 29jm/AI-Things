#!/usr/bin/python3

import pygame, sys
from random import randrange
import random
import itertools

class Butterfly(pygame.sprite.Sprite):
    def __init__(self, color=None, position=None):
        self.image = pygame.image.load('butterfly.png')
        self.rect = self.image.get_rect()
        if color == None:
            self.randomize()
        else:
            self.setColor(color)
            if position != None:
                self.rect.x = position.x
                self.rect.y = position.y

    def randomize(self):
        self.rect.x = randrange(width-self.rect.w)
        self.rect.y = randrange(height-self.rect.h)
        rdcolor = (randrange(255),randrange(255),randrange(255))
        self.setColor(rdcolor)

    def setColor(self, color):
        self.color = [col for col in ''.join(format(c, '08b') for c in color)]
        pxarray = pygame.PixelArray(self.image)
        pxarray.replace((255, 255, 255), color)

def crossover(mum, dad):
    if random.uniform(0, 1) < crossover_rate:
        pos = randrange(len(mum.color))
        for i in range(pos, len(dad.color)):
            mum.color[i], dad.color[i] = dad.color[i], mum.color[i]

def getNewPopulation(old_pop):
    pop = []
    for couple in itertools.combinations(old_pop, 2):
        if len(pop) >= pop_size:
            break
        crossover(couple[0], couple[1])
        pop.append(couple[0])
        pop.append(couple[1])
    return pop

size = width, height = 800, 600

screen = pygame.display.set_mode(size)

crossover_rate = 0.7
pop_size = 30
allowed_time = 1000*15 # 20 sec in millliseconds
timer_event = pygame.USEREVENT+1

def main():
    population = [Butterfly() for i in range(pop_size)]
    pygame.time.set_timer(timer_event, allowed_time)
    while True:
        if len(population) <= 1:
            print("You've extermined this butterfly specy !")
        timed_out = False
        print("outside timed loop")
        while not timed_out:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("exiting...")
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for b in population:
                        if b.rect.collidepoint(event.pos):
                            population.remove(b)
                            break
                if event.type == timer_event:
                    print(len(population))
                    population = getNewPopulation(population)
                    print(len(population))
                    timed_out = True
            screen.fill((255, 255, 255))
            for b in population:
                screen.blit(b.image, b.rect)
            pygame.display.flip()
            pygame.time.delay(10)

if __name__ == '__main__':
    main()
