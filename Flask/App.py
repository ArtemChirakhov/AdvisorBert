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
from numpy import dot
from numpy.linalg import norm

app = Flask(__name__, static_folder='build', static_url_path='/')
data = open("venv/data.json", 'r')
abstract_vectors = numpy.loadtxt('1.csv')
app.vectors = abstract_vectors
app.data = json.load(data)
searchResults = {'doctor': [{'info': {'name': "Billy Jones", 'description': "adghdgfgsfgfgaf", 'rating': 1, 'link': "ya.ru"}, 'lat': 18.52043, 'lng': 73.856743 }, {'info': {'name': "MD. Popov", 'description': "Greatest Medical Doctor Ever", 'rating': 100, 'link': "ya.ru"}, 'lat': 0, 'lng': 0 }],
'scientist': [{'info': {'name': "Albert Einstein", 'description': "Greatest Scientist Ever", 'rating': 10, 'link': "https://ya.ru"}, 'lat': 23.52043, 'lng': 34.856743 }]}



@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/search/<searchQuery>')
def get_current_search(searchQuery):
    model = SentenceTransformer('msmarco-distilbert-base-v4')
    query_embedding = model.encode(searchQuery)
    for i in range(1):
        vectors = dot(current_app.vectors, query_embedding)/(norm(query_embedding) * norm(current_app.vectors))
        passages = []
        for i in range(len(vectors)):
            passages.append([vectors[i], i])
        passages = sorted(passages, key=lambda x: x[0], reverse=True)
        print(passages)
        new_passages = []
        for i in range(len(passages)):
            if passages[i][0] >= 0:
                print(passages[i][0])
                new_passages.append(passages[i])
            else:
                break
        print(new_passages[0])
        author_count = {}
        for m in range(len(new_passages)):
            j = new_passages[m][1]
            for i in range(len(data[j]['authorships'])):
                if data[j]['authorships'][i][0] in author_count:
                    author_count[data[j]['authorships'][i][0]][0] += 1
                    author_count[data[j]['authorships'][i][0]][1].append(j)
                else:
                    author_count[data[j]['authorships'][i][0]] = [1, [j]]
            print(author_count[data[j]['authorships'][i][0]])
        return sorted(author_count.items(), key=lambda item: item[1], reverse=True)
