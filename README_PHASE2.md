# Phase 2 — 실제 데이터 준비: Cyclone Fani 2019, Odisha

모의 데이터 파이프라인을 확인했다면, 이제 실제 데이터를 넣는 단계입니다.

이 단계의 목표는 다음 2개입니다.

1. GADM India District 경계에서 Odisha 주만 잘라 `data/raw/odisha_districts.geojson` 만들기
2. GEE에서 Cyclone Fani 전후 VIIRS NTL 데이터를 District 단위로 추출하기

---

## 1. 1차 분석 이벤트

```text
event_name: cyclone_fani_2019
event_date: 2019-05-03
state: Odisha
main_area: Puri/Odisha coast
baseline: 2018-11 ~ 2019-04
post-disaster: 2019-05 ~ 2020-04
```

처음부터 인도 전체를 돌리지 말고, Odisha District만 대상으로 테스트하세요.

---

## 2. GADM 데이터 준비

GADM에서 India administrative boundaries를 다운로드합니다.

권장 파일 형식:

```text
gadm41_IND.gpkg
```

다운로드한 파일을 아래 위치에 넣으세요.

```text
data/raw/gadm41_IND.gpkg
```

그다음 실행:

```cmd
python scripts/07_prepare_odisha_boundary.py
```

생성 파일:

```text
data/raw/odisha_districts.geojson
data/raw/odisha_district_lookup.csv
```

---

## 3. GEE 인증 확인

`.env` 파일에 본인 GEE Project ID를 넣으세요.

```text
GEE_PROJECT_ID=your-earth-engine-project-id
```

그다음:

```cmd
python scripts/01_gee_auth_test.py
```

---

## 4. 실제 VIIRS NTL 추출

```cmd
python scripts/02_extract_viirs_ntl.py --boundary data/raw/odisha_districts.geojson
```

이 스크립트는 Earth Engine Export Task를 제출합니다.

작업이 끝나면 Google Drive에서 CSV를 다운로드해 아래 파일명으로 저장하세요.

```text
data/raw/ntl_raw.csv
```

---

## 5. GEE Export CSV 컬럼 확인

다운로드한 CSV의 컬럼명을 확인합니다.

```cmd
python scripts/99_check_raw_columns.py
```

현재 파이프라인이 요구하는 기본 컬럼은 다음입니다.

```text
district_id
date
avg_rad
cf_cvg
```

만약 GEE Export 결과가 `mean`, `avg_rad_mean`, `cf_cvg_mean` 같은 이름으로 나오면,
`08_format_gee_export.py`에서 컬럼명을 맞추면 됩니다.

```cmd
python scripts/08_format_gee_export.py --input data/raw/gee_export.csv --output data/raw/ntl_raw.csv
```

---

## 6. 실제 데이터 파이프라인 실행

`data/raw/ntl_raw.csv`가 준비되면 기존 파이프라인을 그대로 실행합니다.

```cmd
python scripts/03_preprocess_ntl.py
python scripts/04_compute_resilience.py
python scripts/05_stats_visualize.py
python scripts/06_ai_predict_shap.py
```

---

## 7. 현재 단계에서의 해석 주의

Odisha 1개 이벤트만으로는 “인도 전체의 회복력 불평등”을 일반화하면 안 됩니다.

보고서에는 이렇게 쓰는 것이 안전합니다.

> 본 단계는 Cyclone Fani 2019를 대상으로 한 파일럿 분석이며, 제안한 NTL 기반 회복력 지수 산출 파이프라인의 작동 가능성을 검증하는 것을 목적으로 한다. 이후 복수 재난과 복수 주로 확장하여 회복력 불평등의 일반성을 검증한다.
