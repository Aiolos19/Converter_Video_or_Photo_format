import os
from PIL import Image

# Direktori tempat gambar berada
input_directory = r'D:\Converter'

# Fungsi untuk mengonversi gambar apapun ke .jpg atau .png
def convert_image_to_format(input_image_file, output_format='jpg'):
    try:
        # Buka gambar
        with Image.open(input_image_file) as img:
            base_filename = os.path.splitext(input_image_file)[0]
            output_image_file = f"{base_filename}.{output_format}"

            if output_format == 'jpg':
                img = img.convert('RGB')
            
            # Simpan file dalam format baru
            img.save(output_image_file, format=output_format.upper())
            print(f"Konversi selesai: {input_image_file} -> {output_image_file}")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat mengonversi {input_image_file}: {e}")

# Fungsi untuk menemukan dan mengonversi semua file gambar di direktori
def batch_convert_images(directory, output_format='jpg'):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            input_image_file = os.path.join(directory, filename)
            convert_image_to_format(input_image_file, output_format)

# Jalankan fungsi batch konversi
batch_convert_images(input_directory, 'jpg')  # Ganti 'jpg' dengan 'png'
