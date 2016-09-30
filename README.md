DreamJUB
========
(Pronounced 'enPR: drēmhub, IPA(key): /dɹiːmhʌb/')

Jacobs Directory Exploration and Mapping Server written in Python 3.5

Development Setup
-----------------
- Ensure you have Python 3.5 installed
- Ensure you have bower installed: `bower --version`. In case bower is not installed,
  install it using `npm install -g bower`. If you don't have npm installed, you need
  to [install npm and node](https://nodejs.org/en/download/).
- create virtual environment: `python3.5 -m virtualenv env`
- Launch the environment: `source env/bin/activate`
- Migrate the database: `python manage.py migrate`
- Fetch the polymer components: `bower install`
- Run the server: `python manage.py runserver`
- The project should now be deployed at `localhost:8000`

