import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
df = pd.read_csv("dfall_clean.csv")


df = df[df["category_tag"].notna()]
df = df[df["category_tag"] != "unknown"]
df = df[df["location_display"].notna()]
df = df[df["country"].notna()]

output_folder = "radar_jobs"
os.makedirs(output_folder, exist_ok=True)


job_categories = df["category_tag"].unique()
for job in job_categories:
    job_df = df[df["category_tag"] == job]
    country_counts = job_df.groupby("country")["title"].count()
    country_counts = country_counts[country_counts > 0]
    if len(country_counts) == 0:
        continue
    countries = list(country_counts.index)
    counts = list(country_counts.values)
    values = counts + [counts[0]]
    N = len(countries)
    base_angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    angles = np.concatenate([base_angles, base_angles[:1]])

    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, color="#FF5733")
    ax.fill(angles, values, alpha=0.25, color="#FF5733")
    label_with_number = [
        f"{c}\n({n} jobs)" for c, n in zip(countries, counts)
    ]
    ax.set_xticks(base_angles)
    ax.set_xticklabels(label_with_number, fontsize=10)

    
    ax.set_yticklabels([])
    ax.set_ylim(0, max(values) * 1.25)
    ax.set_title(f"Job Openings Radar – {job}", fontsize=16, pad=30)
    safe_job = job.replace("/", "-")
    save_path = os.path.join(output_folder, f"radar_job_openings_{safe_job}.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
