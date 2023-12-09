import os
import string
import requests
from dotenv import load_dotenv

load_dotenv()
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
STEAM_USER_ID = os.getenv('STEAM_USER_ID')

def get_all_achievemnts_for_game(game_id):
    url = f'https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={STEAM_API_KEY}&appid={game_id}'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def get_users_achievements(game_id):
    url = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={game_id}&key={STEAM_API_KEY}&steamid={STEAM_USER_ID}'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def format_achievements(achievements, user_achievements):
    formatted_achievements = {}
    formatted_achievements['name'] = user_achievements["playerstats"]["gameName"]
    formatted_achievements['achievements'] = []
    user_achievements_array = []
    for achievement in user_achievements["playerstats"]["achievements"]:
        achievement_dict = {}
        achievement_dict['api_name'] = achievement['apiname']
        achievement_dict['achieved'] = achievement['achieved']
        all_achievements = achievements['game']['availableGameStats']['achievements']
        a = list(filter(lambda achievement_name_dict: achievement_name_dict['name'] == achievement['apiname'], all_achievements))[0]
        achievement_dict['name'] = a['displayName']
        achievement_dict['description'] = a['description'] if 'description' in a else "Hidden"
        user_achievements_array.append(achievement_dict)
    formatted_achievements['achievements'] = user_achievements_array    
    return formatted_achievements

def print_to_csv(achievements):
    all_achievements = achievements['achievements']
    with open(f'achievements_{format_filename(achievements["name"])}.csv', 'w') as f:
        f.write('Name,Discription,Achieved\n')
        for achievement in all_achievements:
            f.write(f"{format_for_csv(achievement['name'])},{format_for_csv(achievement['description'])},{achievement['achieved']}\n")

def format_for_csv(s):
    return s.replace(',', ' ')

def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.
    
    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

def main():
    game_id = input('Enter game id: ')
    achievements = get_all_achievemnts_for_game(game_id)
    user_achievements = get_users_achievements(game_id)
    if achievements is None:
        print('Could not retrieve achievements')
        return
    formatted_achievements = format_achievements(achievements, user_achievements)
    print_to_csv(formatted_achievements)

if __name__ == '__main__':
    main()
