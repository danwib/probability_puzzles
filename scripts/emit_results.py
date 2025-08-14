# scripts/emit_results.py
import json, math
from pathlib import Path

from src.birthday import prob_shared_birthday
from src.coupon_collector import expected_trials_to_collect, expected_trials_approx
from src.bayes import ppv, npv
from src.order_stats import expected_max_uniform, expected_kth_uniform
from src.balls_bins import expected_empty_bins

def rows():
    # Birthday paradox
    for n in [5, 10, 20, 23, 30, 50]:
        yield ("Birthday paradox", f"n={n}", {"p_shared": prob_shared_birthday(n)})

    # Coupon collector (exact + approx)
    for n in [3, 10, 20, 50, 100]:
        exact = expected_trials_to_collect(n)
        approx = expected_trials_approx(n)
        yield ("Coupon collector", f"n={n}", {"E[T]_exact": exact, "E[T]_approx": approx})

    # Bayes (two illustrative prevalences)
    for prev in [0.01, 0.10]:
        sens, spec = 0.90, 0.95
        yield ("Bayes PPV/NPV", f"sens={sens}, spec={spec}, prev={prev}",
               {"PPV": ppv(sens, spec, prev), "NPV": npv(sens, spec, prev)})

    # Order statistics (U(0,1))
    for n in [5, 10]:
        yield ("Order stats", f"E[max], n={n}", {"E[max]": expected_max_uniform(n)})
        for k in [1, (n+1)//2, n]:
            yield ("Order stats", f"E[X_(k)], n={n}, k={k}", {"E[X_(k)]": expected_kth_uniform(n, k)})

    # Balls into bins
    for m, n in [(10, 10), (20, 10), (100, 10), (100, 50)]:
        yield ("Balls in bins", f"m={m}, n={n}", {"E[empty]": expected_empty_bins(m, n)})

def fmt(x):
    if isinstance(x, float):
        return f"{x:.6g}"
    return str(x)

def make_markdown(data):
    lines = ["## Results", "| Puzzle | Case | Metrics |", "|---|---|---|"]
    for r in data:
        puzzle, case, metrics = r["puzzle"], r["case"], r["metrics"]
        met = ", ".join(f"{k}={fmt(v)}" for k, v in metrics.items())
        lines.append(f"| {puzzle} | {case} | {met} |")
    return "\n".join(lines) + "\n"

def main(write_md=True, write_json=True):
    data = [{"puzzle": p, "case": c, "metrics": m} for (p, c, m) in rows()]

    # Print nicely to terminal
    for d in data:
        print(f"[{d['puzzle']}] {d['case']} -> " + ", ".join(f"{k}={fmt(v)}" for k, v in d["metrics"].items()))

    # Write files
    if write_json:
        Path("results.json").write_text(json.dumps(data, indent=2))
        print("Wrote results.json")
    if write_md:
        Path("RESULTS.md").write_text(make_markdown(data))
        print("Wrote RESULTS.md")

if __name__ == "__main__":
    main()
