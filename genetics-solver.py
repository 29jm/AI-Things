#!/usr/bin/python3

import random
import math
import sys
from itertools import zip_longest

class Chromosome:
    def __init__(self):
        self.genes = ['0001', '0010',
                      '0011', '0100',
                      '0101', '0110',
                      '0111', '1000',
                      '1001',
                      '1010', '1011',
                      '1100', '1101']
        self.chromo_length = 400
        self.gene_length = 4
        self.chromo = self.randomChromo()
        self.value = self.decode()

    def randomChromo(self):
        chromo = []
        for i in range(0, self.chromo_length, self.gene_length):
            for c in self.randomNum():
                chromo.append(c)
            for c in self.randomOp():
                chromo.append(c)
        return chromo[:len(chromo)-4] # Pop last operator

    def decode(self):
        needOperator = False
        self.equation = ""
        for gene in grouper(self.gene_length, self.chromo):
            try:
                val = int(''.join(gene), 2)
            except:
                continue
            if needOperator:
                if val < 10:
                    continue
                else:
                    if val == 10:
                        self.equation += "+"
                    elif val == 11:
                        self.equation += "-"
                    elif val == 12:
                        self.equation += "*"
                    elif val == 13:
                        self.equation += "//"
                    else:
                        continue
                    needOperator = False
            else:
                if val > 9:
                    continue
                else:
                    self.equation += str(val)
                    needOperator = True
        if not needOperator:
            if self.equation[len(self.equation)-1] == '/':
                self.equation = self.equation[:len(self.equation)-2] # Remove last operator
            else:
                self.equation = self.equation[:len(self.equation)-1] # Remove last operator
        while self.equation.find("//0") != -1:
            self.equation = self.equation.replace("//0", "+0")
        return eval(self.equation)

    def getFitness(self, searched_value):
        if self.value == searched_value:
            return 10
        else:
            return 1/math.fabs(searched_value-self.value)

    def randomNum(self):
        return self.genes[random.randrange(0, 9)]

    def randomOp(self):
        return self.genes[random.randrange(9, len(self.genes))]

def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

def crossover(mum, dad):
    if random.uniform(0, 1) < crossover_rate:
        pos = random.randrange(len(mum.chromo))
        for i in range(pos, len(dad.chromo)):
            mum.chromo[i], dad.chromo[i] = dad.chromo[i], mum.chromo[i]

def mutate(chromo):
    for i in range(len(chromo.chromo)):
        if random.uniform(0, 1) < mutation_rate:
            chromo.chromo[i] = 0 if chromo.chromo[i] else 1

def roulette(chromos, sum_fitness):
    part = random.uniform(0, sum_fitness)
    value = 0
    for c in chromos:
        if value > part:
            return c
        value += c.getFitness(searched_value)
    highest = getBestChromosome(chromos)
    print("Closest:", highest.value)
    return highest

def getBestChromosome(chromos):
    highest = chromos[0]
    for c in chromos:
        if c.getFitness(searched_value) > highest.getFitness(searched_value):
            highest = c
    return highest

pop_size = 100
crossover_rate = 0.7
mutation_rate = 0.001
max_generation = 300
searched_value = 1505

def main():
    searched_value = int(sys.argv[1]) if len(sys.argv) > 1 else 555
    population = [Chromosome() for i in range(pop_size)]
    found = False
    generation = 1
    while not found and generation < max_generation:
        new_population = []
        while len(new_population) < pop_size:
            sum_fitness = 0
            for c in population:
                fit = c.getFitness(searched_value)
                if fit == 10:
                    found = True
                sum_fitness += fit
            winner1 = roulette(population, sum_fitness)
            winner2 = roulette(population, sum_fitness)

            crossover(winner1, winner2)
            mutate(winner1)
            mutate(winner2)

            winner1.value = winner1.decode()
            winner2.value = winner2.decode()

            new_population.append(winner1)
            new_population.append(winner2)
        print("generation", generation)
        generation += 1
    if generation >= max_generation:
        print("Solution not found, closest:", getBestChromosome(population).value)
    else:
        print("Solution found in", generation, "generations")

if __name__ == '__main__':
    main()
