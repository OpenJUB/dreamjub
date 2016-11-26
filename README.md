DreamJUB
========
(Pronounced 'enPR: drēmhub, IPA(key): /dɹiːmhʌb/')

Jacobs Directory Exploration and Mapping Server written in Python 3.5

[![Build Status](https://travis-ci.org/OpenJUB/dreamjub.svg?branch=master)](https://travis-ci.org/OpenJUB/dreamjub)

Development Setup
-----------------
- Ensure you have Python 3.5 installed
- Ensure you have bower installed: `bower --version`. In case bower is not installed,
  install it using `npm install -g bower`. If you don't have npm installed, you need
  to [install npm and node](https://nodejs.org/en/download/).
- create virtual environment: `python3.5 -m virtualenv env`. If you don't have virtualenv installed, run `pip3 install virtualenv` first.
- Launch the environment: `source env/bin/activate`
- Install the requirements: `pip install -r requirements.txt`
- Migrate the database: `python manage.py migrate`
- Fetch the polymer components: `bower install`
- Run the server: `python manage.py runserver`
- The project should now be deployed at `localhost:8000`
- To serve media files in development, run a simple http server in the media_files directory:
  - `python -m http.server 8080`

Development
-----------
- Upon modifying a database model, generate the migrations: `python manage.py makemigrations` and
  make sure you commit the migrations.
- For adding frontend dependencies, prefer installing with bower (i.e. `bower install package_name`)
