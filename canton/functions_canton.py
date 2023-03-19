import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

def canton_input(filename):
    col_names = ['SITE_id','HEAD','DDMMYY','HHMM','SS','HH','RESCOD','lane_id','D','HEAD_t','GAP','SPD','LENTH','CS', 'CH']
    canton_df = pd.read_table(filename, names = col_names, skiprows = 18, skipinitialspace=True, delim_whitespace = True)
    canton_df['hour'] = canton_df['HHMM'].apply(lambda x: x[:2])
    canton_df['min'] = canton_df['HHMM'].apply(lambda x: x[2:])
    canton_df['DDMMYY'] = pd.to_datetime(canton_df['DDMMYY'], format = "%d%m%y")
    canton_df['wkday']=canton_df['DDMMYY'].apply(lambda x: x.timetuple()[6] + 1)
    return canton_df.loc[:,['SITE_id','lane_id','HEAD', 'DDMMYY', 'wkday','hour', 'min', 'SS', 'HH', 'SPD','D','CS']].iloc[:-1,:] 



def preprocess_canton(df):
    df.dropna(inplace = True)
    df['SPD'] = df['SPD'].astype('int')
    df['CS'] = df['CS'].astype('int')
    df['hour'] = df['hour'].astype('int')
    df['min'] = df['min'].astype('int')
    return 0


def aggregate_canton(df, columns, groupby_columns, agg_dict):
    return df[columns].groupby(by= groupby_columns , as_index = False).agg(agg_dict)
