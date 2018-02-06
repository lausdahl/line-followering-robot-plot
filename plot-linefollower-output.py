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


a = np.loadtxt(args.map)

#print a
print "original"
matrix = np.matrix(a)

#print matrix

print matrix[0,0]
#print np.squeeze(np.asarray(matrix))

print len (np.asarray(matrix).reshape(-1))
print matrix[0,-1]
print matrix[-1,0]

print matrix.shape

print "done"
#print "MapSimulation min: %s, max: %s" % (min(d['{bodyFMU}.body.robot_y']),max(d['{bodyFMU}.body.robot_y']))
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




df = pd.read_csv(args.input)


print np.matrix(df)

fig = plt.figure()
ax = fig.add_subplot(1,4,1)
ax.set_aspect('equal')
plt.title('Robot Raw')
d=df[['{bodyFMU}.body.robot_x','{bodyFMU}.body.robot_y']]

s=1 #1000
ox=0 #300
oy=0 #400
print "Simulation min: %s, max: %s" % (min(d['{bodyFMU}.body.robot_y']),max(d['{bodyFMU}.body.robot_y']))
plt.scatter(d['{bodyFMU}.body.robot_x'],d['{bodyFMU}.body.robot_y'])

ax = fig.add_subplot(1,4,2)
plt.scatter(500+(d['{bodyFMU}.body.robot_x']*1000),500+(d['{bodyFMU}.body.robot_y']*1000))
ax.set_ylim([0,1000])
ax.set_xlim([0,1000])
plt.title('Corrected')
ax.set_aspect('equal')

ax = fig.add_subplot(1,4,3)
plt.title('Map')
ax.set_aspect('equal')
ax.autoscale_view(True,True,True)
plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower')
ax = fig.add_subplot(1,4,4)
plt.title('Corrected+Map')

plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower')

plt.scatter(500+(1000*d['{bodyFMU}.body.robot_x']),500+(1000*d['{bodyFMU}.body.robot_y']))
ax.set_aspect('equal')
ax.autoscale_view(True,True,True)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower')

xc=matrix.shape[1]/2
yc=matrix.shape[0]/2

plt.scatter(xc+(1000*d['{bodyFMU}.body.robot_x']),yc+(1000*d['{bodyFMU}.body.robot_y']))
ax.set_aspect('equal')
ax.autoscale_view(True,True,True)
plt.show()


