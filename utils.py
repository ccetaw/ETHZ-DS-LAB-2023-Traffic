import pandas as pd
import os
from tqdm import tqdm
from datetime import datetime
import numpy as np

def read_from_ids(ids, daytype, dir):
    """Reading csv files for a list of sensor ids
    Args:
        - ids: list of ids
        - daytype: choose from {"workday", "weekend", "holiday"}
        - dir: directory containing files

    Returns:
        - A dict with keys being id and value being corresponding dataframe
    """
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
    """Query the aggregated data from the sensor data list in (begin, end) for a scale.
    The finest scale is hour. Could also choose "day", "week" and "month". For missing id, ignore it.

    Args:
    - sensor_data: A list of sensor data
    - begin, end: datetime
    - scale: {hour, day, week, month}

    Returns:
    - Statistics(a pd.Series) on these sensors during a specific time range
    """
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

def relative(array):
    """Get the relative values of an array, i.e., every element sums up to 1
    nan values are treated with np.nansum(), i.e., ignored

    Args:
    - array: numpy array

    Returns:
    - relative values
    """
    assert len(array.shape) == 1
    return array / np.nansum(array)

def normalize(array):
    """
    Args:
    - array: np.array

    Returns:
    - normalized values
    """
    assert len(array.shape) == 1
    return (array - np.mean(array)) / np.std(array)
   
def compute_yoy(before, after):
    """ Compute year over year increase/decrease percentage
    Args:
    - before: scalar or numpy array
    - after: scalar or numpy array

    Returns:
    - ratio: increase/decrease percentage
    """
    assert type(before) == type(after)
    if type(before) == np.ndarray:
        assert len(before) == len(after)

    return (after - before) / before

# Testing 
if __name__ == "__main__":
    id_path = "./preprocessed_data/city/city_id.csv"
    data_path = "./preprocessed_data/city"
    id = list(pd.read_csv(id_path)["detid"])
    weekend_df_dict = read_from_ids(id, "weekend", data_path)
    weekend_df_list = list(weekend_df_dict.values())
    weekend_agg_df = query(weekend_df_list, datetime(2018,1,1), datetime(2018,2,1), "hour")
    print(weekend_agg_df)
    print(relative(weekend_agg_df["occ"].to_numpy()))
    print(normalize(weekend_agg_df["occ"].to_numpy()))