#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.login.models import User


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_unique_nickname(self):
        new_user1 = User(username='john', password='1', email='john@example.com',
                        firstname='John', lastname='L', admin=False)
        db.session.add(new_user1)
        db.session.commit()
        try:
            new_user2 = User(username='john', password='123', email='john2@example.com',
                            firstname='John', lastname='L', admin=False)
            db.session.add(new_user2)
            db.session.commit()
            saved = True
        except:
            saved = False
        assert saved == False


if __name__ == '__main__':
    unittest.main()
