#<editor-fold desc="Imports">
import pandas as pd
import os.path as path

import Serialization
import Graphs
#</editor-fold>

#Var Holders For The File URl
validJPXURL = False
urlInput = ""

#Loops Indefinitely Until A Correct JPX File Is Passed In
while not validJPXURL:
    #Asks The User For An URL
    print("Enter The URL To A JPX File For Analysis:")
    urlInput = input()

    #Checks That It Is A Real File And That It's A '.jpx' File
    if path.exists(urlInput) and path.splitext(urlInput)[1] == ".jpx":
        validJPXURL = True

#Parse The JPX File And Converts The Waypoints Back To A Pandas DataFrame
jpxFile = Serialization.ReadFile(urlInput)
jpxFrame = pd.json_normalize(jpxFile["Waypoints"])

#Loops Indefinitely (Well Until The Quit Option Is Picked) Allowing All The Tools To Be Used On File Without Having To Keep Re-Running The Program
while True:
    print("""Modes:
    - RG | Route Graph: Creates A Route Map With Colours Representing Either Speed Or Elevation
    - T | Telemetry: Creates A Telemetry Graph Showing Speed And Elevation
    - Q | Quit""")
    modeInput = str(input())

    if modeInput.lower() == "rg" or modeInput.lower() == "route graph":
        print("Enter S For A Speed Graph, Or E For An Elevation Graph")
        optionInput1 = str(input())
        print("Enter A Specific Lap Number, Or 0 For All Laps")
        optionInput2 = int(input())

        if optionInput1.lower() == "s":
            Graphs.RouteGraph(jpxFrame, "Speed", optionInput2, jpxFile["Name"])
        elif optionInput1.lower() == "e":
            Graphs.RouteGraph(jpxFrame, "Elevation", optionInput2, jpxFile["Name"])
        else:
            print("Invalid Options")

    elif modeInput.lower() == "t" or modeInput.lower() == "telemetry":
        print("Enter A Specific Lap Number, Or 0 For All Laps")
        optionInput1 = int(input())

        Graphs.Telemetry(jpxFrame, optionInput1)

    elif modeInput.lower() == "q" or modeInput.lower() == "quit":
        quit()