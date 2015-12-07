from leagueChromeExtension import app, db
from leagueChromeExtension.models import Summoner, SummonerNames
from riot_api.core import RiotApi


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route("/get/summonerId/<summonerName>", methods=["GET"])
def get_summoner_Id(summonerName):
    print "Retrieving summoner ID for: {0}".format(summonerName)
    cleanSummonerName = summonerName.replace(" ", "").lower()
    summonerEntry = SummonerNames.query.filter_by(summonerNameTrim=cleanSummonerName).first()
    if summonerEntry is None:
        try:
            riotApiHelper = RiotApi()
            response = riotApiHelper.get_summoner_id_from_name(summonerName, "na")
            newSummoner = Summoner(summonerId=response["id"])
            newSummonerName = SummonerNames(summonerName=response["name"], summonerNameTrim=cleanSummonerName,
                                            summoner=newSummoner)
            db.session.add(newSummoner)
            db.session.add(newSummonerName)
            db.session.commit()
            response['Message'] = "Found through API and added to database"
            response['Error'] = False
            response['summonerId'] = response['id']
            return response
        except Exception as e:
            return {'Message': unicode(e).encode("utf-8"),
                    'Error': True}
    else:
        return {'Message': 'Found in database',
                'Error': False,
                'summonerId': summonerEntry.summoner.summonerId,
                'summonerName': summonerEntry.summonerName}


@app.route('/get/ingameInfo/by-name/<summonerName>', methods=['GET'])
def get_In_game_Info_Name(summonerName):
    # Get the summoner id through getId API
    print "Retrieving summoner in game info for summoner: {0}".format(summonerName)
    summoner = get_summoner_Id(summonerName)
    if summoner['Error']:
        # If there is an error from the API then return the error json
        return summoner
    else:
        print summoner
        return getIngameInfoId(str(summoner['summonerId']))


@app.route('/get/ingameInfo/by-id/<summonerId>', methods=['GET'])
def getIngameInfoId(summonerId):
    print "Retrieving summoner in game info for summoner id: {0}".format(summonerId)
    riotApiHelper = RiotApi()
    try:
        return riotApiHelper.get_current_game_info(summonerId, "NA1")
    except Exception as e:
        return {'Message': unicode(e).encode("utf-8"),
                'Error': True}
