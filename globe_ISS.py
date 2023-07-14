# copyright Andrea Gemmani 2023
# https://github.com/AndreaGemmani/ISS-tracker-artistic-plotter
# project start: 2023/07/10

# TODO:
# calculate actual tiles dimensions and resolution DONE circa dai
# plot ISS position given latitude and longitude DONE

# ISSUES:
# - meshgrid CREA UNA MATRICE QUADRATA quindi u e v finiscono per avere dimenisone uguale,
#   pari al valore più grande fra i due
# - mega wacky calculations for resolution, crashes for most values that are not cool divisors,
#   still, it works sometimes :))))
# - sometimes non si vede il puntino zio pera scompare dietro la Terra
#   https://stackoverflow.com/questions/40649354/surface-disappears-in-matplotlib-3d-plot






import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

import requests
# import json

# Load the image from your desktop
# image_path = "earth_clouds.jpg" # from https://www.solarsystemscope.com/textures/ # 400x200
image_path = "8k_earth_daymap.jpg" # 8192x4096
texture_image = Image.open(image_path)
width, height = texture_image.size # https://stackoverflow.com/questions/6444548/how-do-i-get-the-picture-size-with-pil
print(f"IMG\tw: {width}, h: {height}")

# QUESTI VALORI VENGONO DIVISI PER rstride=1, cstride=1 !!
lat_res = 128 # NORD-SUD
# lon_res = 40 # EST-OVEST non utilizzata al momento per problemi con meshgrid che usa solo valore più grande

# slice_lon_res = int(np.ceil(width / lon_res)) # GIUSTO MA DEVO PRIMA RISOLVERE MESHGRID SAME DIM
slice_lon_res = int(np.ceil(width / lat_res))
slice_lat_res = int(np.ceil(height / lat_res))

# Convert the image to a NumPy array and normalize the values
texture_array = np.array(texture_image) / 255.0

print("pre[h]: " + str(len(texture_array)))
print("pre[w]: " + str(len(texture_array[0])))

# SLICING per prendere solo punti di interesse per la texture CREDO
# https://stackoverflow.com/questions/25876640/subsampling-every-nth-entry-in-a-numpy-array
# https://www.w3schools.com/python/numpy/numpy_array_slicing.asp
# https://stackoverflow.com/questions/46083412/numpy-slicing-inner-array-of-a-2d-array-in-one-go
# https://stackoverflow.com/questions/31493109/nested-python-numpy-arrays-dimension-confusion
texture_array = texture_array[::slice_lat_res]
texture_array = texture_array[:,::slice_lon_res]

# Generate spherical data
u = np.linspace(0, 2 * np.pi, lat_res)
v = np.linspace(0, np.pi, lat_res)

# print(f"pre-mesh:\tu: {len(u)}, v: {len(v)}")
r_Terra = 10
u, v = np.meshgrid(u, v)
x = r_Terra * np.cos(u) * np.sin(v)
y = r_Terra * np.sin(u) * np.sin(v)
z = r_Terra * np.cos(v)
# print(f"post-mesh:\tu: {len(u)}, v: {len(v)}")

# Create a figure object and a 3D subplot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# Draw the spherical surface with the texture
# https://stackoverflow.com/questions/58205213/matplotlibs-rstride-cstride-messes-up-color-maps-in-plot-surface-3d-plot
ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=texture_array)



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
ISS_data = response.json()


print(ISS_data)


ISS_lat = float(ISS_data['iss_position']['latitude'])
ISS_lon = float(ISS_data['iss_position']['longitude'])

# daje Roma daje
# ISS_lat = 41.0
# ISS_lon = 12.0

ISS_lon += 180.0 # perché l'immagine di partenza ha y(0) = -180deg di longitudine

ISS_lat = float(ISS_lat) * np.pi / 180.0
ISS_lon = float(ISS_lon) * np.pi / 180.0

print(f"ISS lat: {ISS_lat}, \tISS lon: {ISS_lon}")

r_ISS = r_Terra * 1.2 # per disegnare leggermente più in alto, non preciso con altitudine reale ISS

# https://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates
# https://en.wikipedia.org/wiki/World_Geodetic_System
ISS_x = r_ISS * np.cos(ISS_lat) * np.cos(ISS_lon)
ISS_y = r_ISS * np.cos(ISS_lat) * np.sin(ISS_lon)
ISS_z = r_ISS * np.sin(ISS_lat)

# draw ISS as a point for now
ax.scatter(ISS_x, ISS_y, ISS_z, color="g", s=100)

# Show the plot
plt.show()

