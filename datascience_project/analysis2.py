import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("dfall_clean.csv")

df = df[df['category_tag'].notna()]
df = df[df['category_tag'] != 'unknown']
job_counts = df['category_tag'].value_counts().sort_values(ascending=False)

plt.figure(figsize=(18, 8))
bars = plt.bar(job_counts.index, job_counts.values, color="#4A90E2")
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

