import json
from analytics import compute_funnel, compute_segments, compute_lift
from sessions import build_sessions, sample_traces
from llm import generate_hypotheses, critique_hypotheses, generate_experiments
from experiments import attach_sample_size
from report import generate_report
from sample_size import write_sample_size_doc


FUNNEL_STEPS = [
    "landing", "signup_form", "email_verify",
    "kyc_doc_upload", "kyc_review",
    "first_deposit", "first_trade"
]

def run():
    print("INIT")

    with open("events.json") as f:
        events = json.load(f)

    sessions = build_sessions(events)

    funnel = compute_funnel(sessions, FUNNEL_STEPS)
    json.dump(funnel, open("outputs/funnel.json", "w"), indent=2)

    segments = compute_segments(sessions, FUNNEL_STEPS)
    json.dump(segments, open("outputs/segments.json", "w"), indent=2)

    traces = sample_traces(sessions)
    json.dump(traces, open("outputs/sampled_traces.json", "w"), indent=2)

    hypotheses = generate_hypotheses(funnel, segments, traces)
    json.dump(hypotheses, open("outputs/hypotheses.json", "w"), indent=2)

    ranked = compute_lift(hypotheses, funnel, segments)
    ranked = critique_hypotheses(ranked)
    json.dump(ranked, open("outputs/ranked_hypotheses.json", "w"), indent=2)

    experiments = generate_experiments(ranked[:4])
    experiments = attach_sample_size(experiments, funnel)
    json.dump(experiments, open("outputs/experiments.json", "w"), indent=2)

    generate_report(funnel, segments, ranked, experiments)
    write_sample_size_doc()
    print("DONE")

if __name__ == "__main__":
    run()