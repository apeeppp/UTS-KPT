import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

# Load data
df = pd.read_csv('benchmark_results.csv')

# Format Configuration Label
df['Konfigurasi'] = df.apply(lambda row: f"T{row['Thread']}P{row['Process']}\n({row['Data']} data)", axis=1)
df['Config_Short'] = df.apply(lambda row: f"C{row['No']}: T{row['Thread']}P{row['Process']} (N={row['Data']})", axis=1)

# Color palette
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# ---------------------------------------------------------
# 1. Grafik Waktu vs Jumlah Thread
# ---------------------------------------------------------
plt.figure(figsize=(10, 6), dpi=300)
# Filtering data for 1620 data count (where thread variation is highest: 4, 6, 8 with P=3) and all datasets
for data_val, color in zip(sorted(df['Data'].unique()), ['#3498db', '#e67e22', '#2ecc71']):
    sub = df[df['Data'] == data_val]
    # Group by thread and mean time if multiple processes
    plt.plot(sub['Thread'], sub['Waktu'], marker='o', linewidth=2.5, markersize=8, label=f'Data = {data_val}', color=color)
    for _, row in sub.iterrows():
        plt.annotate(f"P={row['Process']}\n{row['Waktu']}s", 
                     (row['Thread'], row['Waktu']),
                     textcoords="offset points", 
                     xytext=(0,10), 
                     ha='center', fontsize=8,
                     fontweight='bold')

plt.title('Grafik Waktu Eksekusi vs Jumlah Thread', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Jumlah Thread', fontsize=12, labelpad=10)
plt.ylabel('Waktu Eksekusi (detik)', fontsize=12, labelpad=10)
plt.xticks(sorted(df['Thread'].unique()))
plt.legend(title='Jumlah Data', frameon=True)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('waktu_vs_thread.png', dpi=300)
plt.close()

# ---------------------------------------------------------
# 2. Grafik Waktu vs Jumlah Process
# ---------------------------------------------------------
plt.figure(figsize=(10, 6), dpi=300)
# Select configurations where Process changes (Process 2 vs 3 for Thread 4 across Data 540, 1080, 1620)
sub_p = df[df['Thread'] == 4]
for data_val, color in zip(sorted(sub_p['Data'].unique()), ['#3498db', '#e67e22', '#2ecc71']):
    data_sub = sub_p[sub_p['Data'] == data_val]
    plt.plot(data_sub['Process'], data_sub['Waktu'], marker='s', linewidth=2.5, markersize=8, label=f'Data = {data_val} (Thread=4)', color=color)
    for _, row in data_sub.iterrows():
        plt.annotate(f"{row['Waktu']}s", 
                     (row['Process'], row['Waktu']),
                     textcoords="offset points", 
                     xytext=(0,10), 
                     ha='center', fontsize=9,
                     fontweight='bold')

plt.title('Grafik Waktu Eksekusi vs Jumlah Process (Thread = 4)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Jumlah Process', fontsize=12, labelpad=10)
plt.ylabel('Waktu Eksekusi (detik)', fontsize=12, labelpad=10)
plt.xticks([2, 3])
plt.legend(title='Jumlah Data', frameon=True)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('waktu_vs_process.png', dpi=300)
plt.close()

# ---------------------------------------------------------
# 3. Grafik Speedup vs Konfigurasi
# ---------------------------------------------------------
plt.figure(figsize=(12, 6), dpi=300)
bars = plt.bar(df['Konfigurasi'], df['Speedup'], color='#9b59b6', edgecolor='black', alpha=0.85, width=0.6)

# Highlight max speedup
max_speedup_idx = df['Speedup'].idxmax()
bars[max_speedup_idx].set_color('#e74c3c')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.2f}x', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.title('Grafik Speedup vs Konfigurasi', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Konfigurasi (Thread, Process, Jumlah Data)', fontsize=12, labelpad=10)
plt.ylabel('Speedup (x-fold)', fontsize=12, labelpad=10)
plt.ylim(0, max(df['Speedup']) * 1.15)
plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.7, label='Baseline (1.0x)')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('speedup_vs_konfigurasi.png', dpi=300)
plt.close()

# ---------------------------------------------------------
# 4. Combined Dashboard (3 dalam 1)
# ---------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), dpi=300)

# Plot 1: Waktu vs Thread
for data_val, color in zip(sorted(df['Data'].unique()), ['#3498db', '#e67e22', '#2ecc71']):
    sub = df[df['Data'] == data_val]
    axes[0].plot(sub['Thread'], sub['Waktu'], marker='o', linewidth=2, label=f'{data_val} Data', color=color)
axes[0].set_title('Waktu Eksekusi vs Thread', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Jumlah Thread')
axes[0].set_ylabel('Waktu (detik)')
axes[0].set_xticks(sorted(df['Thread'].unique()))
axes[0].legend()
axes[0].grid(True, linestyle='--', alpha=0.5)

# Plot 2: Waktu vs Process
sub_p = df[df['Thread'] == 4]
for data_val, color in zip(sorted(sub_p['Data'].unique()), ['#3498db', '#e67e22', '#2ecc71']):
    data_sub = sub_p[sub_p['Data'] == data_val]
    axes[1].plot(data_sub['Process'], data_sub['Waktu'], marker='s', linewidth=2, label=f'{data_val} Data', color=color)
axes[1].set_title('Waktu Eksekusi vs Process (Thread=4)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Jumlah Process')
axes[1].set_ylabel('Waktu (detik)')
axes[1].set_xticks([2, 3])
axes[1].legend()
axes[1].grid(True, linestyle='--', alpha=0.5)

# Plot 3: Speedup vs Konfigurasi
bars = axes[2].bar(range(1, len(df)+1), df['Speedup'], color='#9b59b6', alpha=0.85)
bars[max_speedup_idx].set_color('#e74c3c')
axes[2].set_title('Speedup vs Konfigurasi', fontsize=12, fontweight='bold')
axes[2].set_xlabel('No. Konfigurasi (1-10)')
axes[2].set_ylabel('Speedup (x)')
axes[2].set_xticks(range(1, len(df)+1))
axes[2].axhline(y=1.0, color='gray', linestyle='--', alpha=0.7)
axes[2].grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    yval = bar.get_height()
    axes[2].text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f'{yval:.2f}x', ha='center', va='bottom', fontsize=8)

plt.suptitle('Analisis Performa Parallel File Analyzer (UTS Komputasi Paralel & Terdistribusi)', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('benchmark_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("Grafik berhasil dibuat:")
print("1. waktu_vs_thread.png")
print("2. waktu_vs_process.png")
print("3. speedup_vs_konfigurasi.png")
print("4. benchmark_dashboard.png")
