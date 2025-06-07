import pandas as pd
from pathlib import Path


df = pd.read_csv(Path(r"/home/rwth1591/transfer-learning/blue_waters/data/blue_waters_dataset_processed/blue_waters_posix_withapps_no_negative_outliers_no_time_witherrors.csv"))

mae = (df['error'].abs() / df['mean']).median()
print(mae)
