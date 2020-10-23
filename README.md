# Example flask application for managing the schedule of courses.

### 1. Install 
```
$ git clone https://github.com/anavozhko/flask-scheduler-example
$ cd flask-scheduler-example
$ pip install -r requirements.txt
```

### 2. Create app.db
`$ python db_create.py`

### 3. Edit config.py

### 4. Run
`$ python manage.py runserver # run on 127.0.0.1:5000`


### 5. Translations
Translations make use of Flask-Babel plugin
Tag strings with gettext in py code and {{ _() }} in jinja templates
Then to build a catalog for the Locales you want to create run:

`$ pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .`

Next, run (eg for italian):

`$ pybabel init -i messages.pot -d translations -l it`

If the strings change or new are added create a new messages.pot like above and then let pybabel merge the changes:

`$ pybabel update -i messages.pot -d translations`

You can now start translating the msgstr values. When you are done editing, there is only one step left, compile all .po files in your translation directory:

`$ pybabel compile -d translations`
