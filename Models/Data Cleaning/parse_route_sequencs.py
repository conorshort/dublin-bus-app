import pandas as pd


df = pd.read_csv("C:/Users/cls15/Google Drive/Comp Sci/Research Practicum/Code/dublin-bus-app/Models/Data Cleaning/routesequences.csv")

df = df[df.Operator == "Dublin Bus"]
df = df.drop(columns=['RouteData', "AtcoCode"])

df['HasPole'].loc[df['HasPole'] == "Pole"] = 1
df['HasPole'].loc[df['HasPole'] == "No Pole"] = 0
df['HasPole'].loc[df['HasPole'] == "Unknown"] = ""

df['HasShelter'].loc[df['HasShelter'] == "Shelter"] = 1
df['HasShelter'].loc[df['HasShelter'] == "No Shelter"] = 0
df['HasShelter'].loc[df['HasShelter'] == "Unknown"] = ""

df = df.rename(columns={'Direction': 'DirectionInbound'})
df['DirectionInbound'].loc[df['DirectionInbound'] == "Outbound"] = 0
df['DirectionInbound'].loc[df['DirectionInbound'] == "Inbound"] = 1


print(df[df["HasShelter"] == ""])
