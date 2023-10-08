import pygame as pg
from pygame.locals import *
from rt import Raytracer
from figures import *
from materials import *
from lights import *

width = 720
height = 720

pg.init()

screen = pg.display.set_mode((width, height), pg.DOUBLEBUF | pg.HWACCEL | pg.HWSURFACE)
screen.set_alpha(None)

raytracer = Raytracer(screen=screen)

red = Material(diffuse=(0.94, 0, 0.2))
black = Material(diffuse=(0, 0, 0))
wall = Material(diffuse=(0.8, 0.8, 0.8))
tex1 = pg.image.load("tex1.jpg")
tex1 = Material(texture=tex1)
tex2 = pg.image.load("tex2.jpg")
tex2 = Material(texture=tex2)
glass = Material(diffuse=(0.9, 0.9, 0.9), specular=64, ks=0.2, ior=1.5, matType=REFLECTIVE)

## -------------------- Cuarto -----------------------------
#Techo
raytracer.scene.append(Plane(position=(0,1.5,0), normal=(0,1,0), material=black))
#Suelo
raytracer.scene.append(Plane(position=(0,-1.5,0), normal=(0,1,0), material=black))
#Fondo
raytracer.scene.append(Plane(position=(0,0,-5), normal=(0,0,1), material=red))
#Lados
raytracer.scene.append(Plane(position=(-1.5,0,0), normal=(1,0,0), material=wall))
raytracer.scene.append(Plane(position=(1.5,0,0), normal=(1,0,0), material=wall))

## -------------------- Figuras -----------------------------
#Cubos
sizeDim = 0.5
raytracer.scene.append(AABB(position=(0.5,-0.6,-2.7), size=(sizeDim,sizeDim,sizeDim), material=tex1))
raytracer.scene.append(AABB(position=(-0.5,0.6,-2.7), size=(sizeDim,sizeDim,sizeDim), material=tex2))

#Discos
raytracer.scene.append(Disk(position=(0.5,-1,-2.5), normal=(0,1,0), radius=0.5, material=glass))
raytracer.scene.append(Disk(position=(-0.5,1,-2.5), normal=(0,1,0), radius=0.5, material=glass))


#Lights
raytracer.lights.append(AmbientLight(0.9))


isRunning = True
while(isRunning):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                isRunning = False
            elif event.key == pg.K_s:
                pg.image.save(screen, "image.bmp")
    raytracer.rtClear()
    raytracer.rtRender()
    pg.display.flip()



pg.quit()
