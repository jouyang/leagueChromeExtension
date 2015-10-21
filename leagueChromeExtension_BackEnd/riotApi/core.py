import requests
from leagueChromeExtension import app
from exceptions import *


class riotApi:
    ROOT_URL = 'https://na.api.pvp.net'
    SUMMONER_API_PLATFORM = 'api/lol'
    REGIONS = ['br', 'eune', 'euw', 'kr', 'lan', 'las', 'na', 'oce', 'ru', 'tr']
    PLATFORMS = ['NA1', 'BR1', 'LA1', 'LA2', 'OC1', 'EUN1', 'TR1', 'RU', 'EUW1', 'KR']
    VERSION = 'v1.4'
    API_KEY = app.config['RIOT_API_KEY']
    SUMMONER_API = 'summoner'
    CURRENT_GAME_URL = 'observer-mode/rest/consumer/getSpectatorGameInfo'

    # Sample:https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/jouyang?api_key=47aca7db-75ec-488a-9ef2-d025f90ccc0c
    def getSummonerIdFromName(self, summonerName, region):
        # Check for valid region
        if region not in self.REGIONS:
            raise RegionError(region)

        # Setup get url and api key
        url = '/'.join([self.ROOT_URL, self.SUMMONER_API_PLATFORM, region, self.VERSION, self.SUMMONER_API, 'by-name', summonerName])
        payload = {'api_key': self.API_KEY}
        response = requests.get(url, params=payload)

        # The returned json uses lower case, space-stripped summoner names as keys to summoner info
        print'Received response from url: %r' % response.url
        if response.status_code == 200:
            return response.json()[summonerName.lower().replace(' ', '')]
        else:
            HttpResponseErrorHandler(response.status_code, 'summonerInfo')

    # Sample:https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/44979352?api_key=47aca7db-75ec-488a-9ef2-d025f90ccc0c
    def getCurrentGameInfo(self, summonerId, platform):
        # Check for valid region
        if platform not in self.PLATFORMS:
            raise PlatformError(platform)

        # Setup get url and api key
        url = '/'.join([self.ROOT_URL, self.CURRENT_GAME_URL, platform, summonerId])
        payload = {'api_key': self.API_KEY}
        response = requests.get(url, params=payload)
        print'Received response from url: %r' % response.url
        if response.status_code == 200:
            return self.gameInfoFilter(response.json(), summonerId)
        else:
            HttpResponseErrorHandler(response.status_code, 'gameInfo')

    def gameInfoFilter(self, gameInfo, summonerId):
        for participant in gameInfo['participants']:
            if str(participant['summonerId']) == summonerId:
                return {'masteries': participant['masteries'],
                        'runes': participant['runes'],
                        'championId': participant['championId'],
                        'summonerName': participant['summonerName'],
                        'summonerId': participant['summonerId']}

    # TODO: Make internal helper functions that grabs the data of the champion, runes, mastery data and image links
