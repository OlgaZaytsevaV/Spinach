db = SQLAlchemy()

def connect_to_db(app, db_name):
    """Connect to database"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql':///' + db_name
    app.config['SQLALCHEMY_ECHO'] = True
    db.app=app
    db.init_app(app)

    connect_to_db(app, 'web')


class Restaurants(db.Model):
    """Restaurants info"""  

    __tablename__ = 'places'

    yelp_id = db.Column(db.Integer, primary_key = True,)
    name=db.Column(db.String(100), nullable=False,)

class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    user_id=db.Column(db.Integer, Foreignkey=True, nullable=False,)
    score=db.Column(db.Integer, nullable=False,)
    yelp_id=db.Column(db.Integer, Foreignkey = True, nullable=False,)
    num_vegan_dishes=db.Column(db.Integer, nullable=True,)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
    name=db.Column(db.String(100), nullable=False,)
    email = db.Column(db.String(100), nullable=False,)


class Saved_places(db.Model):
    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True,)
    yelp_id=db.Column(db.Integer, Foreignkey=False, nullable=False,)
    save_date=db.Column(db.DateTime, nullable=False,)
             
    