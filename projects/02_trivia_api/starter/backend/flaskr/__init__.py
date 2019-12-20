import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request_handler(response):
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
        response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')

        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    def _paginated_list(request, item_list):
        page = request.args.get('page', None)

        if page is None:
            page = 1

        start = (int(page) - 1) * QUESTIONS_PER_PAGE
        print(start)
        end = start + QUESTIONS_PER_PAGE
        print(end)

        if start > len(item_list):
            abort(422) # Unprocessable Entity

        return item_list[start:end]

    @app.route('/categories')
    def get_categories():
        all_categories = [item.format() for item in Category.query.all()]
        return jsonify(all_categories)

    @app.route('/categories/<int:category_id>/questions')
    def get_category(category_id):
        single_category = Category.query.filter_by(Category.id == category_id).one_or_none()

        if single_category is None:
            abort(404)

        questions_per_category = Question.query.filter_by(Question.category == single_category.id).all()

        return jsonify(
            {
                'questions': [item.format() for item in questions_per_category],
                'total_quesitons': len(questions_per_category),
                'current_category': single_category.type
            }
        )

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions_paginated():
        all_questions = [item.format() for item in Question.query.all()]
        all_categories = [item.format() for item in Category.query.all()]
        paginated_questions = _paginated_list(request, all_questions)

        return jsonify(
            {
                'questions': paginated_questions,
                'total_questions': len(all_questions),
                'categories': all_categories,
                'current_category': {'id': 1, 'type': 'prova'}
            }
        )

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
    
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    return app
