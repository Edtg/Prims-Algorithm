import random
import os
import time
import math


class Generator(object):
    def __init__(self, startx, starty, size = 11):
        StartTime = time.time()

        self.Grid = [[0 for i in range(size)] for j in range(size)]
        self.Grid[starty][startx] = 1
        self.Frontier = []
        for row in self.Grid:
            print(row)

        Pathways = 0
        self.CalculateFrontier(startx, starty)
        while (len(self.Frontier) > 0):
            self.Expand()
            self.CleanFrontier()
            #input()
            os.system("cls")
            #print("Generating Maze")
            Pathways += 1
            #self.PrintGrid()
            #for row in self.Grid:
            #    print(row)
            print("Frontier:")
            print(self.Frontier)
            #time.sleep(0.2)
        
        print("Adding loops")
        self.AddLoops(round(pow(round(size/5), 2)))
        #time.sleep(0.5)

        EndTime = time.time()

        os.system("cls")
        self.PrintGrid()
        print("Generated Maze in " + str(EndTime - StartTime) + " seconds")
        print("Maze width/height: " + str(size))
        print("Number of pathways created: " + str(Pathways))
        print("Number of loops inserted: " + str(round(pow(round(size/5), 2))))

    def SetGridValue(self, x, y, Value):
        self.Grid[y][x] = Value

    def GetGridValue(self, x, y):
        return self.Grid[y][x]

    def CalculateFrontier(self, x, y):
        print("Calculating frontier around:")
        print(x, y)
        if (x >= 0 and x <= len(self.Grid)-1 and y >= 0 and y <= len(self.Grid)-1):
            if (x - 2 >= 0 and x - 2 <= len(self.Grid)-1 and self.Grid[y][x-2] != 1):
                if (not [x-2, y] in self.Frontier):
                    self.Frontier.append([x-2, y])
                    print("Adding", x-2, y)

            if (x + 2 >= 0 and x + 2 <= len(self.Grid)-1 and self.Grid[y][x+2] != 1):
                if (not [x+2, y] in self.Frontier):
                    self.Frontier.append([x+2, y])
                    print("Adding", x+2, y)

            if (y - 2 >= 0 and y - 2 <= len(self.Grid)-1 and self.Grid[y-2][x] != 1):
                if (not [x, y-2] in self.Frontier):
                    self.Frontier.append([x, y-2])
                    print("Adding", x, y-2)

            if (y + 2 >= 0 and y + 2 <= len(self.Grid)-1 and self.Grid[y+2][x] != 1):
                if (not [x, y+2] in self.Frontier):
                    self.Frontier.append([x, y+2])
                    print("Adding", x, y+2)

        print(self.Frontier)

    def CleanFrontier(self):
        ToRemove = []
        for i in self.Frontier:
            if (self.Grid[i[1]][i[0]] == 1):
                ToRemove.append(i)
        for j in ToRemove:
            self.Frontier.remove(j)

    def GetNeighbors(self, x, y):
        Neighbors = []
        print("Neighboring:", x, y)
        if (x >= 0 and x <= len(self.Grid)-1 and y >= 0 and y <= len(self.Grid)-1):
            if (x-2 >= 0):
                if (self.Grid[y][x-2] == 1):
                    Neighbors.append([x-2, y])
            if (x+2 <= len(self.Grid)-1):
                if (self.Grid[y][x+2] == 1):
                    Neighbors.append([x+2, y])
            if (y-2 >= 0):
                if (self.Grid[y-2][x] == 1):
                    Neighbors.append([x, y-2])
            if (y+2 <= len(self.Grid)-1):
                if (self.Grid[y+2][x] == 1):
                    Neighbors.append([x, y+2])
            print(Neighbors)
        return Neighbors

    def GetDirectNeighbors(self, x, y):
        Neighbors = []
        if (x >= 0 and x <= len(self.Grid)-1 and y >= 0 and y <= len(self.Grid)-1):
            if (x-1 >= 0):
                if (self.Grid[y][x-1] == 1):
                    Neighbors.append([x-1, y])
            if (x+1 <= len(self.Grid)-1):
                if (self.Grid[y][x+1] == 1):
                    Neighbors.append([x+1, y])
            if (y-1 >= 0):
                if (self.Grid[y-1][x] == 1):
                    Neighbors.append([x, y-1])
            if (y+1 <= len(self.Grid)-1):
                if (self.Grid[y+1][x] == 1):
                    Neighbors.append([x, y+1])
        return Neighbors

    def Expand(self):
        FrontierIndex = random.randint(0, len(self.Frontier)-1)
        FE = self.Frontier[FrontierIndex]
        print("Chosen frontier:")
        print(FE)
        Neighbors = self.GetNeighbors(FE[0], FE[1])
        NeighborIndex = random.randint(0, len(Neighbors)-1)

        #x = y = 0
        #if (FE[0] == Neighbors[NeighborIndex][0]):
        #    x = FE[0]
        #    y = abs(FE[1] - Neighbors[NeighborIndex][1])
        #elif (FE[1] == Neighbors[NeighborIndex][1]):
        #    y = FE[1]
        #    x = abs(FE[0] - Neighbors[NeighborIndex][0])
        
        Mid = self.__Mid(FE, Neighbors[NeighborIndex])
        x = Mid[0]
        y = Mid[1]

        print("Midpoint:")
        print(x, y)

        self.Grid[FE[1]][FE[0]] = 1
        self.Grid[y][x] = 1

        print("Removing:", self.Frontier[FrontierIndex])
        self.Frontier.remove(FE)
        print("Removed", FE, "from frontier")

        self.CalculateFrontier(FE[0], FE[1])

    def AddLoops(self, NumLoops):
        for i in range(NumLoops):
            p1 = [round(random.randint(0, len(self.Grid)-1)/2)*2, round(random.randint(0, len(self.Grid)-1)/2)*2]
            p2 = random.choice(self.GetNeighbors(p1[0], p1[1]))
            while (self.Grid[self.__Mid(p1, p2)[0]][self.__Mid(p1, p2)[1]] == 1):
                p1 = [round(random.randint(0, len(self.Grid)-1)/2)*2, round(random.randint(0, len(self.Grid)-1)/2)*2]
                p2 = random.choice(self.GetNeighbors(p1[0], p1[1]))
            self.Grid[self.__Mid(p1, p2)[0]][self.__Mid(p1, p2)[1]] = 1

    def __Mid(self, p1, p2):
        x = y = 0
        # X is equal
        if (p1[0] == p2[0]):
            x = p1[0]
            # Calc y
            if (p1[1] > p2[1]):
                y = p2[1] + 1
            else:
                y = p1[1] + 1
        # Y is equal
        elif (p1[1] == p2[1]):
            y = p1[1]
            # Calc x
            if (p1[0] > p2[0]):
                x = p2[0] + 1
            else:
                x = p1[0] + 1

        return [x, y]

    def PrintGrid(self):
        y = 0
        #for i in range(len(self.Grid)):
        #    print(" " + str(i), end="")
        #print("\n", end="")
        for row in self.Grid:
        #    print(y, end="")
            y += 1
            for cell in row:
                if (cell == 0):
                    print(" ", end=" ")
                    #print("\u25A1", end=" ")
                elif (cell == 1):
                    print("\033[1;32;40m\u25A0\033[1;30;40m", end=" ")
                    #print("\u25A0", end=" ")
                elif (cell == 2):
                    print("\033[1;34;40m\u25A0\033[1;30;40m", end=" ")
                elif (cell == 3):
                    print("\033[1;31;40m\u25A0\033[1;30;40m", end=" ")
            print("\n", end="")


        

if (__name__ == "__main__"):
    GridSize = 15

    x = math.floor(random.randint(0,GridSize)/2)*2
    y = math.floor(random.randint(0,GridSize)/2)*2
    print("Starting at:", x, y)
    #input()

    Generator(x, y, GridSize)


