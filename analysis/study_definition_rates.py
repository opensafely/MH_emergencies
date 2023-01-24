from cohortextractor import (
    StudyDefinition,
    Measure,
    patients,
)

from codelists import *

start_date = "2015-01-01"
end_date = "2022-12-01"

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "2015-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
        },
    index_date="2015-01-01", # for measures
    population=patients.satisfying(
        """
        registered
        AND NOT has_died
        """
    ),
    registered=patients.registered_as_of(
        "index_date",
        return_expectations={"incidence":0.95}
    ),
    has_died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
    ),
# demographics
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "exponential_increase",
            "int": {"distribution": "population_ages"},
        },
    ),
    age_group=patients.categorised_as(
        {
            "Missing": "DEFAULT",
            "<=18": """ age <= 18""",
            "19-25": """ age > 18 AND age <= 25""",
            "26-64": """ age > 25 AND age < 65""",
            "65+": """ age >= 65""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Missing": 0.2, 
                    "<=18": 0.2,
                    "19-25": 0.2,
                    "26-64": 0.2,
                    "65+": 0.2,
                }
            },
        },
    ),
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and the Humber": 0.2,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East of England": 0.1,
                    "London": 0.1,
                    "South East": 0.2,
                },
            },
        },
    ),
    imd_cat=patients.categorised_as(
        {
            "Missing": "DEFAULT",
            "IMD_1": """index_of_multiple_deprivation >=1 AND index_of_multiple_deprivation < 32844*1/5""",
            "IMD_2": """index_of_multiple_deprivation >= 32844*1/5 AND index_of_multiple_deprivation < 32844*2/5""",
            "IMD_3": """index_of_multiple_deprivation >= 32844*2/5 AND index_of_multiple_deprivation < 32844*3/5""",
            "IMD_4": """index_of_multiple_deprivation >= 32844*3/5 AND index_of_multiple_deprivation < 32844*4/5""",
            "IMD_5": """index_of_multiple_deprivation >= 32844*4/5 AND index_of_multiple_deprivation < 32844""",
        },
        index_of_multiple_deprivation=patients.address_as_of(
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Missing": 0.05,
                    "IMD_1": 0.19,
                    "IMD_2": 0.19,
                    "IMD_3": 0.19,
                    "IMD_4": 0.19,
                    "IMD_5": 0.19,
                }
            },
        },
    ),
######### self-harm
# A&E: SNOMED_codes
    self_harmAE=patients.attended_emergency_care(
        with_these_diagnoses=self_harm_SNOMED, 
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# hospital admissions: icd10_codelist
    self_harmHosp=patients.admitted_to_hospital(
        with_these_diagnoses=self_harm_icd10,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# mortality
    self_harmDead=patients.with_these_codes_on_death_certificate(
        self_harm_icd10,
        match_only_underlying_cause=False,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
)
measures = [
    Measure(
        id="self_harmAE_rate",
        numerator="self_harmAE",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmAEbyRegion_rate",
        numerator="self_harmAE",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmAEbyIMD_rate",
        numerator="self_harmAE",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmAEbyEthnicity_rate",
        numerator="self_harmAE",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmAEbyAge_rate",
        numerator="self_harmAE",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
]