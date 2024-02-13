import datahandling
import pandas as pd

# --- Input parameters ---
analysis_data_csv   = '/Volumes/NASpi/data/MT5/analysis_data'

df = datahandling.read_analysis_csv_data(analysis_data_csv, 1)

#print(df.head(200).to_string())