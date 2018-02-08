
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import sys
import argparse
from matplotlib import colors
import os

parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')

parser.add_argument('--map', help='the map as txt')
parser.add_argument('--inputs', nargs='+', help='the output files from simulations in CSV in "file" "file"...')


args = parser.parse_args()

print len(args.inputs)
if args.map is None or args.inputs is None or len(args.inputs) > 3:
  print ("Both map and input must be set and length of the input must be >= 1 and <= 3")
  sys.exit(-1)

print args.map
print args.inputs
inputColors=['red','orange','blue']
zipped = zip(args.inputs,inputColors)
print zipped

inputColorsAndStyles=[('red','-'),('blue','--'),('orange','.-')]
zipped2 = zip(args.inputs,inputColorsAndStyles)
print zipped2
programPause = raw_input("Press the <ENTER> key to continue...")

# Load Map
a = np.loadtxt(args.map)
matrix= np.matrix(a)
print "Map matrix size: %s" % str(matrix.shape)

# Scaling ration of input
xc=matrix.shape[1]/2
yc=matrix.shape[0]/2
scale=1000

# Figure 2
# make a color map of fixed colors
mapColorMap = colors.ListedColormap(['gray', 'white'])
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.imshow(matrix, interpolation='nearest', cmap=mapColorMap, origin='lower', label='map')
for csv,(col,style) in zipped2:
    print csv
    print col
    print style

    # Load input
    df = pd.read_csv(csv)
    d=df[['{bodyFMU}.body.robot_x','{bodyFMU}.body.robot_y']]
    # Removing first 0.0 value
    d = d.iloc[1:]

    print "Simulation min: %s, max: %s" % (min(d['{bodyFMU}.body.robot_y']),max(d['{bodyFMU}.body.robot_y']))

    legend = os.path.splitext(os.path.basename(csv))[0]
    plt.plot(xc+(scale*d['{bodyFMU}.body.robot_x']),yc+(scale*d['{bodyFMU}.body.robot_y']), style, markevery=50, linewidth=2, color=col, label=legend)
# for csv,col in zipped:
#     # Load input
#     df = pd.read_csv(csv)
#     d=df[['{bodyFMU}.body.robot_x','{bodyFMU}.body.robot_y']]

#     print "Simulation min: %s, max: %s" % (min(d['{bodyFMU}.body.robot_y']),max(d['{bodyFMU}.body.robot_y']))


#     plt.plot(xc+(scale*d['{bodyFMU}.body.robot_x']),yc+(scale*d['{bodyFMU}.body.robot_y']), '--',linewidth=2,color=col )
#     ax.set_aspect('equal')
#     ax.autoscale_view(True,True,True)
ax.set_aspect('equal')
ax.autoscale_view(True,True,True)
ax.set_xlabel('Position x [mm]')
ax.set_ylabel('Position y [mm]')
plt.legend(loc='lower center')
plt.show()

