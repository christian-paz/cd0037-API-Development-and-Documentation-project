from ast import And
from crypt import methods
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify ,Response ,flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, question):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [category.format() for category in question]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    app.config['JSON_SORT_KEYS'] = False
    

    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # Only allows cross origins with specific routes in this case all (*)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    # Kept the same after_request decorator as the excercises
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_all_categories():
        categories = Category.query.all()
        formated_category = {category.id:category.type for category in categories}
        
        if len(formated_category) == 0:
            abort(404)

        return jsonify({
                "success": True,
                "categories": formated_category,
            })

    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        try:
            # Questions queries
            questions = Question.query.all()
            current_questions = paginate_questions(request, questions)

            if len(current_questions) == 0:
                abort(404)

            # Category queries
            categories = Category.query.all()
            formated_category = {category.id:category.type for category in categories}

            # print(current_questions)
            
            for question in questions:
                formatted_questions = {
                    "id": question.id,
                    "question": question.question,
                    "answers": question.answer,
                    "difficulty": question.difficulty,
                    "category": question.category,
                }
            
                # determines currentCategory

                if formatted_questions.get('category') == 1:
                    currentCategory = "Science"
                
                elif formatted_questions.get('category') == 2:
                    currentCategory = "Art"
                
                elif formatted_questions.get('category') == 3:
                    currentCategory = "Geography"
                
                elif formatted_questions.get('category') == 4:
                    currentCategory = "History"

                elif formatted_questions.get('category') == 5:
                    currentCategory = "Entertainment"
                
                elif formatted_questions.get('category') == 6:
                    currentCategory = "Sports"
        except:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "totalQuestion": len(Question.query.all()),
            "categories": formated_category,
            "currentCategory" : currentCategory,
        })
    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                "success": True,
                "question_id": question_id,
            })

        except:
            abort(404)

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()

            print(question)

            return jsonify ({
                "success": True,
                "created": question.id,
            })

        except:
            abort(404)
     
    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get("searchTerm", None)

        try:
            search_result = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            
            if len(search_result) > 0:
                final_questions = paginate_questions(request, search_result)

                return jsonify({
                    "success": True,
                    "questions": final_questions,
                    "total_questions": len(final_questions),
                    "current_category": None,
                })
            else:
                return jsonify({
                    "success": True,
                    "questions": [],
                    "total_questions": 0,
                    "current_category": None,
                })

        except:
            abort(422)      

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        paginated_questions = paginate_questions(request, questions)


        for question in questions:
            formatted_questions = {
                'id': question.id,
                'question': question.question,
                'answers': question.answer,
                'difficulty': question.difficulty,
                'category': question.category,
            }

            if formatted_questions.get('category') == 1:
                currentCategory = "Science"
            
            elif formatted_questions.get('category') == 2:
                currentCategory = "Art"
            
            elif formatted_questions.get('category') == 3:
                currentCategory = "Geography"
            
            elif formatted_questions.get('category') == 4:
                currentCategory = "History"

            elif formatted_questions.get('category') == 5:
                currentCategory = "Entertainment"
            
            elif formatted_questions.get('category') == 6:
                currentCategory = "Sports"
            else:
                abort(404)

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "totalQuestions": len(formatted_questions),
            "currentCategory": currentCategory,
        })

    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()

        get_previous_questions = body.get("previous_questions", None)
        get_quiz_category = body.get("quiz_category", None)
        # print(get_quiz_category) prints {'type': 'Geography', 'id': '3'} and {'type': 'click', 'id': 0} when clicking on ALL
        
        previous_questions = []

        try:
            if get_quiz_category['id'] == 0:
                questions = Question.query.filter(Question.id.notin_(get_previous_questions)).all()
                next_question = random.choice(questions).format()
                # print(questions)
                num = next_question['id']
                # print(num)
                previous_questions.append(num)

            else:
                questions = Question.query.filter(Question.id.notin_(get_previous_questions)).filter(Question.category == get_quiz_category['id']).all()
                # print(questions)
                next_question = random.choice(questions).format()
                # print(next_question)
                num = next_question['id']
                # print(num)
                previous_questions.append(num)

            return jsonify({
                "success": True,
                "question": next_question,
            })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    return app

