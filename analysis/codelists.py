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
# Self harm
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
