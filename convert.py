import pandas as pd

# Method 1: Convert JSON to Excel (XLSX)
# Converts JSON data directly to Excel format without flattening nested structures
# df = pd.read_json("scores_data.json")
# df.to_excel("scores_data.xlsx", index=False)
# print("JSON file successfully converted to XLSX!")

# Method 2: Convert JSON to CSV (basic)
# Converts JSON to CSV but may not handle nested objects properly
# Each nested object might appear as a single column instead of separate columns
# df = pd.read_json("scores_data.json")
# df.to_csv("scores_data.csv", sep=",", index=False)
# print("JSON file successfully converted to CSV!")

# Method 3: Convert nested JSON to flattened CSV
# Reads nested JSON structure and transposes it so each game ID becomes a row
# Each attribute (score, wpm, accuracy, etc.) becomes its own column
# Ideal for BigQuery upload with proper column structure
df = pd.read_json("scores_data.json")
df = df.T
df.reset_index(inplace=True)
df.rename(columns={"index": "id"}, inplace=True)

# Save to CSV
df.to_csv("scores_data.csv", index=False)
print("JSON file successfully converted to CSV!")
