from leagueChromeExtension import db


class Twitchuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    summoners = db.relationship('Summoner', backref='twitchuser', lazy='dynamic')

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<TwitchUser ID %r>' % self.username


class Summoner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summonerName = db.Column(db.String(16))
    summonerNameTrim = db.Column(db.String(16))
    summonerId = db.Column(db.Integer)

    twitchuser_id = db.Column(db.Integer, db.ForeignKey('twitchuser.id'))

    def __init__(self, summonerName, summonerNameTrim, summonerId):
        self.summonerName = summonerName
        self.summonerNameTrim = summonerNameTrim
        self.summonerId = summonerId

    def __repr__(self):
        return '<Summoner %r: ID %d>' % (self.summonerName, self.summonerId)
