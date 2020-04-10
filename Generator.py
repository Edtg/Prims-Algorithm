import random
import os
import time
import math
from PIL import Image

SHOWLOGS = False
SHOWMAZEDEVELOPMENT = False
SHOWFINALMAZE = True

def PrintLog(string):
    if SHOWLOGS:
        print(string)

class Generator(object):
    def __init__(self, startx, starty, sizex = 11, sizey = 11):
        self.Grid = [[0 for i in range(sizex)] for j in range(sizey)]
        self.Grid[starty][startx] = 1
        self.Frontier = []
        self.sizex = sizex
        self.sizey = sizey
        for row in self.Grid:
            PrintLog(row)

        self.CalculateFrontier(startx, starty)
        while (len(self.Frontier) > 0):
            self.Expand()
            self.CleanFrontier()
            if SHOWMAZEDEVELOPMENT:
                os.system("cls")
                self.PrintGrid()
            PrintLog("Frontier:")
            PrintLog(self.Frontier)
        
        PrintLog("Adding loops")
        self.AddLoops(math.floor(math.sqrt(sizex*sizey)-1/2))

        if SHOWFINALMAZE:
            os.system("cls")
            self.PrintGrid()
        
        self.SaveImage()


    def CalculateFrontier(self, x, y):
        PrintLog("Calculating frontier around:")
        PrintLog(str(x) + str(y))
        if (x >= 0 and x <= self.sizex-1 and y >= 0 and y <= self.sizey-1):
            if (x - 2 >= 0 and x - 2 <= self.sizex-1 and self.Grid[y][x-2] != 1):
                if (not [x-2, y] in self.Frontier):
                    self.Frontier.append([x-2, y])
                    PrintLog("Adding" + str(x-2) + str(y))

            if (x + 2 >= 0 and x + 2 <= self.sizex-1 and self.Grid[y][x+2] != 1):
                if (not [x+2, y] in self.Frontier):
                    self.Frontier.append([x+2, y])
                    PrintLog("Adding" + str(x+2) + str(y))

            if (y - 2 >= 0 and y - 2 <= self.sizey-1 and self.Grid[y-2][x] != 1):
                if (not [x, y-2] in self.Frontier):
                    self.Frontier.append([x, y-2])
                    PrintLog("Adding" + str(x) + str(y-2))

            if (y + 2 >= 0 and y + 2 <= self.sizey-1 and self.Grid[y+2][x] != 1):
                if (not [x, y+2] in self.Frontier):
                    self.Frontier.append([x, y+2])
                    PrintLog("Adding" + str(x) + str(y+2))

        PrintLog(self.Frontier)

    def CleanFrontier(self):
        ToRemove = []
        for i in self.Frontier:
            if (self.Grid[i[1]][i[0]] == 1):
                ToRemove.append(i)
        for j in ToRemove:
            self.Frontier.remove(j)

    def GetNeighbors(self, x, y):
        Neighbors = []
        PrintLog("Neighboring:" + str(x) + str(y))
        if (x >= 0 and x <= self.sizex-1 and y >= 0 and y <= self.sizey-1):
            if (x-2 >= 0):
                if (self.Grid[y][x-2] == 1):
                    Neighbors.append([x-2, y])
            if (x+2 <= self.sizex-1):
                if (self.Grid[y][x+2] == 1):
                    Neighbors.append([x+2, y])
            if (y-2 >= 0):
                if (self.Grid[y-2][x] == 1):
                    Neighbors.append([x, y-2])
            if (y+2 <= self.sizey-1):
                if (self.Grid[y+2][x] == 1):
                    Neighbors.append([x, y+2])
            PrintLog(Neighbors)
        return Neighbors

    def Expand(self):
        FrontierIndex = random.randint(0, len(self.Frontier)-1)
        FE = self.Frontier[FrontierIndex]
        PrintLog("Chosen frontier:")
        PrintLog(FE)
        Neighbors = self.GetNeighbors(FE[0], FE[1])
        NeighborIndex = random.randint(0, len(Neighbors)-1)

        Mid = self.__Mid(FE, Neighbors[NeighborIndex])
        x = Mid[0]
        y = Mid[1]

        PrintLog("Midpoint:")
        PrintLog(str(x) + str(y))

        self.Grid[FE[1]][FE[0]] = 1
        self.Grid[y][x] = 1

        PrintLog("Removing:" + str(self.Frontier[FrontierIndex]))
        self.Frontier.remove(FE)
        PrintLog("Removed" + str(FE) + str("from frontier"))

        self.CalculateFrontier(FE[0], FE[1])

    def AddLoops(self, NumLoops):
        for i in range(NumLoops):
            p1 = [round(random.randint(0, self.sizex-1)/2)*2, round(random.randint(0, self.sizey-1)/2)*2]
            print(p1)
            p2 = random.choice(self.GetNeighbors(p1[0], p1[1]))
            while (self.Grid[self.__Mid(p1, p2)[1]][self.__Mid(p1, p2)[0]] == 1):
                p1 = [round(random.randint(0, self.sizex-1)/2)*2, round(random.randint(0, self.sizey-1)/2)*2]
                p2 = random.choice(self.GetNeighbors(p1[0], p1[1]))
            self.Grid[self.__Mid(p1, p2)[1]][self.__Mid(p1, p2)[0]] = 1

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
        for row in self.Grid:
            for cell in row:
                if (cell == 0):
                    print(" ", end=" ")
                    #print("\u25A1", end=" ")
                else:
                    print("\u25A0", end=" ")
            print("\n", end="")

    def SaveImage(self):
        imgname = input("Enter a name to save the image as: ")
        cellsize = 0
        while cellsize == 0:
            try:
                max = 100
                cellsize = int(input("Enter a size for the cells between 1 and " + str(max) + ": "))
                if cellsize <= 0 or cellsize > max:
                    cellsize = 0
            except:
                cellsize = 0

        with Image.new("RGB", (self.sizex+2, self.sizey+2), (255,255,255)) as img:
            imgpixels = img.load()

            for border in range(img.size[0]):
                imgpixels[border,0] = (0,0,0)
                imgpixels[border,img.size[1]-1] = (0,0,0)
            for border in range(img.size[1]):
                imgpixels[0,border] = (0,0,0)
                imgpixels[img.size[0]-1,border] = (0,0,0)
            for row in range(len(self.Grid)):
                for cell in range(len(self.Grid[row])):
                    if self.Grid[row][cell] == 0:
                        imgpixels[cell+1,row+1] = (70,100,150)
                    else:
                        imgpixels[cell+1,row+1] = (255,255,255)
            
            img = img.resize(((self.sizex+2) * cellsize, (self.sizey+2) * cellsize), Image.BOX)
            img.show()
            img.save("mazes/" + imgname + ".jpg")
            img.close()


        


GridSizex = 0
GridSizey = 0

while GridSizex < 3 or GridSizey < 3:
    try:
        GridSizex = (round(int(input("Enter the width of the maze: "))/2)*2)+1
        GridSizey = (round(int(input("Enter the height of the maze: "))/2)*2)+1
    except:
        print("Enter an integer more than 3")

x = math.floor(random.randint(0,GridSizex)/2)*2
y = math.floor(random.randint(0,GridSizey)/2)*2
PrintLog("Starting at:" + str(x) + str(y))
if SHOWLOGS:
    input()

Generator(x, y, GridSizex, GridSizey)


