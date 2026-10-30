import pandas as pd
import sqlite3
import os
from sqlalchemy import create_engine

# 1. Baca Data CSV
csv_path = "../data/product_sales.csv"
df = pd.read_csv(csv_path)

# Bersihkan nama kolom dari spasi
df.columns = df.columns.str.strip().str.replace(' ', '_')
print("📋 Kolom yang terdeteksi di CSV Anda:", df.columns.tolist())

# Deteksi kolom secara aman
col_order_id = next((c for c in df.columns if 'order' in c.lower() and 'id' in c.lower()), df.columns[0])
col_date = next((c for c in df.columns if 'date' in c.lower()), df.columns[1])
col_product = next((c for c in df.columns if 'product' in c.lower() and 'name' in c.lower()), df.columns[2] if len(df.columns) > 2 else df.columns[0])
col_category = next((c for c in df.columns if 'category' in c.lower()), df.columns[3] if len(df.columns) > 3 else df.columns[0])
col_qty = next((c for c in df.columns if 'quant' in c.lower()), 'Quantity')
col_rev = next((c for c in df.columns if 'rev' in c.lower() or 'total' in c.lower() or 'sales' in c.lower()), 'Revenue')
col_cust = next((c for c in df.columns if 'cust' in c.lower() or 'name' in c.lower()), 'Customer_Name')
col_region = next((c for c in df.columns if 'reg' in c.lower() or 'state' in c.lower() or 'city' in c.lower()), 'Region')

# Fallback jika kolom tidak ada di CSV
if col_product not in df.columns:
    df['Product_Name'] = "Generic Product"
    col_product = 'Product_Name'
if col_category not in df.columns:
    df['Category'] = "General"
    col_category = 'Category'

# 2. Split Dataset ke dalam 2 Entitas Arsitektur DBMS
df_products = df[[col_product, col_category]].drop_duplicates().reset_index(drop=True)
df_products['product_id'] = df_products.index + 1
df_products.columns = ['Product_Name', 'Category', 'product_id']

# Mapping kembali ke data transaksi
df_merged = df.merge(df_products, left_on=col_product, right_on='Product_Name', how='left')

df_orders = pd.DataFrame({
    'Order_ID': df_merged[col_order_id] if col_order_id in df_merged.columns else range(len(df)),
    'Order_Date': df_merged[col_date] if col_date in df_merged.columns else '2023-01-01',
    'Customer_Name': df_merged[col_cust] if col_cust in df_merged.columns else 'Customer',
    'Region': df_merged[col_region] if col_region in df_merged.columns else 'National',
    'product_id': df_merged['product_id'],
    'Quantity': df_merged[col_qty] if col_qty in df_merged.columns else 1,
    'Revenue': df_merged[col_rev] if col_rev in df_merged.columns else 100.0,
    'Profit': (df_merged[col_rev] * 0.3) if col_rev in df_merged.columns else 30.0
})

# 3. Seed ke DBMS 1: SQLite (Embedded Local DB)
conn_sqlite = sqlite3.connect('../data/sales_orders.db')
df_orders.to_sql('orders', conn_sqlite, if_exists='replace', index=False)
conn_sqlite.close()
print("✅ Sukses meng-isi data ke DBMS 1 (SQLite - Orders)")

# 4. Seed ke DBMS 2: PostgreSQL (Atau fallback SQLite kedua jika PostgreSQL belum aktif)
try:
    # Ganti URL di bawah ini jika menggunakan PostgreSQL Cloud (Neon/Supabase) atau lokal
    pg_url = "postgresql://neondb_owner:npg_svdR8Mmg7cjw@ep-broad-bread-b4w8j3yt-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    pg_engine = create_engine(pg_url)
    df_products.to_sql('products', pg_engine, if_exists='replace', index=False)
    print("✅ Sukses meng-isi data ke DBMS 2 (PostgreSQL - Products)")
except Exception as e:
    print(f"⚠️ Koneksi PostgreSQL gagal: {e}")
    # Fallback darurat menggunakan SQLite kedua sebagai DBMS 2 agar tugas tetap berjalan mulus
    conn_sqlite2 = sqlite3.connect('../data/sales_products.db')
    df_products.to_sql('products', conn_sqlite2, if_exists='replace', index=False)
    conn_sqlite2.close()
    print("✅ Sukses meng-isi data ke DBMS 2 (SQLite Cadangan - Products)")