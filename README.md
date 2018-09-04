# simple-survey

This project aims at providing a simple way to self-host a survey and 
store its results in a self-hosted database. 

The following features are included : 

* Survey import from JSON file
* No registration required, 100% anonymous vote
* Only one vote per user* 
* Verification that the user has visited the poll page

\* _this is done by storing a hash of the IP address and user-agent combination, 
which seems a good enough heuristic according to 
[a study by the EFF](https://panopticlick.eff.org/about)_ 

## Usage

The database stores 3 kinds of information : 

* the polls themselves
* the raw results (as delivered by survey-js)
* the interpreted results

### Setting up the app

1. Clone the project
1. Install dependencies : `pip install -r requirements.txt`
1. (optional, if using SQLite) Setup your database
1. Setup a `.env` file in the root directory with `SQLALCHEMY_DATABASE_URI` and 
`SECRET_KEY`
1. Upgrade the database : `flask db init && flask db migrate -m "Initial" && flask db upgrade`
1. Run the app `flask run`

### Importing polls

Surveys can be written 'by hand' or built using 
[the free online survey-js Builder](https://surveyjs.io/Survey/Builder/) which
exports the survey as a JSON file.

1. Move the file to some location accessible from the host machine
1. Import the poll : ̀`flask poll import /path/to/json "optional poll name"`
1. The poll is now accessible from `http://your_host/polls/<slugified-poll-name>`
and the results can be seen at 
`http://your_host/polls/<slugified-poll-name>/results`

The JSON file can now be safely deleted.

### Giving sense to the raw results

Raw poll results can be converted into a poll-specific model that will be
stored into the database, in order to ease analysis and querying on the 
results.

1. Create the model and upgrade the database : `poll upgrade`
1. Convert the results : `poll convert`

Repeat step 2. as many times as necessary over the poll lifetime.  

## Dependencies

This project relies on the following free pieces of software awesomeness : 

* [Flask web framework](http://flask.pocoo.org/)
* [Flask SQLAlchemy integration](http://flask-sqlalchemy.pocoo.org/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [survey-js library](https://surveyjs.io/Overview/Library/)
* [python-slugify](https://github.com/un33k/python-slugify)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

The survey-js is included through a CDN.