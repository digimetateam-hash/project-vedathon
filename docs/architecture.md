# System Architecture — Black Door

## 1. Arsitektur Tingkat Tinggi (High-Level Architecture)

Platform **Black Door** dibangun menggunakan pola arsitektur modular yang memisahkan antara *Control Plane* (Frontend Dashboard, API Gateway, Evaluator) dan *Execution Plane* (Robotic Provisioning Sandbox).

```
                      +-----------------------------+
                      |   Client Web Browser        |
                      |   (Next.js / React UI)      |
                      +--------------+--------------+
                                     |
                          HTTPS / WSS (Port 443)
                                     |
                                     v
                      +-----------------------------+
                      |       API Gateway           |
                      |   (FastAPI / Express.js)    |
                      +--------------+--------------+
                                     |
              +----------------------+----------------------+
              |                      |                      |
              v                      v                      v
    +-------------------+  +-------------------+  +-------------------+
    | User & Scoring DB |  | Robotic Engine    |  | AI Socratic Agent |
    | (PostgreSQL)      |  | (Docker SDK/API)  |  | (Gemini / Claude) |
    +-------------------+  +---------+---------+  +-------------------+
                                     |
                        Docker Socket / Unix Socket
                                     |
                                     v
    +-----------------------------------------------------------------+
    |                  ISOLATED LAB SANDBOX NETWORK                   |
    |                                                                 |
    |  +----------------------------+   +--------------------------+  |
    |  | Browser Target Node        |   | Virtual IoT Node         |  |
    |  | - BeEF Control Service     |   | - Smart Lock (HTTP/REST) |  |
    |  | - Vulnerable Web (XSS/SQLi)|   | - IP Cam (RTSP/Web stream)| |
    |  +----------------------------+   | - Smart Light (MQTT)     |  |
    |                                   +--------------------------+  |
    +-----------------------------------------------------------------+
```

---

## 2. Komponen Utama

### A. Frontend Dashboard
- **Teknologi:** React / Next.js dengan antarmuka modern, visualisasi grafis topologi jaringan, dan console terminal interaktif.
- **Komunikasi:** REST API untuk operasi CRUD dan WebSockets untuk streaming status log kontainer dan event realtime.

### B. Backend & Robotic Provisioning Engine
- **Teknologi:** Python (FastAPI) terintegrasi langsung dengan Docker Engine API.
- **Tanggung Jawab:**
  - Membuat dan menghapus jaringan bridge privat per-sesi.
  - Men-spin up container simulasi secara instan (< 25 detik).
  - Mengelola resource limit (CPU, Memory) dan timer auto-teardown.

### C. Target Lab Environment
- **Modul BeEF:** Container berisi target rentan (OWASP Juice Shop / DVWA) dan instans BeEF terisolasi.
- **Modul IoT Virtual:** Simulasi node IoT berbasis container ringan yang mengekspos endpoint API rentan dan broker MQTT lokal.

### D. AI Guided Mentor
- Menggunakan LLM terintegrasi via RAG untuk mendampingi peserta membedah alur eksploitasi dan remediasi tanpa membocorkan flag secara instan.
