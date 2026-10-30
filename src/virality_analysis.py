
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import os

# ==========================================
# 1. SETUP
# ==========================================

sns.set_theme(style="whitegrid")

PALETTE = {
    "primary": "#2A9D8F",
    "secondary": "#264653",
    "accent": "#E76F51",
    "Viral Hit": "#2A9D8F",
    "Passive Popular": "#E76F51",
    "Niche Favourite": "#457B9D",
    "Low Traction": "#A8A8A8"
}

os.makedirs("outputs", exist_ok=True)

# ==========================================
# 2. LOAD CLEANED DATASET
# ==========================================

df = pd.read_csv("outputs/youtube_cleaned.csv")

print("Original dataset shape:", df.shape)

# ==========================================
# 3. LOG TRANSFORMATION
# ==========================================

metrics = [
    "view_count",
    "like_count",
    "comment_count"
]

for col in metrics:
    df[col + "_log"] = np.log1p(df[col])

print("\nLog transformation completed.")

# ==========================================
# 4. MIN-MAX NORMALIZATION
# ==========================================

scaler = MinMaxScaler()

normalized_values = scaler.fit_transform(
    df[
        [
            "view_count_log",
            "like_count_log",
            "comment_count_log"
        ]
    ]
)

df["views_norm"] = normalized_values[:, 0]
df["likes_norm"] = normalized_values[:, 1]
df["comments_norm"] = normalized_values[:, 2]

print("Normalization completed.")

# ==========================================
# 5. COMPOSITE VIRALITY SCORE
# ==========================================

df["virality_score"] = (
    0.40 * df["views_norm"] +
    0.30 * df["likes_norm"] +
    0.30 * df["comments_norm"]
) * 100

print("\n========== VIRALITY SCORE ==========")

print("\nVirality Score Statistics:")

print(
    df["virality_score"].describe().round(2)
)

# ==========================================
# 6. TOP 10 VIDEOS BY VIRALITY SCORE
# ==========================================

top_videos = df.nlargest(
    10,
    "virality_score"
)

print("\n========== TOP 10 VIRAL VIDEOS ==========")

print(
    top_videos[
        [
            "title",
            "category",
            "view_count",
            "like_count",
            "comment_count",
            "engagement_rate",
            "virality_score"
        ]
    ].to_string(index=False)
)

top_videos.to_csv(
    "outputs/top_10_viral_videos.csv",
    index=False
)

# ==========================================
# 7. VIRALITY SCORE DISTRIBUTION
# ==========================================

plt.figure(figsize=(12, 7))

sns.histplot(
    data=df,
    x="virality_score",
    bins=30,
    kde=True,
    color=PALETTE["primary"]
)

plt.title(
    "Distribution of Composite Virality Scores",
    fontsize=16,
    weight="bold"
)

plt.xlabel("Virality Score (0-100)")
plt.ylabel("Number of Videos")

plt.tight_layout()

plt.savefig(
    "outputs/virality_distribution.png",
    dpi=300
)

plt.show()

# ==========================================
# 8. ENGAGEMENT ARCHETYPE CLASSIFICATION
# ==========================================

views_median = df["view_count"].median()

engagement_median = df["engagement_rate"].median()

def classify_video(row):

    high_views = row["view_count"] >= views_median

    high_engagement = (
        row["engagement_rate"] >= engagement_median
    )

    if high_views and high_engagement:
        return "Viral Hit"

    elif high_views and not high_engagement:
        return "Passive Popular"

    elif not high_views and high_engagement:
        return "Niche Favourite"

    else:
        return "Low Traction"


df["archetype"] = df.apply(
    classify_video,
    axis=1
)

print("\n========== ENGAGEMENT ARCHETYPES ==========")

print("\nMedian Views:", views_median)

print("Median Engagement Rate:", engagement_median)

print("\nArchetype Counts:")

print(
    df["archetype"].value_counts()
)

# ==========================================
# 9. ENGAGEMENT ARCHETYPE SCATTER PLOT
# ==========================================

plt.figure(figsize=(13, 8))

sns.scatterplot(
    data=df,
    x="view_count",
    y="engagement_rate",
    hue="archetype",
    palette=PALETTE,
    alpha=0.65,
    s=45
)

plt.xscale("log")

# Median threshold lines
plt.axhline(
    engagement_median,
    color="black",
    linestyle="--",
    linewidth=1.5,
    label="Median Engagement"
)

plt.axvline(
    views_median,
    color="black",
    linestyle=":",
    linewidth=1.5,
    label="Median Views"
)

plt.title(
    "YouTube Video Engagement Archetypes",
    fontsize=16,
    weight="bold"
)

plt.xlabel("Views (Log Scale)")
plt.ylabel("Engagement Rate (%)")

plt.legend(
    title="Video Archetype",
    loc="best"
)

plt.tight_layout()

plt.savefig(
    "outputs/engagement_archetypes.png",
    dpi=300
)

plt.show()

# ==========================================
# 10. ARCHETYPE SUMMARY
# ==========================================

summary = (
    df.groupby("archetype")
    .agg(
        video_count=("video_id", "count"),
        median_views=("view_count", "median"),
        median_engagement=("engagement_rate", "median"),
        average_virality=("virality_score", "mean")
    )
    .reset_index()
)

# Add percentage distribution
summary["percentage"] = (
    summary["video_count"] / len(df)
) * 100

print("\n========== ARCHETYPE SUMMARY ==========")

print(
    summary.round(2).to_string(index=False)
)

# ==========================================
# 11. ARCHETYPE DISTRIBUTION BAR CHART
# ==========================================

plt.figure(figsize=(10, 6))

sns.barplot(
    data=summary,
    x="archetype",
    y="video_count",
    hue="archetype",
    palette=PALETTE,
    legend=False
)

plt.title(
    "Distribution of YouTube Engagement Archetypes",
    fontsize=15,
    weight="bold"
)

plt.xlabel("Engagement Archetype")
plt.ylabel("Number of Videos")

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(
    "outputs/archetype_distribution.png",
    dpi=300
)

plt.show()

# ==========================================
# 12. SAVE FINAL DATASETS
# ==========================================

df.to_csv(
    "outputs/youtube_virality_scores.csv",
    index=False
)

summary.to_csv(
    "outputs/archetype_summary.csv",
    index=False
)

print("\n========== EXECUTION COMPLETE ==========")

print("Virality scores calculated successfully!")

print("\nFiles generated:")
print("1. outputs/virality_distribution.png")
print("2. outputs/engagement_archetypes.png")
print("3. outputs/archetype_distribution.png")
print("4. outputs/youtube_virality_scores.csv")
print("5. outputs/archetype_summary.csv")
print("6. outputs/top_10_viral_videos.csv")
