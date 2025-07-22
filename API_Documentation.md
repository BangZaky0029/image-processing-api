# API Dokumentasi - Image Processing API

## Deskripsi
API ini dibuat berdasarkan kode Python yang menggunakan YOLOv5 untuk deteksi objek dan menambahkan teks pada gambar. API ini menyediakan endpoint untuk memproses gambar dengan menambahkan header text dan teks "Zaky Aulia Qolbi" pada area yang terdeteksi.

## Base URL
```
http://100.124.58.32:5001
```

## Endpoints

### 1. Health Check
**Endpoint:** `GET /api/health`

**Deskripsi:** Memeriksa status kesehatan API dan apakah model telah dimuat.

**Response:**
```json
{
    "status": "healthy",
    "message": "Image Processing API is running",
    "model_loaded": false
}
```

**Status Codes:**
- `200 OK`: API berjalan dengan baik

---

### 2. Process Image
**Endpoint:** `POST /api/process_image`

**Deskripsi:** Memproses gambar dengan menambahkan header text dan teks pada area yang terdeteksi oleh model YOLOv5.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `image` (required): File gambar (JPEG, PNG, dll.)
  - `header_text` (optional): Teks untuk header. Default: "0625-00940 (Marsoto, 2 SISI ZIPPER), 1 PCS"
  - `font_color` (optional): Warna teks. Pilihan: 'black', 'white', 'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink'. Default: 'black'

**Response:**
- **Content-Type:** `image/jpeg`
- **Body:** File gambar yang telah diproses

**Status Codes:**
- `200 OK`: Gambar berhasil diproses
- `400 Bad Request`: Input tidak valid (tidak ada file gambar atau warna tidak valid)
- `500 Internal Server Error`: Kesalahan server saat memproses gambar

**Error Response Format:**
```json
{
    "error": "Pesan error"
}
```

## Contoh Penggunaan

### Menggunakan cURL

#### Health Check
```bash
curl -X GET http://100.124.58.32:5001/api/health
```

#### Process Image
```bash
curl -X POST \
  -F "image=@/path/to/your/image.jpg" \
  -F "header_text=Custom Header Text" \
  -F "font_color=blue" \
  http://100.124.58.32:5001/api/process_image \
  --output processed_image.jpg
```

### Menggunakan Python

```python
import requests

# Health check
response = requests.get('http://100.124.58.32:5001/api/health')
print(response.json())

# Process image
with open('input_image.jpg', 'rb') as f:
    files = {'image': f}
    data = {
        'header_text': 'Custom Header',
        'font_color': 'red'
    }
    response = requests.post('http://100.124.58.32:5001/api/process_image', 
                           files=files, data=data)
    
    if response.status_code == 200:
        with open('output_image.jpg', 'wb') as output_file:
            output_file.write(response.content)
        print("Image processed successfully!")
    else:
        print(f"Error: {response.json()}")
```

### Menggunakan JavaScript (Fetch API)

```javascript
// Health check
fetch('http://100.124.58.32:5001/api/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Process image
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('header_text', 'Custom Header');
formData.append('font_color', 'blue');

fetch('http://100.124.58.32:5001/api/process_image', {
  method: 'POST',
  body: formData
})
.then(response => response.blob())
.then(blob => {
  const url = URL.createObjectURL(blob);
  const img = document.createElement('img');
  img.src = url;
  document.body.appendChild(img);
});
```

## Fitur API

1. **Object Detection**: Menggunakan YOLOv5 untuk mendeteksi objek dalam gambar
2. **Text Overlay**: Menambahkan header text di bagian atas gambar
3. **Dynamic Text Placement**: Menambahkan teks "Zaky Aulia Qolbi" di tengah bounding box objek yang terdeteksi
4. **Customizable Colors**: Mendukung berbagai pilihan warna untuk teks
5. **CORS Support**: Mendukung cross-origin requests
6. **Error Handling**: Penanganan error yang komprehensif

## Konfigurasi Warna

API mendukung warna-warna berikut untuk parameter `font_color`:

| Nama Warna | RGB Value |
|------------|-----------|
| black      | (0, 0, 0) |
| white      | (255, 255, 255) |
| red        | (255, 0, 0) |
| blue       | (0, 0, 255) |
| green      | (0, 255, 0) |
| yellow     | (255, 255, 0) |
| orange     | (255, 165, 0) |
| purple     | (255, 0, 255) |
| pink       | (255, 192, 203) |

## Catatan Teknis

1. **Model Loading**: Model YOLOv5 akan dimuat secara lazy (saat pertama kali digunakan)
2. **Font Handling**: API menggunakan font default sistem, dengan fallback ke DejaVu Sans jika tersedia
3. **Image Format**: API mendukung berbagai format gambar input dan selalu mengembalikan JPEG
4. **Memory Management**: Gambar diproses dalam memory tanpa menyimpan file sementara
5. **Performance**: Untuk performa terbaik, gunakan gambar dengan resolusi yang wajar (tidak terlalu besar)

## Deployment

API ini dapat di-deploy menggunakan berbagai metode:

1. **Development**: Jalankan langsung dengan `python src/main.py`
2. **Production**: Gunakan WSGI server seperti Gunicorn
3. **Docker**: Buat container dengan semua dependencies
4. **Cloud**: Deploy ke platform cloud seperti Heroku, AWS, atau Google Cloud

## Dependencies

- Flask
- Flask-CORS
- torch
- torchvision
- opencv-python-headless
- Pillow
- ultralytics
- numpy

## Troubleshooting

### Common Issues

1. **Model Loading Failed**: Pastikan koneksi internet tersedia untuk download model YOLOv5
2. **Memory Error**: Kurangi ukuran gambar input atau tingkatkan RAM server
3. **Font Not Found**: API akan menggunakan font default jika font khusus tidak ditemukan
4. **CORS Error**: Pastikan Flask-CORS telah dikonfigurasi dengan benar

### Error Messages

- `"Tidak ada file gambar yang dikirim"`: Parameter `image` tidak ada dalam request
- `"Tidak ada file yang dipilih"`: File yang dikirim kosong
- `"Warna tidak valid"`: Parameter `font_color` tidak sesuai dengan pilihan yang tersedia
- `"Gagal membaca file gambar"`: File yang dikirim bukan format gambar yang valid

