import pygame
import numpy as np
import math

def uncertanity_add(distance,angle,sigma):
    mean=np.array([distance,angle])

#here we created a matrix where its diagonal elems are the uncertanity
    covariance=np.diag(sigma **2)

#this random.multivariate_normal generates random variable around the mean value
    distance,angle=np.random.multivariate_normal(mean,covariance)

    #for not getting negative values
    distance=max(distance,0)
    angle=max(angle,0)
    return [distance,angle]

#we add uncertanity because the output we get is not perfect
class LaserSensor:
    def __init__(self,Range,map,Uncertanity):
        self.Range=Range

        #rounds per seconds
        self.speed=4

        #sigma is the sensor measurement noise since the output is in distances and angles
        #sigma is the defined uncertanity
        self.sigma=np.array([Uncertanity[0],Uncertanity[1]])

        #initial position is 0,0
        self.position=(0,0)
        self.map=map

        #window dimensions
        self.w, self.h=pygame.display.get_surface().get_size()
        #A list to store the point cloud
        self.sensedObstacles=[]

        #we need to measure the distances between two points in 2d plane eucledian distance formula
    def distance(self,obstaclePosition):
        px=(obstaclePosition[0]-self.position[0])**2
        py=(obstaclePosition[1]-self.position[1])**2
        return math.sqrt(px+py)

    def sense_object(self):
        data=[]
        x1,y1=self.position[0],self.position[1]
        for angle in np.linspace(0,2*math.pi, 60,False):
            #we calculate the cords of these points that represents the end of the line segment
            x2,y2=(x1+self.Range * math.cos(angle), y1-self.Range * math.sin(angle))

        #Sampling:
            for i in range(0,100):
        #we calculate the cords for the points in the line segments
                u=i/100


        #interpolation formula
        #for calculating the coords of our point in the line segment
                x=int(x2 * u + x1 *(1-u))
                y=int(y2 * u + y1  *(1-u))
        #if point within the window
                if 0<x<self.w and 0<y<self.h:
                    color=self.map.get_at((x,y))
                    if(color[0],color[1],color[2])==(0,0,0):
                        distance=self.distance((x,y))
                        output= uncertanity_add(distance,angle,self.sigma)
                        output.append(self.position)
                    #store the measurement
                        data.append(output)
                        break
        #when the senson takes a full turn we return th data for building map
        if len(data)>0:
            return data
        else:
            return False

