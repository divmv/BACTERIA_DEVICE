# -*- coding: utf-8 -*-
# DataProcessor

import os
import pandas as pd
import time
from datetime import datetime
import numpy as np

def create_and_move_csv(input_folder, output_root="ProcessedData"):
    if not os.path.exists(input_folder):
        return "Invalid input folder"

    input_folder = os.path.join(input_folder, "data")

    # Create daily processed folder
    timestamp = time.strftime("%Y%m%d")
    new_folder_name = f"Processed_{timestamp}"
    new_folder_path = os.path.join(output_root, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)

    # Process and merge directly into the new folder
    process_and_merge_csv(input_folder, new_folder_path)
    return f"Processed files written to {new_folder_path}"

def process_and_merge_csv(input_folder, output_folder):
    current_date = datetime.now().strftime("%Y_%m_%d")

    merged_data = pd.DataFrame()

    # Go through all CSVs in RecordedData
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_folder, file_name)

            current_data = pd.read_csv(file_path)
            print(f"Read: {file_name}, shape={current_data.shape}")

            current_data = demeaner(current_data)

            # Add file info if naming convention matches
            file_info = file_name.split('_')
            try:
                if len(file_info) > 6:
                    bacteria = file_info[1]
                    concentration = file_info[2]
                    volume = file_info[3]
                    slide = file_info[4]
                    trail = file_info[6].split('.')[0]
                else:
                    bacteria = file_info[1]
                    concentration = file_info[2]
                    volume = file_info[3]
                    slide = 0
                    trail = file_info[5].split('.')[0]

                current_data['bacteria'] = bacteria
                current_data['concentration'] = concentration
                current_data['volume'] = volume
                current_data['slide'] = slide
                current_data['trail'] = trail
            except Exception as e:
                print(f"⚠️ Skipping metadata extraction for {file_name}: {e}")

            merged_data = pd.concat([merged_data, current_data], ignore_index=True)

    # Clean (prune) data
    merged_data = pruner(merged_data)

    # Write final processed master file
    merged_file_path = os.path.join(output_folder, f'masterData_{current_date}.csv')
    merged_data.to_csv(merged_file_path, index=False)
    print(f"✅ Master data written to: {merged_file_path}")


def demeaner(data):
    # Example demeaner logic (replace with your own)
    # This assumes an "EmptyData" baseline is available
    baseline_file = os.path.join("RecordedData/data", "EmptyData_2024_02_29.csv")
    if os.path.exists(baseline_file):
        df2 = pd.read_csv(baseline_file)
        df2 = avg_calculator(df2)

        count = 0
        for i in [10,20,30,40,50,60]:
            mean1 = df2['Xpos'].iloc[count:(i*1000)].mean()
            mean2 = df2['Ypos'].iloc[count:(i*1000)].mean()
            data.loc[count:(i*1000)-1, 'Xpos'] -= mean1
            data.loc[count:(i*1000)-1, 'Ypos'] -= mean2
            count = i*1000
    return data

def avg_calculator(data):
    columns = ['Xpos','Ypos','bacteria']
    newD = pd.DataFrame(columns=columns)
    for i in data['bacteria'].unique():
        dataX = data[data['bacteria']==i]
        data1 = dataX[dataX["trail"]=="T1"]
        data2 = dataX[dataX["trail"]=="T2"]
        data3 = dataX[dataX["trail"]=="T3"]
        empty_dataset = pd.DataFrame()
        empty_dataset['Xpos']=(np.array(data1['Xpos'])+np.array(data2['Xpos'])+np.array(data3['Xpos']))/3
        empty_dataset['Ypos']=(np.array(data1['Ypos'])+np.array(data2['Ypos'])+np.array(data3['Ypos']))/3
        empty_dataset['bacteria'] = i
        newD=pd.concat([newD,empty_dataset])
    return newD

def pruner(data):
    for col in ['Xpos','Ypos','Pow']:
        if col in data.columns:
            means = data[col].mean()
            stds = data[col].std()
            lower_bounds = means - 3 * stds
            upper_bounds = means + 3 * stds
            data[col] = np.where(data[col].between(lower_bounds, upper_bounds), data[col], np.nan)
    return data
