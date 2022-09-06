# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.


### Documentation

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

Example response:
```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
`GET '/categories/<int:category_id>/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer which is the `category_id`
- Returns: An object with questions for the specified category, total questions, and current category string

Example response:
```json
{
  "success": true,
  "questions": [
    {
      "id": 13,
      "question": "What is the largest lake in Africa?",
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2
    },
    {
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?",
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3
    },
    {
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?",
      "answer": "Agra",
      "category": 3,
      "difficulty": 2
    },
  ],
  "totalQuestions": 5,
  "currentCategory": "Geography"
}
```

`GET '/questions'`

- Fetches a list of a total of 10 questions.
- Request Arguments: None
- Returns: a list of `paginated questions`, number of `total questions`, `current category`, `categories`.

Example response:
```json
{
  "success": true,
  "questions": [
    {
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?",
      "answer": "Agra",
      "category": 3,
      "difficulty": 2
    },
    {
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?",
      "answer": "Escher",
      "category": 2,
      "difficulty": 1
    },
    {
      "id": 17,
      "question": "La Giaconda is better known as what?",
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3
    },
    {
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?",
      "answer": "One",
      "category": 2,
      "difficulty": 4
    },
    {
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?",
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2
    },
    {
      "id": 20,
      "question": "What is the heaviest organ in the human body?",
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4
    },
    {
      "id": 21,
      "question": "Who discovered penicillin?",
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3
    },
    {
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?",
      "answer": "Blood",
      "category": 1,
      "difficulty": 4
    },
    {
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?",
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4
    },
    {
      "id": 74,
      "question": "",
      "answer": "",
      "category": 1,
      "difficulty": 1
    }
  ],
  "totalQuestion": 28,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Geography"
}
```

`DELETE '/questions/<int:question_id>'`

- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Appropriate HTTP status code 200.

```json
{
  "success": true,
}
```

`POST '/questions/`

- Sends a post request in order to add new questions.

Example of the Request Body:
```json
{
  "question":  "Heres a new question string",
  "answer":  "Heres a new answer string",
  "difficulty": 1,
  "category": 3,
}
```

Returns: A `true` response when question has been added successfully.

Example response:
```json
{
  "success": true,
}
```

`POST '/questions/search'`

- Sends a post request in order to search for a specific question by search term

Example response of Request Body:
```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

Returns: any array of `questions`, a number of `totalQuestions` that met the search term and the `current category` string

Example response:
```json
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
      },
    ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```

`POST '/quizzes'`

- Sends a post request in order to get the next question

Example response of Request Body:
```json
{
  "previous_questions": [1, 4, 20, 15],
  "quiz_category": "current category"
}
```

Returns: a single new question object

Example response:
```json
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
