#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def swap(tour,left,right):
    a = tour[left]
    tour[left] = tour[right]
    tour[right] = a

def solve(cities,start):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = start
    unvisited_cities = set(range(0, N))
    unvisited_cities.discard(current_city)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    
    count = 1
    while(count !=0): #swapがなくなるまで繰り返す
        count = 0
        for i in range(N-1):
            for j in range(i+2,N):
                i_a = tour[i]
                i_b = tour[i+1]
                j_a = tour[j]
                j_b = tour[(j+1)%N]

                if((dist[i_a][i_b]+dist[j_a][j_b]) > (dist[i_a][j_a]+dist[i_b][j_b])): #辺を結び変えた後の方が短い時
                    left = i+1
                    right = j
                    while(left < right): 
                        #辺を結び変える(i+1~jの辺も逆方向に繋ぐ)
                        swap(tour,left,right) 
                        count += 1 #swapの回数をカウント
                        left += 1
                        right -= 1 
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
