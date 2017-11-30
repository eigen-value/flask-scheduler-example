#!flask/bin/python
import imp
from migrate.versioning import api
from app import app, db

uri = app.config['SQLALCHEMY_DATABASE_URI']
repo = app.config['SQLALCHEMY_MIGRATE_REPO']

migration = repo + '/versions/%03d_migration.py' %\
                   (api.db_version(uri, repo) + 1)
tmp_module = imp.new_module('old_model')
old_model = api.create_model(uri, repo)
exec old_model in tmp_module.__dict__
script = api.make_update_script_for_model(uri, repo, tmp_module.meta,
                                          db.metadata)
open(migration, "wt").write(script)
api.upgrade(uri, repo)
print 'New migration saved as ' + migration
print 'Current database version: ' + str(api.db_version(uri, repo))
