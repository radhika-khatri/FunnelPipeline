# Friction Report

## Funnel
{'landing': {'entries': 1, 'completions': 1, 'dropoffs': 0, 'conversion_rate': 1.0, 'dropoff_rate': 0.0}, 'signup_form': {'entries': 1, 'completions': 0, 'dropoffs': 1, 'conversion_rate': 0.0, 'dropoff_rate': 1.0}, 'email_verify': {'entries': 0, 'completions': 0, 'dropoffs': 0, 'conversion_rate': 0, 'dropoff_rate': 0}, 'kyc_doc_upload': {'entries': 0, 'completions': 0, 'dropoffs': 0, 'conversion_rate': 0, 'dropoff_rate': 0}, 'kyc_review': {'entries': 0, 'completions': 0, 'dropoffs': 0, 'conversion_rate': 0, 'dropoff_rate': 0}, 'first_deposit': {'entries': 0, 'completions': 0, 'dropoffs': 0, 'conversion_rate': 0, 'dropoff_rate': 0}, 'first_trade': {'entries': 0, 'completions': 0, 'dropoffs': 0, 'conversion_rate': 0, 'dropoff_rate': 0}}

## Top Hypotheses
- The user encountered a critical 'invalid_country_code' error while attempting to submit the signup form, preventing successful completion. | Lift: 0
- The user provided their phone number or country selection in a format that the system's country code validation did not recognize as valid for Brazil. | Lift: 0
- The signup form lacks clear instructions or examples regarding the expected format for country codes, leading to user input errors. | Lift: 0

## Experiments
- Signup Form Invalid Country Code Error Resolution | Sample Size: 151
- Signup Form Enhanced Input Validation Guidance | Sample Size: 151
- Signup Form Explicit Instructions for Country Codes | Sample Size: 151
- Signup Backend Validation Logic Bug Fix | Sample Size: 151
