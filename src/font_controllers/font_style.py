# D:/image_processing_api/src/path_controllers/font_style.py

from PIL import ImageFont

# Default path font (bisa diganti kapan aja)
FONT_PATH = "C:/Windows/Fonts/Arial.ttf"
EMOJI_FONT_PATH = "C:/Windows/Fonts/seguiemj.ttf"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception as e:
        print(f"[ERROR] Font gagal dimuat: {e}")
        raise

def get_emoji_font(size: int):
    try:
        return ImageFont.truetype(EMOJI_FONT_PATH, size)
    except Exception as e:
        print(f"[ERROR] Emoji font gagal dimuat: {e}")
        raise















































