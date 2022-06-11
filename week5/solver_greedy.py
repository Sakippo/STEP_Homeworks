#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    
    '''
    for i in range(N-1):
        for j in range(i+2,N):
            i_a = tour[i]
            i_b = tour[i+1]
            j_a = tour[j]
            j_b = tour[(j+1)%N]

            if((distance(i_a,i_b)+distance(j_a,j_b)) > (distance(i_a,j_a)+distance(i_b,j_b))): 
                tour[i+1] = j_a 
                tour[j] = i_b
    '''
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
