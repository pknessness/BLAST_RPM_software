import numpy as np 
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
 
df = pd.read_csv("uniquesolutions.csv",header=None,sep='\t')
myArray = df.values

points = solutionsarray

def connectpoints(x,y,p1,p2):
   x1, x2 = x[p1], x[p2]
   y1, y2 = y[p1], y[p2]
   plt.plot([x1,x2],[y1,y2],'k-')

 # cube[0][0][0] = 1
 # cube[0][0][1] = 2
 # cube[0][1][0] = 3
 # cube[0][1][1] = 4
 # cube[1][0][0] = 5
 # cube[1][0][1] = 6
 # cube[1][1][0] = 7
 # cube[1][1][1] = 8

 for i in range():
     connectpoints(cube[i][i][i],cube[],points[i],points[i+1]) # Confused!



 ax = fig.add_subplot(111, projection='3d')
 # plot sides

 ax.add_collection3d(Poly3DCollection(verts, 
     facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()