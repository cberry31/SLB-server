from dotenv import load_dotenv
import os
import requests
import logging

# Grab the Steam API key from the .env file
load_dotenv()
STEAM_API_KEY = os.getenv('STEAM_API_KEY')

class SteamAPI():
    def get_all_user_games(self, steam_id):
        """Returns a list of all games owned by a user"""
        url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&format=json'
        res = requests.get(url)
        if res.status_code != 200:
            logging.error(f'get_all_user_games: {res.status_code}')
            return None
        response = res.json()
        logging.debug(f'get_all_user_games: {response}')
        return response
