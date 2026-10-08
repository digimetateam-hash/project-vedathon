# 🛡️ CyberSense × Black Door — Project VedaThon

> **From Browser Compromise to Physical Impact.**  
> *Detect the transition. Break the chain. Protect the physical world.*

[![CI](https://github.com/digimetateam-hash/project-vedathon/actions/workflows/ci.yml/badge.svg)](https://github.com/digimetateam-hash/project-vedathon/actions)
[![Deploy Pages](https://github.com/digimetateam-hash/project-vedathon/actions/workflows/pages.yml/badge.svg)](https://digimetateam-hash.github.io/project-vedathon/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 🏛️ Ecosystem Architecture: Dual Synergy

Proyek ini mengintegrasikan dua pilar utama yang saling melengkapi:

```
                            CYBERSENSE
              (Detection, Correlation & Defense Engine)
                                ▲
                                │ [Cross-Layer Telemetry]
                                ▼
                            BLACK DOOR
                 (Experimental Cyber-Physical Testbed)
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
   ├── BeEF Lab            ├── Robotic             ├── Dashboard
   │   (Client Compromise) │   Provisioning        │   (Dual UI)
   │                       │                       │
   ├── IoT Security Lab    ├── Auto Scoring        └── Physical IoT Demo
   │   (MQTT & Gateways)   │   (Realtime Flags)        (ESP32 & Solenoid)
```

---

## 🔬 CyberSense: The Research & Defense Core

### Core Research Question
> **“Can CyberSense identify the transition from a compromised browser/client to cyber-physical control capability earlier than conventional IoT or network-based detection, and recommend an optimal intervention point before physical impact occurs?”**

### The 15 Novelty Gaps
1. **Cross-Layer Correlation:** Menghubungkan browser, API, MQTT, dan sensor dalam 1 path.
2. **Transition Detection (CPT):** Mengetahui *kapan* serangan berubah menjadi kendali fisik.
3. **Capability-Aware Attack Graph:** Mengikuti kapabilitas nyata penyerang di setiap simpul.
4. **Identity Continuity:** Menjaga konteks token sesi melintasi protokol HTTP dan MQTT.
5. **Temporal Continuity:** Memetakan urutan kausalitas waktu riil antar event.
6. **Physical Reachability:** Status bertingkat dari *Not Reachable* hingga *Control Capable*.
7. **Physical Impact Lead Time:** Mengukur sisa waktu sebelum dampak fisik (misal **11.4 detik**).
8. **Earliest Detectable Transition:** Mendeteksi di fase $T_2/T_3/T_4$ sebelum aktuator berubah ($T_5$).
9. **Counterfactual Intervention:** Menemukan titik pemutusan serangan paling efektif.
10. **Security vs Availability:** Optimasi intervensi dengan *Intervention Efficiency Score (IES)*.
11. **Evidence Chain Forensics:** Setiap node dilengkapi bukti mentah dan tingkat keyakinan.
12. **Explainable Attack Path:** Narasi kausal yang dapat dipahami operator manusia.
13. **Multi-Layer Evidence Fusion:** Fusi 6 lapisan telemetri secara berkelanjutan.
14. **Attack Path Reconstruction:** Menghasilkan cerita serangan terstruktur (*Attack Story*).
15. **CPT-IoT Benchmark Dataset:** Pelabelan data fase transisi dari *STAGE_0* s.d. *STAGE_5*.

---

## ⚡ Black Door: The Lab & Provisioning Platform

Platform laboratorium terisolasi yang mengorkestrasikan seluruh skenario serangan:

```
BLACK DOOR
│
├── BeEF Lab
│   └── Browser exploitation framework & controlled compromise generator
│
├── IoT Security Lab
│   └── Simulated IoT microservices, exposed REST APIs, & MQTT broker
│
├── Robotic Provisioning
│   └── Automated Docker container spin-up & network namespace teardown (< 25s)
│
├── Auto Scoring
│   └── Automated flag validation & passive webhook exploit verifier
│
├── Dashboard
│   └── Unified interface: Student attack lab console + CyberSense defense radar
│
└── Physical IoT Demo
    └── ESP32 microcontroller, relay hardware, & 12V solenoid door lock
```

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
RECONSTRUCTED ATTACK PATH (BLACK DOOR LAB TESTBED)
Browser (Hooked via BeEF Lab)
   ↓ [Capability: Read local context]
Session #A81 (Hijacked Token)
   ↓ [Capability: Access internal API]
IoT Security Gateway (172.28.0.3)
   ↓ [Capability: Publish command topic]
MQTT Broker (home/security/door)
   ↓ [Capability: Alter physical state]
Smart Actuator #03 (Target Reachable)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED COUNTERFACTUAL INTERVENTION
ACTION: [ BLOCK MQTT SESSION #A81 ]

Expected Outcome   : Attack path broken. Physical impact prevented.
Availability Impact: LOW (Only malicious session revoked; gateway stays online)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🧪 Experimental Design & Baselines

- **Scenarios A–F:** Dari lalu lintas normal, kompromi browser murni, hingga pergerakan lateral penuh dan uji intervensi aktif.
- **Baselines B1–B8:** Dibandingkan terhadap *Network-only anomaly detection*, *IoT-only detection*, *Sensor fusion*, *Static graph*, *Dynamic graph*, dan studi ablasi model.

---

## 🚀 Quick Start & Interactive Demo

```bash
# 1. Clone repository
git clone https://github.com/digimetateam-hash/project-vedathon.git
cd project-vedathon

# 2. Buka interactive CyberSense × Black Door Dashboard di browser
open demo/index.html
```

---

## 📄 License

Dirilis di bawah lisensi [MIT](LICENSE). Copyright © 2026 Digimeta Team.
