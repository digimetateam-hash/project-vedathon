# Black Door — Experimental Testbed & Cyber-Physical Lab Platform

**Black Door** adalah platform laboratorium dan lingkungan uji coba (*experimental testbed*) yang menyediakan skenario serangan terkontrol dari kompromi peramban hingga kontrol perangkat fisik. Platform ini berfungsi sebagai fondasi eksperimental bagi engine deteksi **CyberSense**.

---

## 🏛️ 6 Pilar Utama Black Door

```
BLACK DOOR
│
├── 1. BeEF Lab (Browser Exploitation Framework)
│
├── 2. IoT Security Lab (Virtual Nodes & Protocol Brokers)
│
├── 3. Robotic Provisioning (Automated Ephemeral Containers)
│
├── 4. Auto Scoring (Real-Time Flag & Impact Verifier)
│
├── 5. Dashboard (Dual-Perspective Operator & Student UI)
│
└── 6. Physical IoT Demo (ESP32 Relay & Solenoid Hardware Kit)
```

---

### 1. BeEF Lab (Browser Exploitation Framework)
- Berfungsi sebagai **generator kondisi kompromi awal** (*controlled initial compromise generator*).
- Menjalankan target web aplikasi rentan (Stored XSS / DOM Injection) dan BeEF control panel terisolasi.
- Menyuntikkan skrip `hook.js` untuk mensimulasikan peramban korban yang terinfeksi di dalam subnet intranet.

### 2. IoT Security Lab
- Lingkungan simulasi perangkat pintar virtual berbasis container ringan:
  - **Smart Lock API:** REST API internal tanpa otentikasi ketat.
  - **MQTT Gateway:** Broker pesan lokal (`172.28.0.4:1883`) untuk topik telemetri dan kendali.
  - **Virtual Camera & Sensors:** Emulasi RTSP stream dan sensor suhu/kelembaban.
- Menyediakan vektor pergerakan lateral bagi penyerang yang melompat dari sesi browser ke jaringan lokal.

### 3. Robotic Provisioning
- Orkestrasi kontainer dinamis berbasis Docker Engine API.
- Men-spin up environment per-sesi peserta dalam waktu **< 25 detik**.
- Melakukan *automatic teardown* dan isolasi subnet internal per-sesi (`iptables` boundary) untuk mencegah kebocoran trafik ke internet publik.

### 4. Auto Scoring
- Engine evaluasi pasif yang memantau webhook BeEF dan log broker MQTT.
- Memverifikasi secara instan apakah penyerang berhasil:
  - Mengaitkan browser (*hook verification*).
  - Mengakses API internal gateway.
  - Mempublikasikan payload kendali aktuator.
- Menghasilkan skor dan flag tanpa intervensi manual instruktur.

### 5. Interactive Dashboard
- Antarmuka terintegrasi yang menyatukan:
  - **Student / Lab Perspective:** Panduan modul, terminal interaktif, dan status misi.
  - **CyberSense Defense Perspective:** Radar transisi serangan, visualisasi attack path, dan grafik keterjangkauan fisik (*physical reachability*).

### 6. Physical IoT Demo
- Integrasi perangkat keras untuk demonstrasi langsung (*hardware-in-the-loop*):
  - **Mikrokontroler:** ESP32 dengan konektivitas WiFi & MQTT over TLS.
  - **Modul Relay & Solenoid Lock:** Kunci pintu fisik 12V yang terbuka otomatis saat perintah eksploitasi berhasil melewati broker MQTT.
  - Membuktikan dampak dunia nyata secara visual dari serangan yang bermula dari peramban web.
