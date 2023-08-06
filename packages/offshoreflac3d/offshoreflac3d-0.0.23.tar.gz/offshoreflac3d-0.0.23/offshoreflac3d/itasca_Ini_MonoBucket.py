import numpy as np 
from shapely import geometry as geo
import itasca as it
it.command("python-reset-state false")
from itasca import zonearray as za
from itasca import gridpointarray as gpa


# boundary_x = 50
# boundary_y = 50
# soil_layers = [-34,-55.5,-59,-60.5,-63.5,-84.5,-90.5,-101.5,-130]
# #properties####################################

# density = [0.65,0.68,0.90,0.74,0.85,0.88,0.99,0.90]
# elastic = [0.003e6,0.010e6,0.015e6,0.015e6,0.020e6,0.025e6,0.025e6,0.030e6]
# poisson = [0.49,0.49,0.30,0.49,0.49,0.49,0.30,0.49]
# cohesion = [0.015e3,0.030e3,0.001e3,0.040e3,0.070e3,0.070e3,0.001e3,0.070e3]
# friction =[0.1,0.1,27,0.1,0.1,0.1,31,0.1]

def Ini_main(scour_depth,R_max,soil_layers,density,elastic,poisson,cohesion,friction):
    bulk = []
    shear = []
    for i in range(len(density)):
        bulk.append(elastic[i] / (3.0 * (1.0 - 2.0 * poisson[i])))
        shear.append(elastic[i] / (2.0 * (1.0 + poisson[i])))

    # print(bulk)
    # print(shear)


    it.command("model restore 'model_{}'".format(scour_depth))

    it.command("model gravity 9.8")
    it.command("model large-strain off")

    it.command("zone cmodel m-c")


    for i in range(len(density)):
        command1 = "zone property density {} range group 'soil_{}' slot 'soil'"
        command2 = "zone property shear {} bulk {} cohesion {} friction {} tension 1e3 range group 'soil_{}' slot 'soil'"
        command3 = "zone initialize-stresses ratio {} range group 'soil_{}' slot 'soil'"
        it.command(command1.format(density[i],i))
        it.command(command2.format(shear[i],bulk[i],cohesion[i],friction[i],i))
        it.command(command3.format(poisson[i]/(1-poisson[i]),i))
        print("assigning properties in soil_{} finished!".format(i))

    #it.command("zone initialize-stresses ratio 0.85 range group 'soil_3' slot 'soil'")

    for gp in it.gridpoint.list():
        pos_x = gp.pos_x()
        pos_y = gp.pos_y()
        r_dist = pos_x*pos_x + pos_y*pos_y
        if gp.pos_z() == soil_layers[-1]:
            gp.set_fix(0,True)
            gp.set_fix(1,True)
            gp.set_fix(2,True)
        elif r_dist > R_max**2-0.1 and r_dist < R_max**2+0.1:
            gp.set_fix(0,True)
            gp.set_fix(1,True)

    print("boundary conditions assigned!")

    it.command("model solve ratio 1e-6")
    it.command("model save 'Initial_{}'".format(scour_depth))
    print("'Initial' saved!")

