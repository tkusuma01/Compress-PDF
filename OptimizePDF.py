import fitz  # PyMuPDF
import os
import time

def compress_pdf(input_pdf):
    try:
        # Membuka dokumen PDF
        pdf_document = fitz.open(input_pdf)

        # Menentukan nama file output sementara dengan tambahan "_r1"
        base, ext = os.path.splitext(input_pdf)
        temp_output = f"{base}_r1{ext}"

        # Menyimpan file dengan nama sementara
        pdf_document.save(
            temp_output,
            garbage=4,  # Membersihkan objek yang tidak digunakan
            deflate=True,  # Menggunakan kompresi deflate
        )
        pdf_document.close()

        # Hapus file asli
        os.remove(input_pdf)

        # Ganti nama file hasil kompresi menjadi nama file asli
        os.rename(temp_output, input_pdf)

    except Exception as e:
        print(f"File corrupt atau terjadi kesalahan pada file: {input_pdf}")
        print(f"Kesalahan: {e}")
        try:
            # Hapus file corrupt
            os.remove(input_pdf)
            print(f"File corrupt dihapus: {input_pdf}")
        except Exception as delete_error:
            print(f"Gagal menghapus file corrupt: {delete_error}")

def process_pdfs(input_path):
    # Kumpulkan semua file PDF yang akan diproses
    pdf_files = []
    if os.path.isfile(input_path):  # Jika input adalah file tunggal
        pdf_files = [input_path]
    elif os.path.isdir(input_path):  # Jika input adalah folder
        for root, _, files in os.walk(input_path):  # Proses semua subfolder
            for file in files:
                if file.lower().endswith(".pdf"):  # Hanya file PDF
                    pdf_files.append(os.path.join(root, file))

    total_files = len(pdf_files)
    if total_files == 0:
        print("Tidak ada file PDF yang ditemukan untuk diproses.")
        return

    start_time = time.time()

    # Proses file satu per satu
    for idx, pdf_file in enumerate(pdf_files, start=1):
        print(f"[{idx}/{total_files}] Memproses file: {pdf_file}")
        compress_pdf(pdf_file)

        # Hitung progres dan waktu yang tersisa
        elapsed_time = time.time() - start_time
        avg_time_per_file = elapsed_time / idx
        remaining_files = total_files - idx
        estimated_time_left = remaining_files * avg_time_per_file

        # Tampilkan status
        progress_percent = (idx / total_files) * 100
        print(f"Progres: {progress_percent:.2f}%")
        print(f"Perkiraan waktu tersisa: {estimated_time_left:.2f} detik")

    print("Proses selesai!")

def main():
    print("=== PDF Compressor dengan Deteksi File Corrupt ===")
    input_path = input("Masukkan path file atau folder PDF: ").strip()
    
    if not os.path.exists(input_path):
        print("File atau folder tidak ditemukan. Pastikan path benar.")
        return

    process_pdfs(input_path)

if __name__ == "__main__":
    main()