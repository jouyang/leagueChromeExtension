from leagueChromeExtension import db


class Summoner(db.Model):
    __tablename__ = 'Summoner'
    summonerId = db.Column(db.Integer, primary_key=True)
    aliases = db.relationship('SummonerNames', backref='summoner', lazy='dynamic')
    twitch_username = db.Column(db.String(20), unique=True)

    def __repr__(self):
        if not self.twitch_username:
            return '<Summoner ID: {0} >'.format(self.summonerId)
        else:
            return '<Summoner ID: {0} | Twitch Username: {1}>'.format(self.summonerId, self.twitch_username)


class SummonerNames(db.Model):
    __tablename__ = 'SummonerNames'
    summonerName = db.Column(db.String(16), primary_key=True)
    summonerId = db.Column(db.Integer, db.ForeignKey('Summoner.summonerId'))
    summonerNameTrim = db.Column(db.String(16), unique=True)

    def __repr__(self):
        return '<Summoner Name: {0} >'.format(self.summonerName)
