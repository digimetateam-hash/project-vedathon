# System Architecture — CyberSense

## 1. High-Level Architecture & Pipeline

```
           +-----------------------------------------------+
           |               TELEMETRY STREAM                |
           |  (Browser DOM, HTTP Access, MQTT, Sensors)    |
           +-----------------------+-----------------------+
                                   |
                                   v
           +-----------------------------------------------+
           |            TELEMETRY NORMALIZATION            |
           |   Unified Schema across HTTP, MQTT, Syslog    |
           +-----------------------+-----------------------+
                                   |
                                   v
           +-----------------------------------------------+
           |        IDENTITY & TEMPORAL CORRELATION        |
           |      Session Stitching, Source Flow Match     |
           +-----------------------+-----------------------+
                                   |
                                   v
           +-----------------------------------------------+
           |         CAPABILITY-AWARE ATTACK GRAPH         |
           | Nodes = Assets, Edges = Gained Capabilities   |
           +-----------------------+-----------------------+
                                   |
                                   v
           +-----------------------------------------------+
           |         PHYSICAL REACHABILITY EVALUATION      |
           |   Dynamic Path Finding to Target Actuators    |
           +-----------------------+-----------------------+
                                   |
                                   v
           +-----------------------------------------------+
           |    CPT TRANSITION & EARLY WARNING ENGINE      |
           |     Computes Physical Impact Lead Time        |
           +-----------------------+-----------------------+
                                   |
                                   v
           +-----------------------------------------------+
           |      COUNTERFACTUAL INTERVENTION ENGINE       |
           |  Optimal Break Point (Security vs Uptime)     |
           +-----------------------+-----------------------+
                                   |
                                   v
           +-----------------------------------------------+
           |         EXPLAINABLE FORENSIC REPORT           |
           |        Interactive Dashboard Alert UI         |
           +-----------------------------------------------+
```

---

## 2. Core Modules Breakdown

### A. Telemetry Normalizer
Mengonversi format log yang heterogen ke dalam skema standar CyberSense:
- **Browser Event:** Client IP, User-Agent, DOM Hook payload, Timestamp.
- **API Request:** Method, URI, Session Token, Header Fingerprint.
- **IoT Network:** Protocol (MQTT/HTTP), Topic, Payload Size, QoS.
- **Physical Sensor:** Actuator ID, State Change (Open/Closed), Current Draw.

### B. Identity & Temporal Correlator
Mengatasi **GAP #4 & #5** dengan melacak kesinambungan sesi (`session_id`) yang berpindah dari browser web ke request API lokal dan topik MQTT dalam jendela waktu kausal ($\Delta t$).

### C. Capability-Aware Attack Graph Generator
Menggantikan graph statis dengan graph transisi kapabilitas:
- Node $N_1$ (Browser) $\xrightarrow{\text{Cap: Read local context}}$ Node $N_2$ (Session)
- Node $N_2$ (Session) $\xrightarrow{\text{Cap: Authenticated API call}}$ Node $N_3$ (Gateway)
- Node $N_3$ (Gateway) $\xrightarrow{\text{Cap: Publish command}}$ Node $N_4$ (Broker)
- Node $N_4$ (Broker) $\xrightarrow{\text{Cap: Toggle physical solenoid}}$ Node $N_5$ (Actuator #03)

### D. Counterfactual Intervention Engine
Mengevaluasi titik pemutusan (*cut point*) pada attack graph:
$$\text{Efficiency Score} = \frac{\Delta \text{Risk Reduction}}{\text{Operational Disruption Cost}}$$
Sistem secara otomatis merekomendasikan intervensi dengan *disruption* paling rendah (misal: memblokir token sesi tertentu pada MQTT broker, bukan mematikan seluruh IoT Gateway).
