# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Season 1 NerdType Dashboard** - a Streamlit-based analytics dashboard for visualizing typing game performance data from a Finnish typing competition. The application processes 5,173 game scores (5.2MB JSON data) and provides interactive analytics.

## Commands

### Running the Application
```bash
# Activate virtual environment
source .venv/bin/activate

# Run the dashboard
streamlit run dashboard.py
```

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt
```

## Architecture

### Single-File Application
- **Entry Point**: `dashboard.py` (335 lines) - contains entire application
- **Data Source**: `scores_data.json` - typing game scores with timestamps, WPM, accuracy, and user data
- **Framework**: Streamlit with Pandas for data processing and Plotly for visualization

### Key Functions
- `load_data()` (line 40) - Loads and transforms JSON data with caching
- `main()` (line 74) - Application entry point and layout orchestration
- Page configuration (line 9) - Streamlit app settings

### Data Flow
1. JSON data loaded from `scores_data.json` with error handling
2. Data transformed: percentage strings → floats, timestamps → datetime objects
3. Computed fields added: accuracy_float, hour, date_only
4. Cached using `@st.cache_data` for performance

### Dashboard Layout
- 3 rows of 4-column metrics (total players, games, WPM, accuracy, etc.)
- 2x2 chart grid: peak hours, mode popularity, accuracy distribution, difficulty multiplier impact
- Score progression timeline chart

## Data Structure

The JSON contains a `scores` object with score entries:
```json
{
  "accuracy": "97.4%",
  "authenticatedScore": true,
  "date": "2025-06-30T21:01:00.641Z",
  "difficultyMultiplier": 1.2083333333333335,
  "mode": "Custom Mode",
  "score": 728,
  "submittedAt": "2025-06-30T21:01:00.641Z",
  "timestamp": 1751317260641,
  "userEmail": "merkks@protonmail.com",
  "userId": "EtHFTsxMHZPEmUV2pwNb0CnJjSq2",
  "username": "merkks",
  "wordList": "finnish",
  "wpm": 60
}
```

## Finnish Typing Game Context

- **Game Modes**: Custom Mode (with difficulty multiplier ~1.2) and Classic Mode
- **Language**: Finnish wordlist focus
- **Metrics**: WPM, accuracy percentage, authenticated scores
- **Competition**: "Season 1" community typing competition data

## Tech Stack

- **Python 3.10** with virtual environment in `.venv/`
- **Streamlit 1.28.0+** for web application framework
- **Pandas 2.0.0+** for data manipulation
- **Plotly 5.15.0+** for interactive visualizations
- **JSON** for data storage (no database)

## Development Notes

- Application expects `scores_data.json` in root directory
- Uses Streamlit's caching decorator for performance optimization
- All visualization uses Plotly Express and Graph Objects
- No build process required - runs directly from source
- Error handling implemented for file operations with user-friendly messages