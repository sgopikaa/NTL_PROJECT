# Nighttime Lights-Based Post-Disaster Recovery Prediction

> VIIRS NTL과 공간 feature를 활용한 District-level T50 산출 및 AI/XAI 파일럿  
> Pilot event: **Cyclone Fani 2019 · Odisha, India · 30 GAUL level2 districts**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![GEE](https://img.shields.io/badge/Google%20Earth%20Engine-VIIRS%20NTL-green)
![Tests](https://img.shields.io/badge/tests-13%20passed-brightgreen)
![Scope](https://img.shields.io/badge/scope-single--event%20pilot-lightgrey)

---

## 1. What this project does

This project measures how quickly nighttime lights recover after a disaster.

The core idea is:

```text
VIIRS nighttime lights time series
→ district-level recovery curve
→ T50 recovery index
→ compact AI/XAI model for recovery-delay risk
```

The current implementation is a **working single-disaster pilot**, not a final income-inequality or infrastructure-causality study.

### Current scope

| Item | Current implementation |
|---|---|
| Event | Cyclone Fani 2019 |
| Region | Odisha, India |
| Spatial unit | FAO GAUL 2015 level2 District |
| Target | `t50_final` |
| AI model | scikit-learn `RandomForestRegressor` |
| Explanation | SHAP |
| Hardware | CPU is enough; GPU is not required |
| Tests | 13 passed, 3 SHAP-related warnings |

### Out of current scope

The following were considered in the initial plan but are **not used in the current core pipeline**:

```text
slum_ratio
income_proxy
income_group
OSM grid_density
XGBoost
tslearn / K-means clustering
Seaborn
GADM shapefile
```

They can be revisited later, but the current direction prioritizes **reproducibility and multi-disaster scalability**.

---

## 2. Pilot results at a glance

### AI features used

| feature              |
|:---------------------|
| baseline_rad         |
| population_density   |
| built_up_ratio       |
| landfall_distance_km |
| area_km2             |

### Feature importance

| feature              |   importance |
|:---------------------|-------------:|
| landfall_distance_km |        0.37  |
| built_up_ratio       |        0.225 |
| population_density   |        0.171 |
| baseline_rad         |        0.146 |
| area_km2             |        0.089 |

### Model scores

|   fold |   mae |     r2 |
|-------:|------:|-------:|
|      1 | 0.246 |  0.384 |
|      2 | 0.677 | -0.411 |
|      3 | 0.863 |  0.012 |

The model is functioning, but the dataset is small: **30 districts from one event**. Fold-level R² varies, so the AI result should be read as a **pilot XAI analysis**, not a generalized prediction model.

---

## 3. Result figures

### Recovery curves

![Median recovery curves by baseline NTL group](docs/assets/recovery_curves.png)

`recovery_ratio` can exceed 1.0 when post-disaster NTL becomes brighter than the pre-disaster baseline.

### SHAP summary

![SHAP summary plot](docs/assets/shap_summary.png)

Interpretation:

```text
SHAP value > 0  → predicted T50 increases → slower expected recovery
SHAP value < 0  → predicted T50 decreases → faster expected recovery
```

In this pilot, `landfall_distance_km` and `built_up_ratio` have the largest relative influence.

### T50 distribution

![T50 distribution by baseline NTL group](docs/assets/t50_distribution.png)

`baseline_ntl_group` is **not an income group**. It is a high/low split based on pre-disaster nighttime-light brightness.

---

## 4. District recovery examples

### Fastest recovery districts

| district_name   |   t50_final |   resilience_score | baseline_ntl_group   |
|:----------------|------------:|-------------------:|:---------------------|
| Kandhamal       |       0.139 |              0.878 | low_baseline_ntl     |
| Rayagada        |       1.312 |              0.433 | low_baseline_ntl     |
| Cuttack         |       1.893 |              0.346 | high_baseline_ntl    |
| Jagatsinghpur   |       2.307 |              0.302 | high_baseline_ntl    |
| Kendrapara      |       2.343 |              0.299 | high_baseline_ntl    |

### Slowest recovery districts

| district_name   |   t50_final |   resilience_score | baseline_ntl_group   |
|:----------------|------------:|-------------------:|:---------------------|
| Jajpur          |       4.609 |              0.178 | high_baseline_ntl    |
| Kalahandi       |       4.377 |              0.186 | low_baseline_ntl     |
| Malkangiri      |       4.074 |              0.197 | low_baseline_ntl     |
| Jharsuguda      |       3.757 |              0.21  | high_baseline_ntl    |
| Keonjhar        |       3.677 |              0.214 | high_baseline_ntl    |

---

## 5. Method summary

For each district:

```text
baseline_rad = mean pre-disaster NTL
ntl_min      = minimum post-disaster NTL
```

Normalized recovery model:

```text
Recovery(t) = 1 - e^(-k·t)
T50 = ln(2) / k
```

Interpretation:

```text
Lower T50  → faster recovery
Higher T50 → slower recovery
Higher resilience_score → stronger recovery performance
```

---

## 6. Data sources

| Source | Use |
|---|---|
| VIIRS DNB Monthly VCMSLCFG | nighttime-light time series |
| FAO GAUL 2015 level2 | district boundaries |
| WorldPop | population density |
| GHSL Built-up Surface | built-up ratio |
| Cyclone landfall coordinate | distance-to-landfall exposure feature |

---

## 7. Repository structure

```text
.
├─ config.py
├─ requirements.txt
├─ README.md
├─ scripts/
│  ├─ 01_gee_auth_test.py
│  ├─ 02_extract_viirs_ntl_gaul.py
│  ├─ 03_preprocess_ntl.py
│  ├─ 04_compute_resilience.py
│  ├─ 05_stats_visualize.py
│  ├─ 06_ai_predict_shap.py
│  ├─ 09_make_result_tables.py
│  ├─ 10_export_gaul_odisha_boundary.py
│  ├─ 11_make_resilience_maps.py
│  ├─ 20_extract_gee_population_builtup.py
│  ├─ 22_make_landfall_exposure_features.py
│  ├─ 23_build_district_features.py
│  ├─ 24_validate_ai_features.py
│  └─ validate_phase.py
├─ src/ntl_resilience/
├─ tests/
├─ docs/assets/
└─ docs/results/
```

---

## 8. Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Create `.env` from `.env.example`:

```text
GEE_PROJECT_ID=your-earth-engine-project-id
```

Test Earth Engine:

```bash
python scripts/01_gee_auth_test.py
```

---

## 9. Reproduce the pipeline

### Step 1. Export VIIRS NTL

```bash
python scripts/02_extract_viirs_ntl_gaul.py
```

After the GEE Drive export finishes, download and save as:

```text
data/raw/ntl_raw.csv
```

### Step 2. Preprocess and calculate T50

```bash
python scripts/03_preprocess_ntl.py
python scripts/04_compute_resilience.py
```

### Step 3. Export boundary and maps

```bash
python scripts/10_export_gaul_odisha_boundary.py
python scripts/11_make_resilience_maps.py
```

### Step 4. Export AI features

```bash
python scripts/20_extract_gee_population_builtup.py
```

After the GEE Drive export finishes, download and save as:

```text
data/raw/gee_socio_features.csv
```

Then run:

```bash
python scripts/22_make_landfall_exposure_features.py
python scripts/23_build_district_features.py
python scripts/04_compute_resilience.py
```

### Step 5. Run AI/XAI

```bash
python scripts/06_ai_predict_shap.py
python scripts/24_validate_ai_features.py
```

### Step 6. Generate figures and tables

```bash
python scripts/05_stats_visualize.py
python scripts/09_make_result_tables.py
```

### Step 7. Validate

```bash
python scripts/validate_phase.py
python -m pytest tests -q
```

Expected current test result:

```text
13 passed, 3 warnings
```

The warnings are SHAP/Matplotlib deprecation warnings and are not blocking.

---

## 10. How to update README result assets

To make the images in this README render on GitHub, copy the generated files into `docs/assets/`:

```powershell
mkdir docs\assets -Force
copy outputs\figures\recovery_curves.png docs\assets\recovery_curves.png
copy outputs\figures\shap_summary.png docs\assets\shap_summary.png
copy outputs\figures\t50_distribution.png docs\assets\t50_distribution.png
```

For result CSV snapshots:

```powershell
mkdir docs\results -Force
copy outputs\tables\ai_features_used.csv docs\results\ai_features_used.csv
copy outputs\tables\feature_importance.csv docs\results\feature_importance.csv
copy outputs\tables\ai_model_scores.csv docs\results\ai_model_scores.csv
copy outputs\tables\ai_feature_selection_report.csv docs\results\ai_feature_selection_report.csv
```

Do **not** commit raw exports such as `data/raw/ntl_raw.csv`.

---

## 11. Safe interpretation

This project supports the following statement:

```text
The pipeline successfully computes district-level T50 recovery indices from VIIRS NTL and demonstrates a compact AI/XAI workflow using easy-to-obtain spatial features.
```

It does **not** yet support:

```text
a final income-inequality conclusion
a slum vs non-slum comparison
a power-grid infrastructure causal claim
a generalized multi-disaster prediction model
```

---

## 12. Next step: multi-disaster expansion

The next research step is not adding more difficult feature columns.  
It is increasing the number of event-district rows.

Recommended direction:

```text
1 event × 30 districts
→ 2 events × districts
→ district-event long table
→ event-level validation
→ Leave-One-Event-Out evaluation
```

Candidate next events:

```text
Cyclone Amphan 2020
Cyclone Yaas 2021
Cyclone Hudhud 2014
```

Once multiple events are added, the model can move from a working pilot toward a more robust disaster-recovery prediction system.
