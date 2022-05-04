from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0,exposure=1)
scene.set_directional_light((1, 1, 1), 0.1, (1, 0.8, 0.6))
scene.set_background_color(vec3(0,191,255)/255)
scene.set_floor(0, vec3(34,139,34)/255)

yellow_c = vec3(255,255,224)/255
burlyWood_c = vec3(222,184,135)/255

@ti.func
def draw_level(n, center, h):
    for he in range(h):
        nn = n - he*0.7
        ri = int(nn/2)
        for i, j in ti.ndrange((-ri,ri),(-ri,ri)):
            c = yellow_c * 0.5
            if he >= h-2:
                c = yellow_c * 0.8
            elif (i + j + he) % 4 < 2:
                c = yellow_c * 0.6
            scene.set_voxel(vec3(i,he,j)+center, 1, c)

@ti.func
def draw_stairs(m, n, h):
    w = 18
    for he in range(h):
        for i, j in ti.ndrange((-w//2,w//2),(int(-m/2+he*(m-n)/h/2),-n//2)):
            c = burlyWood_c
            if i + w//2 <= 3 or w//2 - i <= 3:
                c = yellow_c * 0.9
            scene.set_voxel(vec3(i,he,j),1,c)
            scene.set_voxel(vec3(j,he,i),1,c)
        for i, j in ti.ndrange((-w//2,w//2),(n//2,int(m/2-he*(m-n)/h/2))):
            c = burlyWood_c
            if i + w//2 <= 3 or w//2 - i <= 3:
                c = yellow_c * 0.9
            scene.set_voxel(vec3(i,he,j),1,c)
            scene.set_voxel(vec3(j,he,i),1,c)
            
@ti.func
def draw_up_house(h, H):
    n = 18
    for he in range(H,H+h):
        c = yellow_c*0.8
        if he == H + 5:
            c = yellow_c
        for i in range(-n//2,n//2+1):
            if he > H + 3 or (i < -2 or i > 2):
                scene.set_voxel(vec3(i,he,n//2),1,c)
            scene.set_voxel(vec3(i,he,-n//2),1,c)
        for j in range(-n//2,n//2+1):
            scene.set_voxel(vec3(n//2,he,j),1,c)
            scene.set_voxel(vec3(-n//2,he,j),1,c)
    for i,j in ti.ndrange((-n//2,n//2+1),(-n//2,n//2+1)):
        scene.set_voxel(vec3(i,H+h,j),1,yellow_c)

@ti.kernel
def initialize_voxels():
    for i in range(9):
        draw_level(100-8*i, vec3(0,i*6,0), 6)
    draw_stairs(128,30,54)
    draw_up_house(8, 54)
        
initialize_voxels()

scene.finish()