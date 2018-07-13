from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(app, db_name):
    """Connect to database"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + db_name
    app.config['SQLALCHEMY_ECHO'] = True
    db.app=app
    db.init_app(app)


class Restaurants(db.Model):
    """Stores restaurants info."""  

    __tablename__ = 'places'

    yelp_id = db.Column(db.Integer, primary_key = True,)
    name=db.Column(db.String(100), nullable=False,)

    ratings = db.relationship('Rating')
    saved = db.relationship('Saved_places')

    def __repr__(self):
        return '< {}>'.format(self.name)


class Rating(db.Model):
    """Stores rating information."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score=db.Column(db.Float, nullable=False,)
    yelp_id=db.Column(db.Integer, db.ForeignKey('places.yelp_id'))
    num_vegan_dishes=db.Column(db.Integer, nullable=True,)

    places = db.relationship('Restaurants')
    user = db.relationship('User')

    def __repr__(self):
        return '< Rating %r>' % self.score


class User(db.Model):
    """Stores uer information."""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    name=db.Column(db.String(100), nullable=False,)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_id


class Saved_places(db.Model):
    """Stores date and places that have been saved by user."""

    __tablename__ = 'saved'

    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True,)
    yelp_id=db.Column(db.Integer, db.ForeignKey('places.yelp_id'))
    save_date=db.Column(db.Date, nullable=False,)

    places = db.relationship('Restaurants')

    def __repr__(self):
        return '<Saved_places %r>' % self.save_date


if __name__ == '__main__':
    
    from server import app
    connect_to_db(app, 'my_data')
    print("Connected to DB.")


















