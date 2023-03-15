# Input:
# - raw data
# Output:
# - Statistics per sensor

import pandas as pd

chunksize = 1000
filename = "./Zurich_2020_raw2"
df = pd.DataFrame()

for chunk in pd.read_csv("./Zurich_2020_raw2", chunksize=chunksize):
    chunk['date'] = pd.to_datetime(chunk['src_time'], infer_datetime_format=True).dt.date
    chunk.rename(columns={'vd_speed_val':'speed', 'vd_length_val':'length', 'vd':'sensor_id'})
    sensor = chunk.groupby(['sensor_id', 'date']).aggregate({'ncars': 'size', 'speed':['mean', 'min', 'max'], 'length': ['mean', 'min', 'max']}).reset_index()
    df.append(sensor)

