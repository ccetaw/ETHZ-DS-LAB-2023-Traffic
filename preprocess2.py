import numpy as np
import pandas as pd
import umap
from utils import (
    read_from_ids,
    query
)
from datetime import datetime, timedelta
from tqdm import tqdm
import os

# Load the data
data_folder = "./raw_data/city"
years = [2018, 2019, 2020, 2021]

# process
label = []
one_day = timedelta(days=1)

for file in tqdm(os.listdir(data_folder)):
    year_df = pd.read_csv(os.path.join(data_folder, file))
    year_df = year_df.groupby(["date", "hour"]).agg(occ = pd.NamedAgg(column="occ", aggfunc="mean"),
                                                    flow = pd.NamedAgg(column="flow", aggfunc="mean"))
    print(year_df.loc[datetime(2018,1,2)])

    del year_df



