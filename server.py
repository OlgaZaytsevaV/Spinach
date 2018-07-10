from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash
# from flask_debugtoolbar import DebugToolbarExtension



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "Secret"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/sign_up', methods=['GET'])

def show_sign_up_form():
    """Shows sign up form."""

    return render_template('sign_up.html') 



@app.route('/sign_up/', methods=['POST'])  

def  submit_sign_up_form():
    """ Submits sign up form."""

    email=request.form.get('email')
    password=request.form.get('password')

    return render_template('sign_up.html', email=email, password=password) 


@app.route('/login', methods =['GET'])
def show_login_form():
    """Shows log in form."""
    
    return render_template('login.html')



@app.route('/login', methods =['POST'])   
def submit_login_form():
    """Submits log in form."""

    # user = User.query.filter_by(email=email, password=password).first()
    # if user:
    #     flash("Login successful")
    #     session['email'] = user.email
    #     return redirect('/')
    # else:
    #     flash("User with email:{} does not exist, please sign up.".format(email))
    #     return redirect('/sign_up')
    

    return render_template('login.html', email=email, password=password)
    pass




@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
        flash('You are now logged out')
        return redirect('/')
    else:
        flash('You are not logged in')
        return redirect('/login')        



@app.route('/search_results')
def show_results():
    """Shows search results."""


    return render_template("search_results.html")
    

@app.route('/show_result')    
def show_indiv_result():

    return render_template("indiv_result.html")




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

  

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
