import pandas as pd
import os
from tqdm import tqdm
from datetime import datetime
import numpy as np

def read_from_ids(ids, daytype, dir):
    data_dict = {}
    for id in tqdm(ids, desc="Reading "+ daytype + " data"):
        try:
            sensor_data = pd.read_csv(os.path.join(dir,daytype,id+".csv"))
            sensor_data["date"] = pd.to_datetime(sensor_data["date"], infer_datetime_format=True)
            data_dict[id] = sensor_data
        except:
            pass
    return data_dict

def query(sensor_data, begin, end, scale):
    """
    Input:
    - sensor_data: A list of sensor data
    - begin, end: datetime, Time range
    - scale: {hour, day, week, month}

    Output:
    - Statistics(a pd.Series) on these sensors during a specific time range

    Details:
    - For missing id, ignore it
    """
    # Select data in [begin, end] 
    # Aggregate by scale
    if scale == "hour":
        data_in_range = []
        for data in sensor_data:
            data_in_range.append(data[(data["date"] >= begin) & (data["date"] < end)].copy(deep=True).reset_index())
        agg_data = pd.concat(data_in_range)
        agg_data = agg_data.groupby(["hour"]).agg(occ = pd.NamedAgg(column="occ", aggfunc="mean"),
                                                  flow = pd.NamedAgg(column="flow", aggfunc="mean")).reset_index()
    elif scale == "day":
        data_in_range = []
        for data in sensor_data:
            data_copy = data[(data["date"] >= begin) & (data["date"] < end)].copy(deep=True).reset_index() 
            data_copy = data_copy.dropna()
            data_in_range.append(data_copy)
        agg_data = pd.concat(data_in_range)
        agg_data = agg_data.groupby(["date"]).agg(occ = pd.NamedAgg(column="occ", aggfunc="mean"),
                                                  flow = pd.NamedAgg(column="flow", aggfunc="mean")).reset_index()
    elif scale == "week":
        data_in_range = []
        for data in sensor_data:
            data_copy = data[(data["date"] >= begin) & (data["date"] < end)].copy(deep=True).reset_index()
            data_copy["week"] = data_copy["date"].apply(lambda x: x.isocalendar().week)
            data_copy = data_copy.dropna()
            data_in_range.append(data_copy)
        agg_data = pd.concat(data_in_range)
        agg_data = agg_data.groupby(["week"]).agg(occ = pd.NamedAgg(column="occ", aggfunc="mean"),
                                                  flow = pd.NamedAgg(column="flow", aggfunc="mean")).reset_index()
                      
    elif scale == "month":
        data_in_range = []
        for data in sensor_data:
            data_copy = data[(data["date"] >= begin) & (data["date"] < end)].copy(deep=True).reset_index()
            data_copy["month"] = data_copy["date"].apply(lambda x: x.month)
            data_copy = data_copy.dropna()
            data_in_range.append(data_copy)
        agg_data = pd.concat(data_in_range)
        agg_data = agg_data.groupby(["month"]).agg(occ = pd.NamedAgg(column="occ", aggfunc="mean"),
                                                  flow = pd.NamedAgg(column="flow", aggfunc="mean")).reset_index()
    return agg_data         

def to_relative(series):
    """
    Input:
    - series: pandas.Series

    Output:
    - relative values
    """
    return series/np.sum(series.to_numpy())

def normalize(series):
    """
    Input:
    - series: pandas.Series

    Output:
    - relative values
    """
    return (series - series.mean()) / series.std()
   

if __name__ == "__main__":
    id_path = "./preprocessed_data/city/city_id.csv"
    data_path = "./preprocessed_data/city"
    id = list(pd.read_csv(id_path)["detid"])
    weekend_df_dict = read_from_ids(id, "weekend", data_path)
    weekend_df_list = list(weekend_df_dict.values())
    weekend_agg_df = query(weekend_df_list, datetime(2018,1,1), datetime(2018,2,1), "hour")
    print(weekend_agg_df)
    weekend_agg_df = query(weekend_df_list, datetime(2018,2,1), datetime(2018,3,1), "hour")
    print(weekend_agg_df)
    print(to_relative(weekend_agg_df["occ"]))
    print(normalize(weekend_agg_df["occ"]))