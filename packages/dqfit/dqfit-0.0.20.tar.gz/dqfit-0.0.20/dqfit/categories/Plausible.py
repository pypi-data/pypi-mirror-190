import pandas as pd
from typing import Any

MIN_DATE = "1900-01-01"
TODAY_ISO = str(pd.to_datetime("today"))[0:10]
DATETIME_PATHS = ["Procedure.performed[x]", "Condition.onset[x]", "Patient.birthDate", "Observation.effective[x]"]
DISCRETE_SETS = {
    "Procedure.status": [
        "preparation",
        "in-progress",
        "not-done",
        "on-hold",
        "stopped",
        "completed",
        "entered-in-error",
        "unknown",
    ],
    "Observation.status": ['final','registered','preliminary','amended'],
    "Patient.gender": ["male", "female", "other", "unknown"],
    "Coding.system": [
        "http://snomed.info/sct",
        "http://hl7.org/fhir/sid/icd-9-cm",
        "http://hl7.org/fhir/sid/icd-10-cm",
        "http://loinc.org",
        "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
        "http://www.ama-assn.org/go/cpt",
        "http://www.nlm.nih.gov/research/umls/rxnorm",
        "http://hl7.org/fhir/sid/ndc",
    ],
}

def _plausible_dt_score(dt: str) -> int:
    date = dt[0:10]
    if MIN_DATE < date <= TODAY_ISO:
        return 1
    else:
        return 0

def _plausible_discrete_score(fhir_path: str, value: Any) -> int:
    "For in range"
    # this could use a better name
    if value in DISCRETE_SETS[fhir_path]:
        return 1
    else:
        return 0

def _plausible_codeable_concept_score(codeable_concept):
    # {
    #     "coding": [{"system": "http://loinc.org", "code": "4548-4"}]
    # }
    coding: list = codeable_concept.get("coding")
    score = 0
    for coding in coding:
        if coding['system'] in DISCRETE_SETS["Coding.system"]:
            score += 0.5
        # if coding['code'] in VALID_CODES
        # todo 
    return score
    
def score(dim: pd.Series):
    fhir_path = dim["path"]
    value = dim["value"]
    if dim['complete'] in [None, 0]:
        return None
    elif fhir_path in DATETIME_PATHS:
        return _plausible_dt_score(value)
    elif fhir_path in DISCRETE_SETS.keys():
        return _plausible_discrete_score(fhir_path, value)
    elif fhir_path.endswith(".code"):
        return _plausible_codeable_concept_score(value)


