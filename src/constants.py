USE_COLS = [
 'health_service_area',
 'hospital_county',
 'facility_name',
 'age_group',
 'gender',
 'race',
 'ethnicity',
 'length_of_stay',
 'type_of_admission',
 'patient_disposition',
 'discharge_year',
 'ccsr_diagnosis_description',
 'apr_drg_description',
 'apr_mdc_description',
 'apr_severity_of_illness_code',
 'apr_severity_of_illness',
 'apr_risk_of_mortality',
 'apr_medical_surgical',
 'payment_typology_1',
 'emergency_department_indicator',
 'total_charges',
 'total_costs',
 'ccsr_procedure_description']

EXPECTED_VALUES = {
    "health_service_area": {
        "Capital/Adirondacks",
        "Central NY",
        "Finger Lakes",
        "Hudson Valley",
        "Long Island",
        "New York City",
        "Southern Tier",
        "Western NY",
    },

    "age_group": {
        "0-17",
        "18-29",
        "30-49",
        "50-69",
        "70 or Older",
    },

    "gender": {
        "M",
        "F",
        "U",
    },

    "race": {
        "Black/African American",
        "Multi-racial",
        "Other Race",
        "White",
    },

    "ethnicity": {
        "Spanish/Hispanic",
        "Not Span/Hispanic",
        "Multi-ethnic",
        "Unknown",
    },

    "type_of_admission": {
        "Elective",
        "Emergency",
        "Newborn",
        "Not Available",
        "Trauma",
        "Urgent",
    },

    "discharge_year": {
        "2024"
    },


    "apr_severity_of_illness_code": {
        '0', 
        '1', 
        '2', 
        '3',
        '4'
    },

    "apr_severity_of_illness": {
        "Undetermined",
        "Minor",
        "Moderate",
        "Major",
        "Extreme",
    },

    "apr_risk_of_mortality": {
        "Undetermined",
        "Minor",
        "Moderate",
        "Major",
        "Extreme",
    },

    "apr_medical_surgical": {
        "Medical",
        "Surgical",
        "Not Applicable",
    },

    "emergency_department_indicator": {
        "Y",
        "N",
    },
}

TEXT_COLUMNS = [
    "health_service_area",
    "hospital_county",
    "facility_name",
    "age_group",
    "gender",
    "race",
    "ethnicity",
    "type_of_admission",
    "patient_disposition",
    "ccsr_diagnosis_description",
    "ccsr_procedure_description",
    "apr_drg_description",
    "apr_mdc_description",
    "apr_severity_of_illness",
    "apr_risk_of_mortality",
    "apr_medical_surgical",
    "payment_typology_1",
    "emergency_department_indicator",
]