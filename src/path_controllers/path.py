import os
import cv2
from datetime import datetime

import numpy as np

# Fungsi bikin folder dan return path lengkap untuk simpan gambar
def get_save_path(base_dir='D:/assets/PRINT', filename='hasil.jpg'):
    # Ambil waktu saat ini
    now = datetime.now()

    # Format nama bulan dalam huruf kapital (e.g. JULI)
    month_name = now.strftime('%B').upper()  # e.g. 'JULI'
    day_number = now.strftime('%d')          # e.g. '04'

    # Gabungkan jadi path
    save_dir = os.path.join(base_dir, month_name, day_number)

    # Kalau belum ada → bikin folder-nya
    os.makedirs(save_dir, exist_ok=True)

    # Path akhir tempat simpan file (misal .jpg)
    final_path = os.path.join(save_dir, filename)
    return final_path

# Contoh: Simpan gambar dummy (buat demo aja)
if __name__ == '__main__':
    # Contoh: Buat gambar putih ukuran 500x500
    dummy_img = 255 * np.ones((500, 500, 3), dtype=np.uint8)

    # Tentuin path simpan otomatis
    output_path = get_save_path(filename='output_test.jpg')

    # Simpan gambar ke sana
    cv2.imwrite(output_path, dummy_img)
    print(f'[✅] Gambar berhasil disimpan di: {output_path}')
