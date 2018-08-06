
import unittest
from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data, User, Saved_places, Restaurants, Rating
from flask import session
import server


class FlaskTest(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_index_route(self):
        """Test homepage page."""
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"""<a href="/">""", result.data)

    def test_login_route(self):
        """Test login page."""

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h3>Login In to Your Account</h3>", result.data )
   

class FlaskTestDataBase(TestCase):
    """Flask test with user logged into session"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        connect_to_db(app, "testdb")
        db.create_all()
        example_data()
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


    def test_important_page(self):
        """Test my_account page."""  
        result = self.client.get("/my_account")  
        self.assertIn(b"<h4>Saved places:</h4>", result.data) 


    def test_login(self):
        """Test login"""  
        result = self.client.post("/login",
                                  data={"email": "email",
                                        "password": "password"},
                                        follow_redirects = True) 
        self.assertIn(b"<p>Please fill in this form to create an account.</p>", result.data)

    
    def test_saved_places(self):

        saved_place_4= Restaurants.query.filter(Restaurants.name =="Name_3").first()
        self.assertEqual(saved_place_4.name, "Name_3" )


    def test_add_new_user(self):
        new_user = User(name="Kim", email="kim@gmail.com", password="12")
        db.session.add(new_user)
        db.session.commit() 
        self.assertEqual(new_user.name, "Kim") 

                       
    def test_rating_table(self):
        rating_1 = Rating.query.filter(Rating.score == "3").first() 
        self.assertEqual(rating_1.score, 3.0) 


    def test_sign_up_route(self):
        """Test sign_up page."""

        result = self.client.get("/sign_up",
                                data={"name":"Olga",
                                      "email":"olg@gmail.com",
                                      "password":"123"}, follow_redirects=True) 
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"""<button type="submit" class="btn">Sign Up</button>""", result.data)



    def test_find_users_in_sample_data(self):
        """Test database for users"""
        user_1 = User.query.filter(User.name == "Olga").first()
        self.assertEqual(user_1.name, "Olga")


    def test_find_users_in_sample_data(self):
        """Test database for users"""
        user_2 = User.query.filter(User.email== "Vic@gmail.com").first()
        self.assertEqual(user_2.email, "Vic@gmail.com")

    def test_find_restaurant(self):
        restaurant = Restaurants.query.filter(Restaurants.yelp_id =="534262890").first()  
        self.assertEqual(restaurant.yelp_id, "534262890")  


    def tearDown(self):

        db.session.remove()
        db.drop_all()     


class MockFlaskTest(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "testdb")
        db.create_all()
        example_data()
        
        def _mock_results_helper(yelp_id, name):
            """Mock individual results page"""
            return {
                "id": "wfa6U2LrTN_Qt9BurOOykw",
                "alias": "veganburg-san-francisco",
                "name": "VeganBurg",
                "image_url": "https://s3-media1.fl.yelpcdn.com/bphoto/28nB1hRFWtSdOSicisKgqQ/o.jpg",
                "is_claimed": True,
                "is_closed": False,
                "url": "https://www.yelp.com/biz/veganburg-san-francisco?adjust_creative=RRfi2ffnhjg1-byxI97LYQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_lookup&utm_source=RRfi2ffnhjg1-byxI97LYQ",
                "phone": "+14155488000",
                "display_phone": "(415) 548-8000",
                "review_count": 581,
                "categories": [
                    {
                        "alias": "vegan",
                        "title": "Vegan"
                    },
                    {
                        "alias": "burgers",
                        "title": "Burgers"
                    },
                    {
                        "alias": "hotdogs",
                        "title": "Fast Food"
                    }
                ],
                "rating": 4,
                "location": {
                    "address1": "1466 Haight St",
                    "address2": None,
                    "address3": "",
                    "city": "San Francisco",
                    "zip_code": "94117",
                    "country": "US",
                    "state": "CA",
                    "display_address": [
                        "1466 Haight St",
                        "San Francisco, CA 94117"
                    ],
                    "cross_streets": "Masonic Ave & Ashbury St"
                },
                "coordinates": {
                    "latitude": 37.77017,
                    "longitude": -122.44646
                },
                "photos": [
                    "https://s3-media1.fl.yelpcdn.com/bphoto/28nB1hRFWtSdOSicisKgqQ/o.jpg",
                    "https://s3-media1.fl.yelpcdn.com/bphoto/f0_lwHpESH-ggbBxaIzukQ/o.jpg",
                    "https://s3-media3.fl.yelpcdn.com/bphoto/BDJ1MWvoHUdXnrXy9xQ7sA/o.jpg"
                ],
                "price": "$$",
                "hours": [
                    {
                        "open": [
                            {
                                "is_overnight": False,
                                "start": "1100",
                                "end": "2100",
                                "day": 0
                            },
                            {
                                "is_overnight": False,
                                "start": "1100",
                                "end": "2100",
                                "day": 1
                            },
                            {
                                "is_overnight": False,
                                "start": "1100",
                                "end": "2100",
                                "day": 2
                            },
                            {
                                "is_overnight": False,
                                "start": "1100",
                                "end": "2100",
                                "day": 3
                            },
                            {
                                "is_overnight": False,
                                "start": "1100",
                                "end": "2200",
                                "day": 4
                            },
                            {
                                "is_overnight": False,
                                "start": "1100",
                                "end": "2200",
                                "day": 5
                            },
                            {
                                "is_overnight": False,
                                "start": "1100",
                                "end": "2100",
                                "day": 6
                            }
                        ],
                        "hours_type": "REGULAR",
                        "is_open_now": True
                    }
                ],
                "transactions": [
                    "pickup",
                    "delivery"
                ]
            }

        
        def _mock_search_helper(term,location):
            """Mock search route."""
            return {
                "businesses": [
                    {
                        "id": "rwiL8C8989DlHMD88bxi3A",
                        "alias": "gracias-madre-san-francisco",
                        "name": "Gracias Madre",
                        "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/Yy2vzxq0fAJUA5Q0cpziFw/o.jpg",
                        "is_closed": False,
                        "url": "https://www.yelp.com/biz/gracias-madre-san-francisco?adjust_creative=RRfi2ffnhjg1-byxI97LYQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=RRfi2ffnhjg1-byxI97LYQ",
                        "review_count": 2853,
                        "categories": [
                            {
                                "alias": "vegan",
                                "title": "Vegan"
                            },
                            {
                                "alias": "mexican",
                                "title": "Mexican"
                            }
                        ],
                        "rating": 4,
                        "coordinates": {
                            "latitude": 37.761606,
                            "longitude": -122.419241
                        },
                        "transactions": [
                            "pickup",
                            "delivery"
                        ],
                        "price": "$$",
                        "location": {
                            "address1": "2211 Mission St",
                            "address2": "",
                            "address3": "",
                            "city": "San Francisco",
                            "zip_code": "94110",
                            "country": "US",
                            "state": "CA",
                            "display_address": [
                                "2211 Mission St",
                                "San Francisco, CA 94110"
                            ]
                        },
                        "phone": "+14156831346",
                        "display_phone": "(415) 683-1346",
                        "distance": 1514.5832835114525
                    },
                ],
                "total": 83,
                "region": {
                    "center": {
                        "longitude": -122.43644714355469,
                        "latitude": 37.76089938976322
                    }
                }
            }


        server.search_helper = _mock_search_helper 

        server.results_helper = _mock_results_helper

    # TESTS
    
    def test_results_route_with_mock(self):
        """Test search page."""
        result = self.client.get("/results?id=wfa6U2LrTN_Qt9BurOOykw&name=VeganBurg")
        self.assertIn(b"<h2><b>VeganBurg</b></h2>", result.data) 
    

    def test_search_route_with_mock(self):
        """Test search page."""

        result = self.client.get("search?search=vegan%2C+vegetarian&address=san+francisco")
        self.assertIn(b"""<a href="/results?id=rwiL8C8989DlHMD88bxi3A&name=Gracias Madre">Gracias Madre</a>""", result.data) 

    def tearDown(self):

        db.session.remove()
        db.drop_all()   

if __name__ == "__main__":
    unittest.main()


    



  