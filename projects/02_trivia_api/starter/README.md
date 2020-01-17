# Full Stack API Final Project

## Introduction

Trivia App provised to you the following actions:

1) Display questions - both all questions and by category.
2) Delete questions.
3) Add questions.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## App structure

The Trivia App is organized in:

1. [`./frontend/`](./frontend/): a `React` app.
2. [`./backend/`](./backend/): REST Api written in `Python` using the `Flask` framework and a Data Layer managed by `SQLAlchemy`

## Installing Dependencies

### Backend

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Frontend

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Running the server

### Backend

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

### Frontend

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Rest API

Following we give a description of the endpoints provided by the API.

### List of Endpoints

    - GET /categories/
    - GET /categories/<int:category_id>/questions
    - GET /questions
    - DELETE /questions/<int:question_id>
    - POST /questions
    - POST /quizzes

### Get list of Categories

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

#### Request

`GET /categories/`

    curl http://localhost:3000/categories/

#### Response
    HTTP/1.1 200 Ok
    {
        'success': True,
        'error': False,
        'categories': {{"id": 1, "type": "Art"}, {...} }
    }

### Get list of Questions per category

Fetches a list of questions for the specified category in which every item is a dict corresponding to a question

#### Request

`GET /categories/<int:category_id>/questions`

    curl http://localhost:3000/categories/1/questions

#### Response
    HTTP/1.1 200 Ok
    {
        "current_category": "Science", 
        "error": false,
        "success": true, 
        "total_questions": 14, 
        "questions": [
            {
                "answer": "The Liver", 
                "category": 1, 
                "difficulty": 4, 
                "id": 20, 
                "question": "What is the heaviest organ in the human body?"
            }, { ... }
        ]
    }

### Get list of Questions

Fetches a list of questions in which every item is a dict corresponding to a question

#### Request

`GET /questions`

    curl http://localhost:3000/questions

#### Response
    HTTP/1.1 200 Ok
    {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        },  
        "error": false,
        "success": true, 
        "total_questions": 14, 
        "questions": [
            {
                "answer": "The Liver", 
                "category": 1, 
                "difficulty": 4, 
                "id": 20, 
                "question": "What is the heaviest organ in the human body?"
            }, { ... }
        ]
    }

### Delete a Question

Deletes a question specified by its ID

#### Request

`DELETE /questions/<int:question_id>`

    curl --request DELETE http://localhost:3000/questions/1

#### Response

    HTTP/1.1 200 Ok
    {
        "error": false,
        "success": true, 
        "question": 1
    }

### Search for Questions

Search for questions matching a pattern submitted as JSON

#### Request

`POST /questions`

    curl --request POST \
         -H "Content-Type: application/json" \
         --data '{"searchTerm":"a"}' \
         http://localhost:3000/questions

#### Response

    HTTP/1.1 200 Ok
    {
        "error": false,
        "success": true, 
        "question": 1
    }

### Post a new Question

Post a new question specified by JSON

#### Request

`POST /questions`

    curl --request POST \
         -H "Content-Type: application/json" \
         --data '{"question": "test","answer": "my test","category": "1","difficulty": "2"}' \
         http://localhost:3000/questions

#### Response

    HTTP/1.1 200 Ok
    {
        "error": false,
        "success": true, 
        "question": 1
    }

### Request to play a Quiz

Allows to start a quiz specifying the category into the request JSON

#### Request

`POST /quizzes`

    curl --request POST \
         -H "Content-Type: application/json" \
         --data '{"previous_questions": [],"quiz_category": {"id": 0, "type": "click"}}' \
         http://localhost:3000/quizzes

#### Response

    HTTP/1.1 200 Ok
    {
      "error": false, 
      "question": {
        "answer": "my test", 
        "category": 1, 
        "difficulty": 2, 
        "id": 45, 
        "question": "test"
      }, 
      "success": true
    }

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Error Handling

Errors are returned as JSON Object in the following format

    {
        "error": 400,
        "success": False, 
        "message": "Bad Request"
    }

The API will return some error types depending on the error matched:

- 400: Bad Request
- 422: Unprocessable Entity
- 404: Not found
- 500: Internal Server Error
