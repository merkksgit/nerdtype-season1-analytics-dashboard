import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Set page config
st.set_page_config(
    page_title="Season 1 Analytics Dashboard",
    page_icon="images/logo-no-keyboard-blue-bg-192x192.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for background color
st.markdown(
    """
<style>
    .stApp {
        background-color: #24283b;
    }
    .main .block-container {
        background-color: #24283b;
    }
    .stPlotlyChart {
        background-color: #24283b;
    }
    div[data-testid="stPlotlyChart"] {
        background-color: #24283b;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Load and process data
@st.cache_data
def load_data():
    try:
        # Load data from JSON file in same directory
        with open("scores_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        st.error(
            "❌ Error: 'scores_data.json' file not found in the current directory."
        )
        st.info("Please make sure the JSON file is in the same folder as this script.")
        st.stop()
    except json.JSONDecodeError:
        st.error("❌ Error: Invalid JSON format in 'scores_data.json'.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

    # Convert to DataFrame
    records = []
    for score_id, score_data in data.items():
        record = score_data.copy()
        record["score_id"] = score_id
        # Convert accuracy percentage to float
        record["accuracy_float"] = float(record["accuracy"].replace("%", ""))
        # Convert timestamp to datetime
        record["datetime"] = pd.to_datetime(record["timestamp"], unit="ms")
        record["hour"] = record["datetime"].hour
        record["date_only"] = record["datetime"].date()
        records.append(record)

    return pd.DataFrame(records)


def main():
    # Header
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("images/logo-text-no-keyboard.png", use_container_width=True)
        st.markdown(
            "<h3 style='text-align: center;'>Season 1 Analytics</h3>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Load data
    df = load_data()

    # Main Metrics Row 1
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_players = df["userId"].nunique()
        st.metric(
            label="Total Players",
            value=total_players,
            help="Unique users who participated in Season 1",
        )

    with col2:
        total_games = len(df)
        st.metric(
            label="Total Games Played",
            value=total_games,
            help="Total number of typing sessions across all users",
        )

    with col3:
        avg_wpm = df["wpm"].mean()
        st.metric(
            label="Community Average WPM",
            value=f"{avg_wpm:.1f}",
            help="Average typing speed across all players",
        )

    with col4:
        avg_accuracy = df["accuracy_float"].mean()
        st.metric(
            label="Community Average Accuracy",
            value=f"{avg_accuracy:.1f}%",
            help="Average accuracy percentage across all players",
        )

    # Additional Metrics Row 2
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        highest_wpm = df["wpm"].max()
        st.metric(
            label="Highest WPM Achieved",
            value=highest_wpm,
            help="Best typing speed recorded in Season 1",
        )

    with col2:
        perfect_games = len(df[df["accuracy_float"] == 100])
        st.metric(
            label="Perfect Accuracy Games",
            value=perfect_games,
            help="Number of games with 100% accuracy",
        )

    with col3:
        avg_score = df["score"].mean()
        st.metric(
            label="Average Score",
            value=f"{avg_score:.0f}",
            help="Average score across all games",
        )

    with col4:
        hardcore_games = len(df[df["mode"] == "Hardcore Mode"])
        st.metric(
            label="Hardcore Mode Games Completed",
            value=hardcore_games,
            help="Number of games completed in Hardcore Mode",
        )

    # Game Mode Metrics Row 3
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        custom_avg = df[df["mode"] == "Custom Mode"]["score"].mean()
        st.metric(
            label="Custom Mode Avg Score",
            value=f"{custom_avg:.0f}",
            help="Average score in Custom Mode",
        )

    with col2:
        classic_avg = df[df["mode"] == "Classic Mode"]["score"].mean()
        st.metric(
            label="Classic Mode Avg Score",
            value=f"{classic_avg:.0f}",
            help="Average score in Classic Mode",
        )

    with col3:
        most_played_wordlist = df["wordList"].value_counts().index[0]
        st.metric(
            label="Most Played Language",
            value=most_played_wordlist.title(),
            help="Most frequently used word list",
        )

    with col4:
        games_that_day = df.groupby("date_only").size().max()
        st.metric(
            label="Peak Daily Games",
            value=games_that_day,
            help="Highest number of games played in a single day",
        )

    st.markdown("---")

    # Charts Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Peak Playing Hours")

        # Create hour activity heatmap data
        hour_activity = df.groupby("hour").size().reset_index(name="games_count")

        # Create a more comprehensive hour range
        all_hours = pd.DataFrame({"hour": range(24)})
        hour_activity = all_hours.merge(hour_activity, on="hour", how="left").fillna(0)

        # Create heatmap-style visualization
        fig_hours = px.bar(
            hour_activity,
            x="hour",
            y="games_count",
            title="Games Played by Hour of Day",
            labels={"hour": "Hour of Day", "games_count": "Number of Games"},
            color="games_count",
            color_continuous_scale="Viridis",
        )
        fig_hours.update_layout(
            xaxis=dict(tickmode="linear", tick0=0, dtick=2),
            showlegend=False,
            plot_bgcolor="#24283b",
            paper_bgcolor="#24283b",
        )
        st.plotly_chart(fig_hours, use_container_width=True)

    with col2:
        st.subheader("Mode Popularity")

        mode_counts = df["mode"].value_counts()

        fig_pie = px.pie(
            values=mode_counts.values,
            names=mode_counts.index,
            title="Distribution of Game Modes",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(plot_bgcolor="#24283b", paper_bgcolor="#24283b")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Charts Row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Accuracy Distribution")

        # Create accuracy ranges
        df["accuracy_range"] = pd.cut(
            df["accuracy_float"],
            bins=[0, 80, 90, 95, 98, 100],
            labels=["<80%", "80-90%", "90-95%", "95-98%", "98-100%"],
            include_lowest=True,
        )

        accuracy_dist = df["accuracy_range"].value_counts().sort_index()

        fig_acc = px.bar(
            x=accuracy_dist.index,
            y=accuracy_dist.values,
            title="Player Accuracy Distribution",
            labels={"x": "Accuracy Range", "y": "Number of Games"},
            color=accuracy_dist.values,
            color_continuous_scale="RdYlGn",
        )
        fig_acc.update_layout(
            showlegend=False, plot_bgcolor="#24283b", paper_bgcolor="#24283b"
        )
        st.plotly_chart(fig_acc, use_container_width=True)

    with col2:
        st.subheader("Difficulty Multiplier Impact")

        # Group by difficulty multiplier ranges
        df["multiplier_range"] = pd.cut(
            df["difficultyMultiplier"],
            bins=[0, 1.0, 1.1, 1.2, 1.3, 1.5, 1.7, float("inf")],
            labels=[
                "1.0",
                "1.0-1.1",
                "1.1-1.2",
                "1.2-1.3",
                "1.3-1.5",
                "1.5-1.7",
                "1.7+",
            ],
            include_lowest=True,
        )

        multiplier_stats = (
            df.groupby("multiplier_range")
            .agg({"score": "mean", "wpm": "mean", "accuracy_float": "mean"})
            .reset_index()
        )

        fig_multiplier = px.bar(
            multiplier_stats,
            x="multiplier_range",
            y="score",
            title="Average Score by Difficulty Multiplier",
            labels={
                "multiplier_range": "Difficulty Multiplier Range",
                "score": "Average Score",
            },
            color="score",
            color_continuous_scale="RdYlBu_r",
        )
        fig_multiplier.update_layout(
            plot_bgcolor="#24283b", paper_bgcolor="#24283b", showlegend=False
        )
        st.plotly_chart(fig_multiplier, use_container_width=True)

    # Charts Row 3 - Score Progression
    st.markdown("---")
    st.subheader("Score Progression Over Time")

    # Calculate daily average scores
    daily_scores = df.groupby("date_only")["score"].mean().reset_index()
    daily_scores["date_only"] = pd.to_datetime(daily_scores["date_only"])

    fig_progression = px.line(
        daily_scores,
        x="date_only",
        y="score",
        title="Average Score Progression",
        labels={"date_only": "Date", "score": "Average Score"},
        markers=True,
    )
    fig_progression.update_traces(
        line_color="#1f77b4", line_width=3, line_shape="spline"
    )
    fig_progression.update_layout(plot_bgcolor="#24283b", paper_bgcolor="#24283b")
    st.plotly_chart(fig_progression, use_container_width=True)


if __name__ == "__main__":
    main()
