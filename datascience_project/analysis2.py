import pandas as pd
import matplotlib.pyplot as plt

# ==================================
# 1. 讀取資料
# ==================================
df = pd.read_csv("dfall_clean.csv")

# ==================================
# 2. 清洗資料：移除沒有 category_tag 的資料
# ==================================
df = df[df['category_tag'].notna()]

# 移除真正無意義分類：unknown
df = df[df['category_tag'] != 'unknown']

# ==================================
# 3. 計算每個職位類別有多少職缺（代表需求量）
# ==================================
job_counts = df['category_tag'].value_counts().sort_values(ascending=False)

print("各職位類別的職缺數量（由多到少）：")
print(job_counts)

# ==================================
# 4. 繪製長條圖（職缺最多 → 最缺人）
# ==================================
plt.figure(figsize=(18, 8))
bars = plt.bar(job_counts.index, job_counts.values, color="#4A90E2")

# 在每個柱子上標數字
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, str(int(yval)),
             ha='center', va='bottom', fontsize=9)

plt.xlabel("Job Category (category_tag)", fontsize=12)
plt.ylabel("Number of Job Openings", fontsize=12)
plt.title("Number of Job Openings by Job Category (Unknown Removed)", fontsize=16)
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# 執行前請先執行：source venv/bin/activate 進入虛擬環境
# 再執行：python analysis2.py
