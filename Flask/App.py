#cd Projet1
#cd Flask
#venv\Scripts\activate
#source venv/bin/activate
#flask --app App.py run

import time
from flask import Flask

app = Flask(__name__)
searchResults = {'doctor': [{'info': {'name': "Billy Jones", 'description': "adghdgfgsfgfgaf", 'rating': 1, 'link': "ya.ru"}, 'lat': 18.52043, 'lng': 73.856743 }, {'info': {'name': "MD. Popov", 'description': "Greatest Medical Doctor Ever", 'rating': 100, 'link': "ya.ru"}, 'lat': 0, 'lng': 0 }], 
'scientist': [{'info': {'name': "Albert Einstein", 'description': "Greatest Scientist Ever", 'rating': 10, 'link': "https://ya.ru"}, 'lat': 23.52043, 'lng': 34.856743 }]}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/search/<searchQuery>')
def get_current_search(searchQuery):
    return searchResults[searchQuery]