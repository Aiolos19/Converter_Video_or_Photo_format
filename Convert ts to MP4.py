import os
import subprocess

# Direktori tempat file .ts berada
input_directory = r'D:\Converter'

# Fungsi untuk mengonversi file .ts ke .mp4
def convert_ts_to_mp4(input_ts_file, output_mp4_file):
    try:
        command = [
            'ffmpeg',
            '-hwaccel', 'cuda',
            '-err_detect', 'ignore_err',
            '-i', input_ts_file,
            '-c:v', 'h264_nvenc',
            '-preset', 'fast',
            '-b:v', '3M',
            '-c:a', 'aac',
            '-b:a', '128k',
            output_mp4_file
        ]
        
        # Jalankan perintah ffmpeg
        subprocess.run(command, check=True)
        print(f"Konversi selesai: {input_ts_file} -> {output_mp4_file}")
    
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat mengonversi {input_ts_file}: {e}")

# Fungsi untuk menemukan dan mengonversi semua file .ts di direktori
def batch_convert_ts_to_mp4(directory):
    # Loop melalui semua file di direktori
    for filename in os.listdir(directory):
        if filename.endswith('.ts'):
            input_ts_file = os.path.join(directory, filename)
            output_mp4_file = os.path.join(directory, filename.replace('.ts', '.mp4'))
            convert_ts_to_mp4(input_ts_file, output_mp4_file)
        else:
            print(f"File sudah mp4: {filename}")

# Jalankan fungsi batch konversi
batch_convert_ts_to_mp4(input_directory)