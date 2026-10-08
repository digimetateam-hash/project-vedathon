# Panduan Kontribusi (Contributing Guidelines)

Terima kasih telah tertarik berkontribusi pada pengembangan **Black Door** (Project VedaThon)!

---

## 🧭 Alur Kerja Kontribusi (Workflow)

1. **Fork & Branch:**
   - Lakukan Fork pada repositori ini jika Anda bukan kontributor langsung.
   - Buat branch baru dari branch `main` dengan format:
     ```bash
     git checkout -b feat/nama-fitur
     # atau
     git checkout -b fix/nama-bug
     ```

2. **Standar Kode & Konvensi Commit:**
   - Gunakan format [Conventional Commits](https://www.conventionalcommits.org/):
     - `feat:` penambahan fitur baru
     - `fix:` perbaikan bug
     - `docs:` pembaruan dokumentasi
     - `refactor:` perombakan kode tanpa mengubah fungsi
     - `test:` penambahan atau penyesuaian unit test

3. **Keamanan & Kredensial:**
   - **DILARANG KERAS** melakukan commit yang memuat API key, password, token PAT, atau data rahasia lainnya ke dalam Git.
   - Gunakan `.env` lokal yang merujuk pada `.env.example`.

4. **Pull Request (PR):**
   - Pastikan seluruh linter dan pengujian lokal lulus sebelum mengajukan PR.
   - Berikan deskripsi yang jelas mengenai perubahan yang dilakukan pada form PR.
