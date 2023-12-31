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
import random

app = Flask(__name__, static_folder='build', static_url_path='/')
with open('../data1.json', 'r') as data_file:
    app.data = json.load(data_file)
with open('vectors.npy', 'rb') as vectors_file:
    app.vectors = numpy.load(vectors_file)
with open('authors_with_inst.json') as ins:
    app.authors_enriched = json.load(ins)

app.model = SentenceTransformer('msmarco-distilbert-base-v4')

@app.route('/search/<searchQuery>')
def get_current_search(searchQuery):
    data = current_app.data
    query_embedding = current_app.model.encode(searchQuery)
    vectors = dot(current_app.vectors, query_embedding)/(norm(query_embedding) * norm(current_app.vectors, axis=1))
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
                author_count[data[j]['authorships'][i][0]]['count'] += 1
                author_count[data[j]['authorships'][i][0]]['publications'].append(data[j]['display-name'])
            else:
                author_count[data[j]['authorships'][i][0]] = {
                    'count': 1,
                    'publications': [data[j]['display-name']]
                }
                [1, [data[j]]]
    
    return_authors = []
    for author_id, data in author_count.items():
        if (author_id in current_app.authors_enriched and data['count'] > 3 and 
           current_app.authors_enriched[author_id]['inst']['lat'] is not None and 
           current_app.authors_enriched[author_id]['inst']['lon'] is not None): 
            return_authors.append({
                'info': {
                    'name': current_app.authors_enriched[author_id]['display_name'],
                    'insitution': current_app.authors_enriched[author_id]['inst']['name']
                },
                'coord': {
                    'lat': current_app.authors_enriched[author_id]['inst']['lat'] + random.random() * 0.1,
                    'lng': current_app.authors_enriched[author_id]['inst']['lon'] + random.random() * 0.1
                },
                'publications': data['publications']
            })

    return return_authors
