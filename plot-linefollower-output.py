import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import sys
import argparse

parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')

parser.add_argument('--map', help='the map')
parser.add_argument('--input', help='the output file from a simulation in CSV')


args = parser.parse_args()

if args.map is None or args.input is None:
  print ("Both map and input must be set")
  sys.exit(-1)
print args.map

# Load Map
a = np.loadtxt(args.map)
matrix= np.matrix(a)
print "Map matrix size: %s" % str(matrix.shape)

# Load input
df = pd.read_csv(args.input)
d=df[['{bodyFMU}.body.robot_x','{bodyFMU}.body.robot_y']]

print "Simulation min: %s, max: %s" % (min(d['{bodyFMU}.body.robot_y']),max(d['{bodyFMU}.body.robot_y']))

# Scaling ration of input
xc=matrix.shape[1]/2
yc=matrix.shape[0]/2
scale=1000


# Figure
fig = plt.figure()

# Sub fig 1
ax = fig.add_subplot(1,4,1)
ax.set_aspect('equal')
plt.title('Robot Raw')

plt.scatter(d['{bodyFMU}.body.robot_x'],d['{bodyFMU}.body.robot_y'])

# Sub fig 2
ax = fig.add_subplot(1,4,2)
ax.set_ylim([0,1000])
ax.set_xlim([0,1000])
plt.title('Corrected')
ax.set_aspect('equal')

plt.scatter(xc+(d['{bodyFMU}.body.robot_x']*scale),yc+(d['{bodyFMU}.body.robot_y']*scale))

# Sub fig 3
ax = fig.add_subplot(1,4,3)
plt.title('Map')
ax.set_aspect('equal')
ax.autoscale_view(True,True,True)

plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower')

# Sub fig 4
ax = fig.add_subplot(1,4,4)
plt.title('Corrected+Map')
ax.set_aspect('equal')
ax.autoscale_view(True,True,True)

plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower')

plt.scatter(xc+(scale*d['{bodyFMU}.body.robot_x']),yc+(scale*d['{bodyFMU}.body.robot_y']))

# Figure 2

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower')

xc=matrix.shape[1]/2
yc=matrix.shape[0]/2

plt.scatter(xc+(scale*d['{bodyFMU}.body.robot_x']),yc+(scale*d['{bodyFMU}.body.robot_y']))
ax.set_aspect('equal')
ax.autoscale_view(True,True,True)
plt.show()


