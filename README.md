# imdb.2024
# IMDb 2024 Movie Data Scraping and Visualization Project

## Project Overview
This project aims to extract, clean, analyze, and visualize movie data from IMDb's 2024 movie releases. It uses web scraping (Selenium), data processing (Pandas), database management (SQL/SQLite), and interactive dashboard creation (Streamlit) to provide insights into movie trends, ratings, and popular genres.

## Features
- Data scraping of movie names, genres, ratings, voting counts, and durations.
- Data cleaning and transformation.
- Storage of data in an SQLite database.
- Interactive Streamlit dashboard with:
    - Filters for ratings, duration, voting counts, and genre.
    - Visualizations including top-rated movies, genre distribution, average duration by genre, rating distribution, and more.

## Technologies Used
- **Languages:** Python
- **Web Scraping:** Selenium
- **Data Manipulation:** Pandas
- **Database:** SQLite (with SQLAlchemy)
- **Visualization & Dashboard:** Streamlit, Matplotlib, Seaborn
- **Version Control:** Git, GitHub

## Project Structure
imdb.2024/
├── README.md                           # This file, providing project overview and instructions.
├── all_imdb_movies_2024_master_combined.csv # The combined dataset of all scraped and cleaned movies.
├── app.py                              # The Streamlit application for interactive visualizations and filtering.
├── chromedriver.exe                    # The Chrome WebDriver executable, required by Selenium for web scraping.
├── imdb.py                             # (Likely) The main script for web scraping, data processing, and database loading.
├── imdb_2024.db                        # An SQLite database file, containing the structured movie data.
├── imdb_data.db                        # Another SQLite database file (please ensure only one is actively used by app.py).
├── imdb_movies_2024_action.csv         # CSV file containing movies classified under the 'Action' genre.
├── imdb_movies_2024_adventure.csv      # CSV file containing movies classified under the 'Adventure' genre.
├── imdb_movies_2024_animation.csv      # CSV file containing movies classified under the 'Animation' genre.
├── imdb_movies_2024_sci_fi.csv         # CSV file containing movies classified under the 'Sci-Fi' genre.
├── imdb_movies_2024_sport.csv          # CSV file containing movies classified under the 'Sport' genre.
└── requirements.txt                    # Lists all Python libraries and their versions required for the project.
## Setup and Installation

### Prerequisites
- Python 3.x installed (ensure 'Add Python to PATH' is checked during installation).
- Google Chrome browser installed.

### Steps
1.  **Clone the Repository (or Download):**
    ```bash
    git clone [https://github.com/mord716/imdb.2024.git](https://github.com/mord716/imdb.2024.git)
    cd imdb.2024
    ```
2.  **Download ChromeDriver:**
    -   Check your Chrome browser version (Open Chrome, go to `Settings` > `Help` > `About Google Chrome`).
    -   Download the corresponding ChromeDriver from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
    -   Place the `chromedriver.exe` (or `chromedriver` for macOS/Linux) file directly into the `imdb.2024/` project folder.
3.  **Install Python Dependencies:**
    Open your terminal/command prompt in the `imdb.2024` folder and run:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Project

Follow these steps in order after completing the setup:

1.  **Run the Data Processing Script:**
    This script typically handles the web scraping, data cleaning, and loading of data into your SQLite database (`imdb_2024.db` or `imdb_data.db`).
    ```bash
    python imdb.py
    ```
    *(Note: This process may take some time depending on the amount of data scraped and website responsiveness. Ensure it completes successfully before moving to the next step.)*

2.  **Run the Streamlit Application:**
    This will launch the interactive dashboard in your web browser, allowing you to explore the movie data.
    Open your terminal/command prompt in the `imdb.2024` folder and run:
    ```bash
    streamlit run app.py
    ```
    *(A new browser tab should open automatically displaying your dashboard. If not, copy the "Network URL" provided in the terminal (e.g., `http://192.168.x.x:8501`) and paste it into your web browser.)*

## Demo Video
[**TODO:** Place the link to your LinkedIn post or YouTube video demonstrating your project here.]

## Project Evaluation
This project adheres to PEP 8 coding standards and is designed for maintainability and portability.

## Contact
- Your Name / [Link to your LinkedIn Profile (Optional)]
