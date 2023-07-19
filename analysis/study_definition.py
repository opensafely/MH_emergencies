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
    index_date="2023-06-01",
    population=patients.all(),
### demographics
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
            "Asian": """ ethnicity_code=3 """,
            "Black": """ ethnicity_code=4 """,
            "Chinese": """ ethnicity_code=5 """,
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Missing": 0.4,
                    "White": 0.1,
                    "Mixed": 0.1,
                    "Asian": 0.1,
                    "Black": 0.1,
                    "Chinese": 0.2,
                }
            },
        },
        ethnicity_code=patients.with_these_clinical_events(
            ethnicity_codes,
            returning="category",
            find_last_match_in_period=True,
            include_date_of_match=False,
            return_expectations={
            "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
            "incidence": 0.75,
            },
        ),
    ),
    imd_cat=patients.categorised_as(
        {
            "Unknown": "DEFAULT",
            "1 (most deprived)": "imd >= 0 AND imd < 32844*1/5",
            "2": "imd >= 32844*1/5 AND imd < 32844*2/5",
            "3": "imd >= 32844*2/5 AND imd < 32844*3/5",
            "4": "imd >= 32844*3/5 AND imd < 32844*4/5",
            "5 (least deprived)": "imd >= 32844*4/5 AND imd <= 32844",
        },
        imd=patients.address_as_of(
            "first_day_of_month(index_date)",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Unknown": 0.05,
                    "1 (most deprived)": 0.19,
                    "2": 0.19,
                    "3": 0.19,
                    "4": 0.19,
                    "5 (least deprived)": 0.19,
                }
            },
        },
    ),
### Variable 1 Self harm
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
### Variable 2. Emotional distress
# A&E: SNOMED_codes
    emotional_distressAE=patients.attended_emergency_care(
        with_these_diagnoses=emotional_distress_SNOMED, 
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# hospital admissions: icd10_codelist
    emotional_distressHosp=patients.admitted_to_hospital(
        with_these_diagnoses=emotional_distress_icd10,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# mortality
    emotional_distressDead=patients.with_these_codes_on_death_certificate(
        emotional_distress_icd10,
        match_only_underlying_cause=False,
        on_or_before="index_date",
        returning="binary_flag",
    ),
### Variable 3. Eating disorders
# A&E: SNOMED_codes
    eating_disordersAE=patients.attended_emergency_care(
        with_these_diagnoses=eating_disorders_SNOMED, 
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# hospital admissions: icd10_codelist
    eating_disordersHosp=patients.admitted_to_hospital(
        with_these_diagnoses=eating_disorders_icd10,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# mortality
    eating_disordersDead=patients.with_these_codes_on_death_certificate(
        eating_disorders_icd10,
        match_only_underlying_cause=False,
        on_or_before="index_date",
        returning="binary_flag",
    ),
### Variable 4. Problems related to lifestyle
# A&E: SNOMED_codes
    lifestyleAE=patients.attended_emergency_care(
        with_these_diagnoses=lifestyle_SNOMED,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# hospital admissions: icd10_codelist
    lifestyleHosp=patients.admitted_to_hospital(
        with_these_diagnoses=lifestyle_icd10,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# mortality
    lifestyleDead=patients.with_these_codes_on_death_certificate(
        lifestyle_icd10,
        match_only_underlying_cause=False,
        on_or_before="index_date",
        returning="binary_flag",
    ),
### Variable 5. Assault and violence
# A&E: SNOMED_codes
    violenceAE=patients.attended_emergency_care(
        with_these_diagnoses=violence_SNOMED, 
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# hospital admissions: icd10_codelist
    violenceHosp=patients.admitted_to_hospital(
        with_these_diagnoses=violence_icd10,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# mortality
    violenceDead=patients.with_these_codes_on_death_certificate(
        violence_icd10,
        match_only_underlying_cause=False,
        on_or_before="index_date",
        returning="binary_flag",
    ),
### Variable 6. SMIs
# A&E: SNOMED_codes
    s_m_illnAE=patients.attended_emergency_care(
        with_these_diagnoses=s_m_illn_SNOMED, 
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# hospital admissions: icd10_codelist
    s_m_illnHosp=patients.admitted_to_hospital(
        with_these_diagnoses=s_m_illn_icd10,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
# mortality
    s_m_illnDead=patients.with_these_codes_on_death_certificate(
        s_m_illn_icd10,
        match_only_underlying_cause=False,
        on_or_before="index_date",
        returning="binary_flag",
    ),
#### A&E: psych emergencies
    psyc_emeAE=patients.attended_emergency_care(
        with_these_diagnoses=psyc_eme_SNOMED,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.20},
    ),
)
