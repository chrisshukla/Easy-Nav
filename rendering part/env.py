import math
import pygame

class buildEnviroment:
    def __init__(self,MapDimensions):
        #initialization of pygame instance
        pygame.init()
        #since it is just a 2d points in a 2d space
        self.pointcloud=[]
        #loading the image onto the the project screen
        self.externalMap=pygame.image.load("R1.jpg")
        self.maph, self.mapw = MapDimensions
        self.mapWindowname="Path planning"
        pygame.display.set_caption(self.mapWindowname)
        #creates a visible surface on the monitor blank page
        self.map=pygame.display.set_mode((self.mapw,self.maph))
        #places an image object on the screen on the vblank page
        self.map.blit(self.externalMap,[0,0])
        #colors declaration
        self.black=(0,0,0)
        self.grey=(70,70,70)
        self.blue=(0,0,255)
        self.Green=(0,255,0)
        self.red=(255,0,0)
        self.white=(255,255,255)

    def add2pos(self,distance,angle,robotPosition):
        #coverts row angle distance into cartesian coordinates
        x= distance * math.cos(angle) + robotPosition[0]
        y= -distance * math.sin(angle)+robotPosition[1]
        return(int(x),int(y))

#passed from sensed object
    def dataStorage(self,data):
        print(len(self.pointcloud))
        for element in data:
            #takes the data and passes to the add2pos method
            point=self.add2pos(element[0],element[1],element[2])
            #checks for the duplicate
            if point not in self.pointcloud:
                self.pointcloud.append(point)

    def show_sensordata(self):
        self.infomap=self.map.copy()
        #for drawing the data in a new map
        for point in self.pointcloud:
            #which will first be intialized to the main map
            self.infomap.set_at((int(point[0]),int(point[1])),(255,0,0))