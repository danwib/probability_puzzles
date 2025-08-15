# scripts/emit_results.py
import json
import os
from pathlib import Path

from src.balls_bins import expected_empty_bins
from src.bayes import npv, ppv
from src.birthday import prob_shared_birthday
from src.coupon_collector import expected_trials_approx, expected_trials_to_collect
from src.order_stats import expected_kth_uniform, expected_max_uniform

# --- Try to import vectorised MC; fall back to classic if not present ---
try:
    from src.sim import simulate_birthday_vec as simulate_birthday_mc
    from src.sim import simulate_coupon_collector_vec as simulate_coupon_mc
except Exception:
    from src.sim import simulate_birthday as simulate_birthday_mc
    from src.sim import simulate_coupon_collector as simulate_coupon_mc

# --- Configurable MC trial counts via env vars (keep defaults modest) ---
MC_TRIALS_BDAY = int(os.environ.get("MC_TRIALS_BDAY", "5000"))
MC_TRIALS_COUP = int(os.environ.get("MC_TRIALS_COUP", "3000"))
MC_SEED = int(os.environ.get("MC_SEED", "0"))
INCLUDE_MC = int(os.environ.get("INCLUDE_MC", "1"))  # 1 = include MC columns, 0 = analytic only


def rows():
    # Birthday paradox (analytic + optional MC)
    for n in [5, 10, 20, 23, 30, 50]:
        p = prob_shared_birthday(n)
        metrics = {"p_shared": p}
        if INCLUDE_MC:
            pmc = simulate_birthday_mc(n, trials=MC_TRIALS_BDAY, days=365, seed=MC_SEED)
            metrics.update({"p_shared_mc": pmc, "abs_err": abs(p - pmc)})
        yield ("Birthday paradox", f"n={n}", metrics)

    # Coupon collector (exact + approx + optional MC)
    for n in [3, 10, 20, 50, 100]:
        exact = expected_trials_to_collect(n)
        approx = expected_trials_approx(n)
        metrics = {"E[T]_exact": exact, "E[T]_approx": approx}
        if INCLUDE_MC:
            emc = simulate_coupon_mc(n, trials=MC_TRIALS_COUP, seed=MC_SEED)
            rel_err = abs(exact - emc) / exact
            metrics.update({"E[T]_mc": emc, "rel_err": rel_err})
        yield ("Coupon collector", f"n={n}", metrics)

    # Bayes (analytic)
    for prev in [0.01, 0.10]:
        sens, spec = 0.90, 0.95
        yield (
            "Bayes PPV/NPV",
            f"sens={sens}, spec={spec}, prev={prev}",
            {"PPV": ppv(sens, spec, prev), "NPV": npv(sens, spec, prev)},
        )

    # Order statistics (U(0,1)) — analytic
    for n in [5, 10]:
        yield ("Order stats", f"E[max], n={n}", {"E[max]": expected_max_uniform(n)})
        for k in [1, (n + 1) // 2, n]:
            yield (
                "Order stats",
                f"E[X_(k)], n={n}, k={k}",
                {"E[X_(k)]": expected_kth_uniform(n, k)},
            )

    # Balls into bins — analytic
    for m, n in [(10, 10), (20, 10), (100, 10), (100, 50)]:
        yield ("Balls in bins", f"m={m}, n={n}", {"E[empty]": expected_empty_bins(m, n)})


def fmt(x):
    if isinstance(x, float):
        return f"{x:.6f}"
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
        print(
            f"[{d['puzzle']}] {d['case']} -> "
            + ", ".join(f"{k}={fmt(v)}" for k, v in d["metrics"].items())
        )

    # Write files
    if write_json:
        Path("results.json").write_text(json.dumps(data, indent=2))
        print("Wrote results.json")
    if write_md:
        Path("RESULTS.md").write_text(make_markdown(data))
        print("Wrote RESULTS.md")


if __name__ == "__main__":
    main()
