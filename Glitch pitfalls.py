import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import noise
import os

pygame.init()
display=(800,600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(45,(display[0]/display[1]),0.1,100.0)
glTranslatef(0.0,0.0,-30)

glRotatef(45,1,0,0)

def generate_noise_2d(shape,x_offset,z_offset,scale=100.0,octaves=6,persistence=0.5,lacunarity=2.0):
    noise_map = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            noise_map[i][j] = noise.pnoise2((i + x_offset) / scale,(j + z_offset) / scale,octaves=octaves, persistence=persistence,lacunarity=lacunarity,repeatx=1024,repeaty=1024,base=42)
    return noise_map

def create_terrain(width, height, x_offset, z_offset):
    noise_map=generate_noise_2d((width, height),x_offset,z_offset)
    vertices=[]
    for i in range(width):
        for j in range(height):
            x =i-width // 2
            z =j-height // 2
            y =noise_map[i][j] * 10
            vertices.append((x, y, z))
    return vertices

def create_tube(vertices, radius, slices):
    tube_vertices=[]
    tube_faces=[]

    for i in range(len(vertices)-1):
        v1=np.array(vertices[i])
        v2=np.array(vertices[i+1])

        direction=v2-v1
        length=np.linalg.norm(direction)
        direction /= length

        if np.linalg.norm(direction) == 0:
            continue
        perpendicular = np.cross(direction, np.array([0,1,0]))
        if np.linalg.norm(perpendicular) == 0:
            perpendicular = np.cross(direction, np.array([1,0,0]))

        perpendicular /= np.linalg.norm(perpendicular)

        for j in range(slices+1):
            angle=2* np.pi * j / slices
            offset=radius * (np.cos(angle) * perpendicular + np.sin(angle) * np.cross(direction, perpendicular))
            current_vertex=v1+offset

            tube_vertices.append(current_vertex)

            if i < len(vertices)-2:
                next_index=(i+1) * (slices+1)+j
                current_index =i * (slices+1)+j
                next_j =(j+1) % (slices+1)

                tube_faces.append([current_index, next_index, next_index+1])
                tube_faces.append([current_index, next_index+1, current_index+1])

    return tube_vertices,tube_faces

def save_to_obj(vertices,width,height,radius,slices,filename):
    tube_vertices = []
    tube_faces = []

    for i in range(width):
        for j in range(height-1):
            v1 = np.array(vertices[i * height+j])
            v2 = np.array(vertices[i * height+j + 1])

            direction=v2-v1
            length=np.linalg.norm(direction)
            direction /= length

            perpendicular = np.cross(direction, np.array([1, 0, 0]))
            if np.linalg.norm(perpendicular) == 0:
                continue
            perpendicular /= np.linalg.norm(perpendicular)

            for k in range(slices + 1):
                angle= 2 * np.pi * k / slices
                offset=radius * (np.cos(angle) * perpendicular + np.sin(angle) * np.cross(direction, perpendicular))

                tube_vertices.append(v1+offset)
                tube_vertices.append(v2+offset)

                if k < slices:
                    tube_faces.append([len(tube_vertices)-2,len(tube_vertices)-1,len(tube_vertices)-1+slices+ 1])
                    tube_faces.append([len(tube_vertices)-2,len(tube_vertices)-1+slices+1, len(tube_vertices)-2+slices+1])

    for j in range(height):
        for i in range(width-1):
            v1=np.array(vertices[j+i * height])
            v2=np.array(vertices[j+(i+1) * height])

            direction=v2-v1
            length=np.linalg.norm(direction)
            direction /= length

            perpendicular=np.cross(direction, np.array([0, 1, 0]))
            if np.linalg.norm(perpendicular) == 0:
                continue
            perpendicular /= np.linalg.norm(perpendicular)

            for k in range(slices + 1):
                angle = 2 * np.pi * k / slices
                offset = radius * (np.cos(angle) * perpendicular + np.sin(angle) * np.cross(direction, perpendicular))

                tube_vertices.append(v1+offset) 
                tube_vertices.append(v2+offset) 

                if k < slices:
                    tube_faces.append([len(tube_vertices)-2, len(tube_vertices)-1,len(tube_vertices)-1+slices + 1])
                    tube_faces.append([len(tube_vertices)-2,len(tube_vertices)-1+slices+1, len(tube_vertices) - 2 + slices + 1])

    with open(filename, "w") as f:
        for vertex in tube_vertices:
            f.write(f"v {vertex[0]:.4f} {vertex[1]:.4f} {vertex[2]:.4f}\n")
        for face in tube_faces:
            f.write(f"f {face[0] + 1} {face[1]+1} {face[2]+1}\n")
    print(f"Model saved as {filename}")

def draw_tube(vertices, width, height, radius, slices):
    for i in range(width):
        for j in range(height-1):
            v1=np.array(vertices[i * height+j])
            v2=np.array(vertices[i * height+j+1])

            direction=v2-v1
            length=np.linalg.norm(direction)
            direction /= length

            perpendicular=np.cross(direction, np.array([1, 0, 0]))
            if np.linalg.norm(perpendicular) == 0:
                continue
            perpendicular /= np.linalg.norm(perpendicular)

            glBegin(GL_QUAD_STRIP)
            for k in range(slices + 1):
                angle=2 * np.pi * k / slices
                offset=radius * (np.cos(angle) * perpendicular + np.sin(angle) * np.cross(direction, perpendicular))

                glVertex3fv(v1+offset)
                glVertex3fv(v2+offset)
            glEnd()

    for j in range(height):
        for i in range(width-1):
            v1 = np.array(vertices[j+i * height])
            v2 = np.array(vertices[j+(i+1) * height])

            direction=v2-v1
            length=np.linalg.norm(direction)
            direction /= length

            perpendicular=np.cross(direction, np.array([0,1,0]))
            if np.linalg.norm(perpendicular) == 0:
                continue
            perpendicular /= np.linalg.norm(perpendicular)

            glBegin(GL_QUAD_STRIP)
            for k in range(slices + 1):
                angle=2 * np.pi * k / slices
                offset=radius * (np.cos(angle) * perpendicular + np.sin(angle) * np.cross(direction, perpendicular))

                glVertex3fv(v1+offset)
                glVertex3fv(v2+offset)
            glEnd()

width,height=20,20
x_offset=0
z_offset=0
clock=pygame.time.Clock()
tube_radius=0.25
slices=10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                z_offset += 5
            if event.key == pygame.K_s:
                z_offset -= 5
            if event.key == pygame.K_a:
                x_offset -= 5
            if event.key == pygame.K_d:
                x_offset += 5
            if event.key == pygame.K_r:
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                vertices = create_terrain(width, height, x_offset, z_offset)
                filename = os.path.join(desktop_path, "terrain_tube.obj")
                save_to_obj(vertices, width, height, tube_radius, slices, filename)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    vertices = create_terrain(width, height, x_offset, z_offset)
    tube_vertices, _ =create_tube(vertices, tube_radius, slices)  
    draw_tube(vertices, width, height, radius=tube_radius, slices=slices)  
    pygame.display.flip()
    clock.tick(60)
