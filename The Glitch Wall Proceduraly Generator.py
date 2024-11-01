import numpy as np
import os

# Параметры
size = 100  # Размер поверхности
hair_length = 10  # Длина волос
hair_density = 0.1  # Плотность волос

# Генерация поверхности
x = np.linspace(0, size, size)
y = np.linspace(0, size, size)
X, Y = np.meshgrid(x, y)

# Генерация волос
hair_x = np.random.uniform(0, size, int(size * size * hair_density))
hair_y = np.random.uniform(0, size, int(size * size * hair_density))
hair_z = np.zeros(int(size * size * hair_density))

# Сохранение модели в формате OBJ на рабочий стол
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = os.path.join(desktop_path, "hair_model.obj")
with open(filename, 'w') as f:
    for i in range(len(hair_x)):
        f.write(f'v {hair_x[i]} {hair_y[i]} {hair_z[i]}\n')
        f.write(f'v {hair_x[i]} {hair_y[i]} {hair_z[i] + hair_length}\n')
        f.write(f'l {i*2+1} {i*2+2}\n')

    # Сохранение поверхности
    for i in range(size):
        for j in range(size):
            f.write(f'v {X[i, j]} {Y[i, j]} 0\n')

    # Сохранение связей между вершинами поверхности
    for i in range(size-1):
        for j in range(size-1):
            f.write(f'f {(i*size+j)+1} {(i*size+j+1)+1} {(i*size+j+size+1)+1} {(i*size+j+size)+1}\n')

print(f"Модель сохранена на рабочий стол как {filename}")

