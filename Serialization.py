#<editor-fold desc="Imports">
import gpxpy.gpx
from geopy import distance

import pandas as pd

import json
from datetime import datetime
#</editor-fold>

#Takes A GPX File And Converts It To A JPX File
def ConvertFile(url, isLaps, outUrl):
    #Opens Up The Provided URL To Access The GPX File
    gpxFile = gpxpy.parse(open(url, 'r'))

    #Creates A Pandas DataFrame To Hold The GPX Data
    gpxFrame = pd.DataFrame(columns=['Long', 'Lat', 'Elevation', 'Time', 'Speed', 'Lap'])

    #Var Holders For The First Point LatLong And Starting Lap Number
    firstPoint = ()
    lapNumber = 1

    #The Loop Count
    loopCount = 0
    #Loops Through All The Tracks -> Segments -> Points To Collect Every Waypoint In The File
    for track in gpxFile.tracks:
        for segment in track.segments:
            for point in segment.points:
                #Instaed Of Working This Out A Maximum Of 3 Times An Increment Just Do It Once Right Away
                currentPointTime = datetime.combine(point.time.date(), point.time.time())

                #If This If The First Point
                if loopCount == 0:
                    #Remeber The This Starting Location (Needed To Work Out When We Get Close To Start Another Lap (If isLaps = True))
                    firstPoint = (point.longitude, point.latitude)

                    #The Speed As You Start Should Be Zero If This Data Wasn't In The File
                    speed = 0.0
                    if point.speed is not None:
                        #If It Was However Use That Correct Value Instead
                        speed = point.speed

                    #Add This Waypoints Data To The DataFrame
                    gpxFrame = gpxFrame.append({'Long': point.longitude, 'Lat': point.latitude, 'Elevation': point.elevation, 'Time': currentPointTime, 'Speed': speed, 'Lap': lapNumber}, ignore_index=True)
                else:
                    #The Current LatLong
                    currentPoint = (point.longitude, point.latitude)

                    #Previous Lap Number
                    prevLapNumber = lapNumber
                    #If This File Actually Contains 'Laps'
                    if isLaps:
                        #Checks To See If The GPS Has Passed The Starting Point Again To Start A New Lap
                        fpDist = distance.distance(firstPoint, currentPoint).km
                        if fpDist <= 0.034:
                            lapNumber += 1

                    if point.speed is None:
                        #Grabs The Previous Entries Info
                        prevDF = gpxFrame.iloc[loopCount - 1]
                        #Creates The Lat&Long Values
                        prevPoint = (prevDF['Long'], prevDF['Lat'])
                        #Finds The Distance And Time Diff
                        dist = distance.distance(prevPoint, currentPoint).meters
                        pointTime = currentPointTime - prevDF['Time']
                        #Uses These To Work Out The Speed
                        speed = (dist / pointTime.total_seconds()) * 3.6
                    else:
                        speed = point.speed

                    # If We Are Converting Into Laps And It's Time For A New One Finish Off The Old One With An Extra Point To Stop The Laps Missing The Final Section
                    if isLaps and prevLapNumber != lapNumber:
                        gpxFrame = gpxFrame.append({'Long': point.longitude, 'Lat': point.latitude, 'Elevation': point.elevation, 'Time': currentPointTime, 'Speed': speed, 'Lap': prevLapNumber}, ignore_index=True)

                    #Add This Waypoints Data To The DataFrame
                    gpxFrame = gpxFrame.append({'Long': point.longitude, 'Lat': point.latitude, 'Elevation': point.elevation, 'Time': currentPointTime, 'Speed': speed, 'Lap': lapNumber}, ignore_index=True)

                #Increment The Loop Count
                loopCount += 1

    #Now We Have All The Points In The DataFrame We Can Move To Converting This To A JPX File
    jpxContents = {
        "Name": gpxFile.tracks[0].name,
        "Time": str(gpxFile.tracks[0].segments[0].points[0].time),
        "Version": 1.0,
        "Waypoints": json.loads(gpxFrame.to_json(orient = "records"))
    }

    with open(outUrl, 'w', encoding='utf-8') as jpxFile:
        json.dump(jpxContents, jpxFile, ensure_ascii = False, indent = 4)

#Reads A JPX File And Returns It For The Program To Use
def ReadFile(url):
    #Loads The File
    jpxFile = json.load(open(url))

    #Goes Through Each Waypoint And Converts The Time From A Unix Timestamp To A DateTime Function For Easier Use Straight Away
    for i in jpxFile["Waypoints"]:
        i["Time"] = datetime.utcfromtimestamp(i["Time"] / 1000)

    return jpxFile