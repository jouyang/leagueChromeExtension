class RegionError(Exception):
    def __init__(self, region):
        self.region = region

    def __str__(self):
        return 'The requested region: %r is not a valid region'.format(self.region)


class PlatformError(Exception):
    def __init__(self, platform):
        self.platform = platform

    def __str__(self):
        return 'The requested platform: %r is not a valid platform'.format(self.platform)


class SummonerNotFoundError(Exception):
    def __init__(self, summonorName):
        self.summnorName = summonorName

    def __str__(self):
        return '404: The Summoner name was not found in the specified region: %s' % self.summnorName


class SummonerNotInGameError(Exception):
    def __init__(self, summonerId):
        self.summonerId = summonerId

    def __str__(self):
        return '404: The Summoner name was found but is currently not in an active game: %s' % self.summonerId


class RuneNotFoundError(Exception):
    def __init__(self, runeId):
        self.runeId = runeId

    def __str__(self):
        return '404: The rune information for the requested rune Id was not found: %d' % self.runeId


class MasteryNotFoundError(Exception):
    def __init__(self, masteryId):
        self.masteryId = masteryId

    def __str__(self):
        return '404: The mastery information for the requested mastery Id was not found: %d' % self.masteryId


class UnauthorizedError(Exception):
    def __str__(self):
        return '401 UnauthorizedError: The request was unauthorized, perhaps the api key has expired or the REST url is malformed'


class LimitExceededError(Exception):
    def __str__(self):
        return '429 LimitExceededError: The calls for this api key has exceeded the limit'


class ServerError(Exception):
    def __str__(self):
        return '500 ServerError: The riot api server has crashed'


class ServiceUnavailable(Exception):
    def __str__(self):
        return '503 ServiceUnavailable: The riot server is currently unavailable'


class HttpResponseErrorHandler:
    common_mapping = {
        401: UnauthorizedError(),
        429: LimitExceededError(),
        500: ServerError(),
        503: ServiceUnavailable()
    }

    def __init__(self, code, api, param):
        if api == 'gameInfo' and code == 404:
            raise SummonerNotInGameError(param)
        elif api == 'summonerInfo' and code == 404:
            raise SummonerNotFoundError(param)
        elif api == 'runeInfo' and code == 404:
            raise RuneNotFoundError(param)
        elif api == 'masteryInfo' and code == 404:
            raise MasteryNotFoundError(param)
        else:
            if code in self.common_mapping:
                raise self.common_mapping[code]
            else:
                raise Exception('Unhandled response code: %d in api: %s' % (code, api))
