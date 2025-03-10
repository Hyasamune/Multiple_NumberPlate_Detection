import cv2 as cv
import easyocr
import re
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import os
import time
from io import BytesIO

ocr_results_path = r'G:/pengujian 5 deteksi/baru/new dataset/Pengujian/detection plat putih hitam/streamlit testing'
detected_texts_file = os.path.join(ocr_results_path, 'detected_texts.txt')
detection_results_file = os.path.join(ocr_results_path, 'detection_results.txt')
ocr_log_file_path = r'G:/pengujian 5 deteksi/baru/new dataset/Pengujian/detection plat putih hitam/streamlit testing/ocr_results_log.txt'
cropped_images_folder = r'G:/pengujian 5 deteksi/baru/new dataset/Pengujian/detection plat putih hitam/streamlit testing/seluruh sub crop image window'
output_path = "G:/pengujian 5 deteksi/baru/new dataset/Pengujian/detection plat putih hitam/streamlit testing/hasil preprocessing.png"

def loadImage(imgPath, width = 2000, height = 1124):
    image = cv.imread(imgPath)
    image = cv.resize(image,(width, height))
    return image

def processGrayscale(image):
    height = len(image)
    width = len(image[0])
    grayscale_image = np.zeros((height, width), dtype=np.uint8)  # Initialize NumPy array

    for y in range(height):
      for x in range(width):
        r, g, b = image[y][x]
        grayscale_value = (int(r) + int(g) + int(b)) // 3

        grayscale_image[y][x] = grayscale_value

    return grayscale_image

kernels = [
    np.array((
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1]), dtype="int"),
    np.array((
    [1, 1, 1],
    [1, -8, 1],
    [1, 1, 1]), dtype="int"),
]

def applyConvolution(image , kernel) :
  returnImage = image.copy()
  image = cv.copyMakeBorder(image, 1, 1, 1, 1, cv.BORDER_CONSTANT, value=255)

  (iH, iW) = image.shape[:2]
  for iy in range(1,iH-1) :
    for ix in range(1,iW-1) :
      result = image[iy-1][ix-1]*kernel[2][2] + image[iy-1][ix]*kernel[2][1] +image[iy-1][ix+1]*kernel[2][0] +\
               image[iy][ix-1]*kernel[1][2] + image[iy][ix]*kernel[1][1] +image[iy][ix+1]*kernel[1][0] +\
               image[iy+1][ix-1]*kernel[0][2] + image[iy+1][ix]*kernel[0][1] +image[iy+1][ix+1]*kernel[0][0]
      result = max(0, min(255, result))
      returnImage[iy-1][ix-1] = result
  return returnImage

def processThreshold(image, threshold):
    height = len(image)
    width = len(image[0])
    threshold_image = np.zeros((height, width), dtype=np.uint8)  # Initialize NumPy array

    for y in range(height):
      for x in range(width):
            threshold_image[y][x] = 128 if image[y][x] < threshold else 255

    return threshold_image

def find_starting_points(image, threshold=128):
    height, width = image.shape
    starting_points = []  # List untuk menyimpan titik awal yang memiliki nilai threshold
    for y in range(height):
        for x in range(width):
            if image[y, x] == threshold:
                starting_points.append((x, y))  # Menyimpan titik yang ditemukan
    return starting_points

def backtrack_fill(image, threshold, min_pixel, max_pixel):
    """
    Perform backtracking and fill regions based on pixel values and pixel count.
    :param image: Input binary image (numpy array)
    :param x: x-coordinate of the starting point
    :param y: y-coordinate of the starting point
    :param threshold: Pixel threshold (value at which the region is considered for processing)
    :param min_pixel: Minimum pixel count for an area to be filled with black (0)
    :param max_pixel: Maximum pixel count for an area to be filled with black (0)
    :return: Processed image
    """
    height, width = image.shape
    filled_image = image.copy()  # Copy image to apply fill operations
    visited = np.zeros_like(image, dtype=bool)  # To mark visited pixels during backtracking

    def backtrack_fill_recursive(x, y):
        # Check if current position is within bounds and not visited
        if x < 0 or x >= width or y < 0 or y >= height or visited[y, x]:
            return

        # Mark the current pixel as visited
        visited[y, x] = True

        # If the pixel has a value of 128, process it
        if image[y, x] == threshold:
            # Start counting the pixels in the region (use a stack for backtracking)
            region_pixels = []  # List to store coordinates of pixels in the region
            stack = [(x, y)]
            while stack:
                cx, cy = stack.pop()
                # Add current pixel to region
                region_pixels.append((cx, cy))
                
                # Check the neighboring pixels (up, down, left, right)
                for nx, ny in [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]:
                    if 0 <= nx < width and 0 <= ny < height and not visited[ny, nx] and image[ny, nx] == threshold:
                        stack.append((nx, ny))
                        visited[ny, nx] = True
            
            # Now check the number of pixels in the region and set accordingly
            pixel_count = len(region_pixels)
            if min_pixel <= pixel_count <= max_pixel:
                # Debugging: Tampilkan informasi region
                # print(f"Region found with {pixel_count} pixels, filling with black.")
                for px, py in region_pixels:
                    filled_image[py, px] = 0
            else:
                # Debugging: Tampilkan informasi region
                # print(f"Region found with {pixel_count} pixels, filling with white.")
                for px, py in region_pixels:
                    filled_image[py, px] = 255

    # Menemukan semua titik dengan nilai threshold (128)
    for sx, sy in find_starting_points(image, threshold):
        backtrack_fill_recursive(sx, sy)

    return filled_image

# Inisialisasi session_state jika belum ada
if "y1" not in st.session_state:
    st.session_state.y1 = 0
if "y2" not in st.session_state:
    st.session_state.y2 = 150

if "filled_image" not in st.session_state:
    st.session_state.filled_image = None  # Inisialisasi filled_image
if "coordinates_list" not in st.session_state:
    st.session_state.coordinates_list = []  # List untuk menyimpan koordinat

# Fungsi untuk gambar bounding box
def draw_bounding_box(image, y1, y2):
    img_copy = image.copy()
    img_copy = cv.cvtColor(img_copy, cv.COLOR_GRAY2BGR)
    cv.rectangle(img_copy, (0, y1), (img_copy.shape[1], y2), (0, 255, 0), 2)
    return img_copy

# Fungsi validasi format plat nomor Indonesia
def validate_plate_format(text):
    pattern = r'^[A-Za-z]{1,2}\s{0,5}\d{1,4}(\s{0,3}\d{1,4})?\s{0,5}[A-Za-z]{1,3}(\s?\d{1,2}\s{0,2}\.\s{0,2}?\d{1,2})?' # Pola sederhana untuk plat nomor
    return re.match(pattern, text) is not None

reader = easyocr.Reader(['en'])  # Anda bisa menambahkan bahasa lain, misalnya ['en', 'id']
 
# Fungsi OCR dengan menggunakan easyocr
def OCR(image):
    # Gunakan EasyOCR untuk membaca teks dari gambar
    ocr_results = reader.readtext(image, detail=0)  # Mengembalikan teks langsung, tanpa detail posisi
    text = " ".join([result.strip() for result in ocr_results])  # Gabungkan teks jika ada beberapa baris
    return text

# Fungsi untuk menyimpan hasil deteksi
def save_detection_results(detected_plates, detection_file_path, texts_file_path):
    with open(detection_file_path, 'w') as detection_file, open(texts_file_path, 'w') as texts_file:
        for plate_info in detected_plates:
            detection_file.write(f"OCR Text: {plate_info['text']}\nCoordinates: ({plate_info['x1']}, {plate_info['y1']}), ({plate_info['x2']}, {plate_info['y2']})\n\n")
            texts_file.write(f"{plate_info['text']}\n")
            # Memastikan semua hasil langsung disimpan ke file tanpa buffer
            detection_file.flush()
            texts_file.flush()

def save_ocr_result(text, texts_file_path):
    with open(texts_file_path, 'a') as texts_file:
        texts_file.write(f"{text}\n")
        texts_file.flush()  # Langsung simpan ke file

# Fungsi untuk menyimpan log hasil OCR ke dalam file log
def save_ocr_log(ocr_result, window_size, coords, log_file_path):
    """
    Simpan hasil OCR beserta ukuran window dan koordinatnya ke dalam file log.
    """
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"OCR Result: '{ocr_result}' at window size {window_size} and coordinates {coords}\n")
        log_file.flush()  # Langsung simpan ke file tanpa buffer

# Modifikasi fungsi resize_window untuk menyimpan setiap cropped image
def save_cropped_image(cropped_image, x, y, width, height):
    """
    Save the cropped image to the specified folder with a unique filename based on coordinates.
    """
    file_name = f'cropped_window_{x}_{y}_{width}x{height}.png'
    file_path = os.path.join(cropped_images_folder, file_name)
    
    # Menyimpan cropped image sebagai file PNG
    cv.imwrite(file_path, cropped_image)
    # print(f'Saved cropped image at {file_path}')

# Fungsi untuk memperbesar ukuran window dan mengembalikan koordinat serta hasil OCR
def resize_window(image, x, y, initial_width, initial_height, max_window_size, scale_height=1.4, scale_width=1.75):
    width, height = initial_width, initial_height

    # Menghitung 1/4 perlebaran dari ukuran window
    width_expansion = max_window_size[0] - initial_width  # Total perlebaran lebar
    height_expansion = max_window_size[1] - initial_height  # Total perlebaran tinggi

    # 1/4 dari total perlebaran
    quarter_width = width_expansion / 4
    quarter_height = height_expansion / 4

    # Loop untuk memperbesar ukuran window hingga salah satu dimensi mencapai batas maksimal
    while width < max_window_size[0] or height < max_window_size[1]:
        x2 = min(x + width, image.shape[1])
        y2 = min(y + height, image.shape[0])

        # Crop area gambar sesuai ukuran window saat ini
        cropped_image = image[y:y2, x:x2]

        # Check if the cropped image is empty
        if cropped_image.size == 0: 
            print(f"Invalid cropped image at coordinates ({x}, {y}), skipping...") 
            return None, None, None

        # Save the cropped image
        save_cropped_image(cropped_image, x, y, width, height)

        # setiap cropped_image akan langsung menerapkan OCR
        ocr_result = OCR(cropped_image)
        print(f"OCR Result: '{ocr_result}' at window size ({width}x{height})")

        # Simpan hasil OCR ke dalam file log
        save_ocr_log(ocr_result, (width, height), (x, y, x2, y2), ocr_log_file_path)

        save_ocr_result(ocr_result, detected_texts_file)

        # Validasi hasil OCR untuk memastikan formatnya sesuai dengan plat nomor
        if ocr_result and validate_plate_format(ocr_result):
            return cropped_image, (x, y, x2, y2), ocr_result

        # Jika sudah mencapai 1/4 dari total perlebaran dan tidak ditemukan karakter, geser window
        if width >= initial_width + quarter_width and height >= initial_height + quarter_height:
            # Cek apakah tidak ada karakter yang ditemukan
            if ocr_result == '':
                print(f"No character found at window size ({width}x{height}), moving to the next window.")
                return None, None, None  # Geser window jika tidak ada karakter

        # Perbesar ukuran window dengan skala
        if width < max_window_size[0] and height < max_window_size[1]:
            # Perbesar lebar dan tinggi jika keduanya belum mencapai batas
            width = int(width * scale_width)
            height = int(height * scale_height)
        elif width >= max_window_size[0] and height < max_window_size[1]:
            # Jika lebar sudah mencapai batas maksimal, hanya perbesar tinggi
            height = int(height * scale_height)
        elif height >= max_window_size[1] and width < max_window_size[0]:
            # Jika tinggi sudah mencapai batas maksimal, hanya perbesar lebar
            width = int(width * scale_width)

    return None, None, None

# Fungsi untuk menampilkan dan menyimpan hasil deteksi
def display_and_save_detection(image, coords, ocr_result):
    x1, y1, x2, y2 = coords
    plate_info = {
        'x1': x1, 'y1': y1,
        'x2': x2, 'y2': y2,
        'text': ocr_result
    }

    # Gambarkan kotak hijau di sekitar plat nomor yang terdeteksi
    image_with_rectangle = image.copy()
    image_with_rectangle = cv.cvtColor(image_with_rectangle, cv.COLOR_GRAY2RGB)
    cv.rectangle(image_with_rectangle, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Menggambar kotak hijau

    return plate_info

# Function to save and draw final bounding boxes on the image
def save_final_detections(image, detected_plates):
    final_image = image.copy()
    final_image = cv.cvtColor(final_image, cv.COLOR_GRAY2RGB)  # Convert to RGB for displaying colored rectangles
    for plate_info in detected_plates:
        x1, y1, x2, y2 = plate_info['x1'], plate_info['y1'], plate_info['x2'], plate_info['y2']
        cv.rectangle(final_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box in green
        cv.putText(final_image, plate_info['text'], (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return final_image  # Return the image with bounding boxes

# Main function to process license plate detection using sliding window
def process_plate_detection_opt(image, start_coords):
    x1, y1, x2, y2 = start_coords
    initial_window_size = (60, 25)  # Initial window size (width x height)
    max_window_size = (180, 50)     # Maximum window size (width x height)
    detected_plates = []

    # Pastikan untuk tidak melewati batas y2 dan x2 dari area pemilihan
    x = x1  # Mulai dari y1
    while x <= x2 - initial_window_size[1]:  # Pastikan tidak melewati batas
        y = y1  # Mulai dari x1
        while y <= y2 - initial_window_size[0]:  # Pastikan tidak melewati batas
            # Resize window and perform OCR on a specific area
            _, coords, ocr_result = resize_window(image, x, y, initial_window_size[0], initial_window_size[1], max_window_size)

            if coords and ocr_result:
                # Display OCR result and coordinates in the console
                print(f"Detected Plate: {ocr_result} at coordinates {coords}")
                
                # If OCR is successful and valid, save detection result
                plate_info = display_and_save_detection(image, coords, ocr_result)
                detected_plates.append(plate_info)

                # Loncat ke posisi setelah bounding box yang terdeteksi
                x = coords[2]  # Mengatur x ke x2 dari bounding box
                y = coords[1]  # Kembali ke y1 untuk baris berikutnya
            else:
                # Move y position to the down if no plate is detected
                y += initial_window_size[1]

        # Setelah selesai memindai vertikal, geser window ke kanan atas
        x += initial_window_size[0]//2
    
    if detected_plates:
        final_image_with_boxes = save_final_detections(image, detected_plates)  # Get final image with bounding boxes

        # Display the final image with bounding boxes
        st.image(final_image_with_boxes, caption="Hasil Deteksi Plat Nomor", channels="RGB", use_container_width=True)

    print("Proses deteksi selesai.")
    return np.array(detected_plates)  # Return numpy array of detection results

# Streamlit UI
st.title("Deteksi Plat")

uploaded_file = st.file_uploader("Upload Gambar", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Simpan gambar sementara di folder lokal
    image_path = "uploaded_image.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Muat gambar menggunakan fungsi loadImage
    image = loadImage(image_path)

    # Tampilkan gambar asli
    st.image(image, caption="Gambar Asli", channels="BGR", use_container_width=True)

    plate_type = st.radio("Pilih Jenis Plat Nomor:", options=["Putih", "Hitam"])

    if st.button("Lakukan Preprocessing"):
        # Preprocess the image: convert to grayscale
        gray_image = processGrayscale(image)

        # Proses berdasarkan jenis plat
        if plate_type == "Putih":
            # st.write("Deteksi untuk plat putih sedang berjalan...")
            # Edge detection untuk plat putih
            edge_detect_putih = applyConvolution(gray_image, kernels[0])
            # Clip pixel values to [0, 255]
            edge_detect_putih = np.clip(edge_detect_putih, 0, 255)

            # Thresholding untuk plat putih
            threshold_value_putih = 25  # You can adjust this value based on your image
            threshold_image_putih = processThreshold(edge_detect_putih, threshold_value_putih)

            # Backtracking untuk segmentasi
            filled_image_putih = backtrack_fill(threshold_image_putih, threshold=128, min_pixel=30, max_pixel=210)

            # Simpan gambar
            cv.imwrite(output_path, filled_image_putih)
            print(f"Gambar telah disimpan di {output_path}")

            # Simpan ke session_state dan tampilkan
            st.session_state.filled_image = filled_image_putih
            st.image(filled_image_putih, caption="Hasil Preprocessing Plat Putih", use_container_width=True)

        elif plate_type == "Hitam":
            # st.write("Deteksi untuk plat hitam sedang berjalan...")
            # Edge detection untuk plat hitam
            edge_detect_hitam = applyConvolution(gray_image, kernels[1])
            # Clip pixel values to [0, 255]
            edge_detect_hitam = np.clip(edge_detect_hitam, 0, 255)

            # Thresholding untuk plat hitam
            threshold_value_hitam = 25  # You can adjust this value based on your image
            threshold_image_hitam = processThreshold(edge_detect_hitam, threshold_value_hitam)

            # Backtracking untuk segmentasi
            filled_image_hitam = backtrack_fill(threshold_image_hitam, threshold=128, min_pixel=30, max_pixel=520)

            # Simpan gambar
            cv.imwrite(output_path, filled_image_hitam)
            print(f"Gambar telah disimpan di {output_path}")

            # Simpan ke session_state dan tampilkan
            st.session_state.filled_image = filled_image_hitam
            st.image(filled_image_hitam, caption="Hasil Preprocessing Plat Hitam", use_container_width=True)

    # Menampilkan slider untuk menggeser window
    st.subheader("Sliding Window Selection")

    # Fungsi untuk mengubah y2 agar bergerak bersama dengan y1
    def adjust_y2_based_on_y1(y1_value):
        return y1_value + 150  # Misalnya, selisih y2 - y1 selalu 150

    # Slider untuk y1, nilai akan ditambah atau dikurangi 5 setiap langkahnya
    st.session_state.y1 = st.slider(
        "Posisi",
        min_value=0,
        max_value=image.shape[0] - 150,  # Sesuaikan dengan tinggi gambar dan selisih antara y1 dan y2
        value=st.session_state.y1,
        step=5,  # Langkah 5 setiap perubahan
    )

    # Perbarui y2 sesuai dengan nilai y1
    st.session_state.y2 = adjust_y2_based_on_y1(st.session_state.y1)

    # Menampilkan koordinat
    st.write(f"Koordinat Y1: {st.session_state.y1}, Y2: {st.session_state.y2}")

    # Tombol untuk menyimpan koordinat
    if st.button("Simpan Koordinat"):
        coords = (st.session_state.y1, st.session_state.y2)
        st.session_state.coordinates_list.append(coords)
        st.write(f"Koordinat tersimpan: {coords}")

    if st.session_state.filled_image is not None:
        img_with_box = draw_bounding_box(st.session_state.filled_image, st.session_state.y1, st.session_state.y2)
        img_with_box_rgb = cv.cvtColor(img_with_box, cv.COLOR_BGR2RGB)
        st.image(img_with_box_rgb, caption="Sliding Window Preview", use_container_width=True)
    else:
        st.write("No image available to draw bounding box.")

    # Tampilkan list koordinat yang telah disimpan
    st.write("Koordinat yang telah disimpan:")
    st.write(st.session_state.coordinates_list)

# Tombol untuk melakukan deteksi plat nomor
if st.session_state.get("filled_image") is not None and st.button("Deteksi Plat Nomor"):
    start_coords = (0, st.session_state.y1, st.session_state.filled_image.shape[1], st.session_state.y2)
    # Mulai pencatatan waktu
    start_time = time.time()
    
    detected_plates = process_plate_detection_opt(st.session_state.filled_image, start_coords)

    # Selesai pencatatan waktu
    end_time = time.time()

    # Hitung dan tampilkan waktu proses
    processing_time = end_time - start_time
    print(f"Waktu proses sliding window deteksi: {processing_time:.2f} detik")

    save_detection_results(detected_plates, detection_results_file, detected_texts_file)

    if detected_plates.size > 0:
        # Tampilkan hasil deteksi dengan bounding box
        save_final_detections(st.session_state.filled_image, detected_plates)

        # Tampilkan teks hasil OCR
        st.subheader("Hasil OCR")
        for plate_info in detected_plates:
            st.write(f"Text: {plate_info['text']}")
            st.write(f"Coordinates: ({plate_info['x1']}, {plate_info['y1']}), ({plate_info['x2']}, {plate_info['y2']})")

        # # Opsi unduhan hasil
        # download_btn = st.download_button(
        #     label="Unduh Hasil Deteksi",
        #     data=f"Hasil OCR dan bounding box: {detected_plates}",
        #     file_name="hasil_deteksi.txt",
        #     mime="text/plain"
    else:
        st.write("Tidak ada plat nomor yang terdeteksi.")