import os

FILES = [
    "outputs/funnel.json",
    "outputs/segments.json",
    "outputs/hypotheses.json",
    "outputs/ranked_hypotheses.json",
    "outputs/experiments.json",
    "reports/friction_report.md"
]

def validate():
    for f in FILES:
        if not os.path.exists(f):
            print("Missing:", f)
            return
    print("All good ✅")

if __name__ == "__main__":
    validate()