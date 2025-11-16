import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("dfall_clean.csv")

df = df[df['salary_mid'].notna()]
avg_salary = df.groupby('category_tag')['salary_mid'].mean()
if "property-jobs" in avg_salary.index:
    avg_salary = avg_salary.drop("property-jobs")

avg_salary = avg_salary.sort_values(ascending=True)
plt.figure(figsize=(14, 8))
plt.bar(avg_salary.index, avg_salary.values, color="#4a90e2")

plt.xticks(rotation=90) 
plt.xlabel("Job Category (category_tag)", fontsize=12)
plt.ylabel("Average Salary (GBP)", fontsize=12) 
plt.title("Average Salary by Job Category (GBP)", fontsize=16)
for i, v in enumerate(avg_salary.values):
    plt.text(i, v + 500, f"{int(v)}", ha='center', fontsize=8)
plt.tight_layout()
plt.show()