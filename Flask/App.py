#cd Projet1
#cd Flask
#venv\Scripts\activate
#source venv/bin/activate
#flask --app App.py run

#!pip install sentence_transformers

import time
import json
from flask import Flask, current_app
import numpy
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__, static_folder='build', static_url_path='/')
data = open('data.json', 'r')
abstract_vectors = open('abstract_vectors.npy')
app.data = json.load(data)
app.abstract_vectors = json.load(abstract_vectors)
searchResults = {'doctor': [{'info': {'name': "Billy Jones", 'description': "adghdgfgsfgfgaf", 'rating': 1, 'link': "ya.ru"}, 'lat': 18.52043, 'lng': 73.856743 }, {'info': {'name': "MD. Popov", 'description': "Greatest Medical Doctor Ever", 'rating': 100, 'link': "ya.ru"}, 'lat': 0, 'lng': 0 }], 
'scientist': [{'info': {'name': "Albert Einstein", 'description': "Greatest Scientist Ever", 'rating': 10, 'link': "https://ya.ru"}, 'lat': 23.52043, 'lng': 34.856743 }]}




@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/search/<searchQuery>')
def get_current_search(searchQuery):
    query_embedding = model.encode(searchQuery)
    vectors = util.cos_sim(query_embedding, current_app.abstract_vectors).tolist()[0]
    passages = []
    for i in range(len(vectors)):
        passages.append([vectors[i], i])
    passages = sorted(passages, key=lambda x: x[0], reverse=True)
    new_passages = []
    for i in range(len(passages)):
        if passages[i][0] >= 0.2:
            new_passages.append(passages[i])
        else:
            break

    author_count = {}
    for m in range(len(new_passages)):
        j = new_passages[m][1]
        for i in range(len(data[j]['authorships'])):
            if data[j]['authorships'][i][0] in author_count:
                author_count[data[j]['authorships'][i][0]][0] += 1
                author_count[data[j]['authorships'][i][0]][1].append(j)
            else:
                author_count[data[j]['authorships'][i][0]] = [1, [j]]
    return sorted(author_count.items(), key=lambda item: item[1], reverse=True)
