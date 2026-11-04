
### Table: detection & temporal metrics (N=300 runs/scenario, 1800 traces)

| ID | Method | Precision | Recall | F1 | FPR | Lead time L (s), mean±sd | Median L | 95% CI | Prevented STAGE_5 (%) |
|----|--------|-----------|--------|----|----|--------------------------|----------|--------|-----------------------|
| B1 | Network-only (Suricata/Snort rules) | 0.637 | 0.235 | 0.344 | 0.016 | 2.70±0.41 | 2.66 | [2.66, 2.73] | 95.3 |
| B2 | IoT-only anomaly (MQTT autoencoder) | 0.644 | 0.235 | 0.345 | 0.015 | 1.59±0.29 | 1.60 | [1.57, 1.62] | 8.2 |
| B3 | Network + sensor fusion (no identity) | 0.641 | 0.471 | 0.543 | 0.031 | 2.70±0.41 | 2.66 | [2.66, 2.73] | 95.3 |
| B4 | Static attack graph (CVE map) | 0.644 | 0.235 | 0.345 | 0.015 | 1.59±0.29 | 1.60 | [1.57, 1.62] | 8.2 |
| B5 | Dynamic attack graph (no capability) | 0.791 | 1.000 | 0.883 | 0.031 | 5.92±0.94 | 5.90 | [5.84, 5.99] | 100.0 |
| B6 | CyberSense w/o capability layer (ablation) | 0.791 | 1.000 | 0.883 | 0.031 | 5.92±0.94 | 5.90 | [5.84, 5.99] | 100.0 |
| B7 | CyberSense w/o browser evidence (ablation) | 1.000 | 0.706 | 0.828 | 0.000 | 5.92±0.94 | 5.90 | [5.84, 5.99] | 100.0 |
| B8 | CyberSense full system (proposed) | 1.000 | 1.000 | 1.000 | 0.000 | 5.92±0.94 | 5.90 | [5.84, 5.99] | 100.0 |

### Wilcoxon signed-rank, B8 lead time vs baseline (paired on E/F runs)

| Baseline | W statistic | p-value | n pairs |
|----------|-------------|---------|---------|
| B1 | 0.0 | 5.978e-100 | 600 |
| B2 | 0.0 | 5.978e-100 | 600 |
| B3 | 0.0 | 5.978e-100 | 600 |
| B4 | 0.0 | 5.978e-100 | 600 |
| B5 | 0.0 | identical lead (n/a) | 600 |
| B6 | 0.0 | identical lead (n/a) | 600 |
| B7 | 0.0 | identical lead (n/a) | 600 |

### Intervention efficiency (IES)

- Block MQTT session (recommended): IES = 0.933 (A_loss = 0.067)
- Shut down IoT gateway: IES = 0.067 (A_loss = 0.933)
