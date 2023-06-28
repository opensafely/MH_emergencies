from cohortextractor import (
    StudyDefinition,
    Measure,
    patients,
)

from codelists import *

start_date = "2015-01-01"
end_date = "2023-06-01"

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
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# Hoital admissions: icd10_codelist
    self_harmHo=patients.admitted_to_hospital(
        with_these_diagnoses=self_harm_icd10,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# mortality
    self_harmDe=patients.with_these_codes_on_death_certificate(
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
# Hoital admissions: icd10_codelist
    emot_distHo=patients.admitted_to_hospital(
        with_these_diagnoses=emotional_distress_icd10,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# mortality
    emot_distDe=patients.with_these_codes_on_death_certificate(
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
# Hoital admissions: icd10_codelist
    eat_disorHo=patients.admitted_to_hospital(
        with_these_diagnoses=eating_disorders_icd10,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# mortality
    eat_disorDe=patients.with_these_codes_on_death_certificate(
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
# Hoital admissions: icd10_codelist
    lifestyleHo=patients.admitted_to_hospital(
        with_these_diagnoses=lifestyle_icd10,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# mortality
    lifestyleDe=patients.with_these_codes_on_death_certificate(
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
# Hoital admissions: icd10_codelist
    violence_Ho=patients.admitted_to_hospital(
        with_these_diagnoses=violence_icd10,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
# mortality
    violence_De=patients.with_these_codes_on_death_certificate(
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
        id="self_harmHo_rate",
        numerator="self_harmHo",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmHobyRegion_rate",
        numerator="self_harmHo",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmHobyIMD_rate",
        numerator="self_harmHo",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmHobyEthnicity_rate",
        numerator="self_harmHo",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmHobyAge_rate",
        numerator="self_harmHo",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmDe_rate",
        numerator="self_harmDe",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmDebyRegion_rate",
        numerator="self_harmDe",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmDebyIMD_rate",
        numerator="self_harmDe",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmDebyEthnicity_rate",
        numerator="self_harmDe",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="self_harmDebyAge_rate",
        numerator="self_harmDe",
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
        id="emot_distHo_rate",
        numerator="emot_distHo",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distHobyRegion_rate",
        numerator="emot_distHo",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distHobyIMD_rate",
        numerator="emot_distHo",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distHobyEthnicity_rate",
        numerator="emot_distHo",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distHobyAge_rate",
        numerator="emot_distHo",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distDe_rate",
        numerator="emot_distDe",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distDebyRegion_rate",
        numerator="emot_distDe",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distDebyIMD_rate",
        numerator="emot_distDe",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distDebyEthnicity_rate",
        numerator="emot_distDe",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="emot_distDebyAge_rate",
        numerator="emot_distDe",
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
        id="eat_disorHo_rate",
        numerator="eat_disorHo",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorHobyRegion_rate",
        numerator="eat_disorHo",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorHobyIMD_rate",
        numerator="eat_disorHo",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorHobyEthnicity_rate",
        numerator="eat_disorHo",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorHobyAge_rate",
        numerator="eat_disorHo",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorDe_rate",
        numerator="eat_disorDe",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorDebyRegion_rate",
        numerator="eat_disorDe",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorDebyIMD_rate",
        numerator="eat_disorDe",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorDebyEthnicity_rate",
        numerator="eat_disorDe",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="eat_disorDebyAge_rate",
        numerator="eat_disorDe",
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
        id="lifestyleHo_rate",
        numerator="lifestyleHo",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleHobyRegion_rate",
        numerator="lifestyleHo",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleHobyIMD_rate",
        numerator="lifestyleHo",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleHobyEthnicity_rate",
        numerator="lifestyleHo",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleHobyAge_rate",
        numerator="lifestyleHo",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleDe_rate",
        numerator="lifestyleDe",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleDebyRegion_rate",
        numerator="lifestyleDe",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleDebyIMD_rate",
        numerator="lifestyleDe",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleDebyEthnicity_rate",
        numerator="lifestyleDe",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="lifestyleDebyAge_rate",
        numerator="lifestyleDe",
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
        id="violence_Ho_rate",
        numerator="violence_Ho",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_HobyRegion_rate",
        numerator="violence_Ho",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_HobyIMD_rate",
        numerator="violence_Ho",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_HobyEthnicity_rate",
        numerator="violence_Ho",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_HobyAge_rate",
        numerator="violence_Ho",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_De_rate",
        numerator="violence_De",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_DebyRegion_rate",
        numerator="violence_De",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_DebyIMD_rate",
        numerator="violence_De",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_DebyEthnicity_rate",
        numerator="violence_De",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="violence_DebyAge_rate",
        numerator="violence_De",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
]