#!flask/bin/python
import os.path
import sys
sys.path.append('../')

from app import app, db
from migrate.versioning import api

db.init_app(app)
with app.test_request_context():
    db.create_all()

uri = app.config['SQLALCHEMY_DATABASE_URI']
repo = app.config['SQLALCHEMY_MIGRATE_REPO']

if not os.path.exists(repo):
    api.create(repo, 'database repository')
    api.version_control(uri, repo)
else:
    api.version_control(uri, repo, api.version.Collection.version(repo))
