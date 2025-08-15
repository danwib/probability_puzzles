# src/prob_main.py
import argparse
import json

from src.birthday import prob_shared_birthday
from src.coupon_collector import expected_trials_approx, expected_trials_to_collect
from src.sim import simulate_birthday, simulate_coupon_collector


def main():
    parser = argparse.ArgumentParser(description="Probability puzzles CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Birthday problem
    b = sub.add_parser("birthday", help="Probability of a shared birthday in a group")
    b.add_argument("--n", type=int, default=23, help="Group size")
    b.add_argument("--days", type=int, default=365, help="Number of equally likely birthdays")
    b.add_argument(
        "--mc-trials",
        type=int,
        default=0,
        help="If >0, include Monte Carlo estimate with this many trials",
    )

    # Coupon collector
    c = sub.add_parser("coupon", help="Expected trials to collect n coupons")
    c.add_argument("--n", type=int, default=50, help="Number of distinct coupons")
    c.add_argument(
        "--approx",
        action="store_true",
        help="Use harmonic-number approximation instead of exact formula",
    )
    c.add_argument(
        "--mc-trials",
        type=int,
        default=0,
        help="If >0 (and not using --approx), include Monte Carlo estimate",
    )

    args = parser.parse_args()

    if args.cmd == "birthday":
        out = {
            "problem": "birthday",
            "n": args.n,
            "days": args.days,
            "p_shared": prob_shared_birthday(args.n, days=args.days),
        }
        if args.mc_trials > 0:
            mc = simulate_birthday(args.n, trials=args.mc_trials, days=args.days, seed=0)
            out.update({"p_shared_mc": mc, "abs_err": abs(out["p_shared"] - mc)})
        print(json.dumps(out))
        return

    if args.cmd == "coupon":
        val = expected_trials_approx(args.n) if args.approx else expected_trials_to_collect(args.n)
        out = {
            "problem": "coupon",
            "n": args.n,
            "expected_trials": val,
            "approx": bool(args.approx),
        }
        if args.mc_trials > 0 and not args.approx:
            mc = simulate_coupon_collector(args.n, trials=args.mc_trials, seed=0)
            out.update({"expected_trials_mc": mc, "rel_err": abs(val - mc) / val})
        print(json.dumps(out))
        return


if __name__ == "__main__":
    main()
