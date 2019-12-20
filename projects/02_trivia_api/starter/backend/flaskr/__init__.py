import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging
from logging import Formatter, FileHandler



from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 5


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

    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

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
        end = start + QUESTIONS_PER_PAGE

        if start > len(item_list):
            abort(422) # Unprocessable Entity

        return item_list[start:end]

    @app.route('/categories')
    def get_categories():
        all_categories_dict = {item.id: item.type  for item in Category.query.all()}
        return jsonify({
            'categories': all_categories_dict
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_category(category_id):
        single_category = Category.query.filter(Category.id == category_id).one_or_none()

        if single_category is None:
            abort(404)

        questions_per_category = Question.query.filter(Question.category == single_category.id).all()

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
        all_categories_dict = {item.id: item.type  for item in Category.query.all()}
        paginated_questions = _paginated_list(request, all_questions)

        return jsonify(
            {
                'questions': paginated_questions,
                'total_questions': len(all_questions),
                'categories': all_categories_dict
            }
        )

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        deleting_question = Question.query.filter(Question.id == question_id).one_or_none()

        if delete_question is None:
            abort(404)

        deleting_question.delete()
        return jsonify(
            {
                'success': True,
                'question': deleting_question.id,
                'error': False
            }
        )

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    def _post_new_question(request):
        request_body_dict = request.get_json()

        new_question = Question(**request_body_dict)
        new_question.insert()

        return jsonify(
            {
                'success': True,
                'question': new_question.id,
                'error': False
            }
        )

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions', methods=['POST'])
    def manage_question_post():
        try:
            request_dict = request.get_json()
            app.logger.info(request_dict)
            if request_dict.get('searchTerm'):
                _search_question(request)
            else:
                _post_new_question(request)
        except:
            abort(400)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
    
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    def _search_question(request):
        found_questions = Question.query.filter(Question.question.ilike('%{}%'.format(request.get_json('searchTerm')))).all()
        app.logger.info(found_questions)

        return jsonify(
            {
                'questions': [item.format() for item in found_questions],
                'total_questions': len(found_questions),
                'current_category': {'ciao'}
            }
        )

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
