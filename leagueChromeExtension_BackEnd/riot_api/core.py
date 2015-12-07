import requests
import json
import os
from leagueChromeExtension import app
from exceptions import *


class RiotApi:
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
        pwd = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(pwd, 'static', 'runes.json')
        with open(file_path) as runes_file:
            self.RUNEDATA = json.load(runes_file)

        file_path = os.path.join(pwd, 'static', 'masteries.json')
        with open(file_path) as masteries_file:
            self.MASTERYDATA = json.load(masteries_file)

    # Sample:https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/jouyang?api_key=[]
    def get_summoner_id_from_name(self, summonerName, region):
        # Check for valid region
        if region not in self.REGIONS:
            raise RegionError(region)

        # Setup get url and api key
        url = '/'.join([self.ROOT_URL, self.SUMMONER_API_PLATFORM, region, self.SUMMONER_API_VERSION, self.SUMMONER_API,
                        'by-name', summonerName])
        payload = {'api_key': self.API_KEY}
        response = requests.get(url, params=payload)

        # The returned json uses lower case, space-stripped summoner names as keys to summoner info
        print 'Received response from url: %r' % response.url
        if response.status_code == 200:
            responseJson = response.json()
            for key in responseJson:
                summonerName = key
                return responseJson[summonerName]
        else:
            HttpResponseErrorHandler(response.status_code, 'summonerInfo', region)

    # Sample:https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/44979352?api_key=[]
    def get_current_game_info(self, summonerId, platform):
        # Check for valid region
        if platform not in self.PLATFORMS:
            raise PlatformError(platform)

        # Setup get url and api key
        url = '/'.join([self.ROOT_URL, self.CURRENT_GAME_URL, platform, summonerId])
        payload = {'api_key': self.API_KEY}
        response = requests.get(url, params=payload)
        print'Received response from url: %r' % response.url
        if response.status_code == 200:
            return self.game_info_filter(response.json(), summonerId)
        else:
            HttpResponseErrorHandler(response.status_code, 'gameInfo', summonerId)

    def game_info_filter(self, gameInfo, summonerId):
        for participant in gameInfo['participants']:
            if str(participant['summonerId']) == summonerId:
                return {'masteries': map(self.masteries_info_detail_local, participant['masteries']),
                        'runes': map(self.rune_info_details_local, participant['runes']),
                        'championId': participant['championId'],
                        'summonerName': participant['summonerName'],
                        'summonerId': participant['summonerId']}

    # Sample: https://global.api.pvp.net/api/lol/static-data/na/v1.2/rune/5273?runeData=all&api_key=[]
    def runes_info_detail(self, runes):
        rune_list = []
        for rune in runes:
            url = '/'.join([self.STATIC_DATA_URL, 'rune', str(rune['runeId'])])
            payload = {'api_key': self.API_KEY, 'runeData': 'all'}
            response = requests.get(url, params=payload)
            print 'Received response from url: %r' % response.url

            if response.status_code == 200:
                rune_info = {}
                full_rune_info = response.json()
                rune_info['description'] = full_rune_info['sanitizedDescription']
                rune_info['imageInfo'] = full_rune_info['image']
                rune_info['name'] = full_rune_info['name']
                rune_info['details'] = full_rune_info['rune']
                rune_info['stats'] = full_rune_info['stats']
                rune_info['amount'] = rune['count']
                rune_list.append(rune_info)
            else:
                HttpResponseErrorHandler(response.status_code, 'runeInfo', rune['runeId'])

        return rune_list

    def rune_info_details_local(self, rune):
        id = rune['runeId']
        rune_info = {}
        full_rune_info = self.RUNEDATA['data'][str(id)]
        rune_info['description'] = full_rune_info['sanitizedDescription']
        rune_info['imageInfo'] = full_rune_info['image']
        rune_info['name'] = full_rune_info['name']
        rune_info['details'] = full_rune_info['rune']
        rune_info['stats'] = full_rune_info['stats']
        rune_info['amount'] = rune['count']
        return rune_info

    # Sample: https://global.api.pvp.net/api/lol/static-data/na/v1.2/6111?masteryData=all&api_key=[]
    def masteries_info_detail(self, masteries):
        mastery_list = []
        for mastery in masteries:
            url = '/'.join([self.STATIC_DATA_URL, 'mastery', str(mastery['masteryId'])])
            payload = {'api_key': self.API_KEY, 'masteryData': 'all'}
            response = requests.get(url, params=payload)
            print 'Received response from url: ' + response.url
            print response.json()
            if response.status_code == 200:
                mastery_info = {}
                full_mastery_info = response.json()
                mastery_info['rank'] = full_mastery_info['ranks']
                mastery_info['id'] = full_mastery_info['id']
                mastery_info['description'] = full_mastery_info['description']
                mastery_info['name'] = full_mastery_info['name']
                mastery_info['imageInfo'] = full_mastery_info['image']
                mastery_info['prereq'] = full_mastery_info['prereq']
                mastery_info['masteryTree'] = full_mastery_info['masteryTree']
                mastery_list.append(mastery_info)
            else:
                HttpResponseErrorHandler(response.status_code, 'masteryInfo', mastery['masteryId'])

        return mastery_list

    def masteries_info_detail_local(self, mastery):
        mastery_info = {}
        full_mastery_info = self.MASTERYDATA['data'][str(mastery['masteryId'])]
        mastery_info['rank'] = full_mastery_info['ranks']
        mastery_info['id'] = full_mastery_info['id']
        mastery_info['description'] = full_mastery_info['description']
        mastery_info['name'] = full_mastery_info['name']
        mastery_info['imageInfo'] = full_mastery_info['image']
        mastery_info['prereq'] = full_mastery_info['prereq']
        mastery_info['masteryTree'] = full_mastery_info['masteryTree']
        return mastery_info