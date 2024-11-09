import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy import ndimage
import os
# Генерация поверхности
def generate_surface(xmin, xmax, ymin, ymax, nx, ny):
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)
    x, y = np.meshgrid(x, y)
    z = np.zeros((ny, nx))  # создаем плоскую поверхность
    return x, y, z

# Создание дырок
def create_holes(x, y, z, max_radius, max_depth):
    holes = []
    for i in range(10):  # генерируем 10 дырок
        x_hole = random.uniform(x.min(), x.max())
        y_hole = random.uniform(y.min(), y.max())
        radius = random.uniform(0.1, max_radius)
        depth = random.uniform(0, max_depth)

        # Создаем дырку с правильным радиусом и глубиной
        x_hole_grid = np.linspace(x_hole - radius, x_hole + radius, 100)
        y_hole_grid = np.linspace(y_hole - radius, y_hole + radius, 100)
        x_hole_grid, y_hole_grid = np.meshgrid(x_hole_grid, y_hole_grid)
        z_hole_grid = np.zeros((100, 100))
        x_hole_grid, y_hole_grid, z_hole_grid = ndimage.gaussian_filter(x_hole_grid, sigma=1), ndimage.gaussian_filter(y_hole_grid, sigma=1), ndimage.gaussian_filter(z_hole_grid, sigma=1)
        x_hole_grid, y_hole_grid, z_hole_grid = ndimage.gaussian_filter(x_hole_grid, sigma=1), ndimage.gaussian_filter(y_hole_grid, sigma=1), ndimage.gaussian_filter(z_hole_grid, sigma=1)

        # Смещаем дырку на поверхность
        x_min = x_hole_grid.min()
        x_max = x_hole_grid.max()
        y_min = y_hole_grid.min()
        y_max = y_hole_grid.max()
        for i in range(int(x.shape[0])):
            for j in range(int(x.shape[1])):
                if x[i, j] >= x_min and x[i, j] <= x_max and y[i, j] >= y_min and y[i, j] <= y_max:
                    z[i, j] = -depth

        holes.append((x_hole, y_hole, radius, depth))

    return x, y, z, holes

# Визуализация поверхности
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y, z = generate_surface(-10, 10, -10, 10, 100, 100)
x, y, z, holes = create_holes(x, y, z, 5, 5)

ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5)
for hole in holes:
    x_hole, y_hole, radius, depth = hole
    x_min = x_hole - radius
    x_max = x_hole + radius
    y_min = y_hole - radius
    y_max = y_hole + radius
    ax.bar3d(x_min, y_min, -depth, x_max-x_min, y_max-y_min, 0, color='r', alpha=0.5)

# Create a copy of the surface
x_copy, y_copy, z_copy = x, y, z.copy()

# Shift the copy of the surface
z_copy += 1  # You can adjust this value to change the distance between the two surfaces

# Plot the copy of the surface
ax.plot_surface(x_copy, y_copy, z_copy, cmap='viridis', alpha=0.5)

# Connect the points of the two surfaces to create a parallelepiped
x_concat = np.concatenate((x.ravel(), x_copy.ravel()))
y_concat = np.concatenate((y.ravel(), y_copy.ravel()))
z_concat = np.concatenate((z.ravel(), z_copy.ravel()))

# Plot the edges of the parallelepiped
ax.plot3D(x_concat[[0, -1]], y_concat[[0, -1]], z_concat[[0, -1]], 'k')  # bottom
ax.plot3D(x_concat[[0, -1]], y_concat[[0, -1]], z_concat[[-1, 0]], 'k')  # front
ax.plot3D(x_concat[[0, -1]], y_concat[[0, -1]], z_concat[[0, -1]], 'k')  # back
ax.plot3D(x_concat[[0, -1]], y_concat[[0, -1]], z_concat[[0, -1]], 'k')  # top
ax.plot3D(x_concat[[0, -1]], y_concat[[0, -1]], z_concat[[0, -1]], 'k')  # left
ax.plot3D(x_concat[[0, -1]], y_concat[[0, -1]], z_concat[[0, -1]], 'k')  # right

# Save the OBJ file to the desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
filename = "parallelepiped.obj"
with open(os.path.join(desktop_path, filename), "w") as f:
    for i in range(len(x_concat)):
        f.write('v {} {} {}\n'.format(x_concat[i], y_concat[i], z_concat[i]))
    for i in range(len(x_concat) - 1):
        f.write('f {} {} {}\n'.format(i + 1, i + 2, i + 3))
    f.write('f {} {} {}\n'.format(len(x_concat) - 1, len(x_concat), len(x_concat) + 1))
    f.write('f {} {} {}\n'.format(len(x_concat) - 1, len(x_concat) + 1, len(x_concat) + 2))
    f.write('f {} {} {}\n'.format(len(x_concat) - 1, len(x_concat) + 2, len(x_concat) + 3))

# Show the plot
plt.show()
