import pandas as pd

file_path = "event_participation_export.xlsx"
df = pd.read_excel(file_path)

# Split the data into two groups: leaders and participant
leaders = df[(df['Rollen'] == 'Klassenlehrer*in') | (df['Rollen'] == 'Kurshelfer*in') | (df['Rollen'] == 'Kursleiter*in')]  
participant = df[df['Rollen'] == 'Teilnehmer/-in']  


# Get the number of persons in both groups
num_leaders = len(leaders)
num_participant = len(participant)

# Print the number of persons in both group
print("Number of persons in leaders group: ", num_leaders)
print("Number of persons in participant group: ", num_participant)
