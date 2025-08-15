import argparse
import json

from src.balls_bins import expected_empty_bins

<<<<<<< HEAD
from src.bayes import npv, ppv
from src.birthday import prob_shared_birthday
from src.coupon_collector import expected_trials_approx, expected_trials_to_collect
from src.order_stats import expected_kth_uniform, expected_max_uniform

=======
from src.sim import simulate_birthday, simulate_coupon_collector

>>>>>>> be18dcb47f38d9c8b538d7e9ab832c70b1517e03


def main():
    p = argparse.ArgumentParser(description="Probability puzzles CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("birthday")
    b.add_argument("n", type=int)
    b.add_argument("--days", type=int, default=365)
    c = sub.add_parser("coupon")
    c.add_argument("n", type=int)
    c.add_argument("--approx", action="store_true")
    by = sub.add_parser("bayes")
<<<<<<< HEAD
    by.add_argument("--sens", type=float, required=True)
    by.add_argument("--spec", type=float, required=True)
    by.add_argument("--prev", type=float, required=True)
    om = sub.add_parser("order-max")
    om.add_argument("n", type=int)
    ok = sub.add_parser("order-k")
    ok.add_argument("n", type=int)
    ok.add_argument("k", type=int)
    eb = sub.add_parser("empty-bins")
    eb.add_argument("m", type=int)
    eb.add_argument("n", type=int)
=======
    by.add_argument("--sens", type=float, required=True); by.add_argument("--spec", type=float, required=True); by.add_argument("--prev", type=float, required=True)
    om = sub.add_parser("order-max"); om.add_argument("n", type=int)
    ok = sub.add_parser("order-k"); ok.add_argument("n", type=int); ok.add_argument("k", type=int)
    eb = sub.add_parser("empty-bins"); eb.add_argument("m", type=int); eb.add_argument("n", type=int)
    b.add_argument("--mc-trials", type=int, default=0, help="If >0, include Monte Carlo estimate")
    c.add_argument("--mc-trials", type=int, default=0, help="If >0, include Monte Carlo estimate")
>>>>>>> be18dcb47f38d9c8b538d7e9ab832c70b1517e03

    args = p.parse_args()
    if args.cmd == "birthday":
        out = {"n": args.n, "days": args.days, "p_shared": prob_shared_birthday(args.n, args.days)}
        if args.mc_trials > 0:
            mc = simulate_birthday(args.n, trials=args.mc_trials, days=args.days, seed=0)
            out.update({"p_shared_mc": mc, "abs_err": abs(out["p_shared"] - mc)})
    elif args.cmd == "coupon":
        val = expected_trials_approx(args.n) if args.approx else expected_trials_to_collect(args.n)
        out = {"n": args.n, "expected_trials": val, "approx": bool(args.approx)}
        if args.mc_trials > 0 and not args.approx:
            mc = simulate_coupon_collector(args.n, trials=args.mc_trials, seed=0)
            out.update({"expected_trials_mc": mc, "rel_err": abs(val - mc) / val})
    elif args.cmd == "bayes":
        out = {
            "ppv": ppv(args.sens, args.spec, args.prev),
            "npv": npv(args.sens, args.spec, args.prev),
        }
    elif args.cmd == "order-max":
        out = {"n": args.n, "E_max": expected_max_uniform(args.n)}
    elif args.cmd == "order-k":
        out = {"n": args.n, "k": args.k, "E_k": expected_kth_uniform(args.n, args.k)}
    else:  # empty-bins
        out = {"m": args.m, "n": args.n, "E_empty": expected_empty_bins(args.m, args.n)}
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
