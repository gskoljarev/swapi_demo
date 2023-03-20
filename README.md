# swapi_demo

## Setup

- create a virtual environment: `python -m venv .venv`
- activate the environment:
  - Linux: `source .venv/bin/activate`
  - Windows: `.\.venv\Scripts\activate`
- install requirements: `pip install -r requirements.txt`


## Run

- within activated virtual environment, run: `python manage.py runserver`
- access the app via http://127.0.0.1:8000/collections/


## Notes

- tested on `Python 3.8.9`
- possible imporovements
  - separate data retrieval & value count features into API endpoints and front-facing stuff into a separate frontend interface
  - store datasets in a database instead of csv
  - enlist async python features to even further speed up data retrieval
  - add user authentication
