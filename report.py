def generate_report(funnel, segments, ranked, experiments):
    with open("reports/friction_report.md", "w") as f:
        f.write("# Friction Report\n\n")

        f.write("## Funnel\n")
        f.write(str(funnel) + "\n\n")

        f.write("## Top Hypotheses\n")
        for h in ranked[:3]:
            f.write(f"- {h['suspected_cause']} | Lift: {h['lift_potential']}\n")

        f.write("\n## Experiments\n")
        for e in experiments:
            f.write(f"- {e['name']} | Sample Size: {e['sample_size_per_arm']}\n")