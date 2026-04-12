import pandas as pd
from gemini import contact_info
import time

filename = "RERA_Mar.xlsx"

df = pd.read_excel(filename)

if "CONTACT NO" not in df.columns:
    df["CONTACT NO"] = ""

for i,row in df.iterrows():
    if pd.notna(row["CONTACT NO"]) and row["CONTACT NO"] != "":
        continue

    name = row["PROMOTER NAME"]
    location = row["ADDRESS"]
    project = row["PROJECT NAME"]
    contact = contact_info(name, location, project)

    df.at[i, "CONTACT NO"] = contact

    df.to_excel(filename, index=False)

    print(f"Processed row {i+1}")
    print(contact)

    time.sleep(4)

print("Excel file saved successfully!")