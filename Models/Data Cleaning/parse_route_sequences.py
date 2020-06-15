import pandas as pd
import numpy as np
print("Reading csv...")
df = pd.read_csv(
    "C:/Users/cls15/Google Drive/Comp Sci/Research Practicum/Code/dublin-bus-app/Models/Data Cleaning/routesequences.csv")

print("Parsing data...")
df = df.copy().loc[df.Operator == "Dublin Bus"]
df = df.drop(columns=['RouteData', "AtcoCode"])

df.loc[df['HasPole'] == "Pole", "HasPole"] = 1
df.loc[df['HasPole'] == "No Pole", "HasPole"] = 0
df.loc[df['HasPole'] == "Unknown", "HasPole"] = None

df.loc[df['HasShelter'] == "Shelter", 'HasShelter'] = 1
df.loc[df['HasShelter'] == "No Shelter", 'HasShelter'] = 0
df.loc[df['HasShelter'] == "Unknown", 'HasShelter'] = None

df = df.rename(columns={'Direction': 'DirectionInbound'})
df.loc[df['DirectionInbound'] == "Outbound", "DirectionInbound"] = 0
df.loc[df['DirectionInbound'] == "Inbound", "DirectionInbound"] = 1

df = df.replace(np.nan, None)
print("Adding to db...")
