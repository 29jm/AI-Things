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
        else:
            self.rect.x = randrange(width-self.rect.w)
            self.rect.y = randrange(height-self.rect.h)

    def randomize(self):
        self.rect.x = randrange(width-self.rect.w)
        self.rect.y = randrange(height-self.rect.h)
        color = (randrange(255),randrange(255),randrange(255))
        self.setColor(color)

    def setColor(self, color):
        self.color = color
        self.gene = [col for col in ''.join(format(c, '08b') for c in color)]
        pxarray = pygame.PixelArray(self.image)
        pxarray.replace((255, 255, 255), color)

def crossover(mum, dad):
    if random.uniform(0, 1) < crossover_rate:
        pos = randrange(len(mum.gene))
        for i in range(pos, len(dad.gene)):
            mum.gene[i], dad.gene[i] = dad.gene[i], mum.gene[i]

def getNewPopulation(old_pop):
    pop = []
    while len(pop) < pop_size:
        for couple in itertools.combinations(old_pop, 2):
            if len(pop) >= pop_size:
                break
            crossover(couple[0], couple[1])
            pop.append(Butterfly(couple[0].color))
            pop.append(Butterfly(couple[1].color))
    return pop

size = width, height = 800, 600

screen = pygame.display.set_mode(size)

crossover_rate = 0.7
pop_size = 60
allowed_time = 1000*10 # 20 sec in millliseconds
respawn_event = pygame.USEREVENT+1

def main():
    pop = [Butterfly() for i in range(pop_size)]
    pygame.time.set_timer(respawn_event, allowed_time)

    running = True
    respawn = False
    while True:
        if respawn:
            pop = getNewPopulation(pop)
        respawn = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for butterfly in pop:
                    if butterfly.rect.collidepoint(event.pos):
                        pop.remove(butterfly)
                        break
            if event.type == respawn_event:
                respawn = True

        screen.fill((255, 255, 255))

        for butterfly in pop:
            screen.blit(butterfly.image, butterfly.rect)
        pygame.display.flip()

if __name__ == '__main__':
    main()
