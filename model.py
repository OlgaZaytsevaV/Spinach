from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_to_db(app, db_name):
    """Connect to database"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + db_name
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app=app
    db.init_app(app)


class Restaurants(db.Model):
    """Stores restaurants info."""  

    __tablename__ = 'places'

    yelp_id = db.Column(db.String(100), primary_key = True,)
    name = db.Column(db.String(100), nullable=False,)

    ratings = db.relationship('Rating')
    saved = db.relationship('Saved_places')

    def __repr__(self):
        return '< {}>'.format(self.name)


class Rating(db.Model):
    """Stores rating information."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    saved_place_id=db.Column(db.Integer, db.ForeignKey('saved.saved_place_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score=db.Column(db.Float, nullable=False,)
    yelp_id=db.Column(db.String(25), db.ForeignKey('places.yelp_id'))
    num_vegan_dishes=db.Column(db.Integer, nullable=True,)

    place = db.relationship('Restaurants')
    saved = db.relationship('Saved_places')
    user = db.relationship('User')

    def __repr__(self):
        return '{} {} {} {}'.format(self.score, self.yelp_id, self.user_id, self.saved_place_id)


class User(db.Model):
    """Stores uer information."""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    name=db.Column(db.String(100), nullable=False,)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    saved = db.relationship('Saved_places')
    ratings=db.relationship('Rating')


    def __repr__(self):
        return '<User %r>' % self.user_id


class Saved_places(db.Model):
    """Stores date and places that have been saved by user."""

    __tablename__ = 'saved'

    saved_place_id=db.Column(db.Integer, primary_key=True, autoincrement=True,)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    yelp_id=db.Column(db.String(25), db.ForeignKey('places.yelp_id'))
    save_date=db.Column(db.Date, nullable=False,)

    rating=db.relationship('Rating', uselist=False)
    place = db.relationship('Restaurants')
    user= db.relationship('User')

    def __repr__(self):
        return '<Saved_places %r>' % self.save_date



def example_data():
    #Create some sample data"
    #In case if this run more then once, empty out existing data
    # Restaurants.query.delete()
    # Rating.query.delete()
    # User.query.delete()
    # Saved_places.query.delete()

    d = datetime.now()
    save_date=(d.strftime("%A, %B, %d, %Y"))

    #table Places:
    place_1= Restaurants(yelp_id = "1inirbvir", name="Name_1")
    place_2= Restaurants(yelp_id = "534262890", name="Name_2")
    place_3= Restaurants(yelp_id = "124354567", name="Name_3")

    #table User:

    user_1 = User(name='Olga', email='olg@gmail.com', password="123")
    user_2 = User(name='Vic', email='Vic@gmail.com', password="12")
    user_3 = User(name='Andres', email='andres@gmail.com', password="321")

    #table Saved_places:
    saved_place_1 =Saved_places(user=user_1, place=place_1,
                                save_date=save_date)
    saved_place_2 =Saved_places(user=user_2, place=place_1,
                                save_date=save_date)
    saved_place_3 =Saved_places(user=user_3, place=place_2,
                                save_date=save_date)
    saved_place_4 =Saved_places(user=user_1, place=place_3,
                                save_date=save_date)

    # table Ratings:

    rating_1 = Rating(score="3", user=user_1, place=place_1, 
                       saved=saved_place_1)
    rating_2 = Rating(score="4",  user=user_2, place=place_1,
                        saved=saved_place_2)
    rating_3 = Rating(score="2",  user=user_3, place=place_2,
                       saved=saved_place_3)
    rating_4 = Rating(score="3",  user=user_1, place=place_3,
                       saved=saved_place_4)
    

    db.session.add_all([place_1, place_2, place_3, user_1, user_2, user_3, 
                        saved_place_1, saved_place_2, saved_place_3,
                        saved_place_4, rating_1, rating_2, rating_3, rating_4])
    db.session.commit()



if __name__ == '__main__':
    db_name = "testdb"
    from server import app
    connect_to_db(app, db_name)
    db.create_all()
    print("Connected to DB.")


















