# OCR Plat Nomor Kendaraan Menggunakan Vision-Language Model (VLM)

Proyek ini merupakan implementasi sistem OCR (Optical Character Recognition) untuk membaca plat nomor kendaraan menggunakan Vision-Language Model (VLM). Model ini dapat mengenali teks pada plat nomor dari gambar input, bahkan dalam kondisi pencahayaan atau sudut miring.

## Fitur Utama

- Ekstraksi teks dari gambar plat nomor.
- Pemrosesan batch gambar.
- Evaluasi hasil OCR terhadap ground truth (format CSV).
- Visualisasi hasil dengan anotasi teks pada gambar.

## Struktur Folder

<pre> ``` . ├── images/ # Gambar plat nomor (input) ├── main.py # Script utama untuk menjalankan OCR ├── evaluasi_cer.csv # File hasil evaluasi Character Error Rate ├── README.md # Dokumentasi project ``` </pre>