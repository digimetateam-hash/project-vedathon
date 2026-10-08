# Security, Isolation & Safety Framework

## 1. Prinsip Keamanan Utama (Defense-in-Depth)

Sebagai platform laboratorium edukasi serangan dan pertahanan siber, keamanan infrastruktur host dan pencegahan penyalahgunaan sistem adalah prioritas mutlak.

---

## 2. Mekanisme Isolasi (Sandbox Boundaries)

### A. Network Isolation (Pemisahan Jaringan)
- Setiap lab sesi dialokasikan ke dalam Docker bridge network tersendiri: `lab_net_<session_id>`.
- **Tanpa Akses Keluar (No Egress to WAN):** Aturan iptables membatasi koneksi dari dalam kontainer target agar tidak dapat menghubungi internet publik atau subnet lokal server host.
- **Pemisahan Antar Peserta:** Sesi peserta A tidak dapat melihat, memindai, atau berinteraksi dengan sesi peserta B.

### B. Pembatasan Sumber Daya (Resource Quotas & Limits)
- Kontainer lab dibatasi dengan opsi `--cpus="0.5"` dan `--memory="512m"` untuk mencegah serangan *Denial of Service (DoS)* terhadap host.
- Pembatasan jumlah proses maksimum (`pids-limit`) guna mencegah serangan *fork bomb*.

### C. Siklus Hidup Otomatis (Lifecycle & Auto-Teardown)
- Sesi lab memiliki batas waktu kedaluwarsa ketat (default: 60 menit).
- *Background Daemon Worker* secara berkala menghapus kontainer, volume sementara, dan subnet virtual yang sudah lewat waktu aktifnya (*garbage collection*).

---

## 3. Manajemen Rahasia & Kredensial
- Seluruh token API pihak ketiga (Gemini, database, JWT secret) disimpan secara aman pada berkas lingkungan server (`.env`) dan tidak pernah dikirimkan ke sisi antarmuka klien.
- Endpoint komunikasi dilindungi oleh otentikasi berbasis JWT dengan durasi masa berlaku token yang singkat.
