from collections import defaultdict

def compute_funnel(sessions, steps):
    funnel = {}

    for i, step in enumerate(steps):
        entries, completions = 0, 0

        for sid, events in sessions.items():
            visited = [e.get("step") for e in events if "step" in e]

            if step in visited:
                entries += 1
                if i+1 < len(steps) and steps[i+1] in visited:
                    completions += 1
                elif i+1 == len(steps):
                    completions += 1

        drop = entries - completions

        funnel[step] = {
            "entries": entries,
            "completions": completions,
            "dropoffs": drop,
            "conversion_rate": completions/entries if entries else 0,
            "dropoff_rate": drop/entries if entries else 0
        }

    return funnel


def compute_segments(sessions, steps):
    segments = defaultdict(dict)

    for sid, events in sessions.items():
        meta = events[0]
        key = (meta.get("country"), meta.get("device"), meta.get("lang"))
        segments[key][sid] = events

    result = {}
    for key, group in segments.items():
        result[str(key)] = compute_funnel(group, steps)

    return result


def compute_lift(hypotheses, funnel, segments):
    for h in hypotheses:
        step = h["step"]
        seg_key = str(tuple(h["segment"].values()))

        seg = segments.get(seg_key, {}).get(step, {})
        base = funnel.get(step, {})

        lift = seg.get("entries", 0) * max(
            0,
            seg.get("dropoff_rate", 0) - base.get("dropoff_rate", 0)
        )

        h["lift_potential"] = lift

    return sorted(hypotheses, key=lambda x: x["lift_potential"], reverse=True)