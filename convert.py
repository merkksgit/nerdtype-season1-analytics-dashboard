import pandas as pd

# Read the JSON file
df = pd.read_json("scores_data.json")

# Export to Excel format
df.to_excel("scores_data.xlsx", index=False)

print("JSON file successfully converted to XLSX!")
