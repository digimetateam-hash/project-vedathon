# AI Usage Disclosure & Ethics Statement

## Overview
Proyek **Black Door** dibangun dengan komitmen terhadap transparansi dan kepatuhan etis dalam pemanfaatan teknologi Artificial Intelligence (AI). Dokumen ini merinci bagaimana AI digunakan sepanjang siklus pengembangan proyek untuk kompetisi **VedaThon**.

---

## 🛠️ AI Tools yang Digunakan

| Tool / Model | Peran dalam Pengembangan | Kontribusi |
| :--- | :--- | :--- |
| **Google Gemini 1.5 Pro / Flash** | Brainstorming & Dialog Mentor | Pengembangan persona *Socratic Cyber Mentor* dan kurikulum skenario lab |
| **Claude 3.5 Sonnet** | Refactoring & Arsitektur | Penyusunan skema modular isolasi Docker dan rancangan API REST |
| **GitHub Copilot / Antigravity IDE** | Pair-Programming | Penulisan boilerplate kode, konfigurasi Dockerfile, dan pembuatan unit test |

---

## 🧭 Prinsip Penggunaan AI

1. **Human-in-the-Loop:**
   Setiap baris kode, arsitektur, dan skenario keamanan yang disarankan oleh AI telah diverifikasi, diuji, dan disesuaikan langsung oleh tim pengembang.
2. **Ethical Security Guardrails:**
   AI Mentor dalam aplikasi dirancang dengan *prompt engineering* berbasis batas keamanan (guardrails) agar tidak pernah memberikan solusi eksploitasi berbahaya secara langsung (*no flag dumping*), melainkan menuntun logika berpikir peserta.
3. **Pencegahan Halusinasi:**
   Seluruh referensi teknis yang digunakan dalam materi praktikum merujuk pada standar industri terverifikasi (OWASP Top 10, CWE, MITRE ATT&CK Framework).
