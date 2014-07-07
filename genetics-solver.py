#!/usr/bin/python3

import random
import math
import sys
from itertools import zip_longest

class Equation:
    """Creates a random sequence of numbers and operators.
    Each number/operator is represented with a binary string."""
    def __init__(self):
        self.genes = ['0001', '0010', # Numbers from 1 to 9
                      '0011', '0100',
                      '0101', '0110',
                      '0111', '1000',
                      '1001',
                      '1010', '1011', # Operators [+-/*]
                      '1100', '1101']
        self.chromo_length = 400
        self.gene_length = 4
        self.chromo = self.randomChromo()
        self.value = self.decode()

    def randomChromo(self):
        """Returns a binary string representing a random equation."""
        chromo = []
        for i in range(0, self.chromo_length, self.gene_length):
            for c in self.randomNum():
                chromo.append(c)
            for c in self.randomOp():
                chromo.append(c)
        return chromo[:len(chromo)-4] # Pop last operator

    def decode(self):
        """Returns the value of the equation, skipping any unknown gene."""
        needOperator = False
        self.equation = ""
        for gene in grouper(self.gene_length, self.chromo):
            try:
                val = int(''.join(gene), 2) # the last gene contains an integer for an unknown reason
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
                        self.equation += "//" # Integer division
                    else:
                        continue
                    needOperator = False
            else:
                self.equation += str(val) # Don't check for val > 9
                needOperator = True
        if not needOperator:
            if self.equation[len(self.equation)-1] == '/':
                self.equation = self.equation[:len(self.equation)-2] # Remove last '//'
            else:
                self.equation = self.equation[:len(self.equation)-1] # Remove last operator
        self.equation = self.equation.replace("//0", "+0") # Remove any zero division
        value = 0
        try:
            value = eval(self.equation)
        except:
            value = 0
        return value

    def getFitness(self, searched_value):
        """Returns a number between 0 and 1, 1 being searched_value."""
        if self.value == searched_value:
            return 1
        else:
            return 1/math.fabs(searched_value-self.value)

    def randomNum(self):
        """Returns a random number in its binary form."""
        return self.genes[random.randrange(0, 9)]

    def randomOp(self):
        """Returns a random operator in its binary form."""
        return self.genes[random.randrange(9, len(self.genes))]

def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

def crossover(mum, dad):
    """Mix the 2 equations at a random point. Happens depending
    on the crossover rate."""
    if random.uniform(0, 1) < crossover_rate:
        pos = random.randrange(len(mum.chromo))
        for i in range(pos, len(dad.chromo)):
            mum.chromo[i], dad.chromo[i] = dad.chromo[i], mum.chromo[i]

def mutate(chromo):
    """Gives each gene in the chromosome a chance to swap its value."""
    for i in range(len(chromo.chromo)):
        if random.uniform(0, 1) < mutation_rate:
            chromo.chromo[i] = 0 if chromo.chromo[i] else 1

def roulette(chromos, sum_fitness):
    """Returns a random equation in chromos, giving more chances to
    the best fitting ones."""
    part = random.uniform(0, sum_fitness)
    value = 0
    for c in chromos:
        if value >= part:
            return c
        value += c.getFitness(searched_value)
    highest = getBestEquation(chromos) # Sometimes the above fails, so return the best one
    return highest

def getBestEquation(chromos):
    """Returns the best fitting equation in chromos."""
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
default = 555

def main():
    searched_value = int(sys.argv[1]) if len(sys.argv) > 1 else default
    population = [Equation() for i in range(pop_size)]
    solution = None
    generation = 1
    while solution == None and generation < max_generation:
        new_population = []
        while len(new_population) < pop_size:
            sum_fitness = 0
            for c in population: # Check for solution and get the fitness sum
                fit = c.getFitness(searched_value)
                if fit == 1:
                    solution = c
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
            if generation % 10 == 0 and len(new_population) >= pop_size:
                print("Closest value:", getBestEquation(population).value)
        print("Generation", generation)
        generation += 1
    if generation >= max_generation:
        closest = getBestEquation(population)
        print("Solution (",searched_value,") not found, closest:", closest.value)
        print(closest.equation)
    else:
        print("Solution (",searched_value,") found in", generation, "generations:")
        print(solution.equation)

if __name__ == '__main__':
    main()
