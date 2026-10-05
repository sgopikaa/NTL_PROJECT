from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_INTERIM = PROJECT_ROOT / "data" / "interim"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUT_FIGURES = PROJECT_ROOT / "outputs" / "figures"
OUTPUT_TABLES = PROJECT_ROOT / "outputs" / "tables"

# ---------------------------------------------------------------------------
# Event configuration
# ---------------------------------------------------------------------------
# The current repository is a single-event pilot, but the configuration is
# structured so additional events can be added without rewriting scripts.
DISASTER_EVENTS = {
    "cyclone_fani_2019": {
        "display_name": "Cyclone Fani 2019",
        "event_date": "2019-05-03",
        "country": "India",
        "admin1_names": ["Odisha", "Orissa"],
        "region_label": "Odisha, India",
        "landfall_lon": 85.8312,
        "landfall_lat": 19.8135,
        "baseline_months": 6,
        "post_months": 12,
    },
    "yaas_2021": {
        "display_name": "Cyclone Yaas 2021",
        "event_date": "2021-05-26",
        "country": "India",
        "admin1_names": ["Odisha", "Orissa"],
        "region_label": "Odisha, India",
        "landfall_lon": 86.90,
        "landfall_lat": 21.45,
        "baseline_months": 6,
        "post_months": 12,
    },
}

ACTIVE_EVENT = "yaas_2021"
EVENT = DISASTER_EVENTS[ACTIVE_EVENT]

EVENT_NAME = ACTIVE_EVENT
EVENT_DISPLAY_NAME = EVENT["display_name"]
EVENT_DATE = EVENT["event_date"]
COUNTRY_NAME = EVENT["country"]
ADMIN1_NAMES = EVENT["admin1_names"]
REGION_LABEL = EVENT["region_label"]
LANDFALL_LON = EVENT["landfall_lon"]
LANDFALL_LAT = EVENT["landfall_lat"]
BASELINE_MONTHS = EVENT["baseline_months"]
POST_MONTHS = EVENT["post_months"]

# Canonical raw feature/boundary file names.
NTL_RAW_FILE = "ntl_raw.csv"
BOUNDARY_GEOJSON_FILE = "gaul_districts.geojson"
BOUNDARY_LOOKUP_FILE = "gaul_district_lookup.csv"
GEE_FEATURE_FILE = "gee_socio_features.csv"
HAZARD_FEATURE_FILE = "hazard_exposure_features.csv"
DISTRICT_FEATURE_FILE = "district_features.csv"

# ---------------------------------------------------------------------------
# VIIRS / GEE settings
# ---------------------------------------------------------------------------
VIIRS_COLLECTION_ID = "NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG"
RADIANCE_BAND = "avg_rad"
COVERAGE_BAND = "cf_cvg"
GEE_SCALE = 750

# ---------------------------------------------------------------------------
# Preprocessing / T50 settings
# ---------------------------------------------------------------------------
MIN_COVERAGE = 0.5
MAX_INTERPOLATE_GAP = 2
IQR_MULTIPLIER = 3.0
RECOVERY_THRESHOLD = 0.50
MIN_OBSERVATIONS = 4

# ---------------------------------------------------------------------------
# AI feature policy
# ---------------------------------------------------------------------------
# Keep the model intentionally small and reproducible.
# These are easy-to-obtain features from VIIRS, WorldPop/GHSL, and simple
# event exposure geometry. OSM, Census, PLFS, slum, and income features are
# intentionally excluded from the current scope.
FEATURE_COLS = [
    "baseline_rad",
    "population_density",
    "built_up_ratio",
    "landfall_distance_km",
    "area_km2",
]

CV_GROUP_COL = "event_id"
N_SPLITS = 3

# ---------------------------------------------------------------------------
# Attribution
# ---------------------------------------------------------------------------
ATTRIBUTION_NTL = "NTL: VIIRS DNB (NOAA, public domain)"
ATTRIBUTION_MAP = (
    "Boundaries: FAO GAUL 2015 via Google Earth Engine · " + ATTRIBUTION_NTL
)
ATTRIBUTION_FEATURES = "Population: WorldPop via GEE · Built-up: GHSL via GEE"

RANDOM_SEED = 42
