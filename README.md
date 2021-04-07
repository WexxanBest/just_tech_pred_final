## For day 2

To get data from We Study API you should use `we_study/api.py`.

## Project description

That project contains scripts to work with [We Study Api](https://help.webinar.ru/ru/articles/3352168-api-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%BE%D0%B2-we-study):

- Get course, students and groups data from it
- Process that data
- Save it to Google Sheets using its API

## Project requirements
Project uses some third-party modules:

- **requests** (sending requests to We Study API)
- **google-api-python-client** (working with Google Sheets API)
- **httplib2** (working with Google Sheets API)
- **oauth2client** (working with auth to work with Google Sheets API)

All dependencies can be installed by prompting:

`pip install -r requirements.txt`

## Project structure

- `main.py` script contains main functions to call all project methods
- `utils.py` script contains additional functions which provide other modules with useful functional
- `Dockerfile` is used to create docker image of a project to easily deploy it
- In `/google_sheets` folder there are scripts to work with Google Sheets API (`google_sheets.py`)
- In `/test` folder there are scripts with unit-tests and test data to make them work
- In `we_study` folder there are scripts to work with We Study API
  (`api.py`) and process obtained data (`data_processing.py`, 
  `student_generator.py`) 