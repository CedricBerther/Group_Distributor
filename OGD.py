import pandas as pd
import numpy as np
import os
import random


# Variables you can edit:
file_path = "event_participation_export.xlsx"
anzahl_gruppen = 6
teilnehmer_pro_gruppe = 4

# Get the path of the Python file
script_path = os.path.abspath(__file__)

# Set the directory of the Python file as the working directory
os.chdir(os.path.dirname(script_path))

# Read the Excel file into a DataFrame
df = pd.read_excel(file_path)
columns_to_keep = ["Vorname", "Nachname", "Pfadiname", "Geschlecht", "Ort", "Hauptebene", "Rollen", "Anrede", "Kantonalverband"]  # List of columns to keep
df = df[columns_to_keep]

# New column "Gruppe" created
df["Gruppe"] = np.nan

# Update the values in the "Rollen" column
df["Rollen"] = np.where(df["Rollen"] == "Teilnehmer/-in", "TN",
                       np.where(df["Rollen"].isin(["Klassenlehrer*in", "Kurshelfer*in", "Kursleiter*in"]), "Leiter", df["Rollen"]))

# List of participants and leaders
teilnehmer = df[df["Rollen"] == "TN"]
leiter = df[df["Rollen"] == "Leiter"]

teilnehmer_count = len(df[df["Rollen"] == "TN"])
leiter_count = len(df[df["Rollen"] == "Leiter"])

# Shuffle the participants randomly with a different random seed each time
teilnehmer = teilnehmer.sample(frac=1, random_state=np.random.randint(10000))

# Calculate the total number of groups needed
anzahl_teilnehmer = 24

# Assign participants to groups
gruppen = np.repeat(range(1, anzahl_gruppen + 1), teilnehmer_pro_gruppe)
gruppen = np.concatenate([gruppen, np.random.randint(1, anzahl_gruppen + 1, anzahl_teilnehmer % teilnehmer_pro_gruppe)])

# Update the "Gruppe" column in the DataFrame
teilnehmer["Gruppe"] = gruppen

# Define functions for calculating points
def get_gender_points(group):
    gender_counts = group["Geschlecht"].value_counts()
    if gender_counts.get("männlich") == 2 and gender_counts.get("weiblich") == 2:
        return 1
    elif (gender_counts.get("männlich") == 3 and gender_counts.get("weiblich") == 1) or (gender_counts.get("männlich") == 1 and gender_counts.get("weiblich") == 3):
        return 0.5
    else:
        return 0

def get_region_points(group):
    kantonalverband_counts = group["Kantonalverband"].value_counts()
    if len(kantonalverband_counts) == 4:
        return 9
    elif len(kantonalverband_counts) == 3:
        return 0.5
    else:
        return 0
    
def get_group_points(group):
    hauptebene_counts = group["Hauptebene"].value_counts()
    if len(hauptebene_counts) == 4:
        return 1
    elif len(hauptebene_counts) == 3:
        return 0.5
    else:
        return 0

# Iterate 100 times and randomly assign participants to groups
max_total_points = 0
max_group_assignment = None
for i in range(1000):

    gruppen = np.random.randint(1, anzahl_gruppen + 1, teilnehmer_count)
    teilnehmer["Gruppe"] = gruppen

    # Iterate over the groups and calculate points for gender and region
    total_points = 0
    for group, participants in teilnehmer.groupby("Gruppe"):
        gender_points = get_gender_points(participants)
        region_points = get_region_points(participants)
        group_points = get_group_points(participants)
        total_points += gender_points + region_points + group_points

    # Keep track of the group assignment with the highest total points
    if total_points > max_total_points:
        max_total_points = total_points
        max_group_assignment = gruppen

# Update the "Gruppe" column in the DataFrame with the group assignment with the highest total points
teilnehmer["Gruppe"] = max_group_assignment

# Print the group assignments and total points after the loop
for group, participants in teilnehmer.groupby("Gruppe"):
    print(f"Group {group}:")
    for index, row in participants.iterrows():
        print(f"{row['Geschlecht']} {row['Hauptebene']} {row['Kantonalverband']}")
    print("\n")

print("\n")
print(max_total_points)

# Replace file_path with the path and name you want to save the Excel file as
file_path = "group_assignments.xlsx"

# Replace teilnehmer with the name of the DataFrame that includes the "Gruppe" column updates
teilnehmer = teilnehmer.sort_values(by=["Gruppe", "Kantonalverband", "Hauptebene"])
teilnehmer.to_excel(file_path, index=False, columns=["Pfadiname", "Geschlecht", "Kantonalverband", "Hauptebene", "Gruppe"])
