import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Mengatur tema seaborn
sns.set_theme(style="darkgrid")

# Menyiapkan data
@st.cache_data
def load_data():
    # Mengambil path folder tempat skrip ini berada
    current_dir = os.path.dirname(__file__)
    
    # Menggabungkan path folder dengan nama file data
    file_path = os.path.join(current_dir, "main_data.csv")
    
    # Membaca data menggunakan path lengkap tersebut
    df = pd.read_csv(file_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

day_df = load_data()

# --- SIDEBAR ---
st.sidebar.title("🚲 Bike Sharing Dashboard")
st.sidebar.markdown("**Oleh:** Michael Valent Satrio Munthe")

# Filter Rentang Waktu
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan input tanggal dari sidebar
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

# --- HEADER DASHBOARD ---
st.title("Bike Sharing Data Dashboard 🚴‍♂️")
st.markdown("Dashboard ini menampilkan hasil analisis data penyewaan sepeda berdasarkan musim dan karakteristik tipe pengguna.")

# Tampilkan metrik utama
col1, col2, col3 = st.columns(3)
with col1:
    total_rent = main_df["cnt"].sum()
    st.metric("Total Penyewaan", value=f"{total_rent:,}")
with col2:
    total_registered = main_df["registered"].sum()
    st.metric("Pengguna Terdaftar", value=f"{total_registered:,}")
with col3:
    total_casual = main_df["casual"].sum()
    st.metric("Pengguna Kasual", value=f"{total_casual:,}")

st.markdown("---")

# --- VISUALISASI 1: Berdasarkan Musim ---
st.subheader("Total Penyewaan Sepeda Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="cnt", 
    x="season",
    data=main_df,
    estimator=sum,
    order=["Spring", "Summer", "Fall", "Winter"],
    errorbar=None,
    palette=["#D3D3D3", "#D3D3D3", "#1f77b4", "#D3D3D3"],
    ax=ax
)
ax.set_ylabel("Total Penyewaan")
ax.set_xlabel("Musim")
ax.ticklabel_format(style='plain', axis='y')
st.pyplot(fig)

# --- VISUALISASI 2: Casual vs Registered di Hari Kerja ---
st.subheader("Perbandingan Pengguna: Hari Kerja vs Hari Libur")

# Persiapan data (melt)
melt_df = main_df.melt(id_vars='workingday', value_vars=['casual', 'registered'], 
                      var_name='user_type', value_name='total_rentals')

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='workingday', 
    y='total_rentals', 
    hue='user_type', 
    data=melt_df, 
    estimator=sum, 
    errorbar=None,
    palette="viridis",
    ax=ax
)
ax.set_ylabel("Total Penyewaan")
ax.set_xlabel(None)
ax.legend(title="Tipe Pengguna")
ax.ticklabel_format(style='plain', axis='y')
st.pyplot(fig)

st.caption("Copyright © 2026")
