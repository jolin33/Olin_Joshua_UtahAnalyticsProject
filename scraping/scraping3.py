import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

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

# Function to get a list of all NHL teams
def get_nhl_teams():
    url = 'https://www.statmuse.com/nhl'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Assuming team links are in links with a specific class or pattern
    team_links = soup.find_all('a', href=True)
    teams = []
    for link in team_links:
        if '/nhl/team/' in link['href'] and link['href'].endswith('/2024'):
            team_url = link['href'].replace('/2024', '/stats/2024')  # Insert '/stats/' before '2024'
            teams.append({
                'name': link.text.strip(),
                'url': f"https://www.statmuse.com{team_url}"
            })

    return teams

# Function to get the top 3 players from a team's stats page
def get_top_players(team_url):
    try:
        response = requests.get(team_url)
        response.raise_for_status()  # Check if the request was successful
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Assuming player names and links are in a table or a specific section
    player_links = soup.find_all('a', href=True)
    
    players = []
    indices = [2, 5, 8]  # Use 0-based index for 2nd, 5th, and 8th players
    count = 0
    for link in player_links:
        if '/nhl/player/' in link['href']:
            count += 1
            if count not in indices:
                continue
            player_url = link['href'].replace('?seasonType=regularSeason', '/game-log')
            players.append({
                'name': link.text.strip(),
                'url': f"https://www.statmuse.com{player_url}"
            })
            if len(players) == 3:  # Stop after getting 3 players
                break

    return players

# Define the range of seasons to scrape (most recent first)
current_year = 2024  # You can set this to the current year or the latest year available
start_year = 2016
seasons = [str(year) for year in range(current_year, start_year - 1, -1)]  # Create a list from current_year to start_year in descending order

# Get the list of NHL teams
teams = get_nhl_teams()
# print(len(teams))
# for i in range(32):
#     print(teams[i]['url'])

# Initialize an empty DataFrame to hold all data
all_players_df = pd.DataFrame()

# Iterate through each team and scrape data for top 3 players
for i in range(32):
    print(f"Scraping data for team: {teams[i]['name']}")
    players = get_top_players(teams[i]['url'])
    for player in players:
        print(f"  Scraping data for player: {player['name']}")
        for season in seasons:
            print(f"    Season: {season}")
            season_df = scrape_game_log(player['url'], season)
            all_players_df = pd.concat([all_players_df, season_df], ignore_index=True)
            time.sleep(1)  # Respectful crawling by adding a delay

# Print the column names to identify the correct labels
print(all_players_df.columns)

# Adjust the selection of columns based on actual headers
required_columns = ['DATE', 'G', 'A', 'TKA', 'Season', 'Player', 'MonthOrPlayoff']
missing_columns = [col for col in required_columns if col not in all_players_df.columns]
if not missing_columns:
    all_players_df = all_players_df[required_columns]
else:
    print(f"Some required columns are missing from the DataFrame: {missing_columns}")

print(all_players_df)

# Optionally, save the DataFrame to a CSV file
all_players_df.to_csv('top_3_players_all_teams_all_seasons_game_log.csv', index=False)
