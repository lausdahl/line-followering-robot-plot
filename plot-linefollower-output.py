import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import sys
import argparse
import matplotlib.image as mpimg
from os.path import basename

parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')

parser.add_argument('--map', help='Map in matrix format i.e. map.txt')
parser.add_argument('--png',help='Map in PNG format')
parser.add_argument('--input', help='the output file from a simulation in CSV where the coordinates are in [m]',nargs='*')
parser.add_argument('--offset',help='Input center point x,y given in [m] or the letter \'c\' for map center')
parser.add_argument('--width',help='Width of the map in [m]')
parser.add_argument('--height',help='Height of the map in [m]')

args = parser.parse_args()
if (args.map is None and args.png is None) or args.input is None:
  print ("Both map and input must be set")
  sys.exit(-1)

width=1
height=1
img=None
mapMatrix=None

pixelWidth=1
pixelHeight=1

if not (args.map is None or args.png is None) and (args.width is None or args.height is None):
  print "The height and width of the map must also be specified"
  sys.exit(-1)

if not args.width is None:
  width = float(args.width)

if not args.height is None:
  height = float(args.height) 

print 'Map/Img size is width: %s, height: %s' % (width, height)

if not args.png is None:
  img=mpimg.imread(args.png)
  pixelHeight,pixelWidth,bpp = np.shape(img)
  

inputXOffset=0
inputYOffset=0

if not args.offset is None:
  if args.offset=='c':
    print "Offset is begin set to map 'center'"
    inputXOffset,inputYOffset=width/2,height/2
  else:
    offset = args.offset.split(',')
    if len(offset) !=2:
      print "Offset must be specified as a touple: 0.01,0.02 but is given as: "+args.offset
      sys.exit(-1)
    else:
      inputXOffset=float(offset[0])
      inputYOffset=float(offset[1])
      print "Input offset is set to (%s [m],%s [m])" % (inputXOffset,inputYOffset)


# Change coordinate system from pixels to the image physical size in [m]
extent=[0,width ,0, height]

if not args.map is None:
  # Load Map
  a = np.loadtxt(args.map)
  mapMatrix= np.matrix(a)
  (pixelWidth, pixelHeight)=mapMatrix.shape

print "Map matrix size: (%s,%s)" % (pixelWidth,pixelHeight)

def plotInput(name,input):
  # Load input
  df = pd.read_csv(input)
  d=df[['{bodyFMU}.body.robot_x','{bodyFMU}.body.robot_y']]

  print "Input min: %s, max: %s" % (min(d['{bodyFMU}.body.robot_y']),max(d['{bodyFMU}.body.robot_y']))

  # Corrected input coordinates - offset
  cix,ciy=(inputXOffset+d['{bodyFMU}.body.robot_x'],inputYOffset+d['{bodyFMU}.body.robot_y'])

  # Figure
  fig = plt.figure(name)

  # Sub fig 1
  ax = fig.add_subplot(1,4,1)
  ax.set_aspect('equal')
  plt.title('Robot Raw')

  plt.scatter(d['{bodyFMU}.body.robot_x'],d['{bodyFMU}.body.robot_y'])

  # Sub fig 2
  ax = fig.add_subplot(1,4,2)
  plt.title('Corrected')
  ax.set_aspect('equal')

  plt.scatter(cix,ciy)

  # Sub fig 3
  ax = fig.add_subplot(1,4,3)
  plt.title('Map')
  ax.set_aspect('equal')
  ax.autoscale_view(True,True,True)

  if img is not None:
    plt.imshow(img, interpolation='nearest', cmap=plt.cm.ocean, origin='lower',extent=extent)

  if not mapMatrix is None:
    print "showing map"
    plt.imshow(mapMatrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower',extent=extent)

  # Sub fig 4
  ax = fig.add_subplot(1,4,4)
  plt.title('Corrected+Map')
  ax.set_aspect('equal')
  ax.autoscale_view(True,True,True)

  if img is not None:
    plt.imshow(img, interpolation='nearest', cmap=plt.cm.ocean, origin='lower',extent=extent)

  if mapMatrix is not None:
    plt.imshow(mapMatrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower',extent=extent)

  plt.scatter(cix,ciy)
  return (cix,ciy)


inputPlots=[]
for idx, input in enumerate(args.input):
  name=basename(input)+"-"+str(idx)
  (cix,ciy)=plotInput(name,input)
  inputPlots.append((name,cix,ciy))

# Figure 2

fig = plt.figure("Overview")
ax = fig.add_subplot(1, 1, 1)

if img is not None:
  plt.imshow(img, interpolation='nearest', cmap=plt.cm.ocean, origin='lower',extent=extent,label="Map.png")

if mapMatrix is not None:
  plt.imshow(mapMatrix, interpolation='nearest', cmap=plt.cm.ocean, origin='lower',extent=extent,label="Map.txt")

for name,cix,ciy in inputPlots:
  plt.scatter(cix,ciy,label=name)

ax.set_aspect('equal')
ax.autoscale_view(True,True,True)
ax.legend(loc='best')
plt.show()


