import argparse, json
from src.birthday import prob_shared_birthday
from src.coupon_collector import expected_trials_to_collect, expected_trials_approx
from src.bayes import ppv, npv
from src.order_stats import expected_max_uniform, expected_kth_uniform
from src.balls_bins import expected_empty_bins

def main():
    p = argparse.ArgumentParser(description="Probability puzzles CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("birthday"); b.add_argument("n", type=int); b.add_argument("--days", type=int, default=365)
    c = sub.add_parser("coupon"); c.add_argument("n", type=int); c.add_argument("--approx", action="store_true")
    by = sub.add_parser("bayes")
    by.add_argument("--sens", type=float, required=True); by.add_argument("--spec", type=float, required=True); by.add_argument("--prev", type=float, required=True)
    om = sub.add_parser("order-max"); om.add_argument("n", type=int)
    ok = sub.add_parser("order-k"); ok.add_argument("n", type=int); ok.add_argument("k", type=int)
    eb = sub.add_parser("empty-bins"); eb.add_argument("m", type=int); eb.add_argument("n", type=int)

    args = p.parse_args()
    if args.cmd == "birthday":
        out = {"n": args.n, "days": args.days, "p_shared": prob_shared_birthday(args.n, args.days)}
    elif args.cmd == "coupon":
        val = expected_trials_approx(args.n) if args.approx else expected_trials_to_collect(args.n)
        out = {"n": args.n, "expected_trials": val, "approx": bool(args.approx)}
    elif args.cmd == "bayes":
        out = {"ppv": ppv(args.sens, args.spec, args.prev), "npv": npv(args.sens, args.spec, args.prev)}
    elif args.cmd == "order-max":
        out = {"n": args.n, "E_max": expected_max_uniform(args.n)}
    elif args.cmd == "order-k":
        out = {"n": args.n, "k": args.k, "E_k": expected_kth_uniform(args.n, args.k)}
    else:  # empty-bins
        out = {"m": args.m, "n": args.n, "E_empty": expected_empty_bins(args.m, args.n)}
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
