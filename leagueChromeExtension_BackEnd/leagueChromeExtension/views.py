from leagueChromeExtension import app, db
from leagueChromeExtension.models import Summoner
from leagueChromeExtension_BackEnd.riotApi.core import riotApi


@app.route('/')
def index():
    return {'hello': 'world'}


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
            response['summonerId'] = response['id']
            return response
        except Exception as e:
            return {'Message': str(e),
                    'Error': True}
    else:
        return {'Message': 'Found in database',
                'Error': False,
                'summonerId': summoner.summonerId,
                'summonerName': summoner.summonerName}


@app.route('/ingameInfo/by-name/<summonerName>', methods=['GET'])
def getIngameInfoName(summonerName):
    # Get the summoner id through getId API
    id = getId(summonerName)
    if id['Error']:
        # If there is an error from the API then return the error json
        return id
    else:
        return getIngameInfoId(str(id['summonerId']))


@app.route('/ingameInfo/by-id/<summonerId>', methods=['GET'])
def getIngameInfoId(summonerId):
    riotApiHelper = riotApi()
    try:
        return riotApiHelper.getCurrentGameInfo(summonerId, "NA1")
    except Exception as e:
        return {'Message': str(e),
                'Error': True}
