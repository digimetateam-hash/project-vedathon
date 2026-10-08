# User Flow & Experience Design

## 1. Alur Pengguna: Peserta Didik (Student Journey)

```
[Mulai]
   │
   ▼
1. Login ke Dashboard
   │
   ▼
2. Pilih Modul & Tingkat Kesulitan (BeEF / IoT Lab)
   │
   ▼
3. Klik "Start Lab" ───► [Robotic Engine membuat container terisolasi (< 30s)]
   │
   ▼
4. Mengakses Lab Console & Target Environment
   │
   ├───► Jika mengalami kesulitan ───► Chat dengan AI Mentor (Socratic Hints)
   │
   ▼
5. Menemukan Celah & Melakukan Eksploitasi
   │
   ▼
6. Verifikasi Flag / Trigger Otomatis
   │
   ▼
7. Perolehan Poin & Pembaruan Dashboard / Leaderboard
   │
   ▼
8. Lab Selesai / Waktu Habis ───► Auto-Teardown & Rekapitulasi Progres
```

---

## 2. Alur Pengguna: Instruktur / Mentor (Instructor Journey)

1. **Akses Dashboard Pengajar:** Memantau seluruh sesi lab aktif di kelas secara waktu nyata (*real-time*).
2. **Monitoring Status Perangkat IoT:** Melihat visualisasi topologi lab peserta (Status: *Secure*, *Vulnerable*, *Compromised*).
3. **Analisis Riwayat & Kendala:** Meninjau rekaman pertanyaan peserta ke AI Mentor untuk mengetahui topik yang paling sering membingungkan siswa.
4. **Ekspor Laporan:** Mengunduh ringkasan performa dan nilai kelas dalam format terstruktur.
