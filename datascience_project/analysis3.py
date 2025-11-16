import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
df = pd.read_csv("dfall_clean.csv")

df = df.dropna(subset=["salary_mid"])
df = df[df["salary_mid"] > 0]
df = df[df["category_tag"] != "unknown"]

output_folder = "radar_salary"
os.makedirs(output_folder, exist_ok=True)

job_categories = df["category_tag"].unique()
for job in job_categories:
    job_df = df[df["category_tag"] == job]
    country_salary = job_df.groupby("country")["salary_mid"].mean()
    country_salary = country_salary[country_salary > 0]
    if len(country_salary) == 0:
        continue

    countries = list(country_salary.index)
    salaries = list(country_salary.values)
    values = salaries + [salaries[0]]
    N = len(countries)
    base_angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    angles = np.concatenate([base_angles, base_angles[:1]])
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    label_with_salary = [
        f"{c}\n(£{int(s):,})" for c, s in zip(countries, salaries)
    ]
    ax.set_xticks(base_angles)
    ax.set_xticklabels(label_with_salary, fontsize=10)
    ax.set_yticklabels([])
    
    ax.set_ylim(0, max(values) * 1.25)
    ax.set_title(f"Salary Radar Chart – {job}", fontsize=16, pad=30)

    safe_job_name = job.replace("/", "-")
    save_path = os.path.join(output_folder, f"radar_{safe_job_name}.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
