from cohortextractor import (
    codelist_from_csv,
    codelist,
)

# DEMOGRAPHIC CODELIST
ethnicity_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_6",
)
ethnicity_codes_16 = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_16",
)
# Variable 1. Self harm
self_harm_SNOMED = codelist_from_csv(
    "codelists/ons-self-harm-intentional-and-undetermined-intent.csv",
    system="snomed",
    column="code",
)
self_harm_icd10 = codelist_from_csv(
    "codelists/user-hjforbes-suicide-icd-10.csv",
    system="icd10",
    column="code",
)
# Variable 2. Emotional distress
emotional_distress_SNOMED = codelist_from_csv(
    "codelists/user-agleman-emotional-distress-snomed-ct.csv",
    system="snomed",
    column="code",
)
emotional_distress_icd10 = codelist_from_csv(
    "codelists/user-agleman-emotional-distress.csv",
    system="icd10",
    column="code",
)
# Variable 3. Eating disorders
eating_disorders_SNOMED = codelist_from_csv(
    "codelists/user-hjforbes-diagnoses-eating-disorder.csv",
    system="snomed",
    column="code",
)
eating_disorders_icd10 = codelist_from_csv(
    "codelists/user-agleman-eating-disorders-icd10.csv",
    system="icd10",
    column="code",
)
# Variable 4. Problems related to lifestyle
# lifestyle_SNOMED = codelist_from_csv(
#     "codelists/.csv",
#     system="snomed",
#     column="code",
# )
lifestyle_icd10 = codelist_from_csv(
    "codelists/user-agleman-lifestyle-problems-icd10.csv",
    system="icd10",
    column="code",
)
# Variable 5. Assault and violence   
# violence_SNOMED = codelist_from_csv(
#     "codelists/.csv",
#     system="snomed",
#     column="code",
# )
violence_icd10 = codelist_from_csv(
    "codelists/user-agleman-assault_violence-icd10.csv",
    system="icd10",
    column="code",
)
