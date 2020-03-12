from flask import Flask, request, jsonify, abort
from functools import wraps

app = Flask(__name__)

greetings = {
            'en': 'hello', 
            'es': 'Hola', 
            'ar': 'مرحبا',
            'ru': 'Привет',
            'fi': 'Hei',
            'he': 'שלום',
            'ja': 'こんにちは'
            }

@app.route('/greeting', methods=['GET'])
def greeting_all():
    return jsonify({'greetings': greetings})

@app.route('/greeting/<lang>', methods=['GET'])
def greeting_one(lang):
    print(lang)
    if(lang not in greetings):
        abort(404)
    return jsonify({'greeting': greetings[lang
    ]})

@app.route('/greeting', methods=['POST'])
def greeting_add():
    info = request.get_json()
    if('lang' not in info or 'greeting' not in info):
        abort(422)
    greetings[info['lang']] = info['greeting']
    return jsonify({'greetings':greetings})

# Let's add a simple decorator to inject a greeting
def add_greeting(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print("Hello!")
        return f(*args, **kwargs)
    return wrapper

@add_greeting
def print_name(name):
    print(name)


print_name("sandy")



# Let's add some complexity in the form of a paramater
def add_greeting(greeting=''):
    def add_greeting_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(greeting)
            return f(*args, **kwargs)
        return wrapper
    return add_greeting_decorator

@add_greeting("what's up!")
def print_name(name):
    print(name)


print_name("kathy")


# We can also pass information back to the wrapped method
def add_greeting(greeting=''):
    def add_greeting_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(greeting)
            return f(greeting, *args, **kwargs)
        return wrapper
    return add_greeting_decorator

@add_greeting("Yo!")
def print_name(greeting, name):
    print(greeting)
    print(name)


print_name("Abe")