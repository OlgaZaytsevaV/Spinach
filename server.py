
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
# YELP_URL_ID= 'https://api.yelp.com/v3/businesses/{id}'
API_KEY = os.environ['API_KEY']
app.jinja_env.undefined = StrictUndefined


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
        flash("User with email: {} does not exist please sign up.".format(email))
        return redirect('/sign_up')
    



@app.route('/my_account')
def show_form():
    yelp_id=request.args.get('yelp_id')
    name = request.args.get('name')
    user = User.query.get(session['user_id'])

    return render_template('my_account.html', user=user, yelp_id=yelp_id)


@app.route('/save', methods=["POST"])   
def save_places():

    yelp_id=request.form.get('yelp_id')
    name = request.form.get('name')
    user = User.query.get(session['user_id'])
    print(request.form)
    # check if restaurant in db and create it if not

    
    restaurant = Restaurants.query.get(yelp_id)
    if restaurant is None:
        restaurant = Restaurants(yelp_id=yelp_id, name=name)
        db.session.add(restaurant) 
    # save the place
        d=datetime.now()
        save_date=(d.strftime("%A, %B, %d, %Y"))
        new_saved_place = Saved_places(place=restaurant, user=user, save_date=save_date)
        new_saved_place 
        db.session.add(new_saved_place)
        db.session.commit()
        places = user.saved
        print('###################')
        print(places)
        print('###################')

        return "The place was saved to your account"
    else:
        return " It already exists in your account"    

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        flash('You are now logged out')
        return redirect('/')
    else:
        flash('You are not logged in')
        return redirect('/')        



@app.route('/search' )
def show_results():
    """Shows search results in json."""

    search = request.args.get('search')
    query = request.args.get('query')
    address=request.args.get('address')
    # if not search:
    #     places = []
    # else:
    #     places= Restaurants.query.filter(Restaurants.name.like('%' + search + '%')).all()


    if search:
        params = { 
                   'term': search,
                   'location': address,
                   }   

        headers = {'Authorization': 'Bearer ' + API_KEY}

        response = requests.get(YELP_URL + 'search?categories=vegan,vegetarian',
                                params=params,
                                headers=headers)
        print(f"response.url = {response.url}")
        data = response.json()   
        print(data.keys()) 

        # import pdb; pdb.set_trace()

        if response.ok:
            for i in data['businesses']:
                print(i['name'])
                print(i['image_url'])
            places = data['businesses']

        else:
            places = []

        return render_template("search.html", places=places,
                               data=pformat(data))    



@app.route('/results')    
def show_indiv_result():


    yelp_id=request.args.get('id')
    name = request.args.get('name') 
    locations=request.args.get('location')
    photos=request.args.get('photos')
    phone=request.args.get('phone')
    price = request.args.get('price')
    categories=request.args.get('categories')
    ratings=request.args.get('rating')
    hours=request.args.get('hours')
    headers = {'Authorization': 'Bearer ' + API_KEY}
    response = requests.get(YELP_URL + yelp_id,
                            headers=headers)
    print(f"response.url = {response.url}")
    data = response.json()  
    print(data.keys())

    print(type(data['hours']))
    print(type(data['hours'][0]))
    print(data['hours'][0]['open'])
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

            end = int(i['end'])

            start = int(i['start'])
            start = int(start/100)
            if end > 1200:
                end = int((end - 1200)/100) 
                hours_strings.append("{} {} - {}".format(i['day'], start, end))
        

   

    yelp_id=data['id']
    photos=data['photos']
    locations=data['location']
    phone=data['phone']
    if price:
        price=data['price']
    categories=data['categories']
    rating=data['rating']
    hours=data['hours']
    # return jsonify(data)
    return render_template("indiv_result.html", name=name, price=price, yelp_id=yelp_id,
                            photos=photos, locations=locations, phone=phone,
                            categories=categories, rating=rating,
                             hours_strings=hours_strings) 
                            




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app, 'my_data')
  

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)
