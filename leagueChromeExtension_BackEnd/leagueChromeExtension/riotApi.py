import requests
from leagueChromeExtension import app


class riotApi():
    ROOT_URL = 'https://na.api.pvp.net'
    SUMMONER_API_PLATFORM = 'api/lol'
    REGIONS = ['br', 'eune', 'euw', 'kr', 'lan', 'las', 'na', 'oce', 'ru', 'tr']
    PLATFORMS = ['NA1', 'BR1', 'LA1', 'LA2', 'OC1', 'EUN1', 'TR1', 'RU', 'EUW1', 'KR']
    VERSION = 'v1.4'
    API_KEY = app.config['RIOT_API_KEY']
    SUMMONER_API = 'summoner'
    CURRENT_GAME_URL = 'observer-mode/rest/consumer/getSpectatorGameInfo'

    #Sample:https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/jouyang?api_key=47aca7db-75ec-488a-9ef2-d025f90ccc0c
    def getSummonerIdFromName(self, summonerName, region):
        #Check for valid region
        if region not in self.REGIONS:
            raise RegionError(region)

        #Setup get url and api key
        url = '/'.join([self.ROOT_URL, self.SUMMONER_API_PLATFORM, region, self.VERSION, self.SUMMONER_API, 'by-name', summonerName])
        payload = {'api_key': self.API_KEY}
        response = requests.get(url, params=payload)

        #The returned json uses lower case, space-stripped summoner names as keys to summoner info
        print'Received response from url: %r' % response.url
        if response.status_code == 404:
            raise SummonerNotFoundError(summonerName, region)
        else:
            return response.json()[summonerName.lower().replace(' ', '')]

    #Sample:https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/44979352?api_key=47aca7db-75ec-488a-9ef2-d025f90ccc0c
    def getCurrentGameInfo(self, summonerId, platform):
        #Check for valid region
        if platform not in self.PLATFORMS:
            raise PlatformError(platform)

        #Setup get url and api key
        url = '/'.join([self.ROOT_URL, self.CURRENT_GAME_URL, platform, summonerId])
        payload = {'api_key': self.API_KEY}
        response = requests.get(url, params=payload)
        print response
        print response.json()
        print'Received response from url: %r' % response.url
        return response.json()



class RegionError(Exception):
    def __init__(self, region):
        self.region = region

    def __str__(self):
        return repr('The requested region: %r is not a valid region'.format(self.region))


class PlatformError(Exception):
    def __init__(self, platform):
        self.platform = platform

    def __str__(self):
        return repr('The requested platform: %r is not a valid platform'.format(self.platform))


class SummonerNotFoundError(Exception):
    def __init__(self, summonerName ,region):
        self.summonerName = summonerName
        self.region = region

    def __str__(self):
        return repr('The Summoner name %r was not found in the specified region: %r' % (self.summonerName, self.region))
