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
    def __str__(self):
        return 'The Summoner name was not found in the specified region'


class SummonerNotInGameError(Exception):
    def __str__(self):
        return 'The Summoner name was found but is currently not in an active game'


class UnauthorizedError(Exception):
    def __str__(self):
        return 'The request was unauthorized, perhaps the api key has expired or the REST url is malformed'


class LimitExceededError(Exception):
    def __str__(self):
        return 'The calls for this api key has exceeded the limit'


class ServerError(Exception):
    def __str__(self):
        return 'The riot api server has crashed'


class ServiceUnavailable(Exception):
    def __str__(self):
        return 'The riot server is currently unavailable'


class HttpResponseErrorHandler:
    common_mapping = {
        401: UnauthorizedError(),
        429: LimitExceededError(),
        500: ServerError(),
        503: ServiceUnavailable()
    }

    def __init__(self, code, api):
        if api == "gameInfo" and code == 404:
            raise SummonerNotInGameError()
        elif api == "summonerInfo" and code == 404:
            raise SummonerNotFoundError()
        else:
            raise self.common_mapping[code]
