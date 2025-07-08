import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
st.set_page_config(layout="wide")

MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'imdb_data'

DATABASE_URL = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
engine = create_engine(DATABASE_URL)

@st.cache_data
def load_movie_data():
    try:
        df = pd.read_sql('SELECT * FROM imdb_movies_2024', con=engine)
        df.rename(columns={'Title': 'Movie Name', 'Rating': 'Ratings', 'Votes': 'Voting Counts', 'Genres': 'Genre', 'Duration': 'Duration_minutes'}, inplace=True)
        df.dropna(subset=['Ratings', 'Voting Counts', 'Duration_minutes'], inplace=True)
        return df
    except Exception as e:
        st.error(f"Failed to load movie data from the database. Check MySQL connection/database: {e}")
        st.stop()

df = load_movie_data()

if df.empty:
    st.warning("No movie data found. Ensure your scraping script populated 'imdb_movies_2024'.")
    st.stop()

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎬 IMDb 2024 Movie Explorer 🍿</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Discover and analyze popular movies released in 2024 from IMDb!</p>", unsafe_allow_html=True)

st.sidebar.header("🔍 Filter Your Movies 🎬")

rating_range = st.sidebar.slider(
    "⭐ Rating Range",
    min_value=float(df['Ratings'].min()), max_value=float(df['Ratings'].max()),
    value=(float(df['Ratings'].min()), float(df['Ratings'].max())), step=0.1
)

duration_range = st.sidebar.slider(
    "⏱️ Duration (minutes)",
    min_value=int(df['Duration_minutes'].min()),
    max_value=int(df['Duration_minutes'].max()),
    value=(int(df['Duration_minutes'].min()), int(df['Duration_minutes'].max())),
    step=1
)

voting_counts_range = st.sidebar.slider(
    "🗳️ Voting Counts",
    min_value=int(df['Voting Counts'].min()),
    max_value=int(df['Voting Counts'].max()),
    value=(int(df['Voting Counts'].min()), int(df['Voting Counts'].max())),
    step=1000
)

all_genres = sorted(df['Genre'].dropna().unique().tolist())
selected_genres = st.sidebar.multiselect("🎭 Select Genre(s)", options=all_genres, default=all_genres)

filtered_df = df[
    (df['Ratings'] >= rating_range[0]) & (df['Ratings'] <= rating_range[1]) &
    (df['Duration_minutes'] >= duration_range[0]) & (df['Duration_minutes'] <= duration_range[1]) &
    (df['Voting Counts'] >= voting_counts_range[0]) & (df['Voting Counts'] <= voting_counts_range[1])
]

if selected_genres:
    filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]

st.subheader("📋 Filtered Movie List")
st.dataframe(filtered_df[['Movie Name', 'Genre', 'Ratings', 'Voting Counts', 'Duration_minutes']].reset_index(drop=True), use_container_width=True)

if filtered_df.empty:
    st.warning("No movies found with the selected filters. Please adjust your choices.")
    st.stop()

st.header("📊 Movie Data Visualizations")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("⭐ Top 10 Movies by Rating")
    top_10_rated = filtered_df.sort_values(by='Ratings', ascending=False).head(10)
    st.dataframe(top_10_rated[['Movie Name', 'Ratings', 'Voting Counts']])

with col_b:
    st.subheader("🎭 Number of Movies per Genre")
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    genre_counts = filtered_df['Genre'].value_counts().nlargest(10)
    sns.barplot(x=genre_counts.index, y=genre_counts.values, hue=genre_counts.index, ax=ax1, palette='viridis', legend=False)
    ax1.set_ylabel("Count of Movies")
    ax1.set_xlabel("Genre")
    ax1.tick_params(axis='x', rotation=45)
    st.pyplot(fig1)

col_c, col_d = st.columns(2)

with col_c:
    st.subheader("⏱️ Average Duration by Genre")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    avg_duration = filtered_df.groupby('Genre')['Duration_minutes'].mean().sort_values(ascending=False).nlargest(10)
    sns.barplot(x=avg_duration.values, y=avg_duration.index, hue=avg_duration.index, ax=ax2, palette='magma', legend=False)
    ax2.set_xlabel("Average Duration (minutes)")
    ax2.set_ylabel("Genre")
    st.pyplot(fig2)

with col_d:
    st.subheader("📊 Average Voting Counts by Genre")
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    avg_votes = filtered_df.groupby('Genre')['Voting Counts'].mean().sort_values(ascending=False).nlargest(10)
    sns.barplot(x=avg_votes.values, y=avg_votes.index, hue=avg_votes.index, ax=ax3, palette='cividis', legend=False)
    ax3.set_xlabel("Average Voting Counts")
    ax3.set_ylabel("Genre")
    st.pyplot(fig3)

st.subheader("📈 Distribution of Ratings")
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_df['Ratings'], bins=10, kde=True, ax=ax4, color='lightgreen')
ax4.set_xlabel("Ratings")
ax4.set_ylabel("Number of Movies")
st.pyplot(fig4)

col_e, col_f = st.columns(2)

with col_e:
    st.subheader("🏆 Top-Rated Movie per Genre")
    top_by_genre = filtered_df.sort_values('Ratings', ascending=False).drop_duplicates('Genre')
    st.dataframe(top_by_genre[['Genre', 'Movie Name', 'Ratings', 'Voting Counts']])

with col_f:
    st.subheader("🥧 Popular Genres by Total Votes")
    genre_votes_total = filtered_df.groupby('Genre')['Voting Counts'].sum().sort_values(ascending=False).head(5)
    fig5, ax5 = plt.subplots(figsize=(8, 8))
    ax5.pie(genre_votes_total, labels=genre_votes_total.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    ax5.axis('equal')
    st.pyplot(fig5)

col_g, col_h = st.columns(2)

with col_g:
    st.subheader("⏳ Shortest Movies")
    shortest_movies = filtered_df.nsmallest(5, 'Duration_minutes')
    st.dataframe(shortest_movies[['Movie Name', 'Genre', 'Duration_minutes', 'Ratings']])

with col_h:
    st.subheader("⌛ Longest Movies")
    longest_movies = filtered_df.nlargest(5, 'Duration_minutes')
    st.dataframe(longest_movies[['Movie Name', 'Genre', 'Duration_minutes', 'Ratings']])

st.subheader("🔥 Average Ratings by Genre (Heatmap)")
fig6, ax6 = plt.subplots(figsize=(10, 7))
heat_df = filtered_df.groupby('Genre')[['Ratings']].mean().sort_values('Ratings', ascending=False)
sns.heatmap(heat_df, annot=True, cmap="YlGnBu", linewidths=0.5, fmt=".2f", ax=ax6)
ax6.set_title("Average Ratings by Genre")
st.pyplot(fig6)

st.subheader("📉 Ratings vs Voting Counts (Correlation)")
fig7, ax7 = plt.subplots(figsize=(10, 7))
sns.scatterplot(data=filtered_df, x='Voting Counts', y='Ratings', hue='Genre', alpha=0.7, ax=ax7, palette='tab10', s=100)
ax7.set_xscale('log')
ax7.set_xlabel("Voting Counts (Log Scale)")
ax7.set_ylabel("Ratings")
ax7.set_title("Movie Ratings vs. Voting Counts by Genre")
st.pyplot(fig7)