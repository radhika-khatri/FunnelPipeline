import os
import json
import re
import hashlib
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# =========================
# Setup
# =========================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
MODEL = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL)

LOG_FILE = "outputs/llm_calls.jsonl"


# =========================
# Logging (REQUIRED)
# =========================
def log(stage, input_files, output_file):
    record = {
        "stage": stage,
        "hypothesis_id": None,
        "timestamp": datetime.utcnow().isoformat(),
        "provider": "google",
        "model": MODEL,
        "prompt_hash": hashlib.md5(str(input_files).encode()).hexdigest(),
        "input_artifacts": input_files,
        "output_artifact": output_file
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")


# =========================
# Safe LLM Call
# =========================
def safe_call(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text if response and hasattr(response, "text") else ""
    except Exception as e:
        print("⚠️ LLM call failed, using fallback:", str(e))
        return ""


# =========================
# Robust JSON Parser
# =========================
def parse_json_safe(text, fallback):
    if not text or text.strip() == "":
        return fallback

    # Remove markdown blocks
    text = re.sub(r"```json|```", "", text).strip()

    # Extract JSON array
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        text = match.group(0)

    try:
        return json.loads(text)
    except Exception as e:
        print("⚠️ JSON parsing failed, fallback used:", str(e))
        return fallback


# =========================
# 1. Hypothesis Generation
# =========================
def generate_hypotheses(funnel, segments, traces):
    prompt = f"""
You are a product analyst.

STRICT RULES:
- Output ONLY valid JSON array
- No explanation, no markdown
- Must return 6-10 hypotheses

Format:
[
  {{
    "hypothesis_id": "h1",
    "step": "signup_form",
    "segment": {{
      "country": "...",
      "device": "...",
      "lang": "..."
    }},
    "suspected_cause": "...",
    "supporting_evidence": [],
    "confidence": "low|medium|high"
  }}
]

Data:
Funnel: {json.dumps(funnel)}
Segments: {json.dumps(segments)}
Traces: {json.dumps(traces[:20])}
"""

    raw = safe_call(prompt)

    fallback = [{
        "hypothesis_id": "h_fallback",
        "step": "signup_form",
        "segment": {
            "country": "BR",
            "device": "mobile_android",
            "lang": "pt-BR"
        },
        "suspected_cause": "phone validation issue",
        "supporting_evidence": [],
        "confidence": "medium"
    }]

    hypotheses = parse_json_safe(raw, fallback)

    log(
        "hypothesis_generation",
        ["outputs/funnel.json", "outputs/segments.json", "outputs/sampled_traces.json"],
        "outputs/hypotheses.json"
    )

    return hypotheses


# =========================
# 2. Causal Critique
# =========================
def critique_hypotheses(hypotheses):
    prompt = f"""
You are reviewing hypotheses for causal plausibility.

STRICT RULES:
- DO NOT change ranking
- Only critique plausibility

Return JSON:
[
  {{
    "hypothesis_id": "h1",
    "critique": "...",
    "final_confidence": "low|medium|high"
  }}
]

Data:
{json.dumps(hypotheses)}
"""

    raw = safe_call(prompt)

    fallback = [
        {
            "hypothesis_id": h["hypothesis_id"],
            "critique": "Plausible but needs validation",
            "final_confidence": h.get("confidence", "medium")
        }
        for h in hypotheses
    ]

    critiques = parse_json_safe(raw, fallback)

    critique_map = {c["hypothesis_id"]: c for c in critiques}

    for h in hypotheses:
        c = critique_map.get(h["hypothesis_id"], {})
        h["critique"] = c.get("critique", "No critique")
        h["final_confidence"] = c.get("final_confidence", h.get("confidence"))

    log(
        "critique",
        ["outputs/ranked_hypotheses.json"],
        "outputs/ranked_hypotheses.json"
    )

    return hypotheses


# =========================
# 3. Experiment Generation
# =========================
def generate_experiments(top_hypotheses):
    prompt = f"""
You are designing A/B tests.

STRICT RULES:
- Output ONLY JSON
- Do NOT compute sample size

Format:
[
  {{
    "experiment_id": "exp_1",
    "name": "...",
    "hypothesis": "...",
    "intervention": "...",
    "primary_metric": "...",
    "guardrail_metric": "...",
    "target_segment": "...",
    "minimum_detectable_effect": 0.05,
    "success_criteria": "..."
  }}
]

Data:
{json.dumps(top_hypotheses)}
"""

    raw = safe_call(prompt)

    fallback = []
    for i, h in enumerate(top_hypotheses):
        fallback.append({
            "experiment_id": f"exp_{i}",
            "name": f"Fix {h['step']}",
            "hypothesis": h["suspected_cause"],
            "intervention": "Improve UX / validation",
            "primary_metric": "conversion_rate",
            "guardrail_metric": "error_rate",
            "target_segment": str(h["segment"]),
            "minimum_detectable_effect": 0.05,
            "success_criteria": "Increase conversion without increasing errors"
        })

    experiments = parse_json_safe(raw, fallback)

    log(
        "experiment_generation",
        ["outputs/ranked_hypotheses.json"],
        "outputs/experiments.json"
    )

    return experiments