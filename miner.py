import logging
import sys
import os
import pandas as pd
import json
import urllib.parse
import urllib.request
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
from rich.logging import RichHandler

def api_key():
    with open('key.txt', mode='r') as fd:
        key = fd.read().rstrip()
    return key

BASE_URL = 'https://api.clashroyale.com/v1'


# Custom exception for our Communicator object.
class ClientError(Exception):
    ...


@dataclass
class Card:
    name: str
    card_id: int
    level: int
    star_level: int
    max_level: int


@dataclass
class Player:
    tag: str
    name:str
    exp_level: int
    trophies: int
    best_trophies: int
    wins: int
    losses: int
    battle_count: int
    three_crown_wins: int


@dataclass
class BattleLogPlayer:
    tag: str
    name: str
    starting_trophies: int
    trophy_change: int
    crowns: int
    king_tower_hit_points: int
    princess_towers_hit_points: Tuple[int, int]
    cards: List[Card]


@dataclass
class BattleLogEntry:
    battle_type: str
    battle_time: datetime
    game_mode_id: int
    game_mode_name: str
    team: List[BattleLogPlayer]
    opponent: List[BattleLogPlayer]


class Client:
    """Wrapper for Clash Royale API communications"""
    def __init__(self):
        self.key = api_key()
        self.api_url = BASE_URL

    
    def __send_request(self, endpoint: str) -> str:
        """Focal point of sending requests to Clash Royale API
            `endpoint` parameter can be a request for cards, battle logs, 
            player info, ... etc.

            Each method in Communicator basically wraps __send_request with 
            a specific request.

        Args:
            endpoint (str): endpoint request name

        Raises:
            ClientError: raised when urllib.request fails to send request

        Returns:
            response (str): JSON string from Clash Royale API
        """
        headers = {
            'Authorization': f'Bearer {self.key}'
        }

        try:
            request = urllib.request.Request(self.api_url + endpoint, None, headers)
            response = urllib.request.urlopen(request).read().decode('utf-8')
        
        except Exception as e:
            raise ClientError(e)

        return json.loads(response)


    def cards(self) -> Dict[int, str]:
        """Retrieve active game cards

        Returns:
            Dict[int, str]: map of card unique id to card name
        """
        endpoint = '/cards'
        cards = self.__send_request(endpoint)

        cards_dict = {}

        for item in cards['items']:
            cards_dict[item['id']] = item['name']

        return cards_dict
    
    def player_data(self, player_tag: str) -> Player:
        """Retrieve player data given a player tag"""
        # API requires that tag starts with a hashtag
        if player_tag[0] != '#':
            player_tag = f'#{player_tag}'
        
        endpoint = r'/players/{0}/battlelog'.format(player_tag)
        endpoint = urllib.parse.quote(endpoint)
        player_data_json = self.__send_request(endpoint)
        
        return Player(
            tag=player_data_json['tag'],
            name=player_data_json['name'],
            exp_level=player_data_json['expLevel'],
            trophies=player_data_json['trophies'],
            best_trophies=player_data_json['bestTrophies'],
            wins=player_data_json['wins'],
            losses=player_data_json['losses'],
            battle_count=player_data_json['battleCount'],
            three_crown_wins=player_data_json['threeCrownWins']
        )
    

    def player_pvp_battle_log(self, player_tag: str):
        ''' Gets latest battles given a player tag '''

        # API requires that tag starts with a hashtag
        if player_tag[0] != '#':
            player_tag = f'#{player_tag}'
        
        endpoint = r'/players/{0}/battlelog'.format(player_tag)
        endpoint = urllib.parse.quote(endpoint)
        battle_log_json = self.__send_request(endpoint)
        
        battle_log: List[BattleLogEntry] = []
        
        for entry in battle_log_json:
            if entry['type'] != 'PvP':
                continue

            battle_log_entry = BattleLogEntry(
                battle_type=entry['type'],
                battle_time=datetime.strptime(
                    entry['battleTime'], '%Y%m%dT%H%M%S.000Z'
                ),
                game_mode_id=entry['gameMode']['id'],
                game_mode_name=entry['gameMode']['name'],
                team=[],
                opponent=[],
            )
                        
            for i in ['team', 'opponent']:
                for player in entry[i]:
                    battle_log_player = BattleLogPlayer(
                        tag=player['tag'],
                        name=player['name'],
                        starting_trophies=player['startingTrophies'],
                        trophy_change=player['trophyChange'],
                        crowns=player['crowns'],
                        king_tower_hit_points=player.get('kingTowerHitPoints', None),
                        princess_towers_hit_points=player.get('princessTowerHitPoints', None),
                        cards=[Card(
                            name=card['name'],
                            card_id=card['id'],
                            level=card['level'],
                            star_level=card.get('starLevel', None),
                            max_level=card['maxLevel'],
                        ) for card in player['cards']]
                    )
                    
                    if i == 'team':
                        battle_log_entry.team.append(battle_log_player)
                    else:
                        battle_log_entry.opponent.append(battle_log_player)
                
            battle_log.append(battle_log_entry)
            
        return battle_log


def create_new_df(log: List[BattleLogEntry]):
    columns = [
        'battle_time',
        # Team data
        'team_tag',
        'team_name',
        'team_starting_trophies',
        'team_trophy_change',
        'team_crowns',
        *[f'team_card_{i}' for i in range(1, 9)],
        *[f'team_card_{i}_level' for i in range(1, 9)],

        # Opponent data
        'opponent_tag',
        'opponent_name',
        'opponent_starting_trophies',
        'opponent_trophy_change',
        'opponent_crowns',
        *[f'opponent_card_{i}' for i in range(1, 9)],
        *[f'opponent_card_{i}_level' for i in range(1, 9)],
        
        # Match result
        'team_won'
    ]
    
    data: List[List] = []
    
    for entry in log:
        data.append([
            entry.battle_time,
            entry.team[0].tag,
            entry.team[0].name,
            entry.team[0].starting_trophies,
            entry.team[0].trophy_change,
            entry.team[0].crowns,
            *[entry.team[0].cards[i].name for i in range(0, 8)],
            *[entry.team[0].cards[i].level for i in range(0, 8)],
            entry.opponent[0].tag,
            entry.opponent[0].name,
            entry.opponent[0].starting_trophies,
            entry.opponent[0].trophy_change,
            entry.opponent[0].crowns,
            *[entry.opponent[0].cards[i].name for i in range(0, 8)],
            *[entry.opponent[0].cards[i].level for i in range(0, 8)],
            entry.team[0].trophy_change > 0
        ])
    
    return pd.DataFrame(data=data, columns=columns)


if __name__ == '__main__':
    # target player tag
    tag = '#2PLQVY2Y0'
    
    # Set-up logger
    logging.basicConfig(
        level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
    )
    logger = logging.getLogger("rich")

    
    logger.info(f'retrieving tag {tag} data')
    try:
        client = Client()
        log = client.player_pvp_battle_log(tag)
    except ClientError:
        logger.error('Could not connect to CR API, wrong API key?')
        sys.exit()
    
    logger.info(f'got {len(log)} PvP battles from server')

    # check if 'data.csv' exists
    log_exists = os.path.isfile('./data.csv')
    
    if not log_exists:
        logger.info('Creating new .csv file with latest battle log')
        df = create_new_df(log)
    
    else:
        # read existing .csv file
        df = pd.read_csv('data.csv')
        
        # update dataframe with latest battle log
        df_new = create_new_df(log)
        
        # concatenate dataframes and remove duplicates
        df = pd.concat([df, df_new])
        df_unique = df.drop_duplicates(
            subset=[
                'opponent_tag',
                'opponent_name',
                'opponent_starting_trophies',
                'opponent_trophy_change'
            ]
        )
        n_duplicates = len(df)
        n_duplicates -= len(df_unique)

        logger.info(
            f'found {len(log) - n_duplicates} new entries'
        )
        
        df = df_unique.reset_index(drop=True)
    
    # save dataframe to .csv file
    logger.info('saving dataframe')
    df.to_csv('./data.csv', index=False)
