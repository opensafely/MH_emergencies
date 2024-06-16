from cohortextractor import (
    codelist_from_csv,
    codelist,
)

# DEMOGRAPHIC CODELIST
ethnicity_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    system="snomed",
    column="snomedcode",
    category_column="Grouping_6",
)
# Variable 1. Self harm
self_harm_SNOMED = codelist_from_csv(
    "codelists/ons-self-harm-intentional-and-undetermined-intent.csv",
    system="snomed",
    column="code",
)
self_harm_icd10 = codelist_from_csv(
    "codelists/user-agleman-self-harm-and-suicide-icd-10.csv",
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
lifestyle_SNOMED = codelist_from_csv(
    "codelists/user-agleman-lifestyle-snomed-ct.csv",
    system="snomed",
    column="code",
)
lifestyle_icd10 = codelist_from_csv(
    "codelists/user-agleman-lifestyle-problems-icd10.csv",
    system="icd10",
    column="code",
)
# Variable 5. Assault and violence
violence_SNOMED = codelist_from_csv(
    "codelists/user-agleman-violence4.csv",
    system="snomed",
    column="code",
)
violence_icd10 = codelist_from_csv(
    "codelists/user-agleman-assault_violence-icd10.csv",
    system="icd10",
    column="code",
)
# Variable 6. Serious Menthal illness   
s_m_illn_SNOMED = codelist_from_csv(
    "codelists/user-hjforbes-severe-mental-illness.csv",
    system="snomed",
    column="code",
)
s_m_illn_icd10 = codelist_from_csv(
    "codelists/user-agleman-smis-mh-emergencies.csv",
    system="icd10",
    column="code",
)
# Variable 7. Psycho emergencies
psyc_eme_SNOMED = codelist_from_csv(
    "codelists/user-agleman-psych-emergencies-snomed.csv",
    system="snomed",
    column="code",
)
