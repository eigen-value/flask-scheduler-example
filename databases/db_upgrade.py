#!flask/bin/python
import sys
sys.path.append('../')

from app import app
from migrate.versioning import api

uri = app.config['SQLALCHEMY_DATABASE_URI']
repo = app.config['SQLALCHEMY_MIGRATE_REPO']
api.upgrade(uri, repo)
print 'Current database version: ' + str(api.db_version(uri, repo))
