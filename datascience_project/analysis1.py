import pandas as pd
import matplotlib.pyplot as plt

# ================================
# 1. 讀取資料
# ================================
df = pd.read_csv("dfall_clean.csv")

# ================================
# 2. 清洗資料：移除沒有薪資的資料
# ================================
df = df[df['salary_mid'].notna()]

# ================================
# 3. 計算不同職位類型的平均薪資
# ================================
avg_salary = df.groupby('category_tag')['salary_mid'].mean()

# ================================
# 4. 移除極端異常值（property-jobs = 2.6M GBP，會破壞圖表）
# ================================
if "property-jobs" in avg_salary.index:
    avg_salary = avg_salary.drop("property-jobs")

# ================================
# 5. 從低到高排序
# ================================
avg_salary = avg_salary.sort_values(ascending=True)

# ================================
# 6. 畫圖（X 軸 = 職位類型，Y 軸 = 平均薪資）
# ================================
plt.figure(figsize=(14, 8))
plt.bar(avg_salary.index, avg_salary.values, color="#4a90e2")

plt.xticks(rotation=90)  # X 軸職位旋轉避免重疊
plt.xlabel("Job Category (category_tag)", fontsize=12)
plt.ylabel("Average Salary (GBP)", fontsize=12)  # 加上 GBP 標註
plt.title("Average Salary by Job Category (GBP)", fontsize=16)

# 在圖表上標出薪資數值（可選）
for i, v in enumerate(avg_salary.values):
    plt.text(i, v + 500, f"{int(v)}", ha='center', fontsize=8)

plt.tight_layout()
plt.show()

print("薪資由低到高：")
print(avg_salary)

# 執行前請先執行：source venv/bin/activate 進入虛擬環境
# 再執行：python analysis1.py