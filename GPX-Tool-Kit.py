#<editor-fold desc="Imports">
import Serialization

import pandas as pd
#</editor-fold>

jpxFile = Serialization.ReadFile("JPX Files/Betteshanger-23KM.jpx")
jpxFrame = pd.json_normalize(jpxFile["Waypoints"])