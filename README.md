pandas
sqlalchemy
psycopg2-binary
sqlite3
streamlit
plotly
python-dotenv

# 📊 Multi-DBMS Sales Analytics & Data Pipeline

*Dashboard* web interaktif berbasis Python dan Streamlit untuk menganalisis data penjualan produk menggunakan pendekatan arsitektur **Multi-DBMS** (*Application-Level Data Federation*).

---

## 🛠️ Tech Stack
* **Language**: Python 3.10+
* **Database Engine**: 
  * **DBMS 1**: SQLite (`sales_orders.db`)
  * **DBMS 2**: SQLite Secondary / PostgreSQL Cloud (`sales_products.db`)
* **Data Processing**: Pandas
* **Web Framework**: Streamlit
* **Visualization**: Plotly

---

## 🏗️ Ringkasan Arsitektur & Pipeline Data

### 1. Penjelasan Arsitektur Multi-DBMS
Web Dashboard ini menggunakan arsitektur pemisahan data (*separation of concerns*) dengan memanfaatkan 2 *engine* basis data yang berbeda:
* **DBMS 1 (SQLite - Local Embedded Engine)**:
  * *Fungsi*: Menyimpan data operasional harian / log transaksi (`orders`) seperti ID Order, Tanggal, Pelanggan, Region, Quantity, dan Pendapatan.
* **DBMS 2 (SQLite Secondary / PostgreSQL Cloud Engine)**:
  * *Fungsi*: Menyimpan data katalog master produk (`products`) yang mencakup Nama Produk, Kategori, dan informasi relasional produk lainnya.

### 2. Alur Integrasi Data (Data Pipeline)
1. **Ekstraksi (Extract)**: Sistem menarik data mentah secara terpisah dari DBMS 1 (`orders.db`) dan DBMS 2 (`products.db`).
2. **Transformasi & Federasi (Transform)**: Kedua dataset digabungkan di tingkat aplikasi (*in-memory*) menggunakan pustaka Pandas melalui operasi penggabungan relasional:
   ```python
   df_final = pd.merge(df_orders, df_products, on='product_id', how='inner')

3. Fitur Interaktivitas Antarmuka Visualisasi yang Dibangun
Antarmuka dashboard dirancang interaktif untuk memudahkan eksplorasi data oleh pengguna, yang mencakup:
1.Dynamic Sidebar Filtering: Menu filter interaktif di bilah sisi (sidebar) bagi pengguna untuk menyaring data secara real-time berdasarkan wilayah (Region) dan kategori produk tertentu.

2.Real-Time KPI Metrics Card: Kartu ringkasan metrik utama di bagian atas halaman yang otomatis memperbarui nilai Total Pendapatan (Revenue), Total Keuntungan (Profit), Jumlah Transaksi, dan Kuantitas Terjual sesuai dengan filter yang dipilih.

3.Multi-Tab Plotly Visualizations: Penyajian grafik interaktif berbasis pustaka Plotly yang dibagi ke dalam beberapa tab menu agar lebih bersih dan terstruktur:

4.Grafik Batang (Bar Chart): Untuk melihat perbandingan pendapatan berdasarkan kategori produk.

5.Diagram Lingkaran (Pie Chart / Donut Chart): Untuk menganalisis proporsi keuntungan berdasarkan wilayah (Region).

6.Grafik Garis (Line Chart): Untuk memantau tren pertumbuhan pendapatan penjualan dari waktu ke waktu.

7.Interactive Data Table Preview: Tabel data interaktif yang menampilkan rincian baris data hasil penggabungan multi-DBMS secara transparan.
