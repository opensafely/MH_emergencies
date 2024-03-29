import pandas as pd
import os

ethnicity_df = pd.read_feather('output/input_ethnicity.feather')

for file in os.listdir('output/measures'):
    #if file.startswith('input'):
        #exclude ethnicity
        #if file.split('_')[1] not in ['ethnicity.csv', 'practice']:
            file_path = os.path.join('output/measures', file)
            df = pd.read_csv(file_path)
            merged_df = df.merge(ethnicity_df, how='left', on='patient_id')
            merged_df.to_csv(file_path)
