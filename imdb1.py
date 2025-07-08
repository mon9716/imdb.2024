import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine

def scrape_imdb_2024_movies():
    url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"

    # Headless browser setup
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    print("Scraping IMDb 2024 feature films...")

    movies_data = []
    movie_blocks = driver.find_elements(By.CLASS_NAME, "lister-item.mode-advanced")
    print(movie_blocks)

    for block in movie_blocks:
        try:
            title = block.find_element(By.CLASS_NAME, "lister-item-header").text.split("\n")[0].strip()
            genre = block.find_element(By.CLASS_NAME, "genre").text.strip() if block.find_elements(By.CLASS_NAME, "genre") else "Unknown"
            duration = block.find_element(By.CLASS_NAME, "runtime").text.strip() if block.find_elements(By.CLASS_NAME, "runtime") else "N/A"
            rating = block.find_element(By.CLASS_NAME, "ratings-imdb-rating").text.strip() if block.find_elements(By.CLASS_NAME, "ratings-imdb-rating") else "N/A"
            votes = block.find_element(By.XPATH, './/p[@class="sort-num_votes-visible"]/span[2]').text.replace(",", "") if block.find_elements(By.XPATH, './/p[@class="sort-num_votes-visible"]/span[2]') else "0"

            movies_data.append({
                "Movie Name": title,
                "Genre": genre,
                "Rating": rating,
                "Votes": votes,
                "Duration": duration
            })

        except Exception as e:
            print("Error scraping a movie:", e)

    driver.quit()
    print(movies_data)
    return movies_data

def save_genre_csvs(movies_data):
    os.makedirs("genre_csvs", exist_ok=True)
    df = pd.DataFrame(movies_data)
    df['Genre'] = df['Genre'].str.split(', ')
    df_exploded = df.explode('Genre')

    for genre in df_exploded['Genre'].dropna().unique():
        genre_df = df_exploded[df_exploded['Genre'] == genre]
        filename = f"genre_csvs/{genre.replace(' ', '_')}.csv"
        genre_df.to_csv(filename, index=False)
        print(f"Saved: {filename}")

    return df_exploded

def combine_and_store(df_exploded):
    combined_df = pd.concat(
        [pd.read_csv(f"genre_csvs/{file}") for file in os.listdir("genre_csvs") if file.endswith(".csv")]
    )
    combined_df.to_csv("combined_movies.csv", index=False)
    print("Combined CSV saved as 'combined_movies.csv'")

    engine = create_engine('sqlite:///movies_2024.db', echo=False)
    combined_df.to_sql("imdb_movies_2024", con=engine, if_exists='replace', index=False)
    print("Data stored in SQLite database: movies_2024.db (table: imdb_movies_2024)")

if __name__ == "__main__":
    movies = scrape_imdb_2024_movies()
    if movies:
        exploded_df = save_genre_csvs(movies)
        combine_and_store(exploded_df)
    else:
        print("No data scraped.")