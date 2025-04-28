import requests
import json
import matplotlib.pyplot as plt


CURR_DIR = 'C:\\Users\\khoal\\Desktop\\imt542\\imt542-Spring-2025\\'

## Code created with the help of ChatGPT
## The code gets user information from a SteamID and the games they owned and exports them into 2 JSON files, one for player info and the other for game info.
## I2 Challenges: Initially, the process of getting an API key from Steam requires that I give them a web domain, despite that the API key is tied to my Steam account.
##             Thankfully it accepted a github webaap URL that I already have. So the process can be a little difficult for someone who has never touched web dev before.

## I3 updates: I have updated to include a visualization of playtime of the given user using a simple pie chart. Games with 0 playtime will not be included
## Prerequisites: matplotlib.pyplot

# Load API key from a file
def load_api_key(filepath='steam_api_key.txt'):
    fullPath = CURR_DIR + filepath
    with open(fullPath, 'r') as file:
        return file.read().strip()

# Get player summary
def get_player_summary(steam_id, api_key):
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    params = {
        'key': api_key,
        'steamids': steam_id
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GetPlayerSummaries failed: {response.status_code} - {response.text}")

# Get owned games and export into a json
def get_owned_games(steam_id, api_key):
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    params = {
        'key': api_key,
        'steamid': steam_id,
        'format': 'json',
        'include_appinfo': 'true',
        'include_played_free_games': 'true'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GetOwnedGames failed: {response.status_code} - {response.text}")
    
def export_playtime_piechart(gamelist, filename = 'playtime_chart.png'):
    fullDir = CURR_DIR + filename
    try:
        # Filter games with playtime > 0
        filtered_gamelist = [game for game in gamelist if game['playtime_forever'] > 0]

        if not filtered_gamelist:
            print("No games with playtime to chart.")
            return

        # Prepare data
        labels = [game['name'] for game in filtered_gamelist]
        sizes = [game['playtime_forever'] for game in filtered_gamelist]

        # Create pie chart
        plt.figure(figsize=(20, 20))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio
        plt.title('Playtime Distribution')

        # Save the pie chart as an image
        plt.savefig(fullDir, bbox_inches='tight')
        plt.close()  # Close the plot to free memory

        print(f"Pie chart saved as {fullDir}")

    except Exception as e:
        print(f"Error while exporting playtime pie chart: {e}")

# Save data to a JSON file
def save_to_json(data, filename):
    fullDir = CURR_DIR + filename
    with open(fullDir, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    api_key = load_api_key()
    steam_id = input("Enter your Steam ID (64-bit format): ").strip()

    try:
        print("\nFetching Player Summary...")
        player_data = get_player_summary(steam_id, api_key)
        save_to_json(player_data, 'player_summary.json')
        print("Player summary saved to player_summary.json")

        print("\nFetching Owned Games...")
        games_data = get_owned_games(steam_id, api_key)
        save_to_json(games_data, 'owned_games.json')
        print("Owned games saved to owned_games.json")
        export_playtime_piechart(games_data['response']['games'])
        print("Playtime chart saved to playtime_chart.png")

    except Exception as e:
        print(f"Error: {e}")