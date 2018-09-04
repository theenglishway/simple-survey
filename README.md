# simple-survey

This project aims at providing a very simple way to self-host a survey and 
store its results in a self-hosted database. 

## Usage

Surveys can be built using 
[the free online survey-js Builder](https://surveyjs.io/Survey/Builder/) and 
stored as a JSON-file within the project. 

The database schema is guessed from the survey file and a SQLite database 
can then be built using the commands :

```
flask db init
flask db migrate
flask db upgrade
```

This database can obviously be used for survey analysis afterwards, using 
any appropriate tool.

The `index.html` page should be served using any web server.

## Dependencies

It relies on : 

* [Flask web framework](http://flask.pocoo.org/)
* [Flask SQLAlchemy integration](http://flask-sqlalchemy.pocoo.org/)
* [survey-js library](https://surveyjs.io/Overview/Library/)

Required packages are installed through `pip install -r requirements.txt`. 

The Javascript library is included in the `index.html` through a CDN.