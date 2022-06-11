#!/usr/bin/env python3

from common import format_tour, read_input

import solver_greedy
import solver_random
import solver_two_opt
from solver_two_opt import distance

CHALLENGES = 7


def generate_sample_output():
    for i in range(CHALLENGES):
        if i == 0:
            N = 5
        elif i == 1:
            N = 8
        elif i == 2:
            N = 16
        elif i == 3:
            N = 64
        elif i == 4:
            N = 128
        elif i == 5:
            N = 512
        else:
            N = 1 #N=2048の時は計算量が大きすぎるため始点は0に固定

        min_length = 10 ** 7
        min_j = 0
        tour = []
        solver = solver_two_opt
        name = 'output'
        cities = read_input(f'input_{i}.csv')

        for j in range(N):
            #始点を変えて一番pathが短いものを記録
            tour = solver.solve(cities,j)
            path_length = sum(distance(cities[tour[i]], cities[tour[(i + 1) % N]]) for i in range(len(tour)))
            if path_length < min_length:
                min_length = path_length
                min_j = j

        tour = solver.solve(cities, min_j)

        with open(f'{name}_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')

        '''
        for solver, name in ((solver_random, 'random'), (solver_greedy, 'greedy')):
            tour = solver.solve(cities)
            with open(f'sample/{name}_{i}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')
        '''

if __name__ == '__main__':
    generate_sample_output()
