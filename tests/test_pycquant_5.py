from secret.local_settings import pycquant_path, analysis_data_csv
import sys
sys.path.insert(0, pycquant_path)
import datahandling
import pandas as pd

# --- Input parameters ---
df = datahandling.read_analysis_csv_data(analysis_data_csv, 1)
print(df.head(50))
print(df.tail(50))
#print(df.head(200).to_string())