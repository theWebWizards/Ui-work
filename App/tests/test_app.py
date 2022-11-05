import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify
from datetime import date

from App.main import create_app
from App.database import create_db
from App.models import User, Image, Rating, Ranking
from App.controllers import (
    create_user,
    get_user,
    get_user_by_username,
    get_all_users,
    get_all_users_json,
    update_user,
    delete_user,

    create_image,
    get_all_images,
    get_all_images_json,
    get_images_by_userid_json,
    get_image,
    get_image_json,
    delete_image,

    create_rating, 
    get_all_ratings,
    get_all_ratings_json,
    get_rating,
    get_ratings_by_target,
    get_ratings_by_creator,
    get_rating_by_actors,
    update_rating,

    create_ranking, 
    get_all_rankings,
    get_all_rankings_json,
    get_ranking,
    get_rankings_by_image,
    get_rankings_by_creator,
    get_ranking_by_actors,
    get_calculated_ranking,
    update_ranking,

    authenticate
)

from wsgi import app


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    def test_toJSON(self):
        user = User("bob", "bobpass")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "images": [], "ratings": []})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class ImageUnitTests(unittest.TestCase):

    def test_new_image(self):
        image = Image(1)
        assert image.rankings == []

    def test_toJSON(self):
        image = Image(1)
        image_json = image.toJSON()
        self.assertDictEqual(image_json, {"id":None, "rankings":[], "userId": 1})

class RatingUnitTests(unittest.TestCase):

    def test_new_rating(self):
        rating = Rating(1, 2, 3)
        assert rating.score == 3

    def test_toJSON(self):
        rating = Rating(1, 2, 3)
        rating_json = rating.toJSON()
        self.assertDictEqual(rating_json, {"id":None, "creatorId":1, "targetId": 2, "score":3, "timeStamp": date.today()})

class RankingUnitTests(unittest.TestCase):

    def test_new_ranking(self):
        ranking = Ranking(1, 2, 3)
        assert ranking.score == 3

    def test_toJSON(self):
        ranking = Ranking(1, 2, 3)
        ranking_json = ranking.toJSON()
        self.assertDictEqual(ranking_json, {"id":None, "creatorId":1, "imageId": 2, "score":3})

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')

def test_authenticate():
        user = create_user("bob", "bobpass")
        assert authenticate("bob", "bobpass") != None


class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_user(self):
        user = get_user(1)
        assert user.username == "bob"

    def test_get_user_by_username(self):
        user = get_user_by_username("rick")
        assert user["username"] == "rick"

    def test_get_all_users(self):
        userList = []
        userList.append(get_user(1))
        userList.append(get_user(2))
        self.assertEqual(get_all_users(), userList)

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob", "images": [], "ratings": []}, {"id":2, "username":"rick", "images": [], "ratings": []}], users_json)

    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    def test_delete_user(self):
        create_user("phil", "philpass")
        delete_user(3)
        user = get_user(3)
        assert user == None

    
