from collections import defaultdict
import random

def build_sessions(events):
    sessions = defaultdict(list)

    for e in events:
        sessions[e["session_id"]].append(e)

    for sid in sessions:
        sessions[sid].sort(key=lambda x: x["ts"])

    return sessions


def sample_traces(sessions, n=50):
    keys = list(sessions.keys())
    random.shuffle(keys)

    traces = []

    for sid in keys[:n]:
        events = sessions[sid]

        steps = [e.get("step") for e in events if "step" in e]
        errors = [e.get("code") for e in events if e.get("event") == "form_validation_error"]

        traces.append({
            "session_id": sid,
            "steps": steps,
            "errors": errors,
            "final_step": steps[-1] if steps else None
        })

    return traces