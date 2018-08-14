
from flask import jsonify
from sys import argv
import requests
from pprint import pprint, pformat
import os
from datetime import datetime
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Restaurants, Saved_places, connect_to_db, db
app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "SECRET"

YELP_URL = 'https://api.yelp.com/v3/businesses/'
API_KEY = os.environ['API_KEY']
app.jinja_env.undefined = StrictUndefined
# GOOGLE_MAPS_URL = "https://www.google.com/maps/embed/v1/js?key=API_KEY_GOOGLE"
# API_KEY_GOOGLE = os.environ['API_KEY_GOOGLE']


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/sign_up', methods=['GET'])
def show_sign_up_form():
    """Shows sign up form."""

    return render_template('sign_up.html') 


@app.route('/sign_up', methods=['POST'])  
def  submit_sign_up_form():
    """ Submits sign up form."""

    name = request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')

    if User.query.filter_by(email=email).first():
        flash("User with this email already exists.")
        return redirect('/')
    else:
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("User added to database. Please log in.")
        return redirect('/login')


@app.route('/login', methods =['GET'])
def show_login_form():
    """Shows log in form."""
    
    return render_template('login.html')


@app.route('/login', methods =['POST'])   
def submit_login_form():
    """Submits login form."""

    email=request.form.get('email')
    password=request.form.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    print(user)
    if user:
        session['user_id'] = user.user_id
        return redirect('/')
    else:
        flash("User with email does not exist please sign up.")
        return redirect('/sign_up')
    

@app.route('/my_account') 
def show_form():
    """User's page"""
   
    name = request.args.get('name')
    user = User.query.get(session['user_id'])
  
    return render_template('my_account.html', user=user, ratings=user.ratings)
       

@app.route('/save', methods=["POST"])   
def save_places():
    """Route to save places on the user's page"""

    yelp_id=request.form.get('yelp_id')
    name = request.form.get('name')
    user = User.query.get(session['user_id'])
    print(request.form)

    # check if restaurant in db and create it if not    
    restaurant = Restaurants.query.get(yelp_id)
    print("################## restaurant_is saved to db")
    if restaurant is None:
        restaurant = Restaurants(yelp_id=yelp_id, name=name)
        print("################ restaurant is not saved to db")
        db.session.add(restaurant) 

    # saving a restautant to saved table    
    #1. we query to check if it saved to the table saved:
    new_saved_place = Saved_places.query.filter_by(yelp_id=yelp_id, user_id=user.user_id).first()
    print("########################")
    print("######## place is saved in Saved")
    print(new_saved_place)
    print("####### place is saved in Saved")

    #2. if it not saved to the table "saved":
    if new_saved_place is None:
        d=datetime.now()
        save_date=(d.strftime("%A, %B, %d, %Y"))
        new_saved_place = Saved_places(place=restaurant, user=user, save_date=save_date)
        print("########################")
        print("########## wasn't in  Saved")
        print(new_saved_place)
        print("########## wasn't in  Saved")
        places = user.saved
        db.session.add(new_saved_place)
        db.session.commit()        
        print('###################')
        print(places)
        print('###################')
        return "The place was saved to your account"

    else:
        return " It already exists in your account"   


@app.route('/ratings', methods=['POST'])  
def save_rating():
    """Rout to create retings for saved places"""

    yelp_id=request.form.get('yelp_id')
    name = request.form.get('name')
    score = request.form.get('rating')
    user = User.query.get(session['user_id'])
    print("###########lalalal")
    print(score)
    print("###########lalalla")

    #check if place is saved, if not create :
    restaurant = Restaurants.query.get(yelp_id)
    print("###########exists")
    print(restaurant)
    print("##########exists")
    if restaurant is None:
        restaurant = Restaurants(yelp_id=yelp_id, name=name)
        print("######## new")
        print(restaurant)
        print("########### new")
        db.session.add(restaurant)
        db.session.commit()
    print("#########") 
    print(restaurant) 
    print("#########s")     
    saved_place = Saved_places.query.filter_by(yelp_id=yelp_id, user_id=user.user_id).first()
    print(saved_place)
    print("##########exists in saved table")
    if saved_place is None:
        d=datetime.now()
        save_date=(d.strftime("%A, %B, %d, %Y"))
        saved_place = Saved_places(user=user, place=restaurant, save_date=save_date)
        db.session.add(saved_place)
        db.session.commit()
        print("##########create a new saved place ")
        print(saved_place)
    print(saved_place)
    print("##########")

    # create score
    #1. Check if it is in DB already:
    rating = Rating.query.filter_by(yelp_id=yelp_id, user=user).first()
    print("############ score")
    print(rating)
    print("############# score")
    if rating is None:
        #db.session.add_all([restaurant, user, saved_place])

        rating = Rating(score=score, place=restaurant, user=user, saved=saved_place)
        db.session.add(rating)
        db.session.commit()
        print("########## rating obj")
        print(rating)
    else:
        rating.score = score
        print("######### rating.score")
        print(rating.score)
        return "You have rated this place already"  
    return "Rating is submited"
    
    db.session.commit()
    print(rating)
  
    return "Rating added"    

            
@app.route('/logout')
def logout():
    """Logout seccion"""
    if 'user_id' in session:
        session.pop('user_id', None)
        flash('You are now logged out')
        return redirect('/')
    else:
        flash('You are not logged in')
        return redirect('/')    


def search_helper(term, location):
    """Uses external API to get search results"""
    params = { 
               'term': term,
               'location': location,
               }   
       
    headers = {'Authorization': 'Bearer ' + API_KEY}
    response = requests.get(YELP_URL + 'search?categories=vegan,vegetarian',
                               params=params,
                               headers=headers)
    if response.ok:
        return response.json()
    else:
        return None
   
   
@app.route('/search')
def show_results():
    """Shows search results in json."""

    search = request.args.get('search')
    query = request.args.get('query')
    address=request.args.get('address')
    if search:
        data = search_helper(search, address)   
        print(data.keys()) 
        if data: 
           
            for i in data['businesses']:
                print("########tata")
                # print(data['businesses'])
                print(i['image_url'])
                print(i['coordinates'])
                print(type(i['coordinates']['latitude']))
                print(i['coordinates']['longitude'])
            places = data['businesses']
            print(type(places))
           
        else:
            places = []
        return render_template("search.html", places=places,
                               data=pformat(data))  
                                


def results_helper(yelp_id, name):
    """Uses external API to get results based in yelp_id and name of the place"""

    headers = {'Authorization': 'Bearer ' + API_KEY}
    response = requests.get(YELP_URL + yelp_id,
                            headers=headers)

    if response.ok:
        return response.json()
    else:
        return None
   

@app.route('/results')    
def show_indiv_result():
    """Route for rendering businesses ditails of the place"""
    
    yelp_id = request.args.get('id')
    name = request.args.get('name') 
    data = results_helper(yelp_id, name)   
    print(data.keys()) 
    if data:
        hours_operations = data['hours'][0]['open']
        hours_strings = []

        for i in hours_operations:
            if i != False:
                if i['day'] == 1:
                    i['day']='Mon'
                elif i['day'] == 2:
                    i['day']='Tue'
                elif i['day'] == 3:
                    i['day']='Wed'
                elif i['day'] == 4:
                    i['day']='Thu'
                elif i['day'] == 5:
                    i['day']='Fri' 
                elif i['day'] == 6:
                    i['day']='Sat'
                elif i['day'] == 0:
                    i['day']='Sun' 
                print(i['day'], i['start'], i['end']) 
                print(type(i['day'])) 

        days={}
        d=data['hours'][0]['open']
        for i in d:
            day=i['day']
            start=i['start']
            end=i['end']
            end = int(i['end'])
            start = int(i['start'])
            if start > 1200:
                start= int((start - 1200)/100)
            else:
                start=int(start/100)
            if end > 1200:
                end = int((end - 1200)/100)
            else:
                end=int(end/100)
            if day not in days:
                days[day]={}
                days[day]['hours']=[]
                days[day]['hours'].append((start, end))
            else:
                days[day]['hours'].append((start, end))
        print(days)    

        yelp_id=data['id']
        photos=data['photos']
        locations=data['location']['display_address']
        phone=data['display_phone']
        price=data.get('price')
        categories=data['categories']
        rating=data['rating']
        hours=data['hours']
        is_open_now=data['hours'][0]['is_open_now']
        coordinate_lat =data['coordinates']['latitude']
        coordinate_long= data['coordinates']['longitude']
        url=data['url']
        
        print("##############")
        print(coordinate_lat)
        print(coordinate_long)
        print("##########")

    # return jsonify(data)
    return render_template("indiv_result.html", name=name, price=price, yelp_id=yelp_id,
                            photos=photos, locations=locations, phone=phone,
                            categories=categories, rating=rating, hours_strings=hours_strings,
                            days=days, is_open_now=is_open_now, coordinate_long=coordinate_long,
                            coordinate_lat=coordinate_lat, url=url) 
                            




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app, 'my_data')
  

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)
