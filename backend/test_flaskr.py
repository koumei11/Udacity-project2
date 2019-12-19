import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.sample_data = {
            'question': 'Who introduced the theory of relativity?',
            'answer': 'Albert Einstein',
            'difficulty': 1,
            'category': 1
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
    def test_get_categories(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_error_get_questions(self):
        res = self.client().get('/questions?page=1000')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Page not found.")

    # Please replace id for your environment
    def test_delete_question(self):
        res = self.client().delete('/questions/63')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_error_delete_question(self):
        res = self.client().delete('/questions/1000')
        self.assertEqual(res.status_code, 422)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "unprocessable")

    def test_post_question(self):
        res = self.client().post('/questions', json=self.sample_data)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)

    def test_get_questions_by_search_term(self):
        res = self.client().post('/questions', json={'searchTerm': 'theory of relativity'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], True)

    def test_get_questions_by_search_term_no_result(self):
        res = self.client().post('/questions', json={'searchTerm': ''})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)

    def test_error_post_question(self):
        res = self.client().post('/questions')
        self.assertEqual(res.status_code, 500)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 500)
        self.assertEqual(data['message'], 'Server errro occurred.')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], 1)

    def test_error_get_questions_by_category(self):
        res = self.client().get('/categories/1000/questions')
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Page not found.')

    # Please replace id for your environment
    def test_get_next_question(self):
        q1 = Question.query.filter(Question.id == 50).one_or_none()
        q2 = Question.query.filter(Question.id == 51).one_or_none()
        res = self.client().post('/quizzes', json={
            'previous_questions': [q1.format(), q2.format()],
            'quiz_category': {'type': 'Science', 'id': 1}
        })

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)

        self.assertTrue(data['question'])


    def test_error_422_get_next_question(self):
        q1 = Question.query.filter(Question.id == 50).one_or_none()
        q2 = Question.query.filter(Question.id == 51).one_or_none()
        res = self.client().post('/quizzes', json={
            'previous_questions': [q1.format(), q2.format()],
            'quiz_category': {'type': 'Science', 'id': 1000}
        })

        self.assertEqual(res.status_code, 422)
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()