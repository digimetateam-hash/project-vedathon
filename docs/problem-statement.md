# Problem Statement & Research Gaps — CyberSense

## 1. Problem Statement

Serangan cyber-physical modern jarang terjadi dalam satu lompatan terisolasi. Penyerang menembus perimeter melalui evolusi multi-tahap:

$$\text{Browser/Client} \longrightarrow \text{Session} \longrightarrow \text{Web/API} \longrightarrow \text{IoT Network} \longrightarrow \text{IoT Device} \longrightarrow \text{Physical State}$$

Masalah fundamental penelitian keamanan saat ini adalah:
1. **Analisis Terpisah (Siloed):** Lapisan browser, jaringan, IoT, dan sensor fisik dianalisis oleh sistem monitoring yang berbeda tanpa korelasi identitas atau kausalitas waktu.
2. **Keterlambatan Deteksi:** Sebagian besar sistem deteksi intrusi fisik baru membunyikan alarm setelah aktuator atau sensor fisik mengalami manipulasi.

---

## 2. 15 Gap Utama (Research Gaps)

1. **GAP #1 — Browser $\rightarrow$ IoT $\rightarrow$ Physical Belum Dikorelasikan End-to-End:** Belum adanya kerangka kerja yang menghubungkan bukti forensik browser, API lokal, jaringan MQTT, hingga kondisi aktuator fisik dalam satu attack path terpadu.
2. **GAP #2 — Deteksi Transisi (Cyber-to-Physical Transition):** Bergeser dari sekadar mendeteksi anomali (*"Apakah ini serangan?"*) menjadi mendeteksi fase kritis (*"Kapan serangan ini berubah menjadi kemampuan mengendalikan dunia fisik?"*).
3. **GAP #3 — Capability-Aware Attack Graph:** Mengganti grafik statis ($A \rightarrow B \rightarrow C$) dengan grafik berbasis kapabilitas nyata yang diperoleh penyerang di setiap titik ($A \xrightarrow{\text{capability}} B \xrightarrow{\text{capability}} C$).
4. **GAP #4 — Identity Continuity:** Mengaitkan atribut identitas (`session_id`, `device_id`, `source_id`, `flow_id`, client token) melintasi protokol web HTTP dan protokol IoT MQTT.
5. **GAP #5 — Temporal Continuity:** Membangun *Temporal Attack Path* yang memperhitungkan urutan dan interval waktu kausal antar event.
6. **GAP #6 — Physical Reachability Metric:** Mengukur keterjangkauan fisik secara bertingkat: *NOT REACHABLE $\rightarrow$ POTENTIALLY REACHABLE $\rightarrow$ REACHABLE $\rightarrow$ CONTROL CAPABLE $\rightarrow$ PHYSICAL IMPACT*.
7. **GAP #7 — Physical Impact Lead Time:** Mengukur seberapa lama (dalam detik) sistem memberikan peringatan sebelum aktuator fisik berubah secara tidak sah (misal 11.4 detik).
8. **GAP #8 — Earliest Detectable Transition:** Menemukan titik awal optimal ($T_2/T_3/T_4$) sebelum mencapai dampak fisik ($T_5$).
9. **GAP #9 — Counterfactual Intervention:** Mensimulasikan skenario *"Bagaimana jika node ini diblokir sekarang?"* untuk memilih titik intervensi optimal.
10. **GAP #10 — Security vs Availability Optimization:** Menyeimbangkan mitigasi risiko tanpa melumpuhkan seluruh operasional gateway atau jaringan IoT (*Intervention Efficiency Score*).
11. **GAP #11 — Evidence Chain Forensics:** Setiap node memiliki bukti konkret (timestamp, confidence, privilege, capability, dan signature).
12. **GAP #12 — Explainable Attack Path:** Menyajikan narasi kausal yang dapat dipahami operator keamanan (*Machine Detection $\rightarrow$ Human Explanation*).
13. **GAP #13 — Multi-Layer Evidence Fusion:** Fusi 6 lapisan data (Browser + Web/API + Network + IoT + Device + Physical Sensor).
14. **GAP #14 — Attack Path Reconstruction:** Menghasilkan cerita lengkap: *WHO $\rightarrow$ FROM WHERE $\rightarrow$ USING WHAT SESSION $\rightarrow$ ACCESSING WHAT $\rightarrow$ GAINED WHAT CAPABILITY $\rightarrow$ REACHED WHICH DEVICE $\rightarrow$ COULD CHANGE WHAT PHYSICAL STATE*.
15. **GAP #15 — CPT-IoT Dataset:** Dataset terstandarisasi yang melabeli fase transisi dari *STAGE_0 (Benign)* hingga *STAGE_5 (Physical Impact)*.
