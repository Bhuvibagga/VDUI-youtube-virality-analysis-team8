
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned dataset
df = pd.read_csv("outputs/youtube_cleaned.csv")

sns.set_theme(style="whitegrid")

PALETTE = [
    "#264653", "#2A9D8F", "#E9C46A",
    "#F4A261", "#E76F51", "#6D597A"
]

os.makedirs("outputs", exist_ok=True)

# --------------------------------
# CHART 1: CATEGORY ENGAGEMENT
# --------------------------------

category_data = (
    df.groupby("category")
    .agg(
        median_engagement=("engagement_rate", "median"),
        video_count=("video_id", "count")
    )
    .reset_index()
)

# Exclude categories with fewer than 20 videos
category_data = category_data[
    category_data["video_count"] >= 20
]

category_data = category_data.sort_values(
    "median_engagement",
    ascending=True
)

plt.figure(figsize=(12, 7))

ax = sns.barplot(
    data=category_data,
    x="median_engagement",
    y="category",
    color=PALETTE[1]
)

plt.title(
    "Median Engagement Rate by YouTube Category",
    fontsize=16,
    weight="bold"
)

plt.xlabel("Median Engagement Rate (%)")
plt.ylabel("Video Category")

for container in ax.containers:
    ax.bar_label(container, fmt="%.2f%%", padding=4)

plt.tight_layout()

plt.savefig(
    "outputs/chart1_category.png",
    dpi=300
)

plt.show()

print("\nCategory engagement ranking:")
print(category_data.sort_values(
    "median_engagement",
    ascending=False
).to_string(index=False))



# --------------------------------
# CHART 2: VIEWS VS LIKES
# --------------------------------

import re

scatter_data = df[
    (df["view_count"] > 0) &
    (df["like_count"] > 0)
].copy()

fig, ax = plt.subplots(figsize=(12, 7))

points = ax.scatter(
    scatter_data["view_count"],
    scatter_data["like_count"],
    c=scatter_data["engagement_rate"],
    cmap="viridis",
    alpha=0.65,
    s=35
)

ax.set_xscale("log")
ax.set_yscale("log")

# Continuous colour scale
cbar = plt.colorbar(points, ax=ax)
cbar.set_label("Engagement Rate (%)")

# Remove unsupported Unicode characters from annotations
def clean_title(title):
    return re.sub(r"[^A-Za-z0-9 ]", "", str(title))[:25]

outliers = scatter_data.nlargest(
    3, "engagement_rate"
)

for _, row in outliers.iterrows():
    ax.annotate(
        clean_title(row["title"]),
        (row["view_count"], row["like_count"]),
        fontsize=8,
        xytext=(7, 7),
        textcoords="offset points"
    )

ax.set_title(
    "Relationship Between Views and Likes",
    fontsize=16,
    weight="bold"
)

ax.set_xlabel("Views (Log Scale)")
ax.set_ylabel("Likes (Log Scale)")

plt.tight_layout()

plt.savefig(
    "outputs/chart2_views_likes.png",
    dpi=300
)

plt.show()



# --------------------------------
# CHART 3: UPLOAD HOUR VS ENGAGEMENT
# --------------------------------

time_data = (
    df.groupby("upload_hour")
    .agg(
        median_engagement=("engagement_rate", "median"),
        video_count=("video_id", "count")
    )
    .reset_index()
)

plt.figure(figsize=(12, 7))

sns.lineplot(
    data=time_data,
    x="upload_hour",
    y="median_engagement",
    marker="o",
    color=PALETTE[1],
    linewidth=2.5,
    markersize=8
)

# Highlight highest median engagement hour
best_hour = time_data.loc[
    time_data["median_engagement"].idxmax()
]

plt.annotate(
    f"Highest: {int(best_hour['upload_hour'])}:00",
    (
        best_hour["upload_hour"],
        best_hour["median_engagement"]
    ),
    xytext=(10, 15),
    textcoords="offset points",
    arrowprops={"arrowstyle": "->"}
)

plt.xticks(range(0, 24))

plt.title(
    "Engagement Rate by Upload Hour (IST)",
    fontsize=16,
    weight="bold"
)

plt.xlabel("Upload Hour (IST)")
plt.ylabel("Median Engagement Rate (%)")

plt.tight_layout()

plt.savefig(
    "outputs/chart3_upload_hour.png",
    dpi=300
)

plt.show()

print("\nEngagement by upload hour:")
print(time_data.to_string(index=False))




# --------------------------------
# CHART 4: DURATION VS ENGAGEMENT
# --------------------------------

duration_data = df[
    df["duration_seconds"] > 0
].copy()

# Remove extreme engagement values only for display
upper_limit = duration_data[
    "engagement_rate"
].quantile(0.99)

plot_data = duration_data[
    duration_data["engagement_rate"] <= upper_limit
].copy()

fig, ax = plt.subplots(figsize=(12, 7))

# Scatter plot with a consistent colour
ax.scatter(
    plot_data["duration_seconds"],
    plot_data["engagement_rate"],
    color="#2A9D8F",
    alpha=0.35,
    s=25,
    label="Individual videos"
)

ax.set_xscale("log")

# Calculate median engagement in logarithmic duration bins
bins = np.logspace(
    np.log10(plot_data["duration_seconds"].min()),
    np.log10(plot_data["duration_seconds"].max()),
    15
)

plot_data["duration_bin"] = pd.cut(
    plot_data["duration_seconds"],
    bins=bins
)

trend = (
    plot_data.groupby(
        "duration_bin",
        observed=True
    )
    .agg(
        median_engagement=("engagement_rate", "median"),
        median_duration=("duration_seconds", "median")
    )
    .dropna()
)

# Overlay median trend
ax.plot(
    trend["median_duration"],
    trend["median_engagement"],
    color="#E76F51",
    marker="o",
    linewidth=2.5,
    label="Median engagement trend"
)

# Annotate top 3 observations
outliers = plot_data.nlargest(
    3, "engagement_rate"
)

for _, row in outliers.iterrows():
    ax.annotate(
        clean_title(row["title"]),
        (row["duration_seconds"], row["engagement_rate"]),
        fontsize=8,
        xytext=(6, 6),
        textcoords="offset points"
    )

ax.set_title(
    "Video Duration vs Engagement Rate",
    fontsize=16,
    weight="bold"
)

ax.set_xlabel("Video Duration (Seconds, Log Scale)")
ax.set_ylabel("Engagement Rate (%)")

ax.legend()

plt.tight_layout()

plt.savefig(
    "outputs/chart4_duration.png",
    dpi=300
)

plt.show()
