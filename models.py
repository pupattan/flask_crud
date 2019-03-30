from config import db


class Team(db.Model):
    id = db.Column('identifier', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80), nullable=False)
    logo_uri = db.Column('logoUri', db.String(2048))

    def __str__(self):
        return '{}'.format(self.name)

    def as_dict(self):
        return {
            'identifier': self.id,
            'name': self.name,
            'logoUri': '<img src="{}" height="30" width="30"></img>'.format(self.logo_uri),
        }


class Player(db.Model):
    id = db.Column('identifier', db.Integer, primary_key=True)
    firstname = db.Column('firstName', db.String(80), nullable=False)
    lastname = db.Column('lastName', db.String(80))
    image_uri = db.Column('imageUri', db.String(2048))
    team_id = db.Column(db.Integer, db.ForeignKey('team.identifier'), nullable=False)

    def __str__(self):
        return '{}'.format(self.firstname)

    def as_dict(self):
        return {
            'identifier': self.id,
            'firstName': self.firstname,
            'lastName': self.lastname,
            'imageUri': '<img src="{}" height="30" width="30"></img>'.format(self.image_uri),
            'team_id': self.team_id,
        }