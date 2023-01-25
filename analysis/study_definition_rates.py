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
### Variable 1 Self harm
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
### Variable 2. Emotional distress
# A&E: SNOMED_codes
    emot_distAE=patients.attended_emergency_care(
        with_these_diagnoses=emotional_distress_SNOMED, 
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# hospital admissions: icd10_codelist
    emot_distHosp=patients.admitted_to_hospital(
        with_these_diagnoses=emotional_distress_icd10,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# mortality
    emot_distDead=patients.with_these_codes_on_death_certificate(
        emotional_distress_icd10,
        match_only_underlying_cause=False,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
### Variable 3. Eating disorders
# A&E: SNOMED_codes
    eat_disorAE=patients.attended_emergency_care(
        with_these_diagnoses=eating_disorders_SNOMED, 
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# hospital admissions: icd10_codelist
    eat_disorHosp=patients.admitted_to_hospital(
        with_these_diagnoses=eating_disorders_icd10,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# mortality
    eat_disorDead=patients.with_these_codes_on_death_certificate(
        eating_disorders_icd10,
        match_only_underlying_cause=False,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
### Variable 4. Problems related to lifestyle
# A&E: SNOMED_codes
    # lifestyleAE=patients.attended_emergency_care(
    #     with_these_diagnoses=lifestyle_SNOMED, 
    #     between=[
    #         "first_day_of_month(index_date)",
    #         "last_day_of_month(index_date)",
    #         ],
    #     returning="binary_flag",
    #     return_expectations={"incidence": 0.50},
    # ),
# hospital admissions: icd10_codelist
    lifestyleHosp=patients.admitted_to_hospital(
        with_these_diagnoses=lifestyle_icd10,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# mortality
    lifestyleDead=patients.with_these_codes_on_death_certificate(
        lifestyle_icd10,
        match_only_underlying_cause=False,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
### Variable 5. Assault and violence_
# A&E: SNOMED_codes
    # violence_AE=patients.attended_emergency_care(
    #     with_these_diagnoses=violence_SNOMED, 
    #     between=[
    #         "first_day_of_month(index_date)",
    #         "last_day_of_month(index_date)",
    #         ],
    #     returning="binary_flag",
    #     return_expectations={"incidence": 0.50},
    # ),
# hospital admissions: icd10_codelist
    violence_Hosp=patients.admitted_to_hospital(
        with_these_diagnoses=violence_icd10,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# mortality
    violence_Dead=patients.with_these_codes_on_death_certificate(
        violence_icd10,
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
    Measure(
        id="self_harmHosp_rate",
        numerator="self_harmHosp",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmHospbyRegion_rate",
        numerator="self_harmHosp",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmHospbyIMD_rate",
        numerator="self_harmHosp",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmHospbyEthnicity_rate",
        numerator="self_harmHosp",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmHospbyAge_rate",
        numerator="self_harmHosp",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmDead_rate",
        numerator="self_harmDead",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmDeadbyRegion_rate",
        numerator="self_harmDead",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmDeadbyIMD_rate",
        numerator="self_harmDead",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmDeadbyEthnicity_rate",
        numerator="self_harmDead",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmDeadbyAge_rate",
        numerator="self_harmDead",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
### Variable 2 Emotional distress
    Measure(
        id="emot_distAE_rate",
        numerator="emot_distAE",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distAEbyRegion_rate",
        numerator="emot_distAE",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distAEbyIMD_rate",
        numerator="emot_distAE",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distAEbyEthnicity_rate",
        numerator="emot_distAE",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distAEbyAge_rate",
        numerator="emot_distAE",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distHosp_rate",
        numerator="emot_distHosp",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distHospbyRegion_rate",
        numerator="emot_distHosp",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distHospbyIMD_rate",
        numerator="emot_distHosp",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distHospbyEthnicity_rate",
        numerator="emot_distHosp",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distHospbyAge_rate",
        numerator="emot_distHosp",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distDead_rate",
        numerator="emot_distDead",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distDeadbyRegion_rate",
        numerator="emot_distDead",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distDeadbyIMD_rate",
        numerator="emot_distDead",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distDeadbyEthnicity_rate",
        numerator="emot_distDead",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distDeadbyAge_rate",
        numerator="emot_distDead",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
### Variable 3 eating disorder
    Measure(
        id="eat_disorAE_rate",
        numerator="eat_disorAE",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorAEbyRegion_rate",
        numerator="eat_disorAE",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorAEbyIMD_rate",
        numerator="eat_disorAE",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorAEbyEthnicity_rate",
        numerator="eat_disorAE",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorAEbyAge_rate",
        numerator="eat_disorAE",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorHosp_rate",
        numerator="eat_disorHosp",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorHospbyRegion_rate",
        numerator="eat_disorHosp",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorHospbyIMD_rate",
        numerator="eat_disorHosp",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorHospbyEthnicity_rate",
        numerator="eat_disorHosp",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorHospbyAge_rate",
        numerator="eat_disorHosp",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorDead_rate",
        numerator="eat_disorDead",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorDeadbyRegion_rate",
        numerator="eat_disorDead",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorDeadbyIMD_rate",
        numerator="eat_disorDead",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorDeadbyEthnicity_rate",
        numerator="eat_disorDead",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorDeadbyAge_rate",
        numerator="eat_disorDead",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
### Variable 4. Problems related to lifestyle
    # Measure(
    #     id="lifestyleAE_rate",
    #     numerator="lifestyleAE",
    #     denominator="population",
    #     group_by="population",
    #     small_number_suppression=True,
    # ),
    # Measure(
    #     id="lifestyleAEbyRegion_rate",
    #     numerator="lifestyleAE",
    #     denominator="population",
    #     group_by="region",
    #     small_number_suppression=True,
    # ),
    # Measure(
    #     id="lifestyleAEbyIMD_rate",
    #     numerator="lifestyleAE",
    #     denominator="population",
    #     group_by="imd_cat",
    #     small_number_suppression=True,
    # ),
    # Measure(
    #     id="lifestyleAEbyEthnicity_rate",
    #     numerator="lifestyleAE",
    #     denominator="population",
    #     group_by="ethnicity",
    #     small_number_suppression=True,
    # ),
    # Measure(
    #     id="lifestyleAEbyAge_rate",
    #     numerator="lifestyleAE",
    #     denominator="population",
    #     group_by="age_group",
    #     small_number_suppression=True,
    # ),
    Measure(
        id="lifestyleHosp_rate",
        numerator="lifestyleHosp",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleHospbyRegion_rate",
        numerator="lifestyleHosp",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleHospbyIMD_rate",
        numerator="lifestyleHosp",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleHospbyEthnicity_rate",
        numerator="lifestyleHosp",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleHospbyAge_rate",
        numerator="lifestyleHosp",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleDead_rate",
        numerator="lifestyleDead",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleDeadbyRegion_rate",
        numerator="lifestyleDead",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleDeadbyIMD_rate",
        numerator="lifestyleDead",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleDeadbyEthnicity_rate",
        numerator="lifestyleDead",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleDeadbyAge_rate",
        numerator="lifestyleDead",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
### Variable 5. Assault and violence
    # Measure(
    #     id="violence_AE_rate",
    #     numerator="violence_AE",
    #     denominator="population",
    #     group_by="population",
    #     small_number_suppression=True,
    # ),
    # Measure(
    #     id="violence_AEbyRegion_rate",
    #     numerator="violence_AE",
    #     denominator="population",
    #     group_by="region",
    #     small_number_suppression=True,
    # ),
    # Measure(
    #     id="violence_AEbyIMD_rate",
    #     numerator="violence_AE",
    #     denominator="population",
    #     group_by="imd_cat",
    #     small_number_suppression=True,
    # ),
    # Measure(
    #     id="violence_AEbyEthnicity_rate",
    #     numerator="violence_AE",
    #     denominator="population",
    #     group_by="ethnicity",
    #     small_number_suppression=True,
    # ),
    # Measure(
    #     id="violence_AEbyAge_rate",
    #     numerator="violence_AE",
    #     denominator="population",
    #     group_by="age_group",
    #     small_number_suppression=True,
    # ),
    Measure(
        id="violence_Hosp_rate",
        numerator="violence_Hosp",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_HospbyRegion_rate",
        numerator="violence_Hosp",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_HospbyIMD_rate",
        numerator="violence_Hosp",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_HospbyEthnicity_rate",
        numerator="violence_Hosp",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_HospbyAge_rate",
        numerator="violence_Hosp",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_Dead_rate",
        numerator="violence_Dead",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_DeadbyRegion_rate",
        numerator="violence_Dead",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_DeadbyIMD_rate",
        numerator="violence_Dead",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_DeadbyEthnicity_rate",
        numerator="violence_Dead",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_DeadbyAge_rate",
        numerator="violence_Dead",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
]