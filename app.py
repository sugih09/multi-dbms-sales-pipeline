import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Dashboard Analisis Penjualan Multi-DBMS", layout="wide")

st.title("📊 Dashboard Analisis Penjualan Produk (Multi-DBMS Pipeline)")
st.markdown("Aplikasi Visualisasi Data Interaktif Berbasis Integrasi **DBMS 1: SQLite (Local Embedded Database)** dan **DBMS 2: PostgreSQL (Cloud / Serverless Database)**")

# 1. DATA PIPELINE (ETL / Merge di Aplikasi)
@st.cache_data
def load_and_federate_data():
    # Fetch dari DBMS 1 (SQLite Orders)
    conn_sqlite1 = sqlite3.connect('data/sales_orders.db')
    df_orders = pd.read_sql_query("SELECT * FROM orders", conn_sqlite1)
    conn_sqlite1.close()

    # Fetch dari DBMS 2 (SQLite Products)
    conn_sqlite2 = sqlite3.connect('data/sales_products.db')
    df_products = pd.read_sql_query("SELECT * FROM products", conn_sqlite2)
    conn_sqlite2.close()

    # Merging Data di Tingkat Aplikasi via Pandas
    df_final = pd.merge(df_orders, df_products, on='product_id', how='inner')
    df_final['Order_Date'] = pd.to_datetime(df_final['Order_Date'], errors='coerce')
    return df_final

df = load_and_federate_data()

# 2. SIDEBAR FILTER INTERAKSIF
st.sidebar.header("Filter Data")
region_options = df["Region"].unique() if "Region" in df.columns else []
region_filter = st.sidebar.multiselect("Pilih Wilayah (Region):", options=region_options, default=region_options)

df_filtered = df[df["Region"].isin(region_filter)] if region_filter else df

# 3. METRIK & KPI UTAMA
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pendapatan (Revenue)", f"${df_filtered['Revenue'].sum():,.2f}")
col2.metric("Total Keuntungan (Profit)", f"${df_filtered['Profit'].sum():,.2f}")
col3.metric("Jumlah Transaksi", f"{len(df_filtered):,}")
col4.metric("Jumlah Produk Terjual", f"{df_filtered['Quantity'].sum():,}")

st.markdown("---")

# 4. VISUALISASI INTERAKSIF (PLOTLY)
if "Category" in df_filtered.columns and "Revenue" in df_filtered.columns:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Pendapatan berdasarkan Kategori Produk")
        fig_cat = px.bar(
            df_filtered.groupby("Category")["Revenue"].sum().reset_index(),
            x="Category", y="Revenue", color="Category",
            title="Total Revenue per Category"
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with c2:
        st.subheader("Proporsi Keuntungan berdasarkan Region")
        if "Region" in df_filtered.columns:
            fig_pie = px.pie(
                df_filtered, values="Profit", names="Region", hole=0.4,
                title="Profit Distribution by Region"
            )
            st.plotly_chart(fig_pie, use_container_width=True)