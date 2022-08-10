#<editor-fold desc="Imports">
import pandas as pd
from datetime import timedelta

from rich.console import Console
from rich.table import Table
from rich import box
from rich.style import Style
#</editor-fold>

#<editor-fold desc="Set Ups">
console = Console(highlight = False)
mainStyle = Style(color = "yellow")
#</editor-fold>

def LapTimes(jpxFrame):
    #Creates The Table
    lapTimeTable = Table(title="Lap Times", box=box.SIMPLE, title_style=mainStyle)
    #Adds The Columns
    lapTimeTable.add_column("Lap", justify="center")
    lapTimeTable.add_column("Time", justify="center")

    for lapNum in range(jpxFrame['Lap'].min(), jpxFrame['Lap'].max()):
        #Gets The Current Laps Info As A New Frame
        lapFrame = jpxFrame[jpxFrame['Lap'] == lapNum]

        #Subtracts The First Time From The Last Time In The Lap And Reformat's It Through A New TimeDelta Object
        lapTime = timedelta(seconds=(lapFrame['Time'].iloc[-1] - lapFrame['Time'].iloc[0]).total_seconds())

        #Adds The Lap Time To The Row
        lapTimeTable.add_row(str(lapNum), str(lapTime))

    #Prints The Table
    console.print(lapTimeTable)

def SectorTimes(jpxFrame, outLapNum):
    #Creates The Table
    lapTimeTable = Table(title="Sector Times For Lap " + str(outLapNum), box=box.SIMPLE, title_style=mainStyle)
    #Adds The Columns
    lapTimeTable.add_column("Sector", justify="center")
    lapTimeTable.add_column("Time", justify="center")

    #Makes A New Frame With The Current Lap Data
    lapFrame = jpxFrame[jpxFrame['Lap'] == outLapNum]

    minLapDistance = lapFrame['CDistance'].iloc[0]
    totalLapDistance = lapFrame['CDistance'].iloc[-1] - minLapDistance

    sectorLength = totalLapDistance / 3

    for sectorMulti in range (1, 4):
        #Builds A New Frame With The Info From This Current Sector
        sectorFrame = lapFrame[lapFrame['CDistance'] <= minLapDistance + (sectorLength * sectorMulti)]
        #Removes Any Times From The Previous Sectors
        sectorFrame = sectorFrame[sectorFrame['CDistance'] > minLapDistance + (sectorLength * (sectorMulti - 1))]

        #Works Out The Sector Time
        sectorTime = timedelta(seconds=(sectorFrame['Time'].iloc[-1] - sectorFrame['Time'].iloc[0]).total_seconds())

        #Adds The Lap Time To The Row
        lapTimeTable.add_row(str(sectorMulti), str(sectorTime))

    #Prints The Table
    console.print(lapTimeTable)