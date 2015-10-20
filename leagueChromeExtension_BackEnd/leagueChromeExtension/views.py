from leagueChromeExtension import app, db
from leagueChromeExtension.models import Summoner
from leagueChromeExtension.riotApi import riotApi, RegionError, SummonerNotFoundError

@app.route('/')
def index():
    return {'hello': 'world',
            'name': 'jeff'}


@app.route('/summonerId/<summonerName>', methods=['GET'])
def getId(summonerName):
    summoner = Summoner.query.filter_by(summonerNameTrim=summonerName.lower().replace(" ", "")).first()
    if summoner is None:
        try:
            riotApiHelper = riotApi()
            response = riotApiHelper.getSummonerIdFromName(summonerName, "na")
            newSummoner = Summoner(response['name'], response['name'].lower().replace(" ", ""), response['id'])
            db.session.add(newSummoner)
            db.session.commit()
            response['Message'] = "Found through API and added to database"
            response['Error'] = False
            return response
        except (RegionError, SummonerNotFoundError) as e:
            return {'Message': str(e),
                    'Error': True}
    else:
        return {'Message': 'Found in database',
                'Error': False,
                'summonerId': summoner.summonerId,
                'summonerName': summoner.summonerName}


@app.route('/ingameInfo/<summonerId>', methods=['GET'])
def getIngameInfor(summonerId):
    riotApiHelper = riotApi()
    return riotApiHelper.getCurrentGameInfo(summonerId, "NA1")