import numpy as np 
from shapely import geometry as geo
import itasca as it
it.command("python-reset-state false")
from itasca import zonearray as za
from itasca import gridpointarray as gpa

# #size of suction caisson#########################
# R = 12.0/2.0
# L = 12.0
# #meshing#########################################
# num_zone = 10
# radiul_num_zone1 = 8
# radiul_num_zone2 = 10
# radiul_ratio1 = 1.2
# radiul_ratio2 = 1.1
# #Foundation######################################
# distance = 23.5
# boundary_x = 50
# boundary_y = 50
# scour_depth = 3.0
# soil_layers = [-34,-55.5,-59,-60.5,-63.5,-84.5,-90.5,-101.5,-130]
#
def model_main(R,L,radiul_num_zone1,radiul_num_zone2,radiul_ratio1,radiul_ratio2,distance,boundary_x,boundary_y,scour_depth,soil_layers):
    layering = []
    for i in soil_layers:
        layering.append(i)
    layering.append(soil_layers[0]-scour_depth)
    layering.append(soil_layers[0]-L)
    layering.sort(reverse=True)
    print(layering)
    #model new#########################
    it.command("model new")
    it.command("program echo off")
    it.fish.set('R',R)
    it.fish.set('mudline',soil_layers[0])
    it.fish.set('scour_depth',scour_depth)
    it.fish.set('distance',distance)
    it.fish.set('boundary_x',boundary_x)
    it.fish.set('boundary_y',boundary_y)
    it.fish.set('boundary_z',soil_layers[-1])
    #basic model
    command1 = '''zone import 'zone_{}.inp' format abaqus
    zone group 'SC' slot 'suction caisson'
    '''.format(int(R))
    command2 = '''
    zone create radial-cylinder point 0 0  0  0 ...
                point 1 	[distance/2] 0 0 ...
                point 2 	0 0 1 ...
                point 3 	0 [-distance/2] 0 ...
                point 4 	[distance/2] 0 1 ...
                point 5 	0 [-distance/2] 1 ...
                point 6 	[distance/2] [-distance/2] 0 ...
                point 7 	[distance/2] [-distance/2] 1 ...
                point 8 	[R] 0 0 ...
                point 9 	0 [-R] 0 ...
                point 10 	[R] 0 1 ...
                point 11 	0 [-R] 1 ...
                size 6 1 12 {} ...
                ratio 1 1 1 {} ...
                group 'Block2' slot 'Block'
    ;zone reflect origin 0 0 0 normal 0 1 0 range group 'Block2' slot 'Block'
    '''.format(radiul_num_zone1,radiul_ratio1)
    command3 = '''
    zone group 'NoSC' slot 'suction caisson' range group 'SC' slot 'suction caisson' not
    zone reflect origin 0 0 0 normal 0 1 0 merge on
    zone reflect origin 0 0 0 normal 1 0 0 merge on
    '''
    it.command(command1)
    #it.command(command2)
    #it.command(command3)

    # for gp in it.gridpoint.list():
        # gp.set_pos_x(gp.pos_x()+distance/2)
        # gp.set_pos_y(gp.pos_y()+distance/2)

    command = '''
    zone create radial-tunnel point 0 (0 0 0)...
                point 1 	[boundary_x] 	0 		0 ...
                point 2 	0 		0 		1 ...
                point 3 	0 		[-boundary_y] 	0 ...
                point 4 	[boundary_x] 	0 		1 ...
                point 5 	0 		[-boundary_y] 	1 ...
                point 6 	[boundary_x] 	[-boundary_y] 	0 ...
                point 7 	[boundary_x] 	[-boundary_y] 	1 ...
                point 8 	[distance] 	0 		0 ...
                point 9 	0 		[-distance] 	0 ...
                point 10 	[distance] 	0 		1 ...
                point 11 	0 		[-distance] 	1 ...
                point 12 	[distance] 	[-distance] 	0 ...
                point 13 	[distance] 	[-distance] 	1 ...
                size 12 1 12 {} ...
                ratio 1 1 1 {} ...
                group 'Block3' slot 'Block'
    '''.format(radiul_num_zone2,radiul_ratio2)
    #it.command(command)
    
    command = '''
    zone reflect origin 0 0 0 normal 0 1 0 merge on
    zone reflect origin 0 0 0 normal 1 0 0 merge on
    '''
    it.command(command)
    #layering
    for gp in it.gridpoint.list():
        gp.set_pos_z(gp.pos_z()+soil_layers[0]-0.1)

    command_template = ("zone copy 0 0 {} merge on range position-z {} {}")

    for i in layering:
        if i == layering[0]:
            continue
        elif i == layering[-1]:
            continue
        else:
            it.command(command_template.format(i-layering[0],layering[0],layering[1]))
        
    for gp in it.gridpoint.list():    
        for i in range(len(layering)-1):
            if round(gp.pos_z(),3) == round((layering[i]-0.1),3):
                # print(layering[i+1])
                gp.set_pos_z(layering[i+1])

    # print(soil_layers)
      
    for z in it.zone.list():
        for i in range(len(soil_layers)-1):
            if z.pos_z() <= soil_layers[i] and z.pos_z() >= soil_layers[i+1]:
                z.set_group("soil_{}".format(i),"soil")

    for i in range(len(layering)-1):
        if layering[i]-layering[i+1] <= 0.5:
            continue
        elif layering[i]-layering[i+1] > 0.5 and layering[i]-layering[i+1] < 1.0:
            it.command("zone densify global segments 1 1 2 range position-z {} {}".format(layering[i],layering[i+1]))
        else:
            if layering[0]-L < layering[i+1]:
                command = "zone densify global segments 1 1 {} range position-z {} {}"
                it.command(command.format(int(layering[i]-layering[i+1])*2,layering[i],layering[i+1]))
            else:
                command = "zone densify global segments 1 1 {} range position-z {} {}"
                it.command(command.format((int(layering[i]-layering[i+1])+1)*1,layering[i],layering[i+1]))

    it.command("zone attach by-face tolerance-absolute 0.1")
    it.command("model save 'model_{}'".format(scour_depth))
    print("'model' saved!")





























