import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import sys

MAPX = 0.594
MAPY = 0.841

a = np.loadtxt('map.txt')

#print a
print "original"
matrix = np.matrix(a)

#print matrix

print matrix[0,0]
#print np.squeeze(np.asarray(matrix))

#print len (np.asarray(matrix).reshape(-1))
print matrix[0,-1]

print matrix[-1,0]

#scalars (left, right, bottom, top), optional, default: None
#extent=[0,matrix[0,-1]*0.001,0,matrix[-1,0]*0.001]
#extent=[0,matrix[0,-1],0,matrix[-1,0]]
extent=[-MAPX/2.0,MAPX/2.0,-MAPY/2.0,MAPY/2.0]
#extent=[0,matrix[0,-1]*1,0,matrix[-1,0]*4]
#extent=[0,2,0,2]
#extent=[0,1,0,1]
print extent
#sys.exit()

print "fixed"
#matrix[0]=matrix[0]*1000 #0.001
print matrix


df = pd.read_csv('outputs.csv')

print np.matrix(df)

fig = plt.figure()
ax = fig.add_subplot(1,4,1)
plt.title('Robot Raw')
d=df[['{bodyFMU}.body.robot_x','{bodyFMU}.body.robot_y']]

s=1 #1000
ox=0 #300
oy=0 #400
print min(d['{bodyFMU}.body.robot_y'])
plt.scatter(d['{bodyFMU}.body.robot_x'],d['{bodyFMU}.body.robot_y'])

ax = fig.add_subplot(1,4,2)
plt.scatter(d['{bodyFMU}.body.robot_x']*3198.7753,(1+d['{bodyFMU}.body.robot_y'])*211)
plt.title('subplot Corrected')

ax = fig.add_subplot(1,4,3)
plt.title('Map')
ax.set_aspect('equal')
ax.autoscale_view(True,True,True)
#plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower',extent=extent)
plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower')
#plt.imshow(matrix, extent=extent)
ax = fig.add_subplot(1,4,4)
plt.title('Corrected+Map')
plt.scatter(d['{bodyFMU}.body.robot_x']*3198.7753,(1+d['{bodyFMU}.body.robot_y'])*286.49)
ax.set_aspect('equal')
ax.autoscale_view(True,True,True)
#plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower',extent=extent)
plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower')

#plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, extent=extent)
#plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower')
#plt.colorbar()
#plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower')
plt.show()

