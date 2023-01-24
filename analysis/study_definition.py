from codelists import *
from cohortextractor import (
    StudyDefinition,
    Measure,
    codelist,
    codelist_from_csv,
    combine_codelists,
    filter_codes_by_category,
    patients,
)

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "2000-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    index_date="2022-12-01",
    population=patients.all(),
# demographics
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "exponential_increase",
            "int": {"distribution": "population_ages"},
        },
    ),
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    ethnicity=patients.categorised_as(
        {
            "Missing": "DEFAULT",
            "White": """ ethnicity_code=1 """,
            "Mixed": """ ethnicity_code=2 """,
            "South Asian": """ ethnicity_code=3 """,
            "Black": """ ethnicity_code=4 """,
            "Other": """ ethnicity_code=5 """,
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Missing": 0.4,
                    "White": 0.2,
                    "Mixed": 0.1,
                    "South Asian": 0.1,
                    "Black": 0.1,
                    "Other": 0.1,
                }
            },
        },
        ethnicity_code=patients.with_these_clinical_events(
            ethnicity_codes,
            returning="category",
            find_last_match_in_period=True,
            on_or_before="index_date",
            return_expectations={
            "category": {"ratios": {"1": 0.4, "2": 0.4, "3": 0.2, "4":0.2,"5": 0.2}},
            "incidence": 0.75,
            },
        ),
    ),

### Self harm

# A&E: SNOMED_codes
    self_harmAE=patients.attended_emergency_care(
        with_these_diagnoses=self_harm_SNOMED, 
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# hospital admissions: icd10_codelist
    self_harmHosp=patients.admitted_to_hospital(
        with_these_diagnoses=self_harm_icd10,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# mortality
    self_harmDead=patients.with_these_codes_on_death_certificate(
        self_harm_icd10,
        match_only_underlying_cause=False,
        on_or_before="index_date",
        returning="binary_flag",
    ),
)
