from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import re
import os
from sqlalchemy import create_engine

genres_to_scrape = ["action", "adventure", "animation", "sport", "sci-fi"]

base_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31&genres="

driver = webdriver.Chrome()

def click_load_more():
    try:
        load_more_button = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button/span/span')
        ActionChains(driver).move_to_element(load_more_button).perform()
        load_more_button.click()
        time.sleep(3)
        return True
    except:
        return False

for genre_name in genres_to_scrape:
    print(f"\n--- Scraping movies for genre: {genre_name.upper()} ---")
    
    url = f"{base_url}{genre_name}"
    driver.get(url)
    time.sleep(3)

    while click_load_more():
        print(f"Clicked 'Load More' button for {genre_name}")
    print(f"No more content to load for {genre_name}.")

    titles = []
    ratings = []
    votings = []
    durations = []
    genres = []

    movie_items = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li')

    for movie_item in movie_items:
        try:
            title = movie_item.find_element(By.XPATH, './div/div/div/div[1]/div[2]/div[1]/a/h3').text
            rating = movie_item.find_element(By.XPATH, './div/div/div/div[1]/div[2]/span/div/span/span[1]').text
            voting = movie_item.find_element(By.XPATH, './div/div/div/div[1]/div[2]/span/div/span/span[2]').text
            duration = movie_item.find_element(By.XPATH, './div/div/div/div[1]/div[2]/div[2]/span[2]').text
            
            movie_genre = genre_name

            titles.append(title)
            ratings.append(rating)
            votings.append(voting)
            durations.append(duration)
            genres.append(movie_genre)

        except Exception as e:
            print(f"Error extracting data for a movie in {genre_name}: {e}")
            continue

    df = pd.DataFrame({
        'Title': titles,
        'Rating': ratings,
        'Votes': votings,
        'Duration': durations,
        'Genres': genres
    })

    def clean_votes(vote_str):
        if pd.isna(vote_str) or not isinstance(vote_str, str):
            return None
        cleaned_str = re.sub(r'[(),]', '', vote_str).strip()
        if 'K' in cleaned_str.upper():
            try:
                value = float(cleaned_str.upper().replace('K', '')) * 1000
                return int(value)
            except ValueError:
                return None
        else:
            try:
                return int(cleaned_str)
            except ValueError:
                return None

    def clean_rating(rating_str):
        if pd.isna(rating_str):
            return None
        try:
            return float(rating_str)
        except ValueError:
            return None

    def convert_duration_to_minutes(duration_str):
        if pd.isna(duration_str) or not isinstance(duration_str, str):
            return None
        
        total_minutes = 0
        hours_match = re.search(r'(\d+)\s*h', duration_str, re.IGNORECASE)
        if hours_match:
            total_minutes += int(hours_match.group(1)) * 60
        
        minutes_match = re.search(r'(\d+)\s*(min|m)', duration_str, re.IGNORECASE)
        if minutes_match:
            total_minutes += int(minutes_match.group(1))
            
        if total_minutes == 0 and re.search(r'\d+', duration_str):
            try:
                num_str = re.sub(r'[^0-9]', '', duration_str) 
                if num_str:
                    total_minutes = int(num_str)
            except ValueError:
                pass

        return total_minutes if total_minutes > 0 else None

    df['Votes'] = df['Votes'].apply(clean_votes)
    df['Rating'] = df['Rating'].apply(clean_rating)
    df['Duration'] = df['Duration'].apply(convert_duration_to_minutes)

    csv_filename = f"imdb_movies_2024_{genre_name}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Scraped {len(df)} movies for {genre_name.upper()} and saved to {csv_filename}")

driver.quit()
print("Scraping complete for all specified genres.")

print("\n--- Combining individual CSV files ---")

all_dfs_to_combine = []
for genre_name in genres_to_scrape:
    csv_filename = f"imdb_movies_2024_{genre_name}.csv"
    if os.path.exists(csv_filename):
        try:
            all_dfs_to_combine.append(pd.read_csv(csv_filename))
        except Exception as e:
            print(f"Error reading {csv_filename}: {e}")
    else:
        print(f"Warning: {csv_filename} not found.")

if all_dfs_to_combine:
    master_dataframe_final = pd.concat(all_dfs_to_combine, ignore_index=True)
    print(f"Combined {len(all_dfs_to_combine)} files into a single DataFrame with {len(master_dataframe_final)} rows.")
    
    final_master_csv_filename = 'all_imdb_movies_2024_master_combined.csv'
    master_dataframe_final.to_csv(final_master_csv_filename, index=False)
    print(f"Combined master DataFrame saved to '{final_master_csv_filename}'.")

    print("\n--- Loading combined data to MySQL ---")

    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'imdb_data'

    db_connection_str = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    
    try:
        engine = create_engine(db_connection_str)
        
        master_dataframe_final.to_sql('imdb_movies_2024', con=engine, index=False, if_exists='replace')
        print(f"DataFrame successfully loaded to MySQL table 'imdb_movies_2024' in database '{MYSQL_DATABASE}'.")
        
        print("\nVerifying data in MySQL (first 5 rows from database):")
        read_df_from_mysql = pd.read_sql('SELECT * FROM imdb_movies_2024', con=engine)
        print(read_df_from_mysql.head())
        
    except Exception as e:
        print(f"\nError connecting to or saving to MySQL: {e}")
        print("Please check your MySQL server status, credentials, database name, and ensure 'mysql-connector-python' is installed.")
    finally:
        if 'engine' in locals():
            engine.dispose()

else:
    print("No CSV files were successfully loaded for combination. Skipping MySQL loading.")

print("Full script execution complete.")