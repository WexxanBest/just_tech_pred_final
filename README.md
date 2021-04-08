# Project description

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
  (like logging, saving data to csv, etc.)
- `Dockerfile` is used to create docker image of a project to easily deploy it 
  
    - Just run `docker image build [OPTIONS] .` to create docker image
  

- In `/google_sheets` folder there are scripts to work with Google Sheets API
  
  - `google_sheets.py` contains all essential methods to work with Google Sheets API
  - `keys.json` - credentials to authorize to Google Sheets API (they are empty
     for security reasons)
    

- In `/test` folder there are scripts with unit-tests and test data to make them work
  
  - Just run `test.py` to run all the tests
  

- In `we_study` folder there are scripts to work with We Study API
  and process obtained data
  
  - `api.py` contains methods to work with We Study API
  - `data_processing.py` contains methods to process data
  - `student_generator.py` contains methods to generate students
    groups with different parameters
  - `/cache` folder contains cached data to reduce amount of
    requests to the server and to get data from local files
  - `/data` folder contains row and processed data to work with
    later
  - `/generated_students` folder contains generated students 
  data sets 
  
## Examples
### Getting data from We Study API

The code below will automatically fetch courses data from We
Study API and save it to `data/courses.csv` file.
```python
# built-in module that will help to print data in more readable way
from pprint import pprint 

# our module for fetching data from We Study API
from we_study.api import ApiManager

API_KEY = 'your-We-Study-API-key-here'

if __name__ == '__main__':
    manager = ApiManager(API_KEY)
    courses = manager.get_courses_data(save_data_to_file=True, file='data/courses.csv')
    pprint(courses) # output courses data
```
The output will be:
```
[['id', 'name', 'groups_id'],
 [49185, 'Русский язык Гр1', [60257]],
 [49187, 'Математика Гр1', [60259]],
 [49191, 'Математика Гр2', [60263]]]
```

### Loading obtained data to Google Sheets

Before using code below you should create Google Sheet 
credentials (see how to do that [here](https://developers.google.com/workspace/guides/create-credentials))
 and place them in `google_sheets/keys.json` file

Code below will upload `data/courses.csv` to Google Sheet.

```python
# importing our modules to work with Google Sheet
from google_sheets.google_sheets import (Spreadsheet, SpreadsheetManager)

URL = 'url-of-your-spreadsheet'

if __name__ == '__main__':
    spreadsheet = Spreadsheet().get_spreadsheet_by_url(URL)
    manager = SpreadsheetManager(spreadsheet)
    manager.upload_csv('data/courses.csv')
```
If you've done all right, it will output:
```
12 cells updated.
```
### Working with Google Sheets
You can do much stuff with Google Sheets due to our modules. See
examples below:
#### Accessing to Spreadsheet
```python
from google_sheets.google_sheets import (Spreadsheet, SpreadsheetManager)

SpreadsheetId = 'your-spreadsheet-id'
SpreadsheetUrl = 'your-spreadsheet-url'


if __name__ == '__main__':
    # you can access spreadsheet by several ways
    spreadsheet = Spreadsheet()
    # by its id
    spreadsheet.get_spreadsheet_by_id(SpreadsheetId)
    # or by its url
    spreadsheet.get_spreadsheet_by_url(SpreadsheetUrl)
    # or you can even create a new spreadsheet
    spreadsheet.create_spreadsheet()
```
#### Dealing with data
```python
from google_sheets.google_sheets import (Spreadsheet, SpreadsheetManager)

SpreadsheetId = 'your-spreadsheet-id'

data = [
  ['hello', 3],
  [2, 90]
]
range_name = 'A1:B2'


if __name__ == '__main__':
    spreadsheet = Spreadsheet(spreadsheet_id=SpreadsheetId)
    # you can update data in range
    spreadsheet.update_data(data=data, range_name=range_name)
    
    # you can get data from range
    obtained_data = spreadsheet.get_data_by_range(range_name=range_name)
    print(obtained_data) # output data
    
    # you can clear data in range
    spreadsheet.clear_data(range_name=range_name)

    # you can get data from range
    obtained_data = spreadsheet.get_data_by_range(range_name=range_name)
    print(obtained_data) # output data
```
The output will be:
```
4 cells udpdated.

[['hello', 3], [2, 90]]

[]
```
#### Dealing with sheets 
```python
from google_sheets.google_sheets import (Spreadsheet, SpreadsheetManager)

SpreadsheetId = 'your-spreadsheet-id'


if __name__ == '__main__':
    spreadsheet = Spreadsheet(SpreadsheetId)
    
    # you can add new sheet to spreadsheet
    spreadsheet.add_sheet(title='Test Sheet')
    
    # you can get a list of sheets
    sheet_list = spreadsheet.sheet_list
    for sheet in sheet_list:
        if sheet['title'] == 'Test Sheet':
            sheet_id = sheet['sheetId']

    # you can delete sheet
    spreadsheet.delete_sheet(sheet_id=sheet_id)
```
### Student Generator
You can generate data sets of students with certain parameters. The 
code below will generate data set of students and save it to 
`/generated_students` folder
```python
from we_study.student_generator import (StudentGenerator, BadGroup, GoodGroup, ExcellentGroup, MixedGroup)
groups = [
    BadGroup(),
    GoodGroup(),
    ExcellentGroup(),
    MixedGroup()
    ]
courses = ['1st Course', '2nd Course', '3rd Course']

if __name__ == '__main__':
    generator = StudentGenerator(students_amount=100, groups=groups, courses_name_list=courses)
    generator.main()
```