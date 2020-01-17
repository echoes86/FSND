import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from random import randint

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    def test_get_categories(self):
        response = self.client().get('/categories')
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('error'), False)
        self.assertTrue(json_data.get('categories'))
        self.assertTrue(len(json_data.get('categories')))

    def test_fail_categories(self):
        response = self.client().get('/categories')
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(json_data.get('success'), False)
        self.assertNotEqual(json_data.get('error'), True)
        self.assertTrue(json_data.get('categories'))
        self.assertTrue(len(json_data.get('categories')))

    def test_get_questions_categorized(self):
        response = self.client().get('/categories/1/questions')
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('error'), False)
        self.assertTrue(json_data.get('questions'))
        self.assertTrue(json_data.get('current_category'))
        self.assertGreaterEqual(json_data.get('total_questions'), 0)
        # self.assertTrue(len(json_data.get('questions')))
        # Not needed. Questions could be ideally = 0

    def test_fail_get_questions_categorized(self):
        response = self.client().get('/categories/10000/questions')
        self.assertEqual(response.status_code, 404)

    def test_get_questions(self):
        response = self.client().get('/questions')
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('error'), False)
        self.assertTrue(json_data.get('questions'))
        self.assertTrue(json_data.get('categories'))
        self.assertGreaterEqual(json_data.get('total_questions'), 0)
        self.assertTrue(len(json_data.get('categories')))

        # self.assertTrue(len(json_data.get('questions')))
        # Not needed. Questions could be ideally = 0

    def test_fail_get_questions(self):
        response = self.client().get('/categories/10000/questions')
        self.assertNotEqual(response.status_code, 200)

    def test_delete_question(self):
        test_questions = json.loads(self.client().get('/questions').data.decode('utf-8'))
        test_question_id = test_questions.get('questions')[0].get('id')

        response = self.client().delete('/questions/{}'.format(test_question_id))
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('error'), False)
        self.assertEqual(json_data.get('question'), test_question_id)

    def test_fail_delete_question(self):
        test_questions = json.loads(self.client().get('/questions').data.decode('utf-8'))
        question_ids = [item['id'] for item in test_questions.get('questions')]

        not_found_id = 1

        while True:
            not_found_id = randint(0, 10000)
            if not_found_id not in question_ids:
                break

        response = self.client().delete('/questions/{}'.format(not_found_id))
        self.assertNotEqual(response.status_code, 200)


    def test_search_question(self):
        response = self.client().post('/questions', json={'searchTerm': 'a'})
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('error'), False)
        self.assertTrue(json_data.get('questions'))
        self.assertTrue(json_data.get('total_questions'))

    def test_no_question_found(self):
        response = self.client().post('/questions', json={'searchTerm': 'impossiblewordisreallyhere'})
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('error'), False)
        self.assertEqual(json_data.get('total_questions'), 0)

    def test_post_new_question(self):
        new_question = {
            'question': 'test',
            'answer': 'my test',
            'category': '1',
            'difficulty': '2'
        }

        response = self.client().post('/questions', json=new_question)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('error'), False)
        self.assertTrue(json_data.get('question'))

    def test_fail_post_new_question(self):
        response = self.client().post('/questions')
        self.assertNotEqual(response.status_code, 200)

    def test_post_new_quiz(self):
        quiz_request_dict = {
            'previous_questions': [],
            'quiz_category': {'id': 0, 'type': 'click'}
        }


        response = self.client().post('/quizzes', json=quiz_request_dict)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data.get('success'), True)
        self.assertEqual(json_data.get('error'), False)
        self.assertTrue(json_data.get('question'))

    def test_fail_post_new_quiz(self):
        quiz_request_dict = {
            'wrong': 'field',
        }

        response = self.client().post('/quizzes', json=quiz_request_dict)
        self.assertNotEqual(response.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
