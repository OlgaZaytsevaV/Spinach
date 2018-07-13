
from flask import jsonify
from sys import argv
import requests
from pprint import pprint, pformat
import os


from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Restaurants, Saved_places, connect_to_db, db
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SECRET"

YELP_URL = 'https://api.yelp.com/v3/businesses/search'
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
        flash("Hi {}!".format(user.name))
        session['user_id'] = user.user_id
        return redirect('/')
    else:
        flash("User with email: {} does not exist please sign up.".format(email))
        return redirect('/sign_up')
    

    return "You are logged in."




@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
        flash('You are now logged out')
        return redirect('/')
    else:
        flash('You are not logged in')
        return redirect('/login')        



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

        response = requests.get(YELP_URL,
                                params=params,
                                headers=headers)
        print(f"response.url = {response.url}")
        data = response.json()    

        # import pdb; pdb.set_trace()

        if response.ok:
            for i in data['businesses']:
                print(i['name'])
            places = data['businesses']

        else:
            places = []

        return render_template("search.html", places=places,
                               data=pformat(data))    



@app.route('/results')    
def show_indiv_result():
    

    params = {
               'id': id,
               }   

    headers = {'Authorization': 'Bearer ' + API_KEY}

    response = requests.get(YELP_URL,
                            params=params,
                            headers=headers)
    print(f"response.url = {response.url}")
    data = response.json()  

    places= data['businesses']



    return render_template("indiv_result.html", data=pformat(data), id=yelp_id)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    connect_to_db(app, 'my_data')
  

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0", debug=True)
