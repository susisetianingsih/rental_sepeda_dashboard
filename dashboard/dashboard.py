import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# FUNGSI-FUNGSI
# rental harian
def create_daily_rental_df(df):
    daily_rental_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum",
    })
    daily_rental_df = daily_rental_df.reset_index()    
    return daily_rental_df

# rental by season
def create_byseason_df(df):
    byseason_df = df.groupby(by="season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    byseason_df = byseason_df.reset_index()
    return byseason_df

# rental by workingday
def create_byworking_df(df):
    byworking_df = hour_df.groupby(by="workingday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    byworking_df = byworking_df.reset_index()
    return byworking_df

# rental by weekday
def create_byweekday_df(df):
    byweekday_df = df.groupby(by="weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).sort_values(by="weekday")
    byweekday_df = byweekday_df.reset_index()
    return byweekday_df

# rental by temperature
def create_bytemp_df(df):
    bytemp_df = df.groupby(by='temp').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).sort_values(by="cnt")
    # bytemp_df = bytemp_df.reset_index()    
    return bytemp_df

# rental by humadity
def create_byhum_df(df):
    byhum_df = df.groupby(by='hum').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).sort_values(by="cnt")
    # byhum_df = byhum_df.reset_index()    
    return byhum_df

# rental by windspeed
def create_bywindspeed_df(df):
    bywindspeed_df = hour_df.groupby(by='windspeed').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).sort_values(by="cnt")
    # bywindspeed_df = bywindspeed_df.reset_index()    
    return bywindspeed_df

#  rental (jam) paling banyak
def create_top5_df(df):
    hrtop5_df = hour_df.groupby(by="hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).sort_values(by="cnt", ascending=False)
    return hrtop5_df

#  rental (jam) paling sedikit
def create_bottom5_df(df):
    hrbottom5_df = hour_df.groupby(by="hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).sort_values(by="cnt", ascending=True)
    return hrbottom5_df

# PANGGIL DATASET
hour_df = pd.read_csv("hour_data.csv")

# KERANGKA WEBSITE
# cleaned
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
hour_df["temp"] = hour_df['temp'].apply(lambda x: x * 41)
hour_df["hum"] = hour_df['hum'].apply(lambda x: x * 100)
hour_df["windspeed"] = hour_df['windspeed'].apply(lambda x: x * 67)

# filter data
min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()

# Sidebar
with st.sidebar:
    # Nama Perusahaan
    st.title("Rental Sepedaku")
    
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/premium-vector/feeling-good-outside_921084-1500.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    st.info('Aplikasi ini merupakan sebuah dashboard yang menampilkan rental harian sepeda berdasarkan kondisi tertentu dari perusahaan Rental Sepedaku')
    
main_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rental_df = create_daily_rental_df(main_df)
byseason_df = create_byseason_df(main_df)
byworking_df = create_byworking_df(main_df)
byweekday_df = create_byweekday_df(main_df)
bytemp_df = create_bytemp_df(main_df)
byhum_df = create_byhum_df(main_df)
bywindspeed_df = create_bywindspeed_df(main_df)
hrtop5_df = create_top5_df(main_df)
hrbottom5_df = create_bottom5_df(main_df)

# MAINPAGE
# plot number of daily rental (2011-2012)
st.header('Rental Sepedaku Dashboard :sparkles:')

st.subheader('Daily Rental')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_rental = daily_rental_df.cnt.sum()
    st.metric("Total Rental", value=total_rental)
    
with col2:
    total_casual = daily_rental_df.casual.sum()
    st.metric("Total Casual", value=total_casual)
    
with col3:
    total_registered = daily_rental_df.registered.sum()
    st.metric("Total Registered", value=total_registered)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rental_df.index,
    daily_rental_df["casual"],
    marker='o', 
    linewidth=2,
    color="#4DB6AC",
    label='Casual'
)
ax.plot(
    daily_rental_df.index,
    daily_rental_df["registered"],
    marker='o', 
    linewidth=2,
    color="#00695C",
    label='Registered'
)
ax.legend()
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# Rental By Season
st.subheader("Jumlah Rental Berdasarkan Musim")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(16, 8))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    labels = ['Fall', 'Springer', 'Summer', 'Winter']
    colors = ['#00695C', '#B2DFDB', '#009688', '#4DB6AC']
    ax.pie(
        byseason_df['cnt'], 
        labels=labels, 
        autopct='%1.1f%%',
        startangle=90,
        colors=colors
    )
    ax.set_title('Jumlah sepeda rental untuk setiap musim')
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8, 8))
    x = np.arange(len(byseason_df['casual']))  # Mengatur posisi bar
    width = 0.35  # Lebar bar

    # Mengatur bar plot pertama
    bar1_plot = ax.bar(x - width/2, byseason_df['casual'], width, label='Casual', color='#4DB6AC')

    # Mengatur bar plot kedua
    bar2_plot = ax.bar(x + width/2, byseason_df['registered'], width, label='Registered', color='#00695C')

    # Menambahkan nilai pada setiap bar plot
    for bar, data in zip([bar1_plot, bar2_plot], [byseason_df['casual'], byseason_df['registered']]):
        for i, val in enumerate(data):
            ax.text(bar[i].get_x() + bar[i].get_width()/2, val,
                    str(val), ha='center', va='bottom', fontsize=8)

    # Menambahkan label, judul, dan legend
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Pengguna')
    ax.set_title('Perbandingan Jumlah Pengguna Casual dan Registered\nBerdasarkan Musim')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    st.pyplot(fig)

# Rental By Workingday
st.subheader("Performa Rental di hari libur dan hari kerja")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8,8))
    labels = ['Hari Kerja', 'Hari Libur']
    colors = ['#4DB6AC', '#00695C']
    ax.pie(
        byworking_df['cnt'], 
        labels=labels,
        autopct='%1.1f%%',
        startangle=90, 
        colors=colors, 
        wedgeprops = {'width':0.6}
    )
    ax.set_title('Jumlah sepeda rental untuk hari kerja vs hari libur', size = 16)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8,8))
    x = np.arange(len(byworking_df['casual']))  # Mengatur posisi bar
    width = 0.35  # Lebar bar

    # Mengatur bar plot pertama
    bar1_plot = ax.bar(x - width/2, byworking_df['casual'], width, label='Casual', color='#4DB6AC')

    # Mengatur bar plot kedua
    bar2_plot = ax.bar(x + width/2, byworking_df['registered'], width, label='Registered', color='#00695C')

    # Menambahkan nilai pada setiap bar plot
    for bar, data in zip([bar1_plot, bar2_plot], [byworking_df['casual'], byworking_df['registered']]):
        for i, val in enumerate(data):
            ax.text(bar[i].get_x() + bar[i].get_width()/2, val,
                    str(val), ha='center', va='bottom', fontsize=8)

    # Menambahkan label, judul, dan legend
    ax.set_xlabel('Kerja/Libur', size=16)
    ax.set_ylabel('Jumlah Rental', size=16)
    ax.set_title('Perbandingan Jumlah Pengguna Casual dan Registered\nBerdasarkan Hari Kerja/Hari Libur', size=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    st.pyplot(fig)

#  Rental Berdasarkan hari dalam seminggu
st.subheader("Hari dengan Jumlah Rental Sepeda Terbanyak")
fig, ax = plt.subplots(figsize=(16,8))
colors_ = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#4DB6AC", "#D3D3D3"]
nama_hari = {
    0: 'Minggu',
    1: 'Senin',
    2: 'Selasa',
    3: 'Rabu',
    4: 'Kamis',
    5: 'Jumat',
    6: 'Sabtu'
}
sns.barplot(
    x=byweekday_df.index.map(nama_hari), 
    y='cnt',
    data=byweekday_df,
    palette=colors_,
    ax=ax
)
ax.set_xlabel('Hari', size=16)
ax.set_ylabel('Jumlah Rental', size=16)
ax.set_title('Hari dengan Jumlah Rental Sepeda Terbanyak', size=16)
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)
st.pyplot(fig)

# Performa Rental Berdasarkan Jam
st.subheader("Performa Rental Berdasarkan Jam")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(16,8))
    colors_ = ["#D3D3D3", "#D3D3D3", "#4DB6AC", "#D3D3D3", "#D3D3D3"]

    # Menyortir DataFrame dan mengambil lima data teratas
    top_5_hour_df = hrtop5_df.head()

    sns.barplot(
        x=top_5_hour_df.index, 
        y="cnt",
        data=top_5_hour_df,
        palette=colors_
    )
   
    ax.set_xlabel('Jam', size=30)
    ax.set_ylabel('Jumlah Rental', size=30)
    ax.set_title("Waktu dengan jumlah rental terbanyak (Jam)", loc="center", fontsize=30)
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(16,8))
    colors_ = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#4DB6AC", "#D3D3D3"]

    # Menyortir DataFrame dan mengambil lima data teratas
    bottom_5_hour_df = hrbottom5_df.head()

    sns.barplot(
        x=bottom_5_hour_df.index, 
        y="cnt",
        data=bottom_5_hour_df,
        palette=colors_
    )
    
    ax.set_xlabel('Jam', size=30)
    ax.set_ylabel('Jumlah Rental', size=30)
    ax.set_title("Waktu dengan jumlah rental tersedikit (Jam)", loc="center", fontsize=30)
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
#  Pengaruh suhu, kelembapan, dan kecepatan angin terhadap rental
st.subheader('Pengaruh suhu, kelembapan, dan kecepatan angin terhadap rental Sepeda')
col1, col2, col3 = st.columns(3)
before_temp = main_df.iloc[-2]['temp']
new_temp = main_df.iloc[-1]['temp']
before_hum = main_df.iloc[-2]['hum']
new_hum = main_df.iloc[-1]['hum']
before_windspeed = main_df.iloc[-2]['windspeed']
new_windspeed = main_df.iloc[-1]['windspeed']

col1.metric("Temperature", f"{round(new_temp,2)} °C", f"{round(new_temp-before_temp, 2)} °C")
col2.metric("Humadity", f"{round(new_hum,2)}%", f"{round(new_hum-before_hum, 2)}%")
col3.metric("Wind Speed", f"{round(new_windspeed,2)}  mph", f"{round(new_windspeed-before_windspeed, 2)} mph")

fig, ax = plt.subplots(figsize=(16,8))
ax.scatter(x=bytemp_df.index, y=bytemp_df["casual"], color='#00695C')
ax.scatter(x=bytemp_df.index, y=bytemp_df["registered"], color='#4DB6AC')
ax.set_xlabel('Suhu', size=30)
ax.set_ylabel('Jumlah Rental', size=30)
ax.set_title("Pengaruh Suhu terhadap Jumlah Rental Sepeda", loc="center", fontsize=30)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.legend()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16,8))
ax.scatter(x=byhum_df.index, y=byhum_df["casual"], color='#00695C')
ax.scatter(x=byhum_df.index, y=byhum_df["registered"], color='#4DB6AC')
ax.set_xlabel('Kelembapan', size=30)
ax.set_ylabel('Jumlah Rental', size=30)
ax.set_title("Pengaruh Kelembapan terhadap Jumlah Rental Sepeda", loc="center", fontsize=30)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.legend()
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16,8))
ax.scatter(x=bywindspeed_df.index, y=bywindspeed_df["casual"], color='#00695C')
ax.scatter(x=bywindspeed_df.index, y=bywindspeed_df["registered"], color='#4DB6AC')
ax.set_xlabel('Kecepatan Angin', size=30)
ax.set_ylabel('Jumlah Rental', size=30)
ax.set_title("Pengaruh Kecepatan Angin terhadap Jumlah Rental Sepeda", loc="center", fontsize=30)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.legend()
st.pyplot(fig)
 
st.caption('Copyright (c) Susi Setianingsih 2023')
    
    