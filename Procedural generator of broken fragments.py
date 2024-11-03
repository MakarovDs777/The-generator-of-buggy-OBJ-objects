import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Генерация поверхности
def generate_surface(xmin, xmax, ymin, ymax, zmin, zmax, nx, ny):
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    return X, Y, Z

# Визуализация поверхности и волос
def visualize_surface_and_hair(X, Y, Z, hair_x, hair_y, hair_z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.5)
    ax.plot(hair_x, hair_y, hair_z, 'b-')
    plt.show()
# Генерация волос
def generate_hair(num_hairs, length, radius):
    hair_x = []
    hair_y = []
    hair_z = []
    for _ in range(num_hairs):
        x = np.random.uniform(-10, 10)
        y = np.random.uniform(-10, 10)
        z = 0
        theta = np.linspace(0, 2 * np.pi, 10)
        for k in range(length):
            for t in theta:
                hair_x.append(x + radius * np.cos(t) + np.random.uniform(-0.1, 0.1))
                hair_y.append(y + radius * np.sin(t) + np.random.uniform(-0.1, 0.1))
                hair_z.append(z + k * 0.1)
    return hair_x, hair_y, hair_z

def is_intersecting(hair_x, hair_y, hair_z, new_x, new_y, new_z, radius):
    for i in range(len(hair_x)):
        dx = hair_x[i] - new_x
        dy = hair_y[i] - new_y
        dz = hair_z[i] - new_z
        distance = np.sqrt(dx**2 + dy**2 + dz**2)
        if distance < 2 * radius:
            return True
    return False

# Генерация волос
def generate_hair(num_hairs, length, radius):
    hair_x = []
    hair_y = []
    hair_z = []
    for _ in range(num_hairs):
        x = np.random.uniform(-10, 10)
        y = np.random.uniform(-10, 10)
        z = 0
        theta = np.linspace(0, 2 * np.pi, 10)
        for k in range(length):
            for t in theta:
                new_x = x + radius * np.cos(t) + np.random.uniform(-0.1, 0.1)
                new_y = y + radius * np.sin(t) + np.random.uniform(-0.1, 0.1)
                new_z = z + k * 0.1
                if not is_intersecting(hair_x, hair_y, hair_z, new_x, new_y, new_z, radius):
                    hair_x.append(new_x)
                    hair_y.append(new_y)
                    hair_z.append(new_z)
    return hair_x, hair_y, hair_z

# Сохранение файла
def save_file(hair_x, hair_y, hair_z):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop_path, "hair.obj")
    with open(filename, "w") as f:
        for i in range(len(hair_x)):
            f.write(f"v {hair_x[i]} {hair_y[i]} {hair_z[i]}\n")
        num_hairs = len(hair_x) // 10 // 10
        for i in range(num_hairs):
            for j in range(10):
                for k in range(10):
                    idx1 = i * 10 * 10 + j * 10 + k
                    idx2 = i * 10 * 10 + j * 10 + (k + 1) % 10
                    idx3 = (i * 10 * 10 + (j + 1) * 10 + (k + 1) % 10)
                    idx4 = (i * 10 * 10 + (j + 1) * 10 + k)
                    f.write(f"f {idx1 + 1} {idx2 + 1} {idx3 + 1}\n")
                    f.write(f"f {idx1 + 1} {idx3 + 1} {idx4 + 1}\n")
    print(f"Файл сохранен как {filename}")

# Основная функция
def main():
    hair_x, hair_y, hair_z = generate_hair(100, 10, 0.1)
    save_file(hair_x, hair_y, hair_z)

if __name__ == "__main__":
    main()
