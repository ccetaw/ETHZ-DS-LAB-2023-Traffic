# Input:
# - raw data
# Output:
# - Statistics per sensor

import pandas as pd
import os
import click
from tqdm import tqdm

@click.command()
@click.option('-d', '--data', default='none', type=click.Choice(['astra', 'canton', 'city', 'none'], case_sensitive=False), help='data to be processed', show_default=True)
@click.option('-t', '--timeticks', default='day', type=click.Choice(['year', 'month', 'day'], case_sensitive=False), help='in what time precision is the data processed', show_default=True)
def main(data, timeticks):

    # City data
    if data == 'city':
        chunksize = 10**6
        raw_dir = "./raw_data/city"
        processed_dir = "./preprocessed_data/city/per_" + timeticks
        df = pd.DataFrame(columns=["detid", "day", "count","flow_avg", "occ_avg"])

        for filename in tqdm(os.listdir(raw_dir), desc="Reading files", position=0): # Read the file from raw_dir
            for chunk in  tqdm(pd.read_csv(os.path.join(raw_dir, filename), chunksize=chunksize), desc="Reading chunks", position=1):
                if timeticks == 'day':
                    chunk["date"] = pd.to_datetime(chunk["day"], infer_datetime_format=True) # Organize the data per day
                elif timeticks == 'month':
                    chunk["year"] = pd.to_datetime(chunk["day"], infer_datetime_format=True).dt.year.astype(str)
                    chunk["month"] = pd.to_datetime(chunk["day"], infer_datetime_format=True).dt.month.astype(str)
                    chunk["date"] = df[["year", "month"]].agg('_'.join, axis=1)
                elif timeticks == 'year':
                    chunk["date"] = pd.to_datetime(chunk["day"], infer_datetime_format=True).dt.year

                chunk["occ"] = chunk["occ"] * 3 # number of minutes occupied
                # Don't know how to deal with flow
                chunk = chunk.groupby(["detid", "date"]).agg(occ_max = pd.NamedAgg(column="occ", aggfunc="max"),
                                                             occ_sum = pd.NamedAgg(column="occ", aggfunc="sum"),
                                                             flow_max = pd.NamedAgg(column="flow", aggfunc="max"),
                                                             flow_sum = pd.NamedAgg(column="flow", aggfunc="sum")).reset_index()
                df = pd.concat([df, chunk], ignore_index=True)

        df = df.groupby(["detid", "date"]).agg(occ_max = pd.NamedAgg(column="occ_max", aggfunc="max"),
                                               occ_sum = pd.NamedAgg(column="occ_sum", aggfunc="sum"),
                                               flow_max = pd.NamedAgg(column="flow_max", aggfunc="max"),
                                               flow_sum = pd.NamedAgg(column="flow_sum", aggfunc="sum"))
        
        # Write processed files to processed_dir
        # print(df.index.get_level_values(0).unique())
        for detid in tqdm(df.index.get_level_values(0).unique(), desc="Writing files"):
            df.loc[[detid]].to_csv(processed_dir+"/"+detid+".csv")

    # Canton data
    if data == 'canton':
        pass

    if data == 'astra':
        pass


if __name__ == "__main__":
    main()