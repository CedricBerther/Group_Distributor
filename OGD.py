import pandas as pd
import numpy as np
import os

# Den Pfad der Python-Datei erhalten
script_path = os.path.abspath(__file__)

# Das Verzeichnis der Python-Datei als Arbeitsverzeichnis festlegen
os.chdir(os.path.dirname(script_path))

# Read the Excel file into a DataFrame
file_path = "event_participation_export.xlsx"
df = pd.read_excel(file_path)
columns_to_keep = ["Vorname", "Nachname", "Pfadiname", "Adresse", "Ort", "Hauptebene", "Rollen", "Anrede", "Kantonalverband"]  # List of columns to keep
df = df[columns_to_keep]


teilnehmende = df[df["Rollen"] == "Teilnehmer/-in"]
leitende = df[(df['Rollen'] == 'Klassenlehrer*in') | (df['Rollen'] == 'Kurshelfer*in') | (df['Rollen'] == 'Kursleiter*in')]
