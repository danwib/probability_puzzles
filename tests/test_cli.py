# tests/test_cli.py
import json
import subprocess
import sys


def run_cli(args):
    """Run the CLI as a module and parse its JSON output."""
    cmd = [sys.executable, "-m", "src.prob_main", *args]
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out.strip())


def test_cli_birthday_no_mc():
    res = run_cli(["birthday", "--n", "23", "--days", "365"])
    assert res["problem"] == "birthday"
    assert res["n"] == 23 and res["days"] == 365
    assert 0 <= res["p_shared"] <= 1


def test_cli_birthday_with_mc():
    res = run_cli(["birthday", "--n", "10", "--days", "365", "--mc-trials", "300"])
    assert "p_shared_mc" in res and "abs_err" in res
    assert 0 <= res["p_shared_mc"] <= 1
    assert res["abs_err"] >= 0


def test_cli_coupon_exact_no_mc():
    res = run_cli(["coupon", "--n", "20"])
    assert res["problem"] == "coupon"
    assert res["n"] == 20 and not res["approx"]
    assert res["expected_trials"] > 0


def test_cli_coupon_exact_with_mc():
    res = run_cli(["coupon", "--n", "15", "--mc-trials", "300"])
    assert "expected_trials_mc" in res and "rel_err" in res
    assert res["expected_trials_mc"] > 0 and 0 <= res["rel_err"] < 1


def test_cli_coupon_approx_no_mc():
    res = run_cli(["coupon", "--n", "50", "--approx"])
    assert res["approx"] is True
    # Approx path shouldn't include MC fields
    assert "expected_trials_mc" not in res and "rel_err" not in res
