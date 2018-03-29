import random
import sys
import math

radius = 10000                         #Choose your own radius
radiusInDegrees=float(radius)/111300.0
r = radiusInDegrees
x0 = 40.84
y0 = -73.87

for i in range(1,100):                 #Choose number of Lat Long to be generated

  u = float(random.uniform(0.0,1.0))
  v = float(random.uniform(0.0,1.0))

  w = r * math.sqrt(u)
  t = 2 * math.pi * v
  x = w * math.cos(t)
  y = w * math.sin(t)
  xLat  = x + x0
  yLong = y + y0
