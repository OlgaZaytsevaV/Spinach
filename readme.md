# Spinach

## Summary

Web application gives users a tool to filter for vegetarian and vegan local businesses.

Intended for users who are looking for exclusively vegetarian food. 
Users can search for places by location name or based on Zip Code.
Application  provides direction and geolocation via Google.Maps.

### About the Developer
Spinach was created by Olga Zaytseva during 4 weeks as a part of the Software engineering program at Hackbright.

## Technologies

**Tech Stack:**
- Python
- Flask
- SQLAlchemy
- Jinja2
- HTML
- CSS
- Javascript
- JQuery
- AJAX
- JSON
- Bootstrap
- Python unittest module
- Google Maps API
- Yelp API
- Postman

### 
Spinach is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM.
The front end templating uses Jinja2, the HTML was built using Bootstrap, and the Javascript uses JQuery and AJAX to interact with the backend.
The map is built using the Google Maps API. Server routes are tested using the Python unittest module.

## Features
Search vegetarian/vegan places based on location, name or alias. User account registration not required.<br>
![homepage](/readme_images/homepage.png)<br>

Registred users have account pages they can manage.<br>
![my account](/readme_images/account_page.png)<br><br>

Search results based on the information user inputs in the search forms.<br>
![search](/readme_images/search_results.png)<br><br>

Every search result has business page.<br>
![business_page](/readme_images/business_info.png)<br><br>

## <a name="installation"></a>Setup/Installation ⌨️

#### Requirements:
- Python 3
- PostgreSQL
- Yelp and Google.Maps API keys

To have this app running on your local computer, please follow the below steps:

Clone repository:<br>

  $ git clone https://github.com/olga-coding/my_precious_project.git <br>

Create a virtual environment:<br>

  $ virtualenv env<br>

Activate:<br>

  $ source env/bin/activate <br>

Install :<br>

  $ pip install -r requirements.txt<br>

Get your own secret keys APIs. Save them to a file `secrets.py`.<br>

Create database my_data.<br>

  $ createdb my_data <br>

  $ python model.py<br>

$ python server.py <br>

If you want to use SQLAlchemy to query the database, run in interactive mode. <br>

  $ python -i model.py <br>



