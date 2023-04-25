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

# Neue Spalte "Gruppe" erstellen
df["Gruppe"] = np.nan

# Aktualisieren der Werte in der Spalte "Rollen"
df["Rollen"] = np.where(df["Rollen"] == "Teilnehmer/-in", "TN",
                       np.where(df["Rollen"].isin(["Klassenlehrer*in", "Kurshelfer*in", "Kursleiter*in"]), "Leiter", df["Rollen"]))

# Liste von Teilnehmer und Leiter erstellen
teilnehmer = df[df["Rollen"] == "TN"]
leiter = df[df["Rollen"] == "Leiter"]

# Anzahl von Leitern
anzahl_leiter = leiter.shape[0]

# Gruppieren und Zählen der Anzahl von Personen in jeder Gruppe
max_personen_Adresse = teilnehmer.groupby("Adresse").size().max()
max_personen_Ort = teilnehmer.groupby("Ort").size().max()
max_personen_Hauptebene = teilnehmer.groupby("Hauptebene").size().max()
max_personen_Kantonalverband = teilnehmer.groupby("Kantonalverband").size().max()

# Ausgabe der maximalen Anzahl von Personen mit gleichem Ort
print("Maximale Anzahl von Personen mit gleicher Adresse:", max_personen_Adresse)
print("Maximale Anzahl von Personen mit gleichem Ort:", max_personen_Ort)
print("Maximale Anzahl von Personen mit gleicher Hauptebene:", max_personen_Hauptebene)
print("Maximale Anzahl von Personen mit gleichem Kantonalverband:", max_personen_Kantonalverband)

# Ausgabe der Anzahl Leiter (Gruppen)
print("Anzahl von Leitern:", anzahl_leiter)