
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="The Anatomy of a Viral Video",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. COLOUR PALETTE
# =====================================================

BG = "#080F17"
PANEL = "#101B27"
TEAL = "#21D4C2"
CORAL = "#FF7066"
BLUE = "#6096D6"
MUTED = "#94A3B8"

ARCHETYPE_COLORS = {
    "Viral Hit": TEAL,
    "Passive Popular": CORAL,
    "Niche Favourite": BLUE,
    "Low Traction": "#94A3B8"
}

# =====================================================
# 3. CUSTOM CSS
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #080F17;
    color: #F1F5F9;
}

header[data-testid="stHeader"] {
    background: #080F17;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background-color: #0D1824;
    border-right: 1px solid #243746;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

h1, h2, h3, h4 {
    color: #F1F5F9 !important;
    font-weight: 700;
}

p, label {
    color: #CBD5E1;
}

hr {
    border-color: #243746;
}

/* KPI CARDS */

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #152433, #101B27);
    border: 1px solid #294052;
    border-radius: 14px;
    padding: 20px;
    min-height: 125px;
}

[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
}

[data-testid="stMetricValue"] {
    color: #F1F5F9 !important;
    font-size: 29px !important;
    font-weight: 750 !important;
}

/* INPUTS */

.stTextInput input {
    background-color: #152433 !important;
    color: white !important;
    border: 1px solid #294052 !important;
}

[data-baseweb="select"] {
    background-color: #152433;
}

/* BUTTONS */

.stButton button {
    background-color: #243746;
    color: white;
    border: 1px solid #365166;
    border-radius: 9px;
}

.stButton button:hover {
    border-color: #21D4C2;
    color: #21D4C2;
}

.stDownloadButton button {
    background-color: #21D4C2;
    color: #08151B;
    border: none;
    border-radius: 9px;
    font-weight: 700;
}

.stDownloadButton button:hover {
    background-color: #48E5D5;
    color: #08151B;
}

/* CHART CONTAINERS */

div[data-testid="stPlotlyChart"] {
    background-color: #101B27;
    border: 1px solid #243746;
    border-radius: 14px;
    padding: 8px;
}

/* HERO */

.hero {
    background: linear-gradient(110deg, #102A35, #101B27 60%, #17243A);
    border: 1px solid #294052;
    border-radius: 18px;
    padding: 32px;
    margin-bottom: 25px;
}

.eyebrow {
    color: #21D4C2;
    letter-spacing: 5px;
    font-size: 12px;
    font-weight: 700;
}

.hero-title {
    color: #F8FAFC;
    font-size: 43px;
    font-weight: 850;
    margin-top: 8px;
    line-height: 1.15;
}

.hero-subtitle {
    color: #21D4C2;
    font-size: 19px;
    margin-top: 12px;
}

.hero-description {
    color: #A9BAC9;
    font-size: 15px;
    line-height: 1.7;
    max-width: 850px;
}

/* SECTION LABELS */

.section-label {
    color: #21D4C2;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

/* INSIGHT CARDS */

.insight-card {
    background-color: #101B27;
    border: 1px solid #294052;
    border-radius: 13px;
    padding: 20px;
    min-height: 145px;
}

.insight-title {
    color: #21D4C2;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 10px;
}

.insight-text {
    color: #B6C5D2;
    font-size: 14px;
    line-height: 1.6;
}

/* DARK DATAFRAME */

[data-testid="stDataFrame"] {
    background-color: #101B27 !important;
    border: 1px solid #294052;
    border-radius: 12px;
    overflow: hidden;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #64748B;
    padding: 30px;
    border-top: 1px solid #243746;
    margin-top: 40px;
}


/* SIDEBAR FILTER STYLING */

/* Multiselect main container */
section[data-testid="stSidebar"] 
div[data-baseweb="select"] > div {
    background-color: #111E2B !important;
    border: 1px solid #294052 !important;
    border-radius: 10px !important;
    color: #E6EDF5 !important;
    min-height: 45px;
}

/* Selected filter tags */
section[data-testid="stSidebar"] 
[data-baseweb="tag"] {
    background-color: #16434A !important;
    border: 1px solid #247E79 !important;
    border-radius: 7px !important;
}

/* Tag text */
section[data-testid="stSidebar"] 
[data-baseweb="tag"] span {
    color: #B9F8EC !important;
}

/* Tag close icon */
section[data-testid="stSidebar"] 
[data-baseweb="tag"] svg {
    fill: #B9F8EC !important;
    color: #B9F8EC !important;
}

/* Input text */
section[data-testid="stSidebar"] 
div[data-baseweb="select"] input {
    color: #E6EDF5 !important;
}

/* Dropdown menu */
div[data-baseweb="popover"] {
    background-color: #111E2B !important;
}

div[data-baseweb="popover"] li {
    background-color: #111E2B !important;
    color: #E6EDF5 !important;
}

/* Dropdown hover */
div[data-baseweb="popover"] li:hover {
    background-color: #1B3545 !important;
}

/* Sidebar labels */
section[data-testid="stSidebar"] label {
    color: #D6E0EA !important;
    font-weight: 500 !important;
}

/* Search input */
section[data-testid="stSidebar"] 
.stTextInput input {
    background-color: #111E2B !important;
    color: #E6EDF5 !important;
    border: 1px solid #294052 !important;
    border-radius: 9px !important;
}


</style>
""", unsafe_allow_html=True)


# =====================================================
# 4. LOAD DATASET
# =====================================================

DATA_PATH = (
    Path(__file__).parent
    / "outputs"
    / "youtube_virality_scores.csv"
)


@st.cache_data
def load_data():

    data = pd.read_csv(DATA_PATH)

    numeric_columns = [
        "view_count",
        "like_count",
        "comment_count",
        "engagement_rate",
        "duration_seconds",
        "upload_hour",
        "virality_score"
    ]

    for col in numeric_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(
                data[col],
                errors="coerce"
            )

    return data


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "Dataset not found. Please check "
        "outputs/youtube_virality_scores.csv"
    )
    st.stop()


required_columns = [
    "view_count",
    "like_count",
    "comment_count",
    "engagement_rate",
    "category",
    "virality_score",
    "archetype"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(f"Missing columns: {missing_columns}")
    st.stop()


# =====================================================
# 5. HELPER FUNCTIONS
# =====================================================

def format_views(value):

    value = float(value)

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"

    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"

    return f"{value:,.0f}"


def make_chart(fig, height=430):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(
            family="Arial",
            color="#F1F5F9",
            size=12
        ),
        title_font=dict(
            size=19,
            color="#F1F5F9"
        ),
        height=height,
        margin=dict(
            l=25,
            r=25,
            t=65,
            b=45
        ),
        hoverlabel=dict(
            bgcolor="#152433",
            font_color="white"
        )
    )

    fig.update_xaxes(
        gridcolor="#243746",
        zerolinecolor="#365166"
    )

    fig.update_yaxes(
        gridcolor="#243746",
        zerolinecolor="#365166"
    )

    return fig


# =====================================================
# 6. SIDEBAR FILTERS
# =====================================================

categories = sorted(
    df["category"].dropna().unique().tolist()
)

archetypes = [
    "Viral Hit",
    "Passive Popular",
    "Niche Favourite",
    "Low Traction"
]


def reset_filters():
    st.session_state["category_filter"] = categories
    st.session_state["archetype_filter"] = archetypes
    st.session_state["title_search"] = ""


with st.sidebar:

    st.markdown("""
    <h2 style="color:#21D4C2 !important;">
        ▶ YouTube Analytics
    </h2>
    <p style="color:#94A3B8;">
        Team 8 | PES University
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        '<p class="section-label">FILTERS</p>',
        unsafe_allow_html=True
    )

    if "category_filter" not in st.session_state:
        st.session_state["category_filter"] = categories

    if "archetype_filter" not in st.session_state:
        st.session_state["archetype_filter"] = archetypes

    if "title_search" not in st.session_state:
        st.session_state["title_search"] = ""

    selected_categories = st.multiselect(
        "Select Categories",
        options=categories,
        key="category_filter"
    )

    selected_archetypes = st.multiselect(
        "Select Engagement Archetypes",
        options=archetypes,
        key="archetype_filter"
    )

    search_term = st.text_input(
        "Search Video Title",
        key="title_search",
        placeholder="Search for a video..."
    )

    st.button(
        "↻ Reset Filters",
        use_container_width=True,
        on_click=reset_filters
    )

    st.divider()

    st.caption(
        "Change filters to explore different "
        "engagement patterns."
    )

    st.markdown("""
    <p style="color:#64748B;font-size:12px;">
        TEAM 8 | UE24CS342AA9<br>
        PES University<br>
        Visualization of Data, Understanding and Interpretation
    </p>
    """, unsafe_allow_html=True)


# =====================================================
# 7. FILTER DATA
# =====================================================

filtered_df = df[
    df["category"].isin(selected_categories)
    & df["archetype"].isin(selected_archetypes)
].copy()

if search_term:

    if "title" in filtered_df.columns:

        filtered_df = filtered_df[
            filtered_df["title"]
            .fillna("")
            .str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

if filtered_df.empty:

    st.warning(
        "No videos match these filters. "
        "Please change your selections."
    )
    st.stop()


# =====================================================
# 8. HERO SECTION - HTML FIXED
# =====================================================

with st.container(border=True):
    st.caption("T H E   A N A T O M Y   O F   A")
    st.title("Viral YouTube Video")
    st.subheader("Decoding Engagement Patterns Through Data")
    st.write(
        "Explore how video categories, views, likes, comments, duration "
        "and upload timing influence audience engagement on YouTube."
    )
    st.caption(
        "Team 8 | UE24CS342AA9 | Visualization of Data, "
        "Understanding and Interpretation"
    )


# =====================================================
# 9. KEY PERFORMANCE INDICATORS
# =====================================================

st.markdown(
    '<p class="section-label">OVERVIEW / KEY METRICS</p>',
    unsafe_allow_html=True
)

total_videos = len(filtered_df)

total_views = filtered_df[
    "view_count"
].sum()

median_engagement = filtered_df[
    "engagement_rate"
].median()

average_virality = filtered_df[
    "virality_score"
].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Videos",
        f"{total_videos:,}"
    )

with c2:
    st.metric(
        "Total Views",
        format_views(total_views)
    )

with c3:
    st.metric(
        "Median Engagement",
        f"{median_engagement:.2f}%"
    )

with c4:
    st.metric(
        "Average Virality",
        f"{average_virality:.2f}/100"
    )

st.divider()


# =====================================================
# 10. CATEGORY ENGAGEMENT
# =====================================================

st.markdown(
    '<p class="section-label">01 / CATEGORY ANALYSIS</p>',
    unsafe_allow_html=True
)

st.header("Engagement by Category")

st.caption(
    "Which YouTube categories generate stronger "
    "audience interaction?"
)

category_summary = (
    filtered_df.groupby("category")
    .agg(
        median_engagement=("engagement_rate", "median"),
        video_count=("category", "size")
    )
    .reset_index()
    .sort_values("median_engagement")
)

fig_category = px.bar(
    category_summary,
    x="median_engagement",
    y="category",
    orientation="h",
    text=category_summary[
        "median_engagement"
    ].map(lambda x: f"{x:.2f}%"),
    color="median_engagement",
    color_continuous_scale=[
        "#145C63",
        "#21D4C2",
        "#8AF5E8"
    ],
    hover_data=["video_count"],
    title="Median Engagement Rate by Category"
)

fig_category.update_traces(
    textposition="outside"
)

fig_category.update_layout(
    xaxis_title="Median Engagement Rate (%)",
    yaxis_title="",
    coloraxis_showscale=False
)

st.plotly_chart(
    make_chart(fig_category, 500),
    use_container_width=True
)

st.divider()


# =====================================================
# 11. VIEWS VS LIKES
# =====================================================

st.markdown(
    '<p class="section-label">02 / POPULARITY VS ENGAGEMENT</p>',
    unsafe_allow_html=True
)

st.header("Views vs Likes")

st.caption(
    "Do videos with more views also receive more likes?"
)

scatter_df = filtered_df[
    (filtered_df["view_count"] > 0)
    & (filtered_df["like_count"] > 0)
].copy()

if not scatter_df.empty:

    hover_columns = [
        col for col in [
            "category",
            "comment_count",
            "engagement_rate",
            "virality_score",
            "archetype"
        ]
        if col in scatter_df.columns
    ]

    fig_scatter = px.scatter(
        scatter_df,
        x="view_count",
        y="like_count",
        color="archetype",
        color_discrete_map=ARCHETYPE_COLORS,
        hover_name=(
            "title"
            if "title" in scatter_df.columns
            else None
        ),
        hover_data=hover_columns,
        log_x=True,
        log_y=True,
        opacity=0.7,
        title="Relationship Between Views and Likes"
    )

    fig_scatter.update_layout(
        xaxis_title="Views (Log Scale)",
        yaxis_title="Likes (Log Scale)"
    )

    st.plotly_chart(
        make_chart(fig_scatter, 550),
        use_container_width=True
    )

st.info(
    "A positive relationship means videos with more views "
    "generally also receive more likes. Outliers help "
    "identify videos where this relationship differs."
)

st.divider()


# =====================================================
# 12. UPLOAD TIMING
# =====================================================

st.markdown(
    '<p class="section-label">03 / TEMPORAL ANALYSIS</p>',
    unsafe_allow_html=True
)

st.header("Engagement by Upload Hour")

st.caption(
    "How does median engagement vary across upload hours?"
)

if "upload_hour" in filtered_df.columns:

    timing_df = filtered_df.dropna(
        subset=[
            "upload_hour",
            "engagement_rate"
        ]
    )

    if not timing_df.empty:

        hour_summary = (
            timing_df.groupby("upload_hour")
            .agg(
                median_engagement=(
                    "engagement_rate", "median"
                ),
                video_count=("upload_hour", "size")
            )
            .reset_index()
            .sort_values("upload_hour")
        )

        fig_hour = px.line(
            hour_summary,
            x="upload_hour",
            y="median_engagement",
            markers=True,
            color_discrete_sequence=[TEAL],
            hover_data=["video_count"],
            title="Median Engagement by Upload Hour (IST)"
        )

        fig_hour.update_traces(
            line=dict(width=3),
            marker=dict(size=9, color=TEAL)
        )

        fig_hour.update_layout(
            xaxis_title="Upload Hour (IST)",
            yaxis_title="Median Engagement Rate (%)",
            xaxis=dict(
                tickmode="linear",
                dtick=1
            )
        )

        st.plotly_chart(
            make_chart(fig_hour, 450),
            use_container_width=True
        )

        best_hour = hour_summary.loc[
            hour_summary["median_engagement"].idxmax()
        ]

        st.info(
            f"Highest median engagement in the filtered "
            f"dataset occurs at {int(best_hour['upload_hour']):02d}:00 "
            f"with {best_hour['median_engagement']:.2f}%."
        )

st.divider()


# =====================================================
# 13. VIDEO DURATION ANALYSIS
# =====================================================

st.markdown(
    '<p class="section-label">04 / VIDEO CHARACTERISTICS</p>',
    unsafe_allow_html=True
)

st.header("Video Duration vs Engagement")

st.caption(
    "Does video length appear to influence audience engagement?"
)

if "duration_seconds" in filtered_df.columns:

    duration_df = filtered_df[
        (filtered_df["duration_seconds"] > 0)
        & filtered_df["duration_seconds"].notna()
    ].copy()

    if not duration_df.empty:

        upper = duration_df[
            "engagement_rate"
        ].quantile(0.99)

        duration_plot = duration_df[
            duration_df["engagement_rate"] <= upper
        ].copy()

        fig_duration = px.scatter(
            duration_plot,
            x="duration_seconds",
            y="engagement_rate",
            color="archetype",
            color_discrete_map=ARCHETYPE_COLORS,
            hover_name=(
                "title"
                if "title" in duration_plot.columns
                else None
            ),
            hover_data=[
                col for col in [
                    "category",
                    "view_count",
                    "like_count"
                ]
                if col in duration_plot.columns
            ],
            log_x=True,
            opacity=0.55,
            title="Video Duration vs Engagement Rate"
        )

        fig_duration.update_layout(
            xaxis_title="Duration (Seconds, Log Scale)",
            yaxis_title="Engagement Rate (%)"
        )

        st.plotly_chart(
            make_chart(fig_duration, 520),
            use_container_width=True
        )

        st.caption(
            "The top 1% of engagement values are excluded "
            "from this chart for readability. They remain "
            "in the original dataset."
        )

st.divider()


# =====================================================
# 14. VIRALITY SCORE ANALYSIS
# =====================================================

st.markdown(
    '<p class="section-label">05 / VIRALITY ANALYSIS</p>',
    unsafe_allow_html=True
)

st.header("Composite Virality Score")

st.caption(
    "Understanding the distribution of composite "
    "video performance scores."
)

fig_virality = px.histogram(
    filtered_df,
    x="virality_score",
    nbins=30,
    color_discrete_sequence=[TEAL],
    title="Distribution of Composite Virality Scores"
)

fig_virality.update_layout(
    xaxis_title="Virality Score (0-100)",
    yaxis_title="Number of Videos"
)

st.plotly_chart(
    make_chart(fig_virality, 450),
    use_container_width=True
)

st.markdown("""
**How to interpret the score**

The composite score is calculated in our separate
virality analysis script using views, likes and comments.

A higher score indicates stronger combined performance
on these metrics. It is a comparative measure, not a
prediction of future viral success.
""")

st.divider()


# =====================================================
# 15. ENGAGEMENT ARCHETYPES
# =====================================================

st.markdown(
    '<p class="section-label">06 / ENGAGEMENT ARCHETYPES</p>',
    unsafe_allow_html=True
)

st.header("YouTube Engagement Archetypes")

st.caption(
    "Grouping videos according to their popularity "
    "and engagement characteristics."
)

archetype_summary = (
    filtered_df.groupby("archetype")
    .agg(
        video_count=("archetype", "size"),
        median_views=("view_count", "median"),
        median_engagement=("engagement_rate", "median"),
        average_virality=("virality_score", "mean")
    )
    .reset_index()
)

fig_arch = px.bar(
    archetype_summary,
    x="archetype",
    y="video_count",
    color="archetype",
    color_discrete_map=ARCHETYPE_COLORS,
    text="video_count",
    title="Distribution of Engagement Archetypes"
)

fig_arch.update_traces(
    textposition="outside"
)

fig_arch.update_layout(
    xaxis_title="Engagement Archetype",
    yaxis_title="Number of Videos",
    showlegend=False
)

st.plotly_chart(
    make_chart(fig_arch, 420),
    use_container_width=True
)

st.subheader("Archetype Performance Comparison")

archetype_table = (
    archetype_summary.round(2)
    .style
    .set_properties(**{
        "background-color": "#101B27",
        "color": "#E2E8F0",
        "border-color": "#294052",
        "padding": "10px"
    })
    .set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#172A3A"),
                ("color", "#21D4C2"),
                ("border-color", "#294052"),
                ("padding", "10px")
            ]
        },
        {
            "selector": "td",
            "props": [("border-color", "#294052")]
        }
    ])
    .hide(axis="index")
)

st.dataframe(
    archetype_table,
    use_container_width=True,
    height=250
)


# =====================================================
# 16. ARCHETYPE DEFINITIONS
# =====================================================

st.subheader("Understanding the Four Archetypes")

a1, a2 = st.columns(2)

with a1:

    st.markdown("""
<div class="insight-card">
    <div class="insight-title">🟢 Viral Hit</div>
    <div class="insight-text">
        High views and high engagement.
        These videos combine popularity with
        strong audience interaction.
    </div>
</div>
""", unsafe_allow_html=True)

    st.write("")

    st.markdown("""
<div class="insight-card">
    <div class="insight-title">🔵 Niche Favourite</div>
    <div class="insight-text">
        Lower views but high engagement.
        These videos attract smaller audiences
        that interact strongly.
    </div>
</div>
""", unsafe_allow_html=True)

with a2:

    st.markdown("""
<div class="insight-card">
    <div class="insight-title">🟠 Passive Popular</div>
    <div class="insight-text">
        High views but low engagement.
        These videos attract large audiences
        with comparatively less interaction.
    </div>
</div>
""", unsafe_allow_html=True)

    st.write("")

    st.markdown("""
<div class="insight-card">
    <div class="insight-title">⚪ Low Traction</div>
    <div class="insight-text">
        Low views and low engagement.
        These videos have limited reach
        and audience interaction.
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()


# =====================================================
# 17. TOP 10 VIDEOS
# =====================================================

st.markdown(
    '<p class="section-label">07 / TOP PERFORMERS</p>',
    unsafe_allow_html=True
)

st.header("Top 10 Videos by Virality Score")

top_videos = filtered_df.nlargest(
    10,
    "virality_score"
)

display_columns = [
    col for col in [
        "title",
        "category",
        "view_count",
        "like_count",
        "comment_count",
        "engagement_rate",
        "virality_score",
        "archetype"
    ]
    if col in top_videos.columns
]

# Dark dataframe with readable formatting

column_config = {}

if "view_count" in display_columns:
    column_config["view_count"] = st.column_config.NumberColumn(
        "Views",
        format="localized"
    )

if "like_count" in display_columns:
    column_config["like_count"] = st.column_config.NumberColumn(
        "Likes",
        format="localized"
    )

if "comment_count" in display_columns:
    column_config["comment_count"] = st.column_config.NumberColumn(
        "Comments",
        format="localized"
    )

if "engagement_rate" in display_columns:
    column_config["engagement_rate"] = st.column_config.NumberColumn(
        "Engagement Rate",
        format="%.2f%%"
    )

if "virality_score" in display_columns:
    column_config["virality_score"] = st.column_config.NumberColumn(
        "Virality Score",
        format="%.2f"
    )

top_videos_display = top_videos[display_columns].copy()

top_videos_table = (
    top_videos_display.style
    .set_properties(**{
        "background-color": "#101B27",
        "color": "#E2E8F0",
        "border-color": "#294052",
        "padding": "9px"
    })
    .set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#172A3A"),
                ("color", "#21D4C2"),
                ("border-color", "#294052"),
                ("padding", "10px")
            ]
        },
        {
            "selector": "td",
            "props": [("border-color", "#294052")]
        }
    ])
    .hide(axis="index")
)

st.dataframe(
    top_videos_table,
    use_container_width=True,
    height=420,
    column_config=column_config
)


# =====================================================
# 18. KEY FINDINGS
# =====================================================

st.divider()

st.markdown(
    '<p class="section-label">08 / DISCOVERIES</p>',
    unsafe_allow_html=True
)

st.header("Key Findings from the Data")

i1, i2, i3 = st.columns(3)

with i1:

    st.markdown("""
<div class="insight-card">
    <div class="insight-title">01. Category Matters</div>
    <div class="insight-text">
        Engagement rates differ across content
        categories. View count alone cannot
        describe these differences.
    </div>
</div>
""", unsafe_allow_html=True)

with i2:

    st.markdown("""
<div class="insight-card">
    <div class="insight-title">02. Timing Patterns</div>
    <div class="insight-text">
        Upload-hour comparisons reveal variations
        in median engagement across publishing times.
    </div>
</div>
""", unsafe_allow_html=True)

with i3:

    st.markdown("""
<div class="insight-card">
    <div class="insight-title">03. Popularity vs Engagement</div>
    <div class="insight-text">
        Videos with high views do not necessarily
        have the highest engagement rates.
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()


# =====================================================
# 19. DOWNLOAD FILTERED DATASET
# =====================================================

st.header("Export Your Analysis")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=csv_data,
    file_name="team8_youtube_analysis.csv",
    mime="text/csv"
)


# =====================================================
# 20. FOOTER - HTML FIXED
# =====================================================

st.divider()
st.markdown("### THE ANATOMY OF A VIRAL VIDEO")
st.caption("Decoding YouTube Engagement Patterns")
st.caption("Team 8 | UE24CS342AA9 | PES University")
st.caption("Visualization of Data, Understanding and Interpretation")
st.caption("Data-driven insights. Better visual storytelling.")
