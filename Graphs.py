#<editor-fold desc="Imports">
import pandas as pd

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cycler

from datetime import datetime
#</editor-fold>

#<editor-fold desc="Set Up's">
#Sets Up MatPlotLib With The Nice Looking FastF1 Colour Scheme
COLOR_PALETTE = ['#FF79C6', '#50FA7B', '#8BE9FD', '#BD93F9',
                 '#FFB86C', '#FF5555', '#F1FA8C']

def setUpColourScheme():
    plt.rcParams['figure.facecolor'] = '#292625'
    plt.rcParams['axes.edgecolor'] = '#2d2928'
    plt.rcParams['xtick.color'] = '#f1f2f3'
    plt.rcParams['ytick.color'] = '#f1f2f3'
    plt.rcParams['axes.labelcolor'] = '#F1f2f3'
    plt.rcParams['axes.facecolor'] = '#1e1c1b'
    plt.rcParams['axes.titlesize'] = 'x-large'
    plt.rcParams['font.weight'] = 'medium'
    plt.rcParams['text.color'] = '#F1F1F3'
    plt.rcParams['axes.titlesize'] = '19'
    plt.rcParams['axes.titlepad'] = '12'
    plt.rcParams['axes.titleweight'] = 'light'
    plt.rcParams['axes.prop_cycle'] = cycler('color', COLOR_PALETTE)
    plt.rcParams['legend.fancybox'] = False
    plt.rcParams['legend.facecolor'] = (0.1, 0.1, 0.1, 0.7)
    plt.rcParams['legend.edgecolor'] = (0.1, 0.1, 0.1, 0.9)
    plt.rcParams['savefig.transparent'] = False
    plt.rcParams['axes.axisbelow'] = True
#</editor-fold>

def RouteGraph(jpxFrame, colorVal, outLapNum, fileName):
    #Creates A Color Map For The Graph To Use
    colormap = mpl.cm.YlOrRd

    #If All Laps Are Wanted Just Send The Whole DataFrame In
    if outLapNum == 0:
        lapFrame = jpxFrame
    #Else Just Get All The Points With The Correct Lap Number
    else:
        lapFrame = jpxFrame[jpxFrame['Lap'] == outLapNum]

    #Gets The X, Y And Speed Values
    x = lapFrame['Long']
    y = lapFrame['Lat']
    color = lapFrame[colorVal]

    #Sets Up The Graph
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    fig.suptitle(fileName + "\n" + colorVal + " Graph Lap " + str(outLapNum))

    #Adjusts The Margins And Turns Off The Axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')

    #Creates The Background Route From All The Points
    ax.plot(jpxFrame['Long'], jpxFrame['Lat'], color='black', linestyle='-', linewidth=16, zorder=0)

    #Creates A Continuous Norm To Map The Colours To The Data
    norm = plt.Normalize(jpxFrame[colorVal].min(), jpxFrame[colorVal].max())
    lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

    #Sets The Values To Be Used For The Colour Map
    lc.set_array(color)

    #Merges All The Line Segments Together
    line = ax.add_collection(lc)

    #Creates The Coloured Bar Legend
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=jpxFrame[colorVal].min(), vmax=jpxFrame[colorVal].max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")

    #Shows The Graph
    plt.show()

def Telemetry(jpxFrame, outLapNum):
    #Sets Up Plot Ratios And Sizes
    plotSize = [15, 15]
    plotRatios = [3, 3]

    # If All Laps Are Wanted Just Send The Whole DataFrame In
    if outLapNum == 0:
        lapFrame = jpxFrame
    # Else Just Get All The Points With The Correct Lap Number
    else:
        lapFrame = jpxFrame[jpxFrame['Lap'] == outLapNum]

    timeFrame = lapFrame['Time']

    for i in timeFrame:
        timeFrame.replace(i, i.time())

    # Increase The Plot Size
    plt.rcParams['figure.figsize'] = plotSize

    # Creates The Plot
    fig, ax = plt.subplots(2, gridspec_kw={'height_ratios': plotRatios}, sharex =True)

    # Sets The Plots Title
    ax[0].title.set_text("Telemetry")

    # Plots
    ax[0].plot(timeFrame, lapFrame['Speed'], color="#FF0000", label="Speed")
    ax[0].set(ylabel='Speed')

    ax[1].plot(timeFrame, lapFrame['Elevation'], color="#00FF00", label="Elevation")
    ax[1].set(ylabel='Elevation')
    ax[1].set(xlabel='Time')

    # Cleans Up The Tick Labels
    for a in ax:
        a.label_outer()

    # Outputs The Plot
    plt.show()

setUpColourScheme()