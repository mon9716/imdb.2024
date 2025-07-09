# imdb.2024
# IMDB 2024 Movie Data Scraping and Visualization

## Project Overview
This project extracts, cleans, analyzes, and visualizes movie data from IMDb's 2024 releases. It uses web scraping (Selenium), data processing (Pandas), database management (MySQL), and an interactive dashboard (Streamlit) to provide insights into movie trends, ratings, and popular genres.

## Features
* Data scraping of movie names, genres, ratings, voting counts, and durations.
* Data cleaning and transformation.
* Storage of data in a MySQL database.
* Interactive Streamlit dashboard with:
    * Filters for ratings, duration, voting counts, and genre.
    * Visualizations including top-rated movies, genre distribution, average duration by genre, rating distribution, and more.

## Technologies Used
* **Languages:** Python
* **Web Scraping:** Selenium
* **Data Manipulation:** Pandas
* **Database:** MySQL (with SQLAlchemy and `mysql-connector-python`)
* **Visualization & Dashboard:** Streamlit, Matplotlib, Seaborn
* **Version Control:** Git, GitHub

## Project Structure
imdb.2024/
├── README.md                               # This file
├── all_imdb_movies_2024_master_combined.csv # The combined dataset of all scraped and cleaned movies.
├── app.py                                  # The Streamlit application for interactive visualizations and filtering.
├── chromedriver.exe                        # The Chrome WebDriver executable, required by Selenium.
├── imdb.py                                 # Main script for web scraping, data processing, and database loading.
├── imdb_movies_2024_action.csv             # Example CSV for 'Action' genre.
├── imdb_movies_2024_adventure.csv          # Example CSV for 'Adventure' genre.
├── imdb_movies_2024_animation.csv          # Example CSV for 'Animation' genre.
├── imdb_movies_2024_sci_fi.csv             # Example CSV for 'Sci-Fi' genre.
├── imdb_movies_2024_sport.csv              # Example CSV for 'Sport' genre.
└── requirements.txt                        # Lists all Python libraries and their versions required.
## Setup and Installation

### Prerequisites
* Python 3.x installed (ensure 'Add Python to PATH' is checked during installation).
* Google Chrome browser installed.
* **MySQL Server installed and running.**
* A MySQL user with appropriate permissions to create tables and insert data.

### Steps
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/mord716/imdb.2024.git](https://github.com/mord716/imdb.2024.git)
    cd imdb.2024
    ```
2.  **Download ChromeDriver:**
    * Check your Chrome browser version (Open Chrome, go to `Settings` > `Help` > `About Google Chrome`).
    * Download the corresponding ChromeDriver from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
    * Place the `chromedriver.exe` (or `chromedriver` for macOS/Linux) file directly into the `imdb.2024/` project folder.
3.  **Install Python Dependencies:**
    Open your terminal/command prompt in the `imdb.2024` folder and run:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure MySQL Connection:**
    * Open `imdb.py` (and `app.py` if it also connects directly) and ensure your MySQL connection details (hostname, username, password, database name) are correctly configured. You might need to create an empty database first in your MySQL server.
    * Example connection string structure in Python:
        ```python
        # For imdb.py or app.py
        DATABASE_URL = "mysql+mysqlconnector://user:password@host:port/database_name"
        from sqlalchemy import create_engine
        engine = create_engine(DATABASE_URL)
        ```
        (Replace `user`, `password`, `host`, `port`, `database_name` with your actual MySQL credentials.)

## How to Run the Project

Follow these steps in order after completing the setup:

1.  **Run the Data Processing Script:**
    This script handles the web scraping, data cleaning, and loading of data into your MySQL database.
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
https://www.linkedin.com/posts/monica-umamageswaran_dataanalytics-python-streamlit-activity-7348674663293648896-aARE?utm_source=share&utm_medium=member_desktop&rcm=ACoAAE_7PqYBCyvYmCOnir7XtTdIJhnL6JtNqSA
