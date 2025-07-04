import os
import io
import re
import torch
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from flask import Blueprint, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime

# Modular imports
from src.font_controllers.font_color import COLOR_OPTIONS
from src.font_controllers.font_style import get_font
from src.font_controllers.font_position import calculate_text_position
from src.path_controllers.path import get_save_path

image_bp = Blueprint('image', __name__)
CORS(image_bp)

# Load YOLOv5 model (once)
model = None
def load_model():
    global model
    if model is None:
        try:
            model = torch.hub.load("ultralytics/yolov5", "custom", path="D:/YOLO/yolov5/runs/train/training_06/weights/best.pt", force_reload=False)
            print("[MODEL] YOLOv5 berhasil dimuat.")
        except Exception as e:
            print(f"[ERROR] Gagal load model: {e}")
            model = None
    return model

# Penamaan file
prefix = "Sample_"
ext = ".jpg"

@image_bp.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Validasi file
        if 'image' not in request.files:
            return jsonify({'error': 'Tidak ada file gambar yang dikirim'}), 400
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400

        # Ambil parameter
        header_text = request.form.get('header_text', '0625-00940 (Marsoto, 2 SISI ZIPPER), 1 PCS')
        font_color_name = request.form.get('font_color', 'black')
        nama = request.form.get('nama', 'Zaky Aulia Qolbi')

        font_color = COLOR_OPTIONS.get(font_color_name, (0, 0, 0))

        # Baca gambar langsung dari stream pakai PIL (biar ICC dan DPI tetap kejaga)
        file_stream = file.stream
        image_pil = Image.open(file_stream)

        # Backup ICC Profile & DPI jika ada
        icc_profile = image_pil.info.get('icc_profile')
        dpi = image_pil.info.get('dpi', (300, 300))  # fallback default kalau gak ada

        draw = ImageDraw.Draw(image_pil)

        # Tambahkan header
        try:
            header_font = get_font(size=60)
            header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
            header_x = (image_pil.width - (header_bbox[2] - header_bbox[0])) // 2
            header_y = 10
            draw.text((header_x, header_y), header_text, font=header_font, fill=(255, 0, 0))
        except Exception as e:
            print(f"[WARN] Header gagal ditambahkan: {e}")

        # Deteksi objek (harus convert ke numpy RGB dulu untuk masuk ke YOLO)
        detection_model = load_model()
        if detection_model:
            img_rgb = np.array(image_pil.convert("RGB"))
            results = detection_model(img_rgb)
            detections = results.pandas().xyxy[0]

            font_main = get_font(size=min(260, image_pil.width // 5))

            for _, row in detections.iterrows():
                if row['name'] == 'list_nama':
                    xmin, ymin, xmax, ymax = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
                    text_bbox = font_main.getbbox(nama)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    text_x, text_y = calculate_text_position((xmin, ymin, xmax, ymax), (text_width, text_height))
                    draw.text((text_x, text_y), nama, font=font_main, fill=font_color)
                    break
        else:
            print("[WARN] Model tidak tersedia, fallback ke tengah.")
            font_main = get_font(size=100)
            text_bbox = font_main.getbbox(nama)
            text_x = (image_pil.width - (text_bbox[2] - text_bbox[0])) // 2
            text_y = (image_pil.height - (text_bbox[3] - text_bbox[1])) // 2
            draw.text((text_x, text_y), nama, font=font_main, fill=font_color)

        # Buat path berdasarkan waktu
        now = datetime.now()
        month = now.strftime('%B').upper()
        day = now.strftime('%d')
        base_dir = r"D:/assets/PRINT"
        target_dir = os.path.join(base_dir, month, day)
        os.makedirs(target_dir, exist_ok=True)

        existing_files = [f for f in os.listdir(target_dir) if re.match(rf"{prefix}\d+{ext}", f)]
        next_number = max([int(re.findall(rf"{prefix}(\d+){ext}", f)[0]) for f in existing_files], default=0) + 1
        output_filename = f"{prefix}{next_number}{ext}"
        output_path = get_save_path(base_dir=base_dir, filename=output_filename)

        # Simpan dengan ICC Profile & DPI yang sama
        image_pil.save(output_path, format='JPEG', quality=95, dpi=dpi, icc_profile=icc_profile)
        print(f"[✅] Gambar disimpan ke: {output_path} dengan metadata asli")

        # Kirim ke client
        img_bytes = io.BytesIO()
        image_pil.save(img_bytes, format='JPEG', quality=95, dpi=dpi, icc_profile=icc_profile)
        img_bytes.seek(0)
        return send_file(img_bytes, mimetype='image/jpeg', as_attachment=True, download_name=output_filename)

    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500


@image_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Image Processing API is running',
        'model_loaded': model is not None
    })
