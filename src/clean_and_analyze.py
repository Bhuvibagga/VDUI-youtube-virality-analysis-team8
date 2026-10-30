
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# 1. SETUP
# ==========================================

sns.set_theme(style="whitegrid")

PALETTE = [
    "#264653", "#2A9D8F", "#E9C46A",
    "#F4A261", "#E76F51", "#6D597A"
]

os.makedirs("outputs", exist_ok=True)

# ==========================================
# 2. LOAD DATASET
# ==========================================

df = pd.read_csv("data/youtube_data.csv")

print("Original dataset shape:", df.shape)

# ==========================================
# 3. CATEGORY ID MAPPING
# ==========================================

category_mapping = {
    1: "Film & Animation",
    2: "Autos & Vehicles",
    10: "Music",
    15: "Pets & Animals",
    17: "Sports",
    19: "Travel & Events",
    20: "Gaming",
    22: "People & Blogs",
    23: "Comedy",
    24: "Entertainment",
    25: "News & Politics",
    26: "Howto & Style",
    27: "Education",
    28: "Science & Technology",
    29: "Nonprofits & Activism",
    30: "Movies"
}

df["category"] = (
    df["category_id"]
    .map(category_mapping)
    .fillna("Other / Unmapped")
)

print("\nCategory distribution:")
print(df["category"].value_counts())

print("\nUnmapped category IDs:")
print(sorted(
    df.loc[
        df["category"] == "Other / Unmapped",
        "category_id"
    ].unique()
))

# ==========================================
# 4. CONVERT NUMERICAL COLUMNS
# ==========================================

numeric_columns = [
    "view_count",
    "like_count",
    "comment_count",
    "duration_seconds",
    "category_id"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================================
# 5. CLEAN MISSING VALUES
# ==========================================

print("\nMissing values before cleaning:")
print(df[numeric_columns].isnull().sum())

df = df.dropna(
    subset=[
        "video_id",
        "view_count",
        "like_count",
        "comment_count"
    ]
).copy()

# Remove invalid engagement values
df = df[
    (df["view_count"] > 0) &
    (df["like_count"] >= 0) &
    (df["comment_count"] >= 0)
].copy()

# Keep only valid durations for duration analysis.
# We retain the other videos for the remaining analyses.

# ==========================================
# 6. DATETIME CONVERSION
# ==========================================

df["published_at"] = pd.to_datetime(
    df["published_at"],
    errors="coerce",
    utc=True
)

# Convert UTC to Indian Standard Time
df["published_at_ist"] = (
    df["published_at"].dt.tz_convert("Asia/Kolkata")
)

df["upload_hour"] = df["published_at_ist"].dt.hour

df["upload_day"] = (
    df["published_at_ist"].dt.day_name()
)

# ==========================================
# 7. CALCULATE ENGAGEMENT RATE
# ==========================================

df["engagement_rate"] = (
    (df["like_count"] + df["comment_count"]) /
    df["view_count"]
) * 100

# ==========================================
# 8. DATASET SUMMARY
# ==========================================

print("\n========== CLEANED DATASET ==========")

print("Final rows:", len(df))
print("Final columns:", len(df.columns))

print("\nMedian views:", df["view_count"].median())

print("Median engagement rate:",
      df["engagement_rate"].median())

print("Mean engagement rate:",
      df["engagement_rate"].mean())

print("\nDuration summary:")
print(df["duration_seconds"].describe())

print("\nUpload hour distribution:")
print(df["upload_hour"].value_counts().sort_index())

print("\nCategory summary:")
print(df["category"].value_counts())

# Save cleaned dataset
df.to_csv(
    "outputs/youtube_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")
