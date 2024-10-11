# -*- coding: utf-8 -*-
"""streamlit.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NPEcWbCRItZuxmUSi_BZIvbvklgz5IQk
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Membaca data set
orders_df = pd.read_csv("https://raw.githubusercontent.com/Adri720S/Proyek-Analisis-Data/refs/heads/main/orders_dataset.csv")
product_df = pd.read_csv("https://raw.githubusercontent.com/Adri720S/Proyek-Analisis-Data/refs/heads/main/products_dataset.csv")
product_categories_name_translation_df = pd.read_csv("https://raw.githubusercontent.com/Adri720S/Proyek-Analisis-Data/refs/heads/main/product_category_name_translation.csv")

# Prepare data pertama
# Mengubah kolom tanggal menjadi tipe datetime
orders_df['order_approved_at'] = pd.to_datetime(orders_df['order_approved_at'], errors='coerce')

# Membuat tab untuk tahun 2016, 2017, dan 2018
tab1, tab2, tab3 = st.tabs(["Year 2016", "Year 2017", "Year 2018"])

# Fungsi untuk memproses dan menampilkan grafik per tahun
def visualisasi_tahun(tahun):
    st.subheader(f"Number of Orders per Month in {tahun}")
    
    # Filter data sesuai tahun yang dipilih
    orders_tahun = orders_df[orders_df['order_approved_at'].dt.year == tahun]
    
    # Set kolom 'order_approved_at' sebagai index
    orders_tahun = orders_tahun.set_index('order_approved_at')
    
    # Resample per bulan dan hitung jumlah order_id unik
    monthly_df = orders_tahun.resample(rule='ME').agg({
        "order_id": "nunique"
    })

    # Mengubah index menjadi format Tahun-Bulan
    monthly_df.index = monthly_df.index.strftime('%B')

    # Reset index agar kembali menjadi DataFrame
    monthly_df = monthly_df.reset_index()

    # Mengganti kolom order_id menjadi order_count
    monthly_df.rename(columns={
        "order_id": "order_count",
    }, inplace=True)

    # Membuat mapping untuk urutan bulan
    month_mapping = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    # Tambahkan kolom angka bulan untuk sorting
    monthly_df["month_numeric"] = monthly_df["order_approved_at"].map(month_mapping)
    monthly_df = monthly_df.sort_values("month_numeric")
    monthly_df = monthly_df.drop("month_numeric", axis=1)

    # Membuat visualisasi dengan Seaborn
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(
        x=monthly_df["order_approved_at"],
        y=monthly_df["order_count"],
        marker='o',
        linewidth=2,
        color="#068DA9",
        ax=ax
    )

    ax.set_title(f"Number of Orders per Month in {tahun}", loc="center", fontsize=20)
    ax.set_xlabel("Month", fontsize=15)  # Mengatur label sumbu x
    ax.set_ylabel("Order Quantity", fontsize=15)  # Mengatur label sumbu y
    ax.set_xticklabels(monthly_df["order_approved_at"], fontsize=10, rotation=20)
    ax.set_yticklabels(ax.get_yticks(), fontsize=10)

    # Menampilkan grafik dengan Streamlit
    st.pyplot(fig)

# Visualisasi untuk tab Tahun 2016
with tab1:
    visualisasi_tahun(2016)

# Visualisasi untuk tab Tahun 2017
with tab2:
    visualisasi_tahun(2017)

# Visualisasi untuk tab Tahun 2018
with tab3:
    visualisasi_tahun(2018)

# Visualisasi data kedua
# Membaca dataset
product_df = pd.read_csv("https://raw.githubusercontent.com/Adri720S/Proyek-Analisis-Data/refs/heads/main/products_dataset.csv")
product_categories_name_translation_df = pd.read_csv("https://raw.githubusercontent.com/Adri720S/Proyek-Analisis-Data/refs/heads/main/product_category_name_translation.csv")

# Menggabungkan kedua dataset berdasarkan kolom product_category_name
new_product_df = pd.merge(
    left=product_df,
    right=product_categories_name_translation_df,
    how="inner",
    left_on="product_category_name",
    right_on="product_category_name"
)

# Pilih kolom yang ingin ditampilkan
df_dipilih = new_product_df[['product_category_name_english', 'product_weight_g']]

# Hapus duplikat berdasarkan kategori produk
df_dipilih_unique = df_dipilih.drop_duplicates(subset='product_category_name_english', keep='first')

# Membuat opsi filter interaktif dengan selectbox pada Streamlit
option = st.selectbox(
    'Choose product visualization:',
    ('Heaviest Products', 'Lightest Products')
)

# Menentukan palet warna untuk barplot
colors = sns.color_palette(["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"])

# Visualisasi sesuai dengan pilihan yang dipilih pengguna
if option == 'Heaviest Products':
    st.write("### Products with the heaviest weight")
    
    # Plot produk dengan berat terbesar
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x="product_weight_g", 
        y="product_category_name_english",
        data=df_dipilih_unique.sort_values(by="product_weight_g", ascending=False).head(5),
        palette=colors, ax=ax
    )
    
    ax.set_ylabel("Product Categories")
    ax.set_xlabel("Mass (g)")
    ax.set_title("5 Heaviest Products", loc="center", fontsize=18)
    ax.tick_params(axis='y', labelsize=12)
    
    st.pyplot(fig)

elif option == 'Lightest Products':
    st.write("### Products with the lightest weight")
    
    # Plot produk dengan berat terkecil
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x="product_weight_g", 
        y="product_category_name_english",
        data=df_dipilih_unique.sort_values(by="product_weight_g", ascending=True).head(5),
        palette=colors, ax=ax
    )
    
    ax.set_ylabel("Product Categories", fontsize=15)
    ax.set_xlabel("Mass (g)", fontsize=15)
    ax.invert_xaxis()  # Membalik sumbu X
    ax.set_title("5 Lightest Products", loc="center", fontsize=18)
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    ax.tick_params(axis='y', labelsize=12)
    
    st.pyplot(fig)
