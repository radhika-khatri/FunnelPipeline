# Funnel Pipeline

## Setup

python -m venv venv
venv\Scripts\activate   (Windows)
# source venv/bin/activate   (Mac/Linux)

pip install -r requirements.txt


## Add API Key

Create a file named .env and add:

GEMINI_API_KEY=your_api_key_here


## Create folders

mkdir outputs
mkdir reports


## Run Pipeline

python pipeline.py


## Run Validation

python validate.py


## Output

outputs/:
- funnel.json
- segments.json
- sampled_traces.json
- hypotheses.json
- ranked_hypotheses.json
- experiments.json
- llm_calls.jsonl

reports/:
- friction_report.md
- sample_size_model.md