# 🛡️ CyberSense — From Browser Compromise to Physical Impact

> **Detect the transition. Break the chain. Protect the physical world.**  
> *A capability-aware, temporally correlated, cross-layer attack-path framework for early cyber-to-physical transition detection and counterfactual intervention.*

[![CI](https://github.com/digimetateam-hash/project-vedathon/actions/workflows/ci.yml/badge.svg)](https://github.com/digimetateam-hash/project-vedathon/actions)
[![Deploy Pages](https://github.com/digimetateam-hash/project-vedathon/actions/workflows/pages.yml/badge.svg)](https://digimetateam-hash.github.io/project-vedathon/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 🎯 Core Research Question

> **“Can CyberSense identify the transition from a compromised browser/client to cyber-physical control capability earlier than conventional IoT or network-based detection, and recommend an optimal intervention point before physical impact occurs?”**

*(Apakah CyberSense mampu mengidentifikasi transisi dari kompromi browser/client menjadi kemampuan kendali cyber-physical lebih awal dibandingkan deteksi IoT atau jaringan konvensional, serta menentukan titik intervensi sebelum terjadi dampak fisik?)*

---

## 🚨 Problem Statement

Serangan *cyber-physical* dunia nyata hampir tidak pernah terjadi dalam satu lompatan terisolasi. Penyerang menembus perimeter melalui rantai serangan bertingkat (*multi-stage lateral movement*):

$$\text{Browser/Client} \longrightarrow \text{Session} \longrightarrow \text{Web/API} \longrightarrow \text{IoT Network} \longrightarrow \text{IoT Device} \longrightarrow \text{Physical State}$$

**Contoh Skenario:**
1. Browser pengguna di jaringan lokal dikompromikan (mis. via BeEF/Stored XSS).
2. Attacker membajak sesi terotentikasi (*authenticated session context*).
3. Attacker mengakses antarmuka internal IoT Gateway.
4. Memperoleh kapabilitas untuk mem-publish perintah kendali via protokol MQTT.
5. Status relay/aktuator fisik berubah secara tidak sah (*physical state altered*).

### Masalah Utama Penelitian Saat Ini
Mayoritas sistem deteksi intrusi (NIDS, HIDS, IoT Anomaly Detection) menganalisis setiap lapisan secara **terpisah (siloed)**. Sistem jaringan tidak memahami konteks browser, sistem IoT tidak memahami kontinuitas identitas sesi web, dan sensor fisik baru mendeteksi anomali setelah kerusakan fisik terjadi.

---

## 🔬 15 Gaps & Novelties in CyberSense

| # | Research Gap | Conventional Systems | CyberSense Innovation |
|---|---|---|---|
| **01** | **End-to-End Cross-Layer Correlation** | Lapisan browser, web API, dan IoT dianalisis terpisah | Korelasi kontinu dari kompromi client hingga state fisik dalam 1 attack path |
| **02** | **Detection of Transition (CPT)** | Bertanya: *"Apakah ini serangan?"* | Bertanya: *"Kapan serangan ini berubah menjadi kemampuan mengendalikan dunia fisik?"* |
| **03** | **Capability-Aware Attack Graph** | Graph statis: *Node A $\rightarrow$ Node B $\rightarrow$ Node C* | Graph dinamis berbasis kapabilitas: *Node A $\xrightarrow{\text{capability}}$ Node B $\xrightarrow{\text{capability}}$ Node C* |
| **04** | **Identity Continuity** | Log terpecah tanpa korelasi identitas | Menghubungkan `session_id`, `device_id`, `source_id`, `flow_id`, dan client identity |
| **05** | **Temporal Continuity** | Anomali independen tanpa urutan waktu kausal | Membangun *Temporal Attack Path* berurutan dengan jeda waktu absolut |
| **06** | **Physical Reachability Metric** | Sekadar *risk score* generik (Low/Med/High) | Metrik berjenjang: *Not Reachable $\rightarrow$ Potentially $\rightarrow$ Reachable $\rightarrow$ Control Capable $\rightarrow$ Physical Impact* |
| **07** | **Physical Impact Lead Time** | Hanya F1-Score atau akurasi deteksi | Mengukur durasi peringatan dini sebelum aktuator fisik berubah (mis. **11.4 – 14.7 detik**) |
| **08** | **Earliest Detectable Transition** | Baru mendeteksi saat aktuator fisik berubah ($T_5$) | Deteksi dini di tahap perolehan izin API/Command ($T_2/T_3/T_4$) |
| **09** | **Counterfactual Intervention** | Hanya memberikan peringatan pasif (*alert fatigue*) | Mensimulasikan pemutusan node optimal (*Optimal Intervention Point*) sebelum dampak terjadi |
| **10** | **Security vs Availability Optimization** | Asal memblokir gateway yang melumpuhkan operasional | Menghitung *Intervention Efficiency Score* (manfaat proteksi terbesar dengan disrupsi terkecil) |
| **11** | **Evidence Chain Forensics** | Black-box AI (*"Risk: High"*) tanpa jejak bukti | Setiap node memiliki timestamp, confidence, privilege, capability, dan bukti mentah |
| **12** | **Explainable Attack Path** | Output model sulit dipahami operator manusia | Narasi kausal yang dapat dimengerti manusia (*Machine Detection $\rightarrow$ Human Explanation*) |
| **13** | **Multi-Layer Evidence Fusion** | Hanya Network atau Network + Sensor fisik | Fusi 6 lapisan: Browser + Web/API + Network + IoT + Device + Physical Sensor |
| **14** | **Attack Path Reconstruction** | Deteksi anomali titik tunggal | Rekonstruksi cerita lengkap: *WHO $\rightarrow$ WHERE $\rightarrow$ SESSION $\rightarrow$ CAPABILITY $\rightarrow$ TARGET $\rightarrow$ IMPACT* |
| **15** | **CPT-IoT Benchmark Dataset** | Dataset hanya anomali paket MQTT atau CPS terpisah | Dataset pertama dengan label transisi cyber-ke-fisik (*STAGE_0* s.d. *STAGE_5*) |

---

## 🏗️ CyberSense Architecture

```
              ┌─────────────────────────────────────────┐
              │            BROWSER / CLIENT             │
              │  (Hooking, DOM Anomaly, Session Hijack) │
              └────────────────────┬────────────────────┘
                                   │
                                   ▼
              ┌─────────────────────────────────────────┐
              │             WEB / API LAYER             │
              │  (Reverse Proxy, Token Reuse, REST API) │
              └────────────────────┬────────────────────┘
                                   │
                                   ▼
              ┌─────────────────────────────────────────┐
              │               IoT NETWORK               │
              │     (MQTT Broker, CoAP, Local Subnet)   │
              └────────────────────┬────────────────────┘
                                   │
                                   ▼
              ┌─────────────────────────────────────────┐
              │               IoT DEVICE                │
              │   (Gateway, Microcontroller, Firmware)  │
              └────────────────────┬────────────────────┘
                                   │
                                   ▼
              ┌─────────────────────────────────────────┐
              │          PHYSICAL ENVIRONMENT           │
              │   (Relay, Smart Solenoid, Actuator State│
              └─────────────────────────────────────────┘

                                   │
                                   ▼ [Multi-Layer Telemetry Stream]
             ┌─────────────────────────────────────────────┐
             │            TELEMETRY NORMALIZATION          │
             └─────────────────────┬───────────────────────┘
                                   ▼
             ┌─────────────────────────────────────────────┐
             │      IDENTITY & TEMPORAL CORRELATION        │
             │   (Flow Tracking, Session Fingerprinting)   │
             └─────────────────────┬───────────────────────┘
                                   ▼
             ┌─────────────────────────────────────────────┐
             │       CAPABILITY-AWARE ATTACK GRAPH         │
             └─────────────────────┬───────────────────────┘
                                   ▼
             ┌─────────────────────────────────────────────┐
             │     PHYSICAL REACHABILITY EVALUATION        │
             └─────────────────────┬───────────────────────┘
                                   ▼
             ┌─────────────────────────────────────────────┐
             │   EARLY WARNING & LEAD TIME ENGINE (CPT)    │
             └─────────────────────┬───────────────────────┘
                                   ▼
             ┌─────────────────────────────────────────────┐
             │      COUNTERFACTUAL INTERVENTION ENGINE     │
             │       (Security vs Availability Tradeoff)   │
             └─────────────────────┬───────────────────────┘
                                   ▼
             ┌─────────────────────────────────────────────┐
             │        HUMAN-EXPLAINABLE ATTACK STORY       │
             └─────────────────────────────────────────────┘
```

---

## 🧪 Experimental Design & Baselines

### Skenario Uji Lab
- **Scenario A (Benign Baseline):** Lalu lintas normal pengguna browser dan telemetri IoT reguler.
- **Scenario B (Browser Compromise Only):** Kompromi browser terkontrol via BeEF tanpa pergerakan lateral.
- **Scenario C (Browser $\rightarrow$ Local IoT Discovery):** Akses dari browser korban ke endpoint gateway lokal.
- **Scenario D (Browser $\rightarrow$ IoT $\rightarrow$ Command Capability):** Publikasi perintah MQTT tanpa eksekusi aktuator.
- **Scenario E (Full Kill Chain to Physical Impact):** Rantai penuh dari browser hingga aktuator fisik terpicu.
- **Scenario F (Counterfactual Intervention):** Eksekusi serangan yang sama dengan intervensi pada node berbeda (Browser, Session, API, MQTT Broker) untuk mengukur pemutusan rantai serangan.

### Matriks Pembanding (Baselines B1–B8)
1. **B1:** Network-only anomaly detection (Suricata/Zeek baseline)
2. **B2:** IoT-only anomaly detection
3. **B3:** Network + physical sensor fusion
4. **B4:** Static attack graph
5. **B5:** Dynamic attack graph
6. **B6:** CyberSense *tanpa* capability layer (ablation study)
7. **B7:** CyberSense *tanpa* browser evidence (ablation study)
8. **B8:** **Full CyberSense System** (Proposed)

---

## 📊 Evaluation Metrics (5 Dimensions)

1. **Detection Performance:** Precision, Recall, F1-Score, False Positive Rate (FPR).
2. **Temporal Dynamics:** Detection Latency, Transition Detection Latency, **Physical Impact Lead Time (detik)**.
3. **Graph Fidelity:** Attack Path Precision, Attack Path Recall, Path Completeness.
4. **Capability Tracking:** Capability Transition Accuracy, Physical Reachability Accuracy.
5. **Defense Quality:** Attack Path Break Rate, Intervention Efficiency Score, Availability Impact.

---

## 📟 Killer Dashboard Output

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    CYBERSENSE EARLY WARNING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CYBER → PHYSICAL TRANSITION DETECTED
Risk Level       : CRITICAL
Confidence Score : 94.2%

Current Stage    : IoT Command Capability (T4)
Physical Target  : Smart Actuator #03 (Main Solenoid Lock)
Estimated Impact : HIGH (Physical Entry Breach)
Lead Time Left   : 11.4 seconds before physical state change

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECONSTRUCTED ATTACK PATH
Browser (Hooked)
   ↓ [Capability: Read local context]
Session #A81 (Hijacked Token)
   ↓ [Capability: Access internal API]
Local Gateway (172.28.0.3)
   ↓ [Capability: Publish command topic]
MQTT Broker (home/sensors/actuator)
   ↓ [Capability: Alter physical state]
Smart Actuator #03 (Target Reachable)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY? (EVIDENCE CHAIN)
✓ Browser DOM anomaly captured (hook signature verified)
✓ Identity continuity: Session #A81 reused on internal API
✓ Unauthorized POST /api/v1/door/unlock requested
✓ MQTT publish to control topic observed
✓ Target actuator physically reachable within 11.4s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED COUNTERFACTUAL INTERVENTION
ACTION: [ BLOCK MQTT SESSION #A81 ]

Expected Outcome   : Attack path broken. Physical impact prevented.
Availability Impact: LOW (Only malicious session revoked; gateway stays online)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🚀 Quick Start & Interactive Demo

```bash
# 1. Clone repository
git clone https://github.com/digimetateam-hash/project-vedathon.git
cd project-vedathon

# 2. Buka interactive CyberSense Dashboard demo di browser
open demo/index.html
```

---

## 👥 Research Team — Digimeta Team

- **Cyber-Physical Systems & Attack Graph Lead**
- **Cross-Layer Telemetry & Network Security Engineer**
- **Detection Algorithm & Explainable AI Researcher**

---

## 📄 License

Dirilis di bawah lisensi [MIT](LICENSE). Copyright © 2026 Digimeta Team.
