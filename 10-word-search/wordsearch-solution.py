import string
import re
import collections
import copy
import os

from enum import Enum
Direction = Enum('Direction', 'left right up down upleft upright downleft downright')
    
delta = {Direction.left: (0, -1),Direction.right: (0, 1), 
         Direction.up: (-1, 0), Direction.down: (1, 0), 
         Direction.upleft: (-1, -1), Direction.upright: (-1, 1), 
         Direction.downleft: (1, -1), Direction.downright: (1, 1)}

cat = ''.join
wcat = ' '.join
lcat = '\n'.join

def empty_grid(w, h):
    return [['.' for c in range(w)] for r in range(h)]

def show_grid(grid):
    return lcat(cat(r) for r in grid)

def indices(grid, r, c, l, d):
    dr, dc = delta[d]
    w = len(grid[0])
    h = len(grid)
    inds = [(r + i * dr, c + i * dc) for i in range(l)]
    return [(i, j) for i, j in inds
           if i >= 0
           if j >= 0
           if i < h
           if j < w]


def gslice(grid, r, c, l, d):
    return [grid[i][j] for i, j in indices(grid, r, c, l, d)]


def set_grid(grid, r, c, d, word):
    for (i, j), l in zip(indices(grid, r, c, len(word), d), word):
        grid[i][j] = l
    return grid


def present_many(grid, words):
    w = len(grid[0])
    h = len(grid)
    wordlens = set(len(w) for w in words)
    presences = []
    for r in range(h):
        for c in range(w):
            for d in Direction:
                for wordlen in wordlens:
                    word = cat(gslice(grid, r, c, wordlen, d))
                    if word in words:
                        presences += [(word, r, c, d)]
    return set(presences)



def read_wordsearch(fn):
    lines = [l.strip() for l in open(fn).readlines()]
    w, h = [int(s) for s in lines[0].split('x')]
    grid = lines[1:h+1]
    words = set(lines[h+1:])
    return w, h, grid, words




# ## Part 1


def found_words_length(puzzle):
    width, height, grid, words = puzzle
    return sum(len(p[0]) for p in present_many(grid, words))

def total_found_words_length(puzzles):
    return sum(found_words_length(p) for p in puzzles)






# ## Part 2


def unused_vowels(puzzle, presences):
    width, height, grid, words = puzzle
    
    unused_grid = [[c for c in r] for r in grid]
    for w, r, c, d in presences:
        set_grid(unused_grid, r, c, d, '.' * len(w))
    unused_vowel_count = sum(1 for l in unused_grid for c in l if c in 'aeiou')
    return unused_vowel_count


puzzle = read_wordsearch('10-wordsearch.txt')

width, height, grid, words = puzzle
presences = present_many(grid, words)
# found_words = [p[0] for p in presences]

print("Part 1: Found {} words".format(len(presences)))
print("Part 2: {} unused vowels".format(unused_vowels(puzzle, presences)))
