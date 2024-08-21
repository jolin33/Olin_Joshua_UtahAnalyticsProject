import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to clean the date by removing the day of the week
def clean_date(date_str):
    return re.sub(r'^\w{3,9},\s*', '', date_str).strip()

# Function to determine if the header is a month or a playoff round
def is_month(header_text):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    return any(month in header_text for month in months)

# Function to clean player name by removing trailing numbers
def clean_player_name(name_str):
    return re.sub(r'\d+$', '', name_str).strip()

# Function to scrape game log data for a given player and season
def scrape_game_log(player_url, season_year):
    url = f"{player_url}?seasonYear={season_year}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the season from the button with aria-label='seasonYear'
    button = soup.find('button', {'aria-label': 'seasonYear'})
    if button:
        season = button.text.strip()
    else:
        season = "Unknown"  # Fallback if no button is found

    # Extract player name from the URL and clean it
    player_name = player_url.split('/')[-2].replace('-', ' ').title()  # Example: 'evgeni-malkin' -> 'Evgeni Malkin'
    player_name = clean_player_name(player_name)  # Clean player name by removing trailing numbers

    # Find all h3 headers and tables on the page
    headers = soup.find_all('h3')
    tables = soup.find_all('table')

    # Initialize an empty list to hold DataFrames for each table
    all_data = []
    stop_processing = False

    header_length = None

    # Loop over the headers and tables, assuming headers precede tables
    for i, header in enumerate(headers):
        if i >= len(tables):
            break  # If there are more headers than tables, stop processing

        # Determine if the table corresponds to a month or playoff round
        header_text = header.text.strip()
        is_month_header = is_month(header_text)
        month_or_playoff = 'N' if is_month_header else 'Y'

        table = tables[i]

        if stop_processing:
            break

        # Extract the table headers
        table_headers = [th.text.strip() for th in table.find_all('th')]

        # Check if this is the first table to determine header length
        if header_length is None:
            header_length = len(table_headers)

        # Stop processing if the number of headers does not match
        if len(table_headers) != header_length:
            stop_processing = True
            break

        # Extract the table rows
        rows = []
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cols = [td.text.strip() for td in row.find_all('td')]
            # Exclude rows with 'Total' or similar summary rows
            if 'Total' not in cols:
                # Ensure the number of columns matches the headers
                if len(cols) == len(table_headers):
                    rows.append(cols)

        # Create a DataFrame from the rows and headers
        if rows:  # Only create DataFrame if there are valid rows
            df = pd.DataFrame(rows, columns=table_headers)
            df['Season'] = season  # Add the season column
            df['Player'] = player_name  # Add the player column
            df['MonthOrPlayoff'] = month_or_playoff  # Add the MonthOrPlayoff column

            # Clean the 'Date' column if it exists
            if 'Date' in df.columns:
                df['DATE'] = df['Date'].apply(clean_date)
                df.drop(columns=['Date'], inplace=True)  # Drop the original 'Date' column

            all_data.append(df)

    # Concatenate all DataFrames into a single DataFrame
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
    else:
        combined_df = pd.DataFrame()  # Return an empty DataFrame if no valid tables found

    return combined_df

# Base URL for Evgeni Malkin's game log on StatMuse
base_url = 'https://www.statmuse.com/nhl/player/evgeni-malkin-4266/game-log'

# Define the range of seasons to scrape (most recent first)
current_year = 2024  # You can set this to the current year or the latest year available
start_year = 2016
seasons = [str(year) for year in range(current_year, start_year - 1, -1)]  # Create a list from current_year to start_year in descending order

# Initialize an empty DataFrame to hold all data
all_seasons_df = pd.DataFrame()

# Iterate through each season and scrape data
for season in seasons:
    print(f"Scraping data for season: {season}")
    season_df = scrape_game_log(base_url, season)
    all_seasons_df = pd.concat([all_seasons_df, season_df], ignore_index=True)

# Print the column names to identify the correct labels
print(all_seasons_df.columns)

# Adjust the selection of columns based on actual headers
if 'DATE' in all_seasons_df.columns and 'G' in all_seasons_df.columns and 'A' in all_seasons_df.columns and 'TKA' in all_seasons_df.columns and 'Season' in all_seasons_df.columns and 'Player' in all_seasons_df.columns and 'MonthOrPlayoff' in all_seasons_df.columns:
    all_seasons_df = all_seasons_df[['DATE', 'G', 'A', 'TKA', 'Season', 'Player', 'MonthOrPlayoff']]  # Adjust these labels based on actual headers
else:
    print("Some required columns are missing from the DataFrame.")

print(all_seasons_df)

# Optionally, save the DataFrame to a CSV file
all_seasons_df.to_csv('evgeni_malkin_all_seasons_game_log.csv', index=False)
