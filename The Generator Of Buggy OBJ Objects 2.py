import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import os
from scipy.spatial import Delaunay
import atexit

def draw_delaunay(points, axis):
    # Выполнить триангуляцию Делоне
    triangulation = Delaunay(points)
    for triangle in triangulation.simplices:
        axis.plot3D(points[triangle, 0], points[triangle, 1], points[triangle, 2], 'k-', linewidth=5)

def save_obj(vertices, faces, filename):
    with open(filename, 'w') as f:
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

def on_exit():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "delaunay.obj")
    save_obj(points, triangulation.simplices, desktop_path)
    print(f"OBJ файл сохранен на рабочем столе как 'delaunay.obj'")

# Создаем фигуру и ось для 3D отображения
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Списки для хранения точек и граней
points = []
faces = []

# Начальные параметры
for i in range(100):
    x = np.random.uniform(-100, 100)
    y = np.random.uniform(-100, 100)
    z = np.random.uniform(-100, 100)
    points.append([x, y, z])

# Вызываем функцию для рисования триангуляции Делоне
points = np.array(points)
triangulation = Delaunay(points)
draw_delaunay(points, ax)

# Подключаем обработчик события
atexit.register(on_exit)

# Показываем график
plt.show()
