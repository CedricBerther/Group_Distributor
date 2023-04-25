import pandas as pd
import numpy as np
import os

# Get the path of the Python file
script_path = os.path.abspath(__file__)

# Set the directory of the Python file as the working directory
os.chdir(os.path.dirname(script_path))

# Read the Excel file into a DataFrame
file_path = "event_participation_export.xlsx"
df = pd.read_excel(file_path)
columns_to_keep = ["Vorname", "Nachname", "Pfadiname", "Adresse", "Ort", "Hauptebene", "Rollen", "Anrede", "Kantonalverband"]  # List of columns to keep
df = df[columns_to_keep]

# New column "Gruppe" created
df["Gruppe"] = np.nan

# Update the values in the "Rollen" column
df["Rollen"] = np.where(df["Rollen"] == "Teilnehmer/-in", "TN",
                       np.where(df["Rollen"].isin(["Klassenlehrer*in", "Kurshelfer*in", "Kursleiter*in"]), "Leiter", df["Rollen"]))

# List of participants and leaders
teilnehmer = df[df["Rollen"] == "TN"]
leiter = df[df["Rollen"] == "Leiter"]

# Shuffle the participants randomly
teilnehmer = teilnehmer.sample(frac=1, random_state=42).reset_index(drop=True)

# Number of participants and leaders
anzahl_teilnehmer = teilnehmer.shape[0]
anzahl_leiter = leiter.shape[0]

# Number of groups and participants per group
anzahl_gruppen = 6
teilnehmer_pro_gruppe = 4

# Distribute participants into groups
for i in range(anzahl_teilnehmer):
    gruppe_nummer = (i % anzahl_gruppen) + 1  # Group number starts from 1
    df.at[teilnehmer.index[i], "Gruppe"] = gruppe_nummer

# Group by "Gruppe" and get the count of occurrences
gruppe_counts = df.groupby("Gruppe").size()

# Print the count of occurrences for each group
for gruppe, count in gruppe_counts.items():
    print("Anzahl von Personen in Gruppe {}: {}".format(gruppe, count))
