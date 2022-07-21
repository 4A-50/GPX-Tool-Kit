#<editor-fold desc="Imports">
import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
#</editor-fold>

def RouteGraph(jpxFrame, outLapNum, fileName):
    colormap = mpl.cm.YlOrRd

    lapFrame = jpxFrame[jpxFrame['Lap'] == outLapNum]

    x = lapFrame['Long']
    y = lapFrame['Lat']
    color = lapFrame['Speed']

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    fig.suptitle(fileName + "\nSpeed Graph Lap " + str(outLapNum))

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')

    # After this, we plot the data itself.
    # Create background track line
    ax.plot(jpxFrame['Long'], jpxFrame['Lat'], color='black', linestyle='-', linewidth=16, zorder=0)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(jpxFrame['Speed'].min(), jpxFrame['Speed'].max())
    lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(color)

    # Merge all line segments together
    line = ax.add_collection(lc)

    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=jpxFrame['Speed'].min(), vmax=jpxFrame['Speed'].max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")

    # Show the plot
    plt.show()