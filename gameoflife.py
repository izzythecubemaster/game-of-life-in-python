#!/usr/bin/env python

import curses
import time
import copy
from random import randint
from optparse import OptionParser
from sys import exit


VERSION = "%prog 1.0.0"

DESCRIPTION = """Tommi Asiala's implementation of John Conway's Game of Life in
Python. When running, press any to quit. """

LICENSE = """This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

class Table:

    def __init__(self, height, width, rand_max, table=None):
        if table:
            self.table = table
            self.height = len(table)
            self.width = len(table[0])
        else:
            self.table = []
            self.height = height
            self.width = width
            for y in range(0,self.height):
                self.table.append([])
                for x in range(0,self.width):
                    rand = randint(0,rand_max)
                    if rand == 0:
                        self.table[y].append(1)
                    else:
                        self.table[y].append(0)

    def draw(self, screen):
        """(Re)draw table to screen."""
        y = 0
        x = 0
        for row in self.table:
            for col in row:
                if col == 0:
                    screen.addstr(y, x, ".")
                else:
                    screen.addstr(y, x, "o")
                x = x + 1
            y = y + 1
            x = 0

    def liveNeighbours(self, y, x):
        """Returns the number of live neighbours."""
        count = 0
        if y > 0:
            if self.table[y-1][x]:
                count = count + 1
            if x > 0:
                if self.table[y-1][x-1]:
                    count = count + 1
            if self.width > (x + 1):
                if self.table[y-1][x+1]:
                    count = count + 1

        if x > 0:
            if self.table[y][x-1]:
                count = count + 1
        if self.width > (x + 1):
            if self.table[y][x+1]:
                count = count + 1

        if self.height > (y + 1):
            if self.table[y+1][x]:
                count = count + 1
            if x > 0:
                if self.table[y+1][x-1]:
                    count = count + 1
            if self.width > (x + 1):
                if self.table[y+1][x+1]:
                    count = count + 1

        return count

    def turn(self):
        """Turn"""
        nt = copy.deepcopy(self.table)
        for y in range(0, self.height):
            for x in range(0, self.width):
                neighbours = self.liveNeighbours(y, x)
                if self.table[y][x] == 0:
                    if neighbours == 3:
                        nt[y][x] = 1
                else:
                    if (neighbours < 2) or (neighbours > 3):
                        nt[y][x] = 0
        self.table = nt

def life(self, screen, height, width, refresh, random, table):

    t = Table(height, width, random, table)
    while(1):
        t.draw(screen)
        t.turn()
        screen.refresh()
        time.sleep(refresh/100.0)
        c = screen.getch()
        if c != -1:
            break

def readTableFromFile(file):
    f = open(file, "r")
    table = []

    yy = 0
    for line in f.readlines():
        table.append([])
        for col in range(0, len(line)):
            if line[col] == "o":
                table[yy].append(1)
            else:
                table[yy].append(0)
        yy = yy + 1

    f.close()

    return table

if __name__ == '__main__':
    parser = OptionParser(version=VERSION, description=DESCRIPTION,)
    parser.add_option("--table",
            dest="file", help="Read table from the FILE")
    parser.add_option("--license", action="store_true", default=False,
           dest="license", help="Print the GPLv3 license")
    parser.add_option("--width", type="int",
           dest="width", help="Table width")
    parser.add_option("--height", type="int",
            dest="height", help="Table height")
    parser.add_option("--refresh", type="int",
            dest="refresh", help="Refresh rate in 1/100s")
    parser.add_option("--random", type="int",
            dest="random",
            help="Likelyhood of initial table containing living cells: 1/(RANDOM+1). Minimum: 1") 
    (options,args) = parser.parse_args()

    if options.license:
        print LICENSE
        exit(0)

    if options.height:
        height = options.height
    else:
        height = 10
    if options.width:
        width = options.width
    else:
        width = 10
    if options.random:
        random = options.random
    else:
        random = 4
    if options.refresh:
        refresh = options.refresh
    else:
        refresh = 100
    if options.file:
        table = readTableFromFile(options.file)
    else:
        table = None

    stdscr = curses.initscr()
    stdscr.nodelay(1)
    curses.wrapper(life, stdscr, height, width, refresh, random, table)
