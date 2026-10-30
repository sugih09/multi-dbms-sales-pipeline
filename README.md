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