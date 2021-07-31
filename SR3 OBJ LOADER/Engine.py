#Universidad del Valle de Guatemala
#Graficas por Computadora
#Laboratorio SR3
#Diego Crespo 19541
from Base import LineV2, Engine, color
import random

width = 1920
height = 1080

drawer = Engine(width, height)

drawer.loadOBJ("face.obj", LineV2(width/2, height/6), LineV2(30,30))


drawer.glFinish("SALIDAMODELO3D.bmp")