import pandas as pd
from pathlib import Path

df_blue_waters_posix = pd.read_csv(Path(r"/home/rwth1591/transfer-learning/blue_waters/data/blue_waters_dataset_processed/blue_waters_posix_withapps_no_negative_outliers.csv"))

def compute_concurr_procs(x):
    starts_same_time = (df_blue_waters_posix.start_time_sec >= x.start_time_sec) & (df_blue_waters_posix.start_time_sec <= x.end_time_sec)
    ends_same_time = (df_blue_waters_posix.end_time_sec >= x.start_time_sec) & (df_blue_waters_posix.end_time_sec <= x.end_time_sec)
    return len(df_blue_waters_posix[starts_same_time | ends_same_time])
    
df_blue_waters_posix["concurr_procs"] = df_blue_waters_posix.apply(lambda x: compute_concurr_procs(x),axis=1)

df_blue_waters_posix.to_csv(Path(r"/home/rwth1591/transfer-learning/blue_waters/data/blue_waters_dataset_processed/blue_waters_posix_withapps_no_negative_outliers_concurr_procs.csv"),index=False)
