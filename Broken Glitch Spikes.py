import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import noise
import os

# Инициализация Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Инициализация камеры
gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
glTranslatef(0.0, 0.0, -30)
glRotatef(45, 1, 0, 0)  # Повернуть камеру на 45 градусов вокруг оси X

# Генерация шума
def generate_noise_2d(shape, x_offset, z_offset, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0):
    noise_map = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            noise_map[i][j] = noise.pnoise2((i + x_offset) / scale, (j + z_offset) / scale, octaves=octaves,
                                              persistence=persistence, lacunarity=lacunarity, repeatx=1024,
                                              repeaty=1024, base=42)
    return noise_map

# Создание террейна
def create_terrain(width, height, x_offset, z_offset):
    noise_map = generate_noise_2d((width, height), x_offset, z_offset)
    vertices = []
    for i in range(width):
        for j in range(height):
            x = i - width // 2
            z = j - height // 2
            y = noise_map[i][j] * 10
            vertices.append((x, y, z))
    # Добавляем вершины шипов
    for i in range(width):
        for j in range(height):
            if (i + j) % 2 == 0:  # Добавляем шипы через одну клетку
                x = i - width // 2
                z = j - height // 2
                y = noise_map[i][j] * 10  # Высота шипа
                vertices.append((x, y, z))  # Основание шипа
                vertices.append((x, y + 5, z))  # Вершина шипа
    return vertices

# Отрисовка террейна
def draw_terrain(vertices, width, height):
    glBegin(GL_TRIANGLES)
    for i in range(width - 1):
        for j in range(height - 1):
            x = i - width // 2
            z = j - height // 2
            y_floor = vertices[i * height + j][1]
            y_ceiling = 10  # Высота потолка

            # Пол
            glVertex3fv(vertices[i * height + j])
            glVertex3fv(vertices[(i + 1) * height + j])
            glVertex3fv(vertices[i * height + j + 1])

            glVertex3fv(vertices[(i + 1) * height + j])
            glVertex3fv(vertices[(i + 1) * height + j + 1])
            glVertex3fv(vertices[i * height + j + 1])

            # Стены
            glVertex3fv((x, y_floor, z))
            glVertex3fv((x + 1, y_floor, z))
            glVertex3fv((x, y_ceiling, z))

            glVertex3fv((x + 1, y_floor, z))
            glVertex3fv((x + 1, y_ceiling, z))
            glVertex3fv((x + 1, y_floor, z + 1))

            glVertex3fv((x, y_floor, z + 1))
            glVertex3fv((x, y_ceiling, z + 1))
            glVertex3fv((x, y_floor, z))

            glVertex3fv((x, y_floor, z))
            glVertex3fv((x, y_ceiling, z))
            glVertex3fv((x + 1, y_floor, z))

            glVertex3fv((x + 1, y_floor, z + 1))
            glVertex3fv((x + 1, y_ceiling, z + 1))
            glVertex3fv((x, y_floor, z + 1))

    glEnd()

# Сохранение в OBJ файл
def save_to_obj(vertices, width, height, filename):
    with open(filename, "w") as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for i in range(width):
            for j in range(height):
                # Пол
                f.write(f"f {i * height + j + 1} {(i + 1) * height + j + 1} {i * height + j + 2}\n")
                f.write(f"f {(i + 1) * height + j + 1} {(i + 1) * height + j + 2} {i * height + j + 2}\n")
                # Шипы
                if (i + j) % 2 == 0:  # Добавляем шипы через одну клетку
                    f.write(f"f {i * height + j + 1} {width * height + i * height + j + 1} {width * height + i * height + j + 2}\n")
                    f.write(f"f {width * height + i * height + j + 1} {width * height + i * height + j + 2} {width * height + (i + 1) * height + j + 1}\n")
                    f.write(f"f {i * height + j + 1} {width * height + (i + 1) * height + j + 1} {width * height + i * height + j + 1}\n")
        f.write(f"f {width * height + i * height + j + 1} {width * height + i * height + j + 2} {width * height + (i + 1) * height + j + 1}\n")
        f.write(f"f {width * height + i * height + j + 2} {width * height + (i + 1) * height + j + 1} {width * height + (i + 1) * height + j + 1}\n")

# Основной цикл
width, height = 20, 20
x_offset = 0
z_offset = 0
clock = pygame.time.Clock()
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
            if event.key == pygame.K_r:  # Сохранение на нажатие R
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                filename = os.path.join(desktop_path, "terrain_chunk.obj")
                save_to_obj(create_terrain(width, height, x_offset, z_offset), width, height, filename)
                print(f"Model saved as {filename}")

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    vertices = create_terrain(width, height, x_offset, z_offset)
    draw_terrain(vertices, width, height)
    pygame.display.flip()
    clock.tick(60)
