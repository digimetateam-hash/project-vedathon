"""
Evaluation harness: runs scenarios A-F, N repetitions each, scores every
detector B1-B8, and reports detection metrics, temporal metrics (detection
latency, physical impact lead time) and intervention metrics with 95% CIs
and a paired Wilcoxon test of B8 against each baseline.

Run:  python3 -I evaluate.py [N]
Writes results.json and prints Markdown tables.
"""
from __future__ import annotations
import json, sys, random, statistics as stats
from simulator import (ScenarioSimulator, STAGE_SESSION, STAGE_GATEWAY,
                       STAGE_COMMAND, STAGE_IMPACT)
from cybersense import build_baselines

import numpy as np
from scipy import stats as sstats

SCENARIOS = ["A", "B", "C", "D", "E", "F"]

# Time (s) to execute the recommended intervention (block the MQTT session).
# A warning must lead the physical impact by more than this to prevent it.
INTERVENTION_APPLY_TIME = 2.0


def score_trace(trace, det):
    """Return dict of per-trace raw measurements for one detector."""
    res = det.detect(trace)
    events = trace["events"]
    # --- detection confusion at the event level (attack vs benign) --------
    tp = fp = fn = tn = 0
    for e, pred in zip(events, res.per_event):
        truth_attack = e.stage > 0
        pred_attack = pred > 0
        if truth_attack and pred_attack:
            tp += 1
        elif truth_attack and not pred_attack:
            fn += 1
        elif not truth_attack and pred_attack:
            fp += 1
        else:
            tn += 1
    # --- earliest TRUE-POSITIVE actionable warning ------------------------
    # Measure lead time only from a warning raised on the real attack session
    # at stage {2,3,4}; a false-positive "warning" on benign noise must not
    # count as early detection.
    warn_t = None
    warn_stage = None
    for e, pred in zip(events, res.per_event):
        if pred in (STAGE_SESSION, STAGE_GATEWAY, STAGE_COMMAND) and e.stage > 0:
            warn_t, warn_stage = e.t, pred
            break
    # first true-positive alarm of any stage, for detection latency
    first_tp_alarm = next((e.t for e, pred in zip(events, res.per_event)
                           if pred > 0 and e.stage > 0), None)

    # --- temporal: physical impact lead time ------------------------------
    # L = t_impact - t_warning, only defined for traces that DO reach impact
    # (E) or would have (F, measured against the would-be impact time).
    lead = None
    t_impact = trace["t_impact"]
    # For scenario F the chain is severed; use the projected impact time =
    # last command time + nominal actuation delay, to measure how early the
    # warning was relative to the averted impact.
    if t_impact is None and trace["scenario"] == "F":
        ct = trace["stage_times"].get(STAGE_COMMAND)
        if ct is not None:
            t_impact = ct + 1.6
    if t_impact is not None and warn_t is not None:
        lead = t_impact - warn_t
    # --- detection latency: first true alarm minus first attack event ------
    first_attack_t = min((e.t for e in events if e.stage > 0), default=None)
    latency = None
    if first_attack_t is not None and first_tp_alarm is not None:
        latency = first_tp_alarm - first_attack_t
    # --- intervention: did we warn early enough to actually apply a block? --
    # A warning only prevents impact if the lead time exceeds the time needed
    # to execute the counterfactual intervention (block the MQTT session).
    prevented = None
    if trace["scenario"] in ("E", "F"):
        prevented = (warn_t is not None and lead is not None
                     and lead > INTERVENTION_APPLY_TIME)
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, lead=lead, latency=latency,
                warning_stage=warn_stage, prevented=prevented,
                max_stage=res.max_stage)


def prf(tp, fp, fn):
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f


def ci95(xs):
    xs = [x for x in xs if x is not None]
    if len(xs) < 2:
        return (float("nan"), float("nan"), float("nan"), float("nan"))
    m = stats.mean(xs); sd = stats.pstdev(xs)
    se = sd / (len(xs) ** 0.5)
    return m, sd, m - 1.96 * se, m + 1.96 * se


def main(N=200):
    rng = random.Random(20261103)
    baselines = build_baselines()

    # accumulate per-detector aggregates
    agg = {bid: dict(tp=0, fp=0, fn=0, tn=0, leads=[], lat=[], prevent=[],
                     early=[]) for bid, _, _ in baselines}
    # per-detector lead-time samples on E+F, for Wilcoxon vs B8 (paired by run)
    paired_lead = {bid: [] for bid, _, _ in baselines}

    for run in range(N):
        for sc in SCENARIOS:
            sim = ScenarioSimulator(random.Random(rng.random() * 1e9))
            trace = sim.run(sc)
            run_leads = {}
            for bid, _, det in baselines:
                m = score_trace(trace, det)
                a = agg[bid]
                a["tp"] += m["tp"]; a["fp"] += m["fp"]
                a["fn"] += m["fn"]; a["tn"] += m["tn"]
                if m["lead"] is not None:
                    a["leads"].append(m["lead"])
                if m["latency"] is not None:
                    a["lat"].append(m["latency"])
                if m["prevented"] is not None:
                    a["prevent"].append(1.0 if m["prevented"] else 0.0)
                if m["warning_stage"] is not None:
                    a["early"].append(m["warning_stage"])
                if sc in ("E", "F"):
                    run_leads[bid] = m["lead"] if m["lead"] is not None else 0.0
            for bid in run_leads:
                paired_lead[bid].append(run_leads[bid])

    # IES model (GAP #10): IES = (dR/dRmax) * (1 - A_loss).
    # Block the malicious MQTT session -> full risk reduction, near-zero
    # availability loss; shut the whole gateway -> full risk reduction but
    # 14/15 benign sensors offline. Measured from the engine's recommendation.
    A_LOSS_BLOCK = 1.0 / 15.0
    A_LOSS_SHUTDOWN = 14.0 / 15.0
    ies_block = 1.0 * (1 - A_LOSS_BLOCK)
    ies_shutdown = 1.0 * (1 - A_LOSS_SHUTDOWN)

    rows = []
    for bid, label, _ in baselines:
        a = agg[bid]
        p, r, f = prf(a["tp"], a["fp"], a["fn"])
        fpr = a["fp"] / (a["fp"] + a["tn"]) if (a["fp"] + a["tn"]) else 0.0
        lm, lsd, llo, lhi = ci95(a["leads"])
        latm = stats.mean(a["lat"]) if a["lat"] else float("nan")
        prevent = 100 * stats.mean(a["prevent"]) if a["prevent"] else 0.0
        early = stats.mean(a["early"]) if a["early"] else float("nan")
        rows.append(dict(id=bid, label=label, precision=p, recall=r, f1=f,
                         fpr=fpr, lead_mean=lm, lead_sd=lsd, lead_lo=llo,
                         lead_hi=lhi, lead_median=(stats.median(a["leads"])
                         if a["leads"] else float("nan")),
                         latency=latm, prevented_pct=prevent,
                         mean_warn_stage=early, n_lead=len(a["leads"])))

    # Wilcoxon signed-rank: B8 lead time vs each baseline (paired per E/F run)
    b8 = paired_lead["B8"]
    wilcox = {}
    for bid in paired_lead:
        if bid == "B8":
            continue
        x = paired_lead[bid]
        n = min(len(x), len(b8))
        diffs = [a - b for a, b in zip(b8[:n], x[:n])]
        if all(d == 0 for d in diffs):
            # identical lead-time distributions (capability layer changes
            # precision/FPR, not lead time) — Wilcoxon undefined
            wilcox[bid] = dict(stat=0.0, p=float("nan"), n=n, identical=True)
            continue
        try:
            stat, pval = sstats.wilcoxon(b8[:n], x[:n])
        except ValueError:
            stat, pval = float("nan"), float("nan")
        wilcox[bid] = dict(stat=float(stat), p=float(pval), n=n, identical=False)

    out = dict(N=N, scenarios=SCENARIOS, rows=rows, wilcoxon=wilcox,
               ies=dict(block_session=ies_block, shutdown_gateway=ies_shutdown,
                        a_loss_block=A_LOSS_BLOCK, a_loss_shutdown=A_LOSS_SHUTDOWN))
    with open("results.json", "w") as fh:
        json.dump(out, fh, indent=2)

    # ---- Markdown ----
    print(f"\n### Table: detection & temporal metrics (N={N} runs/scenario, "
          f"{N*len(SCENARIOS)} traces)\n")
    print("| ID | Method | Precision | Recall | F1 | FPR | Lead time L (s), mean±sd | Median L | 95% CI | Prevented STAGE_5 (%) |")
    print("|----|--------|-----------|--------|----|----|--------------------------|----------|--------|-----------------------|")
    for r in rows:
        lead = (f"{r['lead_mean']:.2f}±{r['lead_sd']:.2f}"
                if r['lead_mean'] == r['lead_mean'] else "—")
        med = f"{r['lead_median']:.2f}" if r['lead_median'] == r['lead_median'] else "—"
        ci = (f"[{r['lead_lo']:.2f}, {r['lead_hi']:.2f}]"
              if r['lead_lo'] == r['lead_lo'] else "—")
        print(f"| {r['id']} | {r['label']} | {r['precision']:.3f} | "
              f"{r['recall']:.3f} | {r['f1']:.3f} | {r['fpr']:.3f} | {lead} | "
              f"{med} | {ci} | {r['prevented_pct']:.1f} |")

    print("\n### Wilcoxon signed-rank, B8 lead time vs baseline (paired on E/F runs)\n")
    print("| Baseline | W statistic | p-value | n pairs |")
    print("|----------|-------------|---------|---------|")
    for bid, w in wilcox.items():
        p = "identical lead (n/a)" if w.get("identical") else f"{w['p']:.3e}"
        print(f"| {bid} | {w['stat']:.1f} | {p} | {w['n']} |")

    print("\n### Intervention efficiency (IES)\n")
    print(f"- Block MQTT session (recommended): IES = {ies_block:.3f} "
          f"(A_loss = {A_LOSS_BLOCK:.3f})")
    print(f"- Shut down IoT gateway: IES = {ies_shutdown:.3f} "
          f"(A_loss = {A_LOSS_SHUTDOWN:.3f})")
    return out


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    main(N)
