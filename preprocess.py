# Input:
# - raw data
# Output:
# - Statistics per sensor
import pandas as pd
import os
from tqdm import tqdm
import holidays

# Extract data per sensor and per hour from raw data as our basic data
chunksize = 10**6
raw_dir = "./raw_data/city"
processed_dir = "./preprocessed_data/city" 
ch_zh_holidays = holidays.country_holidays(country='CH', subdiv='ZH')
df_list = []

for filename in tqdm(os.listdir(raw_dir), desc="Reading files", position=1): # Read the file from raw_dir
    i = 0
    for chunk in pd.read_csv(os.path.join(raw_dir, filename), chunksize=chunksize):
        if (i+1)%50 == 0:
            print(f"chunk {i+1} in process.")
        chunk["date"] = pd.to_datetime(chunk["day"], infer_datetime_format=True) # Organize the data per hour
        chunk["hour"] = chunk["interval"].floordiv(3600)
        # Don't know how to deal with flow
        chunk = chunk.groupby(["detid", "date", "hour"]).agg(occ = pd.NamedAgg(column="occ", aggfunc="sum"),
                                                        flow = pd.NamedAgg(column="flow", aggfunc="sum")).reset_index()
        df_list.append(chunk)
        
        i += 1
df = pd.concat(df_list, ignore_index=True)
df["daytype"] = df["date"].apply(lambda x: "holiday" if x in ch_zh_holidays else ("workday" if x.weekday()<5 else "weekend") )
workday_df = df[df["daytype"] == "workday"]
weekend_df = df[df["daytype"] == "weekend"]
holiday_df = df[df["daytype"] == "holiday"]
workday_df = workday_df.groupby(["detid", "date", "hour"]).agg(occ = pd.NamedAgg(column="occ", aggfunc="sum"),
                                        flow = pd.NamedAgg(column="flow", aggfunc="sum"))
weekend_df = weekend_df.groupby(["detid", "date", "hour"]).agg(occ = pd.NamedAgg(column="occ", aggfunc="sum"),
                                        flow = pd.NamedAgg(column="flow", aggfunc="sum"))
holiday_df = holiday_df.groupby(["detid", "date", "hour"]).agg(occ = pd.NamedAgg(column="occ", aggfunc="sum"),
                                        flow = pd.NamedAgg(column="flow", aggfunc="sum"))

# Remove abnormal data and write processed files to processed_dir

# Count how many days are discarded
total_rows = 0
valid_rows = 0
names = ["workday", "weekend", "holiday"]
dfs = [workday_df, weekend_df, holiday_df]
for i in range(len(dfs)):
    total_rows += len(dfs[i].index)
    for detid in tqdm(dfs[i].index.get_level_values(0).unique(), desc="Writing files"):
        sensor_data = dfs[i].loc[detid].copy(deep=True)
        # 1. Remove zeros (due to bad sensors or road construction)
        sensor_data = sensor_data.reset_index() 
        sensor_data = sensor_data.groupby(["date"]).agg(occ = pd.NamedAgg(column="occ", aggfunc="sum"),
                                   flow = pd.NamedAgg(column="flow", aggfunc="sum")).reset_index()
        data_1 = sensor_data[sensor_data["flow"] != 0]
        # 2. Remove extreme values
        q_low = data_1["flow"].quantile(0.01)
        q_hi  = data_1["flow"].quantile(0.99)
        data_2 = data_1[(data_1["flow"] < q_hi) & (data_1["flow"] > q_low)]
        valied_sensor_data = dfs[i].loc[detid].loc[data_2["date"]]
        valid_rows += len((valied_sensor_data.index))
        valied_sensor_data.to_csv(os.path.join(processed_dir, names[i], detid+".csv")) 

        
print(total_rows, valid_rows)


