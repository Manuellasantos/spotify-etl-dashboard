# 🎀 Spotify ETL Dashboard Project

##  Overview

This project was developed as part of a practical ETL challenge using Python and Streamlit.  
The goal was to simulate a real-world data pipeline capable of extracting, transforming, loading, and visualizing Spotify music data.

---

#  Dataset

The dataset contains Spotify music information such as:

- Artists
- Genres
- Popularity
- Danceability
- Energy
- Duration

---

# ⚙️ ETL Process

##  Extract

Loaded CSV data using pandas.

---

##  Transform

- Removed duplicates
- Removed null values
- Renamed columns
- Converted duration from milliseconds to minutes
- Filtered highly popular songs

---

##  Load

Saved processed data as:

```plaintext
spotify_tratado.csv
```

---

# 📈 Dashboard Features

- Interactive dashboard
- Sidebar navigation
- Dynamic filters
- Interactive charts
- Responsive layout
- Pink custom theme

---

# Charts Included

- 🎤 Top Artists
- 🎧 Genre Distribution
- ⚡ Danceability vs Energy
- 📋 Interactive Data Table

---

#  Key Learnings

- Practical ETL pipeline understanding
- Data cleaning and transformation
- Dashboard creation with Streamlit
- Interactive data visualization

---

#  Technologies

- Python
- Pandas
- Streamlit
- Plotly
- CSV Dataset

---

#  How to Run

## Install dependencies

```bash
pip install streamlit pandas plotly
```

## Run project

```bash
python -m streamlit run app.py
```

---

# 💖 Final Note

This project demonstrates practical ETL and dashboard development skills using Python and Streamlit.
