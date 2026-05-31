import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ====================================
# 1. 讀取資料
# ====================================
df = pd.read_csv("dfall_clean.csv")

# 清洗資料：不能為空職位、不能為 unknown
df = df[df["category_tag"].notna()]
df = df[df["category_tag"] != "unknown"]

# 位置欄位不能是空的（否則無法算城市職缺）
df = df[df["location_display"].notna()]

# 國家欄位不能空
df = df[df["country"].notna()]

# ====================================
# 2. 建立輸出資料夾
# ====================================
output_folder = "radar_jobs"
os.makedirs(output_folder, exist_ok=True)

# ====================================
# 3. 找出所有職位類型
# ====================================
job_categories = df["category_tag"].unique()

# ====================================
# 4. 為每個職位畫雷達圖（用職缺數）
# ====================================
for job in job_categories:
    job_df = df[df["category_tag"] == job]

    # 職缺數按國家分組
    country_counts = job_df.groupby("country")["title"].count()

    # 必須大於 0
    country_counts = country_counts[country_counts > 0]

    if len(country_counts) == 0:
        continue

    # 國家與職缺數
    countries = list(country_counts.index)
    counts = list(country_counts.values)

    # 雷達圖補頭項
    values = counts + [counts[0]]
    N = len(countries)

    base_angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    angles = np.concatenate([base_angles, base_angles[:1]])

    # ====================================
    # 繪圖
    # ====================================
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    ax.plot(angles, values, linewidth=2, color="#FF5733")
    ax.fill(angles, values, alpha=0.25, color="#FF5733")

    # 國名 + 數字
    label_with_number = [
        f"{c}\n({n} jobs)" for c, n in zip(countries, counts)
    ]

    ax.set_xticks(base_angles)
    ax.set_xticklabels(label_with_number, fontsize=10)

    # y 軸不顯示，保持乾淨
    ax.set_yticklabels([])

    # 圖表範圍
    ax.set_ylim(0, max(values) * 1.25)

    # title
    ax.set_title(f"Job Openings Radar – {job}", fontsize=16, pad=30)

    # ====================================
    # 儲存圖檔
    # ====================================
    safe_job = job.replace("/", "-")
    save_path = os.path.join(output_folder, f"radar_job_openings_{safe_job}.png")

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()



# 執行前請先執行：source venv/bin/activate 進入虛擬環境
# 再執行：python analysis4.py
