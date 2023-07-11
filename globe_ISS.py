# copyright Andrea Gemmani 2023
# https://github.com/AndreaGemmani
# project start: 2023/07/10

# TODO:
# calculate actual tiles dimensions and resolution
# plot ISS position given latitude and longitude

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

import requests
import json

# Load the image from your desktop
image_path = "earth_clouds.jpg" # from https://www.solarsystemscope.com/textures/
texture_image = Image.open(image_path)

# NOT THE ACTUAL NUMBER OF TILES!
lat_res = 200 # verticale
lon_res = 30 # orizzontale

# Convert the image to a NumPy array and normalize the values
texture_array = np.array(texture_image) / 255.0

# Generate spherical data
u = np.linspace(0, 2 * np.pi, lon_res)
v = np.linspace(0, np.pi, lat_res)
u, v = np.meshgrid(u, v)
x = 10 * np.cos(u) * np.sin(v)
y = 10 * np.sin(u) * np.sin(v)
z = 10 * np.cos(v)

# Create a figure object and a 3D subplot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Draw the spherical surface with the texture
ax.plot_surface(x, y, z, rstride=4, cstride=4, facecolors=texture_array)

# Set the same scale for each axis to make it look spherical
max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() / 2.0
mid_x = (x.max()+x.min()) * 0.5
mid_y = (y.max()+y.min()) * 0.5
mid_z = (z.max()+z.min()) * 0.5
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

# Set the x, y, z axes labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


# Set equal aspect ratio for all axes
ax.set_box_aspect([1, 1, 1])



response = requests.get("http://api.open-notify.org/iss-now.json")
heh = response.json()


print(heh)

print(heh['timestamp'])
print(heh['iss_position']['latitude'])

# Show the plot
plt.show()




