import env
import sensors
from sensors import *
import pygame


enviroment=env.buildEnviroment((600,1200))
#makin a copy of the main map
enviroment.originalMap = enviroment.map.copy()
#creating a laser sensor instance by passing range the og map and the uncertanity
laser=sensors.LaserSensor(200,enviroment.originalMap,Uncertanity=(0.5, 0.01))

enviroment.map.fill((0,0,0))#saving the main map color to black bg

#info map mai pointcloud draw isme hoga
enviroment.infomap=enviroment.map.copy()
running= True

while running:
    sensorsOn=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if pygame.mouse.get_focused():
            sensorsOn=True
        elif not pygame.mouse.get_focused():
            sensorsOn=False

    if sensorsOn:
        position=pygame.mouse.get_pos()
        laser.position=position
        #running the sensor for one turn
        sensor_data=laser.sense_object()
        #taking and storing its data
        enviroment.dataStorage((sensor_data))
        enviroment.show_sensordata()
#since we are drawing the data on the info map we need to first put the infomap on the main map before updating
    enviroment.map.blit(enviroment.infomap,(0,0))
    pygame.display.update()

