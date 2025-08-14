# Probability Puzzles (EV, Bayes, Order Statistics, Balls-in-Bins)

A small Python toolkit for canonical probability puzzles—birthday paradox, coupon collector, Bayes PPV/NPV, order statistics, and balls-in-bins.
Includes analytic derivations, a CLI to generate reproducible results, and tests/coverage for correctness.

## Features
- Closed-form solutions for common puzzles (birthday paradox, coupon collector, Bayes PPV/NPV, order statistics, balls-in-bins)
- Lightweight CLI to compute results quickly
- Unit tests with optional coverage
- Clear results table you can paste into docs or share in reviews

## Getting Started

### Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run the CLI
```bash
# Birthday paradox
python -m src.prob_main birthday 23

# Coupon collector (exact vs. approximate)
python -m src.prob_main coupon 3
python -m src.prob_main coupon 100 --approx

# Bayes (PPV/NPV)
python -m src.prob_main bayes --sens 0.9 --spec 0.95 --prev 0.1

# Order statistics (Uniform(0,1)): E[max], E[X_(k)]
python -m src.prob_main order-max 10
python -m src.prob_main order-k 10 3

# Balls in bins: expected # of empty bins
python -m src.prob_main empty-bins 10 10
```

## Results
Deterministic closed-form outputs for selected cases:

| Puzzle | Case | Metrics |
|---|---|---|
| Birthday paradox | n=5 | p_shared=0.0271356 |
| Birthday paradox | n=10 | p_shared=0.116948 |
| Birthday paradox | n=20 | p_shared=0.411438 |
| Birthday paradox | n=23 | p_shared=0.507297 |
| Birthday paradox | n=30 | p_shared=0.706316 |
| Birthday paradox | n=50 | p_shared=0.970374 |
| Coupon collector | n=3 | E[T]_exact=5.5, E[T]_approx=5.52748 |
| Coupon collector | n=10 | E[T]_exact=29.2897, E[T]_approx=29.298 |
| Coupon collector | n=20 | E[T]_exact=71.9548, E[T]_approx=71.959 |
| Coupon collector | n=50 | E[T]_exact=224.96, E[T]_approx=224.962 |
| Coupon collector | n=100 | E[T]_exact=518.738, E[T]_approx=518.739 |
| Bayes PPV/NPV | sens=0.9, spec=0.95, prev=0.01 | PPV=0.153846, NPV=0.998938 |
| Bayes PPV/NPV | sens=0.9, spec=0.95, prev=0.1 | PPV=0.666667, NPV=0.988439 |
| Order stats | E[max], n=5 | E[max]=0.833333 |
| Order stats | E[X_(k)], n=5, k=1 | E[X_(k)]=0.166667 |
| Order stats | E[X_(k)], n=5, k=3 | E[X_(k)]=0.5 |
| Order stats | E[X_(k)], n=5, k=5 | E[X_(k)]=0.833333 |
| Order stats | E[max], n=10 | E[max]=0.909091 |
| Order stats | E[X_(k)], n=10, k=1 | E[X_(k)]=0.0909091 |
| Order stats | E[X_(k)], n=10, k=5 | E[X_(k)]=0.454545 |
| Order stats | E[X_(k)], n=10, k=10 | E[X_(k)]=0.909091 |
| Balls in bins | m=10, n=10 | E[empty]=3.48678 |
| Balls in bins | m=20, n=10 | E[empty]=1.21577 |
| Balls in bins | m=100, n=10 | E[empty]=0.000265614 |
| Balls in bins | m=100, n=50 | E[empty]=6.63098 |

> Reproduce full results files with:
> ```bash
> python scripts/emit_results.py
> ```
> This prints a summary and writes `RESULTS.md` and `results.json` in the repo root.

## Testing & Coverage
```bash
pytest --maxfail=1 --disable-warnings --cov=src --cov-report=term-missing
```
Tips:
- If you see “No data to report”, ensure `src/__init__.py` exists and tests import modules as `from src.* import ...`.
- In CI, add `pytest-cov` and run the same command. You can enforce a bar, e.g., `--cov-fail-under=90`.

## Techniques Used
- **Linearity of expectation** & **indicator variables** (coupon collector, empty bins)
- **Bayes’ rule** with sensitivity/specificity → **PPV/NPV**
- **Order statistics** for Uniform(0,1): \(\mathbb{E}[\max]=\tfrac{n}{n+1}\), \(\mathbb{E}[X_{(k)}]=\tfrac{k}{n+1}\)
- Log-sum trick for stable probability products (birthday paradox)

## Project Structure
```
src/
  bayes.py
  balls_bins.py
  birthday.py
  coupon_collector.py
  ev.py
  order_stats.py
  prob_main.py          # CLI entry
scripts/
  emit_results.py       # writes RESULTS.md + results.json
tests/
  test_*.py
.github/workflows/ci.yml
README.md
requirements.txt
pyproject.toml
```

## License
MIT — see `LICENSE`.

## Next Steps (ideas)
- Add Monte Carlo simulations to cross-check analytic results (e.g., birthday paradox, coupon collector)
- Include a Jupyter notebook in `examples/` with derivations and quick plots
- Add more puzzles (Monty Hall, Gambler’s Ruin time to absorption, hypergeometric EV/var, negative binomial)
- Pre-commit hooks for formatting/linting

