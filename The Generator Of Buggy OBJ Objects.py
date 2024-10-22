import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import Delaunay
import os

def save_model(verts, faces, filename):
    try:
        with open(filename, 'w') as f:
            for v in verts:
                f.write('v {:.6f} {:.6f} {:.6f}\n'.format(v[0], v[1], v[2]))
            for face in faces:
                f.write('f {} {} {}\n'.format(face[0]+1, face[1]+1, face[2]+1))
        print(f"Model saved as {filename}")
    except Exception as e:
        print(f"Error saving model: {e}")

# Функция для генерации кадра
def update(ax):
    ax.clear()  # Очистка текущего окна

    # Генерация точек
    points = []
    for i in range(100):
        x = np.random.uniform(-100, 100)
        y = np.random.uniform(-100, 100)
        z = np.random.uniform(-100, 100)
        points.append([x, y, z])

    # Преобразование точек в NumPy массив 
    points = np.array(points)

    # Выполнить триангуляцию Делоне
    triangulation = Delaunay(points)

    # Постройте график треугольников
    for triangle in triangulation.simplices:
        ax.plot3D(points[triangle, 0], points[triangle, 1], points[triangle, 2], 'k-', linewidth=1)

# Генерация точек
points = []
for i in range(100):
    x = np.random.uniform(-100, 100)
    y = np.random.uniform(-100, 100)
    z = np.random.uniform(-100, 100)
    points.append([x, y, z])

# Преобразование точек в NumPy массив 
points = np.array(points)

# Выполнить триангуляцию Делоне
triangulation = Delaunay(points)

# Сохранение модели в формате OBJ
output_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'odel.obj')
save_model(points, triangulation.simplices, output_path)

# Визуализация
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Визуализация модели
for triangle in triangulation.simplices:
    verts = points[triangle]
    poly3d = Poly3DCollection([verts], alpha=0.5, edgecolor='k')
    ax.add_collection3d(poly3d)

# Настройки отображения
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(-150, 150)
ax.set_ylim(-150, 150)
ax.set_zlim(-150, 150)

# Показываем окно с моделью
plt.show()

# Сохранение модели в формате OBJ
output_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'odel.obj')
with open(output_path, 'w') as f:
    for triangle in triangulation.simplices:
        verts = points[triangle]
        for v in verts:
            f.write('v {:.6f} {:.6f} {:.6f}\n'.format(v[0], v[1], v[2]))
        f.write('f')
        for v in verts:
            f.write(' {}'.format(v[0]+1))
        f.write('\n')
