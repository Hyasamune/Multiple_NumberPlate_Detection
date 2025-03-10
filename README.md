# Multiple_NumberPlate_Detection


# **USER MANUAL PENGGUNAAN APLIKASI DETEKSI MULTIPLE PLAT NOMOR PADA CITRA KENDARAAN**


# <a name="_toc192543087"></a>**Daftar Isi**
[Daftar Isi	1****](#_toc192543087)**

[**Deskripsi	2****](#_toc192543088)

[**Syarat & Ketentuan	3****](#_toc192543089)

[**Alur Kerja Aplikasi	4****](#_toc192543090)

[**Download & Instalasi	5****](#_toc192543091)

[**Tahap 1 *Source Code*	5****](#_toc192543092)

[**Tahap 2 Dependensi	9****](#_toc192543093)

[**Tahap 3 *Run*	11****](#_toc192543094)

[**Tahap 4 Penggunaan	13****](#_toc192543095)
# **
# <a name="_toc192541693"></a><a name="_toc192543088"></a>**Deskripsi**
![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.001.png)
**
`	`Aplikasi ini digunakan untuk mendeteksi beberapa plat nomor dalam satu gambar, dengan jumlah 3 hingga 5 plat nomor pada kendaraan. Aplikasi ini akan memberikan output berupa :

1. seluruh hasil kotak penemuan/*bounding box* yang menandai plat nomor yang terdeteksi.
1. teks karakter yang ditemukan dari hasil OCR.
1. koordinat plat nomor ditemukan dalam gambar.

`	`Untuk melakukan deteksi pada aplikasi ini menggunakan metode *sliding window* untuk mencari dan memindai seluruh area dari gambar untuk menemukan plat nomor. Proses ini diawali dengan pemilihan area awal yang digunakan sebagai titik referensi awal bagi *sliding window* untuk melakukan pencarian. Metode ini juga dibantu dengan OCR (*Optical Character Recognition*) untuk mengenali karakter yang ditemukan dan karakter tersebut akan divalidasi dengan pola plat nomor Indonesia, sehingga hanya karakter yang sesuai dengan format plat nomor yang dianggap valid.

`	`Aplikasi ini dikembangkan dengan menggunakan *python* dan *streamlit*, dengan memanfaatkan beberapa library untuk melakukan proses penyimpanan, deteksi, pengenalan karakter, dan validasi. Library yang digunakan berupa :

1. *OpenCV* – untuk melakukan load dan pemrosesan gambar.
1. *Re* – untuk validasi karakter dengan pola plat nomor Indonesia.
1. *Numpy* – untuk manipulasi array dalam pemrosesan gambar
1. *easyOCR* – untuk pengenalan karakter dari plat nomor.
1. *streamlit* – untuk membangun antarmuka berbasis web.
1. *os* – untuk manajemen file dan akses sistem.

`	`Keunggulan utama pada aplikasi ini adalah kemampuannya dalam mendeteksi beberapa plat nomor dalam satu gambar, dengan adanya variasi posisi dan ukuran dari plat nomor. Diharapkan aplikasi ini dapat membantu dalam proses deteksi plat nomor, terutama dalam skenario di mana terdapat banyak plat nomor dalam satu gambar.
# <a name="_toc192541694"></a><a name="_toc192543089"></a>**Syarat & Ketentuan**
1. Fungsi Aplikasi
- Aplikasi ini dirancang khusus untuk mendeteksi plat nomor kendaraan dalam sebuah gambar.
- Jumlah plat nomor yang dapat dideteksi dalam satu gambar berkisar antara 3 hingga 5 plat nomor.
1. Batasan Deteksi
- Aplikasi ini hanya mendukung deteksi plat nomor kendaraan umum di Indonesia, yaitu plat hitam dan putih, yang harus dipilih secara manual sebelum proses deteksi
1. Penyesuaian Penggunaan
- Jika aplikasi digunakan pada gambar kendaraan dan plat nomor asli, penyesuaian pada *preprocessing* mungkin diperlukan.
- Nilai parameter pada *preprocessing*, seperti *thresholding* dan *fill color* mungkin perlu disesuaikan kembali untuk mengoptimalkan hasil segmentasi.
1. Penggunaan Aplikasi
- Aplikasi ini berjalan menggunakan *python* dan memerlukan instalasi dependensi tertentu sebelum digunakan.
# <a name="_toc192541695"></a><a name="_toc192543090"></a>**Alur Kerja Aplikasi**
![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.002.png)	Gambar diatas ini merupakan alur kerja dari aplikasi untuk melakukan deteksi beberapa plat nomor kendaraan dalam satu gambar.

1. Aplikasi dimulai dengan penggunakan membuka aplikasi.
1. Pengguna perlu melakukan upload gambar.
1. Setelah upload gambar, pengguna memilih warna plat nomor yang ingin dideteksi.
1. Lalu setelah melakukan pemilihan warna plat nomor, pengguna menekan tombol *preprocessing* untuk melakukan proses *preprocessing* gambar.
1. Lalu, pengguna perlu mengatur *slider* untuk memposisikan area awal *sliding window* akan dimulai.
1. Setelah mengatur *slider*, pengguna harus menyimpan koordinat tersebut sebagai area awal dari *sliding window*.
1. Setelah menyimpan koordinatnya, pengguna menekan tombol deteksi untuk melakukan proses deteksi plat nomor.
1. Aplikasi akan menampilkan hasilnya setelah proses dari deteksi plat nomor selesai.
# <a name="_toc192541696"></a><a name="_toc192543091"></a>**Download & Instalasi**
**	Untuk dapat menggunakan aplikasi ini, perlu mengikuti beberapa tahapan yang dimulai dari *source code*, dependensi, *run*, dan penggunaan. Untuk penjelasan yang lebih lengkap ada dibawah ini.
## <a name="_toc192541697"></a><a name="_toc192543092"></a>**Tahap 1 *Source Code***
`	`Untuk dapat menggunakan aplikasi ini, diperlukan untuk mengunduh *source code*, di mana pada tahapan ini akan mendapatkan folder berupa *source code* aplikasi. Untuk mendapatkan file *source code* dengan cara, sebagai berikut :

1. Dengan melakukan download *source code*, di mana file folder tersebut didapati dari  membuka link <https://github.com/Hyasamune/Multiple_NumberPlate_Detection>.
1. Klik tombol “*code*” yang berwarna hijau, yang dapat dilihat dari gambar dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.003.png)

1. Lalu, klik tombol “Download ZIP” yang telah diberikan kotak merah, yang dapat dilihat pada gambar dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.004.png)

1. Hasil download file zip dengan nama “Multiple\_NumberPlate\_Detection-main.zip” dilakukan ekstraksi dengan klik kiri file zipnya dan klik kanan file tersebut. Setelah itu melakukan klik kanan, akan terlihat menu dari *right click menu* yang dapat dilihat pada gambar dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.005.png)

1. Pada menu terdapat empat pilihan tersebut untuk melakukan ekstraksi. Pilihan pertama dengan membuka WinRAR untuk melakukan ekstraksi, pilihan kedua dengan langsung melakukan ekstrak file dan dapat memilih penyimpanan hasil ekstraksi ke director yang diinginkan, pilihan ketiga dengan melakukan ekstrak file pada satu folder yang sama dengan file zip, dan pilihan keempat dengan membuat folder baru dan menyimpan hasil ekstraksi pada folder tersebut, di mana dapat dilihat pada gambar dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.006.png)

1. Setelah melakukan ekstraksi, copy path direktori folder, contoh : F:\ekstrak zip\Multiple\_NumberPlate\_Detection-main. Lalu, pada *command prompt* atau terminal masukkan direktori folder tersebut dengan menulis cd path direktori folder, contoh : cd F:\ekstrak zip\Multiple\_NumberPlate\_Detection-main. Di mana gambar dapat dilihat dibawah ini.


![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.007.png)

1. Selain melewati *command prompt* atau terminal, dapat juga dengan menggunakan *vs code* dengan cara klik file dan klik open folder. Lalu, pilih folder file dari hasil ekstraksi tersebut. Di mana gambar dapat dilihat dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.008.png)

1. Tahap selanjutnya ke instalasi dependensi pada bagian dependensi.


## <a name="_toc192541698"></a><a name="_toc192543093"></a>**Tahap 2 Dependensi**
`	`Pada tahapan ini merupakan proses lanjutan dari bagian *source code*. Jika sudah mendapatkan folder *source code*, dapat dilanjutkan ke tahapan berikut ini :

1. Pastikan pada perangkat memiliki python, dengan cara pengecekan pada *command prompt* atau pada terminal di *vs code* yang dapat dilihat pada gambar dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.009.png)

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.010.png)

Jika belum ada python, maka perlu install python melewati link <https://www.python.org/downloads/>

1. Setelah itu lakukan instal dependensi dari requirements.txt, yang dapat dilakukan dengan menggunakan *command prompt* atau terminal dari *vs code*. Di mana gambar dapat dilihat dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.011.png)

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.012.png)

1. Selanjutnya adalah menjalankan aplikasi di bagian *run*.


## <a name="_toc192541699"></a><a name="_toc192543094"></a>**Tahap 3 *Run***
`	`Pada tahap ini merupakan tahapan untuk menjalankan aplikasi dengan cara :

1. Jalankan perintah streamlit run "path file direktori" untuk menjalankan streamlit, contoh : streamlit run "F:\ekstrak zip\Multiple\_NumberPlate\_Detection-main\streamlit peraga skripsi plat putih atau hitam.py", yang dapat ditulis pada *command prompt* atau terminal pada *vs code*. Saat perintah tersebut dijalankan, maka aplikasi akan terbuka di browser dengan menggunakan *local* URL atau *network* URL. URL* ini digunakan untuk mengakses aplikasi streamlit melalui browser, yang dapat dilihat pada gambar dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.013.png)

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.014.png)

1. *Local* URL atau *Network* URL* ini juga dapat di klik atau di copy, untuk mengakses aplikasi streamlit di browser baru atau membukanya kembali aplikasi streamlit. Di mana aplikasi akan terbuka dengan menunjukkan antarmuka pada web. Di mana dapat dilihat pada gambar dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.015.png)

1. Penjelasan penggunaan aplikasi dapat dilihat pada bagian penggunaan.


## <a name="_toc192541700"></a><a name="_toc192543095"></a>**Tahap 4 Penggunaan**
`	`Pada tahapan ini akan menjelaskan penggunaan aplikasi untuk mendeteksi plat nomor kendaraan, sebagai berikut :

1. Saat aplikasi terbuka, akan menunjukkan antarmuka web. Pada bagian ini terdapat antarmuka untuk upload gambar dengan cara klik “*browse files*” atau bisa juga dengan melakukan “*drag and drop*”, yang dapat dilihat pada gambar dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.016.png)

1. Setelah melakukan upload gambar, maka antarmuka lainnya akan terlihat. Di mana selanjutnya, lakukan pemilihan warna plat nomor yang ingin dilakukan deteksi yaitu plat berwarna putih atau plat berwarna hitam. Setelah itu melakukan pemilihan, dapat dilanjutkan proses *preprocessing* dengan melakukan klik tombol “lakukan *preprocessing*”. Pemilihan warna plat nomor dan proses *preprocessing* dapat dilihat pada kotak merah, di mana gambar dapat dilihat dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.017.png)

1. Setelah melakukan proses *preprocessing*, hasil *preprocessing* akan diperlihatkan. Setelah itu, lakukan pemilihan area awal *sliding window* dengan menggeser posisi *slider* yang dapat dilihat pada kotak warna merah. Lalu, hasil pemilihan area awal akan diperlihatkan dengan kotak berwarna hijau yang berada pada gambar hasil *preprocessing*, yang berarti *sliding window* akan melakukan pemindaian hanya pada area yang didalam kotak berwarna hijau. Jika koordinat pemilihan area awal sudah cocok, maka klik “simpan koordinat” untuk menyimpan koordinat dari pemilihan area awal yang telah dipilih dan akan diperlihatkan koordinat yang dismpan pada kotak berwarna biru. Gambar dapat dilihat dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.018.png)

1. Jika sudah menyimpan koordinat, dapat dilakukan untuk deteksi plat nomor dengan klik tombol “deteksi plat nomor”. Hasil dari deteksi akan menampilkan hasil outputnya yang berupa seluruh *bounding box* atau kotak penemuan plat nomor, teks OCR yang didapatkan, dan koordinat ditemukannya plat nomor tersebut. Di mana gambar dapat dilihat dibawah ini.

![](Aspose.Words.44f620a8-e744-4343-877b-3b8b4fc56b81.019.png)
