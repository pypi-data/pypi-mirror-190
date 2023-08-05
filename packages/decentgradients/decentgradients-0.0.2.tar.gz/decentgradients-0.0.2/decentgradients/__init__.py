from pyeasyga import pyeasyga


def add_numbers(num1, num2):
    return num1 + num2


def subtract_numbers(num1, num2):
    return num1 - num2


def multiply_numbers(num1, num2):
    return num1 * num2


def divide_numbers(num1, num2):
    return num1 / num2


data = [('pear', 50), ('apple', 35), ('banana', 40)]

ga = pyeasyga.GeneticAlgorithm(data)        # initialise the GA with data


def fitness(individual, data):
    fitness = 0
    if individual.count(1) == 2:
        for selected, (fruit, weight) in zip(individual, data):
            if selected:
                fitness += weight
    return fitness


ga.fitness_function = fitness               # set the GA's fitness function


ga.run()                                    # run the GA
