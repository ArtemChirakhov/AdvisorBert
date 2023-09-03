import json
import requests



def LoadAuthor(date, pages, cites=20):
    answer = []
    for j in range(1, pages + 1):    
        url = f"https://api.openalex.org/works?filter=from_publication_date:{date},cited-by-count:>{cites}&per-page=200&page={j}&select=display_name,id,authorships,abstract_inverted_index"
        response = requests.get(url)
        json_responce = response.json()
        answer_list = json_responce['results']
        for i in range(len(answer_list)):
            authors = []
            for x in range(len(answer_list[i]['authorships'])):
                try:
                    authors = (answer_list[i]['authorships'][x]['author']['id'])
                except KeyError:
                    pass
        del answer_list[i]['authorships']
        answer_list[i]['authorships'] = authors
    print(answer_list[1])
    with open('data.json', 'w+') as f:
        json.dump(answer_list, f)
        
