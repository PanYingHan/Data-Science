import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ====================================
# 1. 讀取資料
# ====================================
df = pd.read_csv("dfall_clean.csv")

# 只保留有薪資的資料（不能是 NaN，也不能是 0）
df = df.dropna(subset=["salary_mid"])
df = df[df["salary_mid"] > 0]

# 刪掉未知職位 unknown
df = df[df["category_tag"] != "unknown"]

# ====================================
# 2. 準備輸出資料夾
# ====================================
output_folder = "radar_salary"
os.makedirs(output_folder, exist_ok=True)

# ====================================
# 3. 所有職位種類
# ====================================
job_categories = df["category_tag"].unique()

# ====================================
# 4. 為每個職位畫雷達圖
# ====================================
for job in job_categories:
    job_df = df[df["category_tag"] == job]

    # 計算每國平均薪水
    country_salary = job_df.groupby("country")["salary_mid"].mean()

    # 只保留有薪資的國家
    country_salary = country_salary[country_salary > 0]

    if len(country_salary) == 0:
        continue

    countries = list(country_salary.index)
    salaries = list(country_salary.values)

    # 值（補第一個到最後）
    values = salaries + [salaries[0]]

    N = len(countries)
    base_angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    angles = np.concatenate([base_angles, base_angles[:1]])

    # ====================================
    # 繪圖
    # ====================================
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    # 👉 在國家名稱後面加上薪資數字
    label_with_salary = [
        f"{c}\n(£{int(s):,})" for c, s in zip(countries, salaries)
    ]

    ax.set_xticks(base_angles)
    ax.set_xticklabels(label_with_salary, fontsize=10)

    # y 軸不要顯示數字（保持乾淨）
    ax.set_yticklabels([])

    # 調整範圍
    ax.set_ylim(0, max(values) * 1.25)

    # 標題
    ax.set_title(f"Salary Radar Chart – {job}", fontsize=16, pad=30)

    # ====================================
    # 6. 儲存檔案
    # ====================================
    safe_job_name = job.replace("/", "-")
    save_path = os.path.join(output_folder, f"radar_{safe_job_name}.png")

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


# 執行前請先執行：source venv/bin/activate 進入虛擬環境
# 再執行：python analysis3.py