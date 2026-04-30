# Funnel Pipeline

A data pipeline for funnel analysis, friction detection, and hypothesis generation — powered by Gemini AI.

---

## Prerequisites

- Python 3.8+
- pip
- A valid [Gemini API key](https://aistudio.google.com/app/apikey)

---

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your API key

Create a `.env` file in the project root and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

### 4. Create output directories

```bash
mkdir outputs
mkdir reports
```

---

## Usage

### Run the pipeline

```bash
python pipeline.py
```

### Run validation

```bash
python validate.py
```

---

## Output

### `outputs/`

| File | Description |
|---|---|
| `funnel.json` | Funnel structure and stage definitions |
| `segments.json` | User segments derived from funnel data |
| `sampled_traces.json` | Sampled user traces through the funnel |
| `hypotheses.json` | Generated hypotheses for funnel friction |
| `ranked_hypotheses.json` | Hypotheses ranked by priority or impact |
| `experiments.json` | Proposed experiments to test hypotheses |
| `llm_calls.jsonl` | Log of all LLM calls made during the run |

### `reports/`

| File | Description |
|---|---|
| `friction_report.md` | Detailed friction analysis report |
| `sample_size_model.md` | Sample size model and statistical guidance |

---

## Project Structure

```
.
├── pipeline.py          # Main pipeline entrypoint
├── validate.py          # Validation script
├── requirements.txt     # Python dependencies
├── .env                 # API key config (not committed)
├── outputs/             # Generated JSON outputs
└── reports/             # Generated markdown reports
```

---

## License

This project is unlicensed. Add a `LICENSE` file if you intend to share or distribute it.