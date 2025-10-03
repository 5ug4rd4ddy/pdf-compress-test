# PDF Compression Demo Application

Aplikasi demo untuk mengkompresi file PDF menggunakan service eksternal melalui API. Aplikasi ini dibangun menggunakan Flask dan mendukung upload file PDF, kompresi asynchronous dengan callback, dan download hasil kompresi.

## Fitur

- Upload file PDF
- Kompresi PDF dengan DPI yang dapat dikonfigurasi
- Callback endpoint untuk menerima hasil kompresi
- Antarmuka web sederhana
- Keamanan API dengan API key
- Daftar file yang sudah dikompresi

## Persyaratan

- Python 3.x
- Flask
- Requests
- Service kompresor PDF eksternal

## Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/5ug4rd4ddy/pdf-compress-test.git
cd pdf-compress-test
```

2. Install dependensi:
```bash
pip install flask requests
```

3. Konfigurasi environment variables (opsional):
```bash
COMPRESSOR_API_KEY=your_api_key
COMPRESS_SERVICE_URL=https://pdf.viscusmedia.com/compress
```

## Penggunaan

1. Jalankan aplikasi:
```bash
python external_app.py
```

2. Buka browser dan akses `http://127.0.0.1:5000`

3. Upload file PDF yang ingin dikompresi

4. File yang sudah dikompresi akan muncul di daftar file setelah proses selesai

## Struktur Direktori

```
pdf-demo/
├── external_app.py     # Aplikasi utama
├── templates/          # Template HTML
│   └── index.html     # Halaman utama
├── uploads/           # Direktori untuk file yang diupload
└── compressed/        # Direktori untuk file hasil kompresi
```

## API Endpoints

### Upload & Kompresi (`/`)
- Method: POST
- Input: Form-data dengan field `file` (PDF)
- Proses: Upload file dan kirim ke service kompresor

### Callback (`/receive`)
- Method: POST
- Headers: `X-API-Key` untuk autentikasi
- Input: Form-data dengan field `job_id` dan `file`
- Proses: Terima dan simpan file hasil kompresi

### Download
- `/uploads/<filename>`: Akses file yang diupload
- `/compressed/<filename>`: Akses file hasil kompresi

## Keamanan

- Validasi API key untuk callback endpoint
- Validasi tipe file
- Penggunaan UUID untuk nama file
- Direktori upload dan compressed yang terpisah

## Catatan

- Aplikasi ini adalah demo dan memerlukan konfigurasi tambahan untuk production
- File yang diupload harus dapat diakses oleh service kompresor
- Dalam implementasi production, gunakan storage publik (seperti S3) untuk file