# Experimental Methodology & Evaluation — CyberSense

## 1. Experimental Lab Setup

```
                    +------------------------+
                    |       CYBERSENSE       |
                    +-----------+------------+
                                |
          +---------------------+---------------------+
          |                     |                     |
     Browser Layer        Network Layer        Physical Layer
  (BeEF Controlled Hub)   (MQTT Broker 1883)  (ESP32 Solenoid Relay)
          |                     |                     |
          +---------------------+---------------------+
                                |
                         Target Actuator
```

---

## 2. Experimental Scenarios (A – F)

- **Scenario A (Benign Baseline):** Trafik penjelajahan web biasa dan telemetri sensor suhu/kelembaban berkala.
- **Scenario B (Browser Compromise Only):** Penyerang melakukan hook ke browser klien via BeEF tanpa melakukan pemindaian jaringan lokal.
- **Scenario C (Browser $\rightarrow$ Local IoT Discovery):** Browser yang terinfeksi mengeksekusi fetch/XHR ke IP gateway lokal (172.28.0.3).
- **Scenario D (Browser $\rightarrow$ IoT $\rightarrow$ Command Capability):** Penyerang berhasil mengautentikasi dan mempublikasikan command ke broker MQTT, namun aktuator dalam status *locked/disabled*.
- **Scenario E (Full Kill Chain to Physical Impact):** Rantai serangan penuh: Browser $\rightarrow$ Session Hijack $\rightarrow$ Gateway $\rightarrow$ MQTT $\rightarrow$ Solenoid Pintu Terbuka Fisik.
- **Scenario F (Counterfactual Intervention Testing):** Eksekusi serangan Skenario E dengan intervensi aktif yang diuji pada 4 titik berbeda:
  1. Revoke Session di Browser
  2. Block Token di API Gateway
  3. Drop Publish di MQTT Broker
  4. Isolate IoT Gateway secara fisik

---

## 3. Baselines for Comparison (B1 – B8)

- **B1:** Network-only anomaly detection (Snort / Suricata signature & threshold rules).
- **B2:** IoT-only anomaly detection (Model autoencoder pada telemetri paket MQTT).
- **B3:** Network + physical sensor fusion (Model korelasi multi-modal konvensional).
- **B4:** Static attack graph (Pemetaan berbasis kerentanan CVE statis).
- **B5:** Dynamic attack graph (Graph berbasis state tanpa pemodelan kapabilitas).
- **B6:** CyberSense *tanpa* capability layer (Uji ablasi).
- **B7:** CyberSense *tanpa* browser evidence (Uji ablasi).
- **B8:** **Full CyberSense System** (Proposed end-to-end model).

---

## 4. Evaluation Metrics (5 Dimensions)

### A. Detection Metrics
- $\text{Precision} = \frac{TP}{TP + FP}$
- $\text{Recall} = \frac{TP}{TP + FN}$
- $\text{F1-Score} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$
- False Positive Rate (FPR)

### B. Temporal Dynamics Metrics
- **Detection Latency:** Selisih waktu antara injeksi payload pertama dan alarm pertama.
- **Transition Detection Latency:** Waktu yang dibutuhkan untuk mendeteksi perpindahan dari ruang cyber ke kontrol fisik ($T_1 \rightarrow T_4$).
- **Physical Impact Lead Time:** Waktu peringatan dini sebelum status aktuator fisik termanipulasi:
  $$\text{Lead Time} = t_{\text{physical\_impact}} - t_{\text{cybersense\_warning}}$$

### C. Graph Metrics
- Attack Path Precision & Recall
- Path Completeness

### D. Capability & Reachability Metrics
- Capability Transition Accuracy
- Physical Reachability Accuracy

### E. Defense & Intervention Metrics
- **Attack Path Break Rate:** Persentase pencegahan dampak fisik setelah intervensi.
- **Intervention Efficiency Score:**
  $$\text{IES} = \frac{\Delta \text{Risk}}{\text{Downtime/Availability Penalty}}$$
