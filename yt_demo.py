"""
Demonstrates how to use GridFigure to generate custom MPL plots using yt
PlotWindow objects (e.g., slices, projections)
"""

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from grid_figure import GridFigure
from matplotlib.colors import LogNorm
import yt

# Create GridFigure object
fig = GridFigure(1, 1, top_buffer=0.02, bottom_buffer=0.15, left_buffer=0.18, right_buffer=0.01, vertical_buffer=0.01, horizontal_buffer=0.005, figsize=(4, 4))

# Now treat fig like a list of NxN elements.  Each element is a MPL axis object
ax = fig[0]

# Generate your desired projection or slice or whatever
ds = yt.load('IsolatedGalaxy/galaxy0030/galaxy0030')
proj = yt.ProjectionPlot(ds, 'x', 'density')

# Use imshow with your axis object to show the FixedResolutionBuffer
# of the projection image data; Render in Log space.
plot = ax.imshow(proj.frb['density'].v, norm=LogNorm())
#plot.set_clim((7e11, 3e23))
plot.set_cmap('dusk')

# Now just treat ax like a normal MPL axis object
ax.set_ylabel('rock on')
plt.savefig('proj.png')
