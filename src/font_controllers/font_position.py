# D:/image_processing_api/src/path_controllers/font_position.py

def calculate_text_position(box, text_size):
    """
    Hitung posisi x dan y untuk menempatkan teks di dalam box.
    box: (xmin, ymin, xmax, ymax)
    text_size: (width, height)
    """
    xmin, ymin, xmax, ymax = box
    box_width = xmax - xmin
    box_height = ymax - ymin

    text_width, text_height = text_size

    text_x = xmin + (box_width - text_width) // 2
    text_y = ymin + (box_height - text_height) // 2.5  # Bisa disesuaikan manual

    return int(text_x), int(text_y)
