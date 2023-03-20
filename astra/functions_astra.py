import pandas as pd
import datetime
import numpy as np

def astra_input(file_path):
  if '.gz' in file_path:
    df = pd.read_csv(file_path, compression='gzip')
  else:
    df = pd.read_csv(file_path)
  df = df[['_id','src_time','zs_id','vd','vd_class_val','vd_dir','vd_speed_val']]
  df['vd_class_val'] = df['vd_class_val'].apply(lambda x: int(str(x)[1:]))
  month = []
  wkday = []
  hour = []
  year = []
  day = []
  num = 0
  for i in df['src_time']:
    i = i[:19]
    val = datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
    tt = val.timetuple()
    year.append(tt[0])
    month.append(tt[1])
    day.append(tt[2])
    hour.append(tt[3])
    wkday.append(tt[6])
  df['year'] = year
  df['month'] = month
  df['day'] = day
  df['hour'] = hour
  df['wkday'] = wkday
  df = df.drop(columns=['src_time'])
  return df

def preprocess_astra(df):
  if df.isnull().sum().sum()/(df.shape[0]) < 0.01:
    df.dropna(inplace = True)
  else:
    print('Impute needed!')
  return 0


def aggregate_astra(df, columns, groupby_columns, agg_dict):
    return df[columns].groupby(by= groupby_columns , as_index = False).agg(agg_dict)

'''def aggregate_astra(df):
  return df.groupby(by=['zs_id','vd','vd_class_val','day','hour'], as_index=False).agg({'vd_speed_val': ['mean','std', 'min', 'max'], '_id':['count']})'''
