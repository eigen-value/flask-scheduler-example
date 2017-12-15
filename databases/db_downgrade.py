#!flask/bin/python
import sys
sys.path.append('../')

from app import app
from migrate.versioning import api

uri = app.config['SQLALCHEMY_DATABASE_URI']
repo = app.config['SQLALCHEMY_MIGRATE_REPO']
v = api.db_version(uri, repo)
api.downgrade(uri, repo, v - 1)
print 'Current database version: ' + str(api.db_version(uri, repo))
