import pandas as pd
from pathlib import Path
import numpy as np
import time
from multiprocessing import Pool

NUM_WORKERS = 4

df_no_time = pd.read_csv(Path(r"/home/rwth1591/transfer-learning/blue_waters/data/blue_waters_dataset_processed/blue_waters_posix_withapps_no_negative_outliers_no_time.csv"))

columns_dissimilar = ["POSIX_MAX_READ_TIME_SIZE", "POSIX_MAX_WRITE_TIME_SIZE", "POSIX_FASTEST_RANK", "POSIX_SLOWEST_RANK",
                      "rank","POSIX_TOTAL_TIME"]

count = df_no_time.groupby(by=list(df_no_time.columns.difference(columns_dissimilar))).agg({"POSIX_TOTAL_TIME":['mean','count']})
indices = df_no_time.groupby(by=list(df_no_time.columns.difference(columns_dissimilar))).indices 
df_no_time_cpy = df_no_time.copy().reset_index()
start = time.time()
for index,a in enumerate(indices):
    if index % 1000 == 0:
        print(str(index) + " of " + str(len(indices.keys())))
    dup_set = df_no_time_cpy.loc[df_no_time_cpy.index.isin(indices[a])]
    if len(dup_set) == 1:
        df_no_time_cpy.loc[df_no_time_cpy.index.isin(indices[a]),'error'] = 0
        continue
    mean = df_no_time_cpy[df_no_time_cpy.index.isin(indices[a])].POSIX_TOTAL_TIME.mean()
    df_no_time_cpy.loc[df_no_time_cpy.index.isin(indices[a]),'mean'] = mean
    #if len(dup_set > 1):
    #    bessel = (len(dup_set) / (len(dup_set) - 1))
    #else:
    #    bessel = 1
    df_no_time_cpy.loc[df_no_time_cpy.index.isin(indices[a]),'error'] = (df_no_time_cpy.loc[df_no_time_cpy.index.isin(indices[a]),'POSIX_TOTAL_TIME'] -  df_no_time_cpy.loc[df_no_time_cpy.index.isin(indices[a]),'mean'])# * bessel
end = time.time()
print(end - start)
df_no_time_cpy.to_csv(Path(r"/home/av639747/Dokumente/masterarbeit/2024_ma_voss_transfer_learning/artifacts/blue_waters_posix_withapps_no_negative_outliers_no_time_witherrors.csv"),index=False)
print(df_no_time_cpy['error'].abs().median() / df_no_time_cpy.POSIX_TOTAL_TIME.mean())
