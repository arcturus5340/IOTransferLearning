# IOTransferLearning – Reproduction of "Maximizing Insights, Minimizing Data: I/O Time Prediction Using Transfer Learning"

**Author**: Dlyaver Djebarov  
**Goal**: Reproduction of the experiments from the papers by Povaliaiev et al. and Voss et al. on predicting I/O performance using transfer learning techniques.

This repository contains all necessary scripts, notebooks, models, and data preparation steps to reproduce the results of the original study. It is organized into modular subfolders that guide the user through data preprocessing, exploratory analysis, model training, optimization, and interpretability.

---

## 📂 Project Structure

| Folder              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `preprocessing/`    | Contains all preprocessing notebooks. Start here.                           |
| `eda/`              | Notebooks for exploring the filtered datasets.                              |
| `training/`         | Model training notebooks for Models A, B, C, D using various strategies.    |
| `cross-validation/` | Baseline comparisons and cross-validation experiments.                      |
| `optimization/`     | Hyperparameter tuning experiments.                                          |
| `interpretability/` | Feature attribution analysis using Captum and other explainability tools.   |
| `models/`           | Saved PyTorch model checkpoints and scalers.                                |
| `parsing/`          | Scripts for parsing raw Darshan logs and merging datasets.                  |
| `results/`          | Saved figures and CSVs with training and explainability results.            |
| `data/`             | Filtered, cleaned, and augmented datasets used for training and evaluation. |
| `Report.pdf`        | Detailed summary of reproduction outcomes, comparison with original work.   |
| `README.md`         | This file.                                                                  |

---

## 🔧 Step-by-Step Usage

### 🔹 Step 1: Data Preprocessing

Navigate to `preprocessing/` and follow the order described in its local `README.md`.

Run these notebooks in order:

- `Blue_Waters_filter_data.ipynb`
- `Blue_Waters_filter_data_by_nprocs.ipynb`
- `Blue_Waters_filter_data_Voss.ipynb`
- `Blue_Waters_remove_time.ipynb`
- `Blue_Waters_remove_dups.ipynb`
- `Blue_Waters_compute_concurr_procs.ipynb`
- `Blue_Waters_compute_MAE.ipynb`
- `Theta_compute_MAE.ipynb`

These scripts will clean, filter, deduplicate, and compute required features.

---

### 🔹 Step 2: Exploratory Data Analysis (EDA)

Move to `eda/` and run:

- `Blue_Waters_IQR.ipynb`
- `Blue_Waters_no_IQR.ipynb`
- `Blue_Waters_exe_col.ipynb`
- `Blue_Waters_Compute_MAE_from_error_df.ipynb`
- `Theta_Compute_MAE_from_error_df.ipynb`
- `Theta_analyse.ipynb`

Visualize how preprocessing affects data structure and MAE scores.

---

### 🔹 Step 3: Train Base Models

Go to `training/` and run:

- `Blue_Waters_Model_A.ipynb`
- `Blue_Waters_Voss_Model_B.ipynb`
- `Blue_Waters_Voss_Model_C.ipynb`
- `Blue_Waters_Voss_Model_D.ipynb`

This will train the four neural networks described in the original paper.

---

### 🔹 Step 4: Fine-Tuning with Theta Dataset

Fine-tune Model D using:

- `Theta_Voss_Model_D_finetuned.ipynb`

This replicates the transfer learning step from Blue Waters to Theta.

---

### 🔹 Step 5: Interpretability & Explainability

Run these notebooks in `interpretability/`:

- `Baselinecheck.ipynb`
- `Model_D_inference.ipynb`
- `Model_D_transfer_plot.ipynb`
- `Model_D_(finetuned)_inference.ipynb`
- `Model_D_(finetuned)_transfer_plot.ipynb`
- `Blue_Waters_captum_analysis.ipynb`
- `Blue_Waters_captum_plot.ipynb`
- `Theta_captum_analysis.ipynb`
- `Theta_captum_plot.ipynb`

Outputs are saved in `results/interpretability/`.

---

## 📊 Results Summary

- **Blue Waters logs used**: 820,701 (vs. 792,311 originally)
- **Theta logs used**: 218,111 (vs. 226,689 originally)
- **MAE Comparison**:
  - Model B: 19.25% (vs. 21.03% original)
  - Model C: 18.57% (vs. 26.90% original)
- **Transfer learning**:
  - Model D achieved 93.75% correct magnitude predictions on electronic structure apps.
  - Lower accuracy on physics apps (1.57%–82%) depending on fine-tuning setup.

See `Report.pdf` for full comparisons with figures and tables.

---

## 📘 Citation & Acknowledgments

Original papers by Povaliaiev et al., Voss et al.  
Reproduction by Dlyaver Djebarov.

Voß, A. 2024. Exploring transfer learning for predicting I/O time across systems. Masterarbeit, RWTH Aachen University: 2024.
Povaliaiev, D. 2023. Transfer learning workflow for I/O bandwidth prediction. Masterarbeit, RWTH Aachen University: 2023.
Povaliaiev, D., Liem, R., Kunkel, J., Lofstead, J., & Carns, P. 2024. High-Quality I/O Bandwidth Prediction with Minimal Data via Transfer Learning Workflow. 2024 IEEE 36th International Symposium on Computer Architecture and High Performance Computing (SBAC-PAD). Presented at the 2024 IEEE 36th International Symposium on Computer Architecture and High Performance Computing (SBAC-PAD), IEEE.
Maximizing Insights, Minimizing Data: I/O Time Prediction Using Transfer Learning TBD.

Theta Dataset was generated from resources of the Argonne Leadership Computing Facility, which is a DOE Office of Science User Facility supported under Contract DE-AC02-06CH11357.

---

## 🧠 Future Work

- Reformat Theta data from ALCF Catalog to test impact on fine-tuning.
- Address feature scaling for better attribution analysis.
- Evaluate agglomerative clustering for dimensionality reduction.

---

## 🔗 Useful Links

- [Blue Waters Dataset](https://bluewaters.ncsa.illinois.edu/data-sets)
- [ALCF Data Catalog](https://reports.alcf.anl.gov/data/)
