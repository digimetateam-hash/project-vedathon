# CyberSense — cross-layer cyber-to-physical transition detector

Reference implementation and reproducible evaluation for the paper
*Cross-Layer Detection of Browser-to-Physical Transitions in Mechatronic
IoT Systems: The CyberSense × Black Door Testbed*.

This is a **defensive log-analysis engine** plus a **software-in-the-loop
telemetry simulator**. It performs no exploitation: the simulator emits
*labelled telemetry* (browser / API / MQTT / syslog / actuator events) for
six controlled scenarios, and the engine scores how early and how accurately
it detects the cyber-to-physical transition. It replaces the hard-coded demo
numbers in `demo/index.html` / `app.py` with measured results.

## Files
| File | What it does |
|------|--------------|
| `simulator.py` | Emits one labelled trace per scenario A–F (stages STAGE_0..STAGE_5), with timing jitter and ±40 ms clock skew. No real attack code. |
| `cybersense.py` | Detection engine (identity + temporal correlation, capability-aware attack graph, lead-time, IES) and baselines B1–B8. |
| `evaluate.py` | Runs N repetitions/scenario, computes Precision/Recall/F1/FPR, detection latency, physical-impact lead time (mean±sd, median, 95% CI), intervention prevention rate, and a paired Wilcoxon test of B8 vs each baseline. Writes `results.json`. |
| `RESULTS.md` | Markdown tables from the last run. |
| `lead_times.csv` | Per-method summary for box-plot / eCDF figures. |

## Reproduce
```bash
pip install numpy scipy
python3 evaluate.py 300      # N=300 runs/scenario -> 1800 traces, seed 20261103
```

## Headline result (N=300, seed 20261103)
- Full engine (B8): Precision 1.00, Recall 1.00, F1 1.00, FPR 0.00.
- Median physical-impact lead time 5.90 s (mean 5.92 ± 0.94), vs 2.66 s for
  the best network-only baseline and 1.60 s for IoT-only.
- With a 2 s intervention-apply time, impact prevented in 100% of E/F runs
  vs 8.2% for IoT-only detection.
- Ablations: removing the capability layer drops precision to 0.79 (FPR
  0.031); removing browser evidence drops recall to 0.71.

## Honest scope
These numbers measure the **detector on simulated telemetry**. They are not
measurements of the physical ESP32/solenoid; end-to-end hardware actuation
latency must be measured separately on the bench. The simulator encodes the
attack-stage structure described in the project docs; parameters
(inter-stage delays, confidences, clock skew, benign-noise rate) are set in
`simulator.py` and should be tuned to match real captures before the numbers
are used as empirical claims.
