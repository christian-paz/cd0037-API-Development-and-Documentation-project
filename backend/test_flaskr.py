import os
import unittest
import json
from settings import DB_HOST, DB_PORT, DB_TEST_NAME
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = f'postgresql://{DB_HOST}:{DB_PORT}/{DB_TEST_NAME}'
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "Where is Cape Town", 
            "answer": "South Africa",
            "difficulty": 2,
            "category": 3,
            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    #  Categories
    #  ----------------------------------------------------------------
    def test_get_categories(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    #  Questions
    #  ----------------------------------------------------------------
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestion'])
        self.assertTrue(data['categories'])       

    def test_404_sent_requesting_beyond_valid_point(self):
        res = self.client().get('/questions?page=1000', json={'category': 4})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test question delete endpoint
    def test_delete_question(self):
        res = self.client().delete('/questions/13')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 13).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertEqual(data['question_id'], 13)
        self.assertEqual(question, None)
        
    def test_delete_question_that_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test add question endpoint
    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
    
    def test_400_if_question_creation_not_allowed(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # test search question endpoint
    def test_search_question(self):
        res = self.client().post('/questions/search', json={'search_term':'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_question_without_result(self):
        res = self.client().post('/questions/search', json={'search_term':'Thiscannotbefound'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)

    # test fetching filtered questions by category
    def test_fetching_and_filtering_paginated_questions_by_categroies(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(['paginated_questions'])
        self.assertTrue(['currentCategory'])
        self.assertTrue(len(['paginated_questions']))

    def test_404_if_filtering_paginated_questions_beyond_valid_categroies(self):
        res = self.client().get('/categories/500/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    #  Quizzes
    #  ----------------------------------------------------------------
    def test_quizzes(self):
        res = self.client().post('/quizzes', json={'previous_questions': [1,2,3,4], 'quiz_category': {'type': 'Geography', 'id': '3'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()