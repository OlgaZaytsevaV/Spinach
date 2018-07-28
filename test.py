
import unittest
from unittest import TestCase
from server import app
# from model import connect_to_db, db, example_data 
from flask import session

# Make a class for testing database
    # def setUp(self):
    #     """Stuff to do before every test."""

    #     # get the Flask test client
    #     self.client = app.test_client()
    #     app.config["TESTING"] = True

    #     #Connect to test database
    #     connect_to_db(app, "postgresql://testdb")
    #     #create tables and add sample data
    #     db.create_all()
    #     example_data()

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


    def test_login(self):
        """Test login"""  
        result = self.client.post("/login",
                                  data={"email": "email",
                                        "password": "password"}) 
        self.assertIn(b"<h3>Login In to Your Account</h3>", result.data)  


    def test_sign_up_route(self):
        """Test signup page."""

        result = self.client.get("/sign_up", follow_redirects=True) 
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"""<button type="submit" class="btn">Sign Up</button>""", result.data)



    # # def test_search_route(self):
    # #     """Test search page."""

    # #     result = self.client.get("/search",
    # #                              data={"name": "vegan ",
    # #                                    "address": "San Jose"})
    # #     self.assertEqual(result.status_code, 200)
    # #     self.assertIn(b"<h3>Search Results</h3>", result.data)


    def test_results_route(self):
        """Test individual results page."""

        result = self.client.get("/results")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h4>Results</h4>", result.data) 


    def test_route_my_account(self):
        result = self.client.get("/my_account")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h4>Saved places:</h4>", result.data)  

    #add user_id  



    # def tearDown(self):

    #     db.session.remove()
    #     db.drop_all()




if __name__ == "__main__":
    unittest.main()


    



   