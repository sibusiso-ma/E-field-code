## Program to produce Electric Potential Contour Maps for Electric Field Lab ##
## Written by S. Wheaton - 22 August 2019                                    ##

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter
from scipy.signal import savgol_filter

## Open potential at points data file ##

f = open('E7.txt','r')    

header = f.readline()                 # read and ignore header

## Create empty lists for x, y and V ##

xlist = []
ylist = []
Vlist = []

i = 0

## Read data into lists ##

for line in f:                       
        line = line.strip()             # remove "/n" character at end of line
        columns = line.split()          # split line into columns
        xlist.append(float(columns[0])) 
        ylist.append(float(columns[1]))
        Vlist.append(float(columns[2]))
        #print(i,xlist[i],ylist[i],Vlist[i])
        i = i + 1
     
     ## Convert lists to arrays ##
     
x = np.array(xlist)
y = np.array(ylist)
V = np.array(Vlist)
     
     ## Create figure ##
     
f = plt.figure()
     
ax1 = f.add_axes([0.1,0.1,0.85,0.85])   # adjust plot position and size
     
ncolours = 40                           # number of colours in contour plot
l = np.arange(0.0,10.0,0.5)             # levels in contour plot: play here 
     
contour=ax1.tricontourf(x,y,V,ncolours,cmap='viridis')
ax1.tricontour(x,y,V,levels = l,colors = 'k',linewidths = 1,linestyles = 'solid')
     
cbar = plt.colorbar(contour, ax=ax1)
cbar.set_label('Field Intensity)')
     
ax1.set(aspect=1,title='Electric Potential Contour Map for an Irregular charged conductor and earth')
     
ax1.set_ylabel("y (cm)")
ax1.set_xlabel("x (cm) ")


plt.show()

#---------------------------------------------------------------


# Create a 2D grid of unique x and y values
X = np.unique(x)
Y = np.unique(y)

# Reshape V to a 2D grid (make sure it matches the grid size)
V_grid = V.reshape(len(Y), len(X))

# Calculate the gradient to get the electric field components
Ex, Ey = np.gradient(-V_grid)

# Create the plot
fig, ax = plt.subplots(figsize=(8, 6))

# Create a contour plot for the potential
contour = ax.contourf(X, Y, V_grid, levels=100, cmap='viridis')
plt.colorbar(contour, ax=ax, label='Electric Potential (V)')
# Overlay the electric field as arrows
ax.quiver(X, Y, Ex, Ey, color='white', pivot='middle', scale=5)

# Set plot title and labels
ax.set_title('Electric Field Lines and Potential field for an irregular charged conductor and earth ')
ax.set_xlabel('x (cm)')
ax.set_ylabel('y (cm)')
ax.set_aspect('equal')

# Show the plot
plt.show()

#----------------------------------------------------


# Create a grid for the voltage data
x_unique = np.unique(x)
y_unique = np.unique(y)
X, Y = np.meshgrid(x_unique, y_unique)

# Reshape the voltage data to match the grid
V_grid = V.reshape(len(y_unique), len(x_unique))

# Calculate the electric field components (E_x and E_y)
E_x, E_y = np.gradient(-V_grid)  # Negative gradient of the voltage

# Smooth the electric field components using a Gaussian filter
E_x_smooth = gaussian_filter(E_x, sigma=2)  # Increase sigma for more smoothing
E_y_smooth = gaussian_filter(E_y, sigma=2)

# Alternatively, smooth using a Savitzky-Golay filter
# window_length = 5  # Adjust as needed
# polyorder = 2  # Polynomial order
# E_x_smooth = savgol_filter(E_x, window_length, polyorder, axis=0)
# E_y_smooth = savgol_filter(E_y, window_length, polyorder, axis=1)

# Calculate the magnitude of the smoothed electric field
E_magnitude_smooth = np.sqrt(E_x_smooth*2 + E_y_smooth*2)
# Create a 3D plot of the smoothed electric field magnitude
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, E_magnitude_smooth, cmap='viridis')

# Labels
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
ax.set_zlabel('|E| [V/cm]')

# Move the z-label to the left
ax.zaxis.set_label_position('bottom')
ax.zaxis.labelpad = 15  # Adjusts the distance of the label from the axis

# Move the colorbar to the left
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)
cbar.set_label('|E| [V/cm]')

plt.title('Electric Field Magnitude Curve for the irregular charged conductor and earth ')
plt.show()
