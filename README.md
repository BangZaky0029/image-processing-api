# Image Processing API

API berbasis Flask untuk memproses gambar dengan deteksi objek menggunakan YOLOv5 dan penambahan teks overlay.

## Fitur

- ✅ Object detection menggunakan YOLOv5
- ✅ Penambahan header text pada gambar
- ✅ Penambahan teks "Zaky Aulia Qolbi" pada area objek yang terdeteksi
- ✅ Kustomisasi warna teks
- ✅ CORS support untuk frontend integration
- ✅ RESTful API design
- ✅ Error handling yang komprehensif

## Instalasi

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. Clone atau download proyek ini
2. Masuk ke direktori proyek:
   ```bash
   cd image_processing_api
   ```

3. Aktifkan virtual environment:
   ```bash
   source venv/bin/activate  # Linux/Mac
   # atau
   venv\Scripts\activate     # Windows
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Menjalankan API

### Development Mode

```bash
python src/main.py
```

Server akan berjalan di `http://localhost:5001`

### Production Mode

Untuk production, gunakan WSGI server seperti Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 src.main:app
```

## Testing

Jalankan script test untuk memverifikasi API:

```bash
python test_api.py
```

## Struktur Proyek

```
image_processing_api/
├── src/
│   ├── main.py              # Entry point aplikasi
│   ├── models/              # Database models
│   ├── routes/
│   │   ├── user.py         # User routes (default)
│   │   └── image.py        # Image processing routes
│   ├── static/             # Static files
│   └── database/           # Database files
├── venv/                   # Virtual environment
├── requirements.txt        # Python dependencies
├── test_api.py            # API testing script
├── API_Documentation.md   # Dokumentasi API lengkap
└── README.md              # File ini
```

## API Endpoints

### Health Check
```
GET /api/health
```

### Process Image
```
POST /api/process_image
```

Untuk dokumentasi lengkap, lihat [API_Documentation.md](API_Documentation.md)

## Contoh Penggunaan

### cURL
```bash
# Health check
curl http://localhost:5001/api/health

# Process image
curl -X POST \
  -F "image=@image.jpg" \
  -F "header_text=Custom Header" \
  -F "font_color=blue" \
  http://localhost:5001/api/process_image \
  --output result.jpg
```

### Python
```python
import requests

# Process image
with open('input.jpg', 'rb') as f:
    files = {'image': f}
    data = {'header_text': 'Test', 'font_color': 'red'}
    response = requests.post('http://localhost:5001/api/process_image', 
                           files=files, data=data)
    
    with open('output.jpg', 'wb') as out:
        out.write(response.content)
```

## Konfigurasi

### Warna yang Didukung
- black, white, red, blue, green, yellow, orange, purple, pink

### Environment Variables
- `FLASK_ENV`: development/production
- `PORT`: Port untuk server (default: 5001)

## Troubleshooting

1. **Port sudah digunakan**: Ubah port di `src/main.py`
2. **Model tidak bisa diload**: Pastikan koneksi internet untuk download YOLOv5
3. **Memory error**: Kurangi ukuran gambar input

## Contributing

1. Fork repository
2. Buat feature branch
3. Commit changes
4. Push ke branch
5. Buat Pull Request

## License

MIT License

## Support

Untuk pertanyaan atau issue, silakan buat issue di repository ini.

