from project import db 
import datetime
from math import sin, cos, sqrt, atan2, radians

class Party(db.Model):
  
  __tablename__ = 'parties'

  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.Text)
  instructions = db.Column(db.Text)
  date = db.Column(db.DATE)
  time = db.Column(db.TIME)
  cost = db.Column(db.Numeric)
  host_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
  attendee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  distance = None
  # distance is used by the distance method to transport data
  #### it is never meant to be commited to the database as it
  #### is relative the the lat/lng submitted to the method.
  # host_rating = db.Column(db.Integer)
  # attendee_rating = db.Column(db.Integer)

  def __init__(self, description, host_id, cost, date, time, instructions=""):
    self.description = description
    self.host_id = host_id
    self.cost = cost
    self.date = date
    self.time = time
    self.instructions = instructions

  def distance(lat,lng,within = 100, qty=10):
    d = datetime.date.isoformat(datetime.date.today())
    parties = Party.query.filter(Party.date >= d)

    my_list = []
    for party in parties:
      # approximate radius of earth in km
      R = 6373.0

      lat1 = radians(float(lat))
      lon1 = radians(float(lng))
      lat2 = radians(float(party.host.latitude))
      lon2 = radians(float(party.host.longitude))

      dlon = lon2 - lon1
      dlat = lat2 - lat1

      a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
      c = 2 * atan2(sqrt(a), sqrt(1 - a))
      distance = R * c
      party.distance = format(distance, '.2f')
      my_list.append(party)

    # users.sort(key=lambda user: user.steamID)
    my_list.sort(key=lambda x: x.distance )
    return my_list[:qty:]


  def __repr__(self):
    return "{} -{}".format(self.description, self.host_id)







