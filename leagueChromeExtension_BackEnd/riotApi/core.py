import requests
import json
import os
from leagueChromeExtension import app
from exceptions import *
from pprint import pprint


class riotApi:
    ROOT_URL = 'https://na.api.pvp.net'
    CURRENT_GAME_URL = 'observer-mode/rest/consumer/getSpectatorGameInfo'
    STATIC_DATA_URL = 'https://global.api.pvp.net/api/lol/static-data/na/v1.2'
    SUMMONER_API_PLATFORM = 'api/lol'
    SUMMONER_API = 'summoner'
    SUMMONER_API_VERSION = 'v1.4'
    REGIONS = ['br', 'eune', 'euw', 'kr', 'lan', 'las', 'na', 'oce', 'ru', 'tr']
    PLATFORMS = ['NA1', 'BR1', 'LA1', 'LA2', 'OC1', 'EUN1', 'TR1', 'RU', 'EUW1', 'KR']
    API_KEY = app.config['RIOT_API_KEY']

    def __init__(self):
        # with open(app.config['STATIC_DIRECTORY'] + 'runes.json') as runes_file:
        pwd = os.path.dirname(os.path.realpath(__file__))
        filePath = os.path.join(pwd, 'static', 'runes.json')
        with open(filePath) as runes_file:
            self.RUNEDATA = json.load(runes_file)

        filePath = os.path.join(pwd, 'static', 'masteries.json')
        with open(filePath) as masteries_file:
            self.MASTERYDATA = json.load(masteries_file)

    # Sample:https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/jouyang?api_key=[]
    def getSummonerIdFromName(self, summonerName, region):
        # Check for valid region
        if region not in self.REGIONS:
            raise RegionError(region)

        # Setup get url and api key
        url = '/'.join([self.ROOT_URL, self.SUMMONER_API_PLATFORM, region, self.SUMMONER_API_VERSION, self.SUMMONER_API, 'by-name', summonerName])
        payload = {'api_key': self.API_KEY}
        response = requests.get(url, params=payload)

        # The returned json uses lower case, space-stripped summoner names as keys to summoner info
        print 'Received response from url: %r' % response.url
        if response.status_code == 200:
            return response.json()[summonerName.lower().replace(' ', '')]
        else:
            HttpResponseErrorHandler(response.status_code, 'summonerInfo', summonerName)

    # Sample:https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/44979352?api_key=[]
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
            HttpResponseErrorHandler(response.status_code, 'gameInfo', summonerId)

    def gameInfoFilter(self, gameInfo, summonerId):
        for participant in gameInfo['participants']:
            if str(participant['summonerId']) == summonerId:
                return {'masteries': map(self.masteriesInfoDetailsLocal, participant['masteries']),
                        'runes': map(self.runesInfoDetailsLocal, participant['runes']),
                        'championId': participant['championId'],
                        'summonerName': participant['summonerName'],
                        'summonerId': participant['summonerId']}

    # Sample: https://global.api.pvp.net/api/lol/static-data/na/v1.2/rune/5273?runeData=all&api_key=[]
    def runesInfoDetails(self, runes):
        runeList = []
        for rune in runes:
            url = '/'.join([self.STATIC_DATA_URL, 'rune', str(rune['runeId'])])
            payload = {'api_key': self.API_KEY, 'runeData': 'all'}
            response = requests.get(url, params=payload)
            print 'Received response from url: %r' % response.url

            if response.status_code == 200:
                runeInfo = {}
                fullRuneInfo = response.json()
                runeInfo['description'] = fullRuneInfo['sanitizedDescription']
                runeInfo['imageInfo'] = fullRuneInfo['image']
                runeInfo['name'] = fullRuneInfo['name']
                runeInfo['details'] = fullRuneInfo['rune']
                runeInfo['stats'] = fullRuneInfo['stats']
                runeInfo['amount'] = rune['count']
                runeList.append(runeInfo)
            else:
                HttpResponseErrorHandler(response.status_code, 'runeInfo', rune['runeId'])

        return runeList

    def runesInfoDetailsLocal(self, rune):
        id = rune['runeId']
        fullRuneInfo = self.RUNEDATA['data'][str(id)]
        runeInfo = {}
        runeInfo['description'] = fullRuneInfo['sanitizedDescription']
        runeInfo['imageInfo'] = fullRuneInfo['image']
        runeInfo['name'] = fullRuneInfo['name']
        runeInfo['details'] = fullRuneInfo['rune']
        runeInfo['stats'] = fullRuneInfo['stats']
        runeInfo['amount'] = rune['count']
        return runeInfo

    # Sample: https://global.api.pvp.net/api/lol/static-data/na/v1.2/mastery/4124?masteryData=all&api_key=[]
    def masteriesInfoDetails(self, masteries):
        masteryList = []
        for mastery in masteries:
            url = '/'.join([self.STATIC_DATA_URL, 'mastery', str(mastery['masteryId'])])
            payload = {'api_key': self.API_KEY, 'masteryData': 'all'}
            response = requests.get(url, params=payload)
            print 'Received response from url: ' + response.url
            print response.json()
            if response.status_code == 200:
                masteryInfo = {}
                fullMasteryInfo = response.json()
                masteryInfo['rank'] = fullMasteryInfo['ranks']
                masteryInfo['id'] = fullMasteryInfo['id']
                masteryInfo['description'] = fullMasteryInfo['description']
                masteryInfo['name'] = fullMasteryInfo['name']
                masteryInfo['imageInfo'] = fullMasteryInfo['image']
                masteryInfo['prereq'] = fullMasteryInfo['prereq']
                masteryInfo['masteryTree'] = fullMasteryInfo['masteryTree']
                masteryList.append(masteryInfo)
            else:
                HttpResponseErrorHandler(response.status_code, 'masteryInfo', mastery['masteryId'])

        return masteryList

    def masteriesInfoDetailsLocal(self, mastery):
        id = mastery['masteryId']
        masteryInfo = {}
        fullMasteryInfo = self.MASTERYDATA['data'][str(id)]
        masteryInfo['rank'] = fullMasteryInfo['ranks']
        masteryInfo['id'] = fullMasteryInfo['id']
        masteryInfo['description'] = fullMasteryInfo['description']
        masteryInfo['name'] = fullMasteryInfo['name']
        masteryInfo['imageInfo'] = fullMasteryInfo['image']
        masteryInfo['prereq'] = fullMasteryInfo['prereq']
        masteryInfo['masteryTree'] = fullMasteryInfo['masteryTree']
        return masteryInfo


    # TODO: Make internal helper functions that grabs the data of the champion, runes, mastery data and image links
