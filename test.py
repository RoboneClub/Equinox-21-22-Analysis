import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

x    = np.linspace(0,1, 100)
y    = np.linspace(0,1, 100)
z    = np.sin(x) * np.cos(y)
cols = np.linspace(0,1,len(x))

points = np.array([x, y, z]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:], points[1:]], axis=1)

fig, ax = plt.subplots()
lc = LineCollection(segments, cmap='viridis')
lc.set_array(cols)
lc.set_linewidth(2)
line = ax.add_collection(lc)
fig.colorbar(line,ax=ax)
plt.show()