## Execution order

Blue_Waters_filter_data.ipynb
- from: blue_waters_posix_with_paths.csv
- to:   blue_waters_posix_no_outliers.csv

Blue_Waters_filter_data_by_nprocs.ipynb
- from: blue_waters_posix_no_outliers.csv
- to:   blue_waters_posix_no_outliers_4_16_48_64_144_240_nprocs.csv

Blue_Waters_filter_data_Voss.ipynb
- from: blue_waters_posix_with_paths.csv
- to:   blue_waters_posix_with_paths_no_negative_outliers.csv
        blue_waters_posix_with_paths_no_outliers.csv

Blue_Waters_remove_time.ipynb
- from: blue_waters_posix_with_paths_no_negative_outliers.csv
-   to: blue_waters_posix_with_paths_no_negative_outliers_no_time.csv
        blue_waters_posix_with_paths_no_outliers_no_time.csv

Blue_Waters_remove_dups.ipynb
- from: blue_waters_posix_with_paths_no_negative_outliers_no_time.csv
- to:   blue_waters_posix_with_paths_no_negative_outliers_no_time_no_dups.csv

Blue_Waters_compute_concurr_procs.ipynb
- from: blue_waters_posix_with_paths_no_negative_outliers.csv
-   to: blue_waters_posix_with_paths_no_negative_outliers_concurr_procs.csv

Blue_Waters_compute_MAE.ipynb
- from: blue_waters_posix_with_paths_no_negative_outliers_no_time.csv
-   to: blue_waters_posix_with_paths_no_negative_outliers_no_time_witherrors.csv

Theta_compute_MAE.ipynb
- from: theta_posix_with_apps_no_negative_outliers_no_time.csv
-   to: theta_posix_with_apps_no_negative_outliers_no_time_witherrors.csv


Theta Dataset was generated from resources of the Argonne Leadership Computing Facility, which is a DOE Office of Science User Facility supported under Contract DE-AC02-06CH11357.