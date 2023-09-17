import json
import time
import requests



def AuthorEncounters(data):
    author_count = {}
    for j in range(len(data)):
        for i in range(len(data[j]['authorships'])):
            if data[j]['authorships'][i][0] in author_count:
                author_count[data[j]['authorships'][i][0]] += 1
            else:
                author_count[data[j]['authorships'][i][0]] = 1
    return sorted(author_count.items(), key=lambda item: item[1], reverse=True)


def LoadText(abstract_inverted_index):
    if abstract_inverted_index is None:
        return ('abstract is missing')
    word_max = 0
    abstract_words = list(abstract_inverted_index)
    for word_index in range(len(abstract_inverted_index)):
        for number in range(len(abstract_inverted_index[abstract_words[word_index]])):
            x = abstract_inverted_index[abstract_words[word_index]][number]
            if int(x) > word_max:
                word_max = int(x)
    text = [' '] * (word_max + 1)
    for word_index in range(len(abstract_inverted_index)):
        for number in range(len(abstract_inverted_index[abstract_words[word_index]])):
            text[abstract_inverted_index[abstract_words[word_index]][number]] = abstract_words[word_index]
    return ' '.join(text)



def LoadAuthor(date, pages, cites=20):
    answer = []
    j = 1
    cursor_file = open('cursor.txt', 'r')
    cursorlist = cursor_file.readlines()
    cursor_file.close()
    print(cursorlist)
    if cursorlist == []:
        cursor = '*'
    else:
        cursor = cursorlist[-1].replace('\n', '')
    cur = open('cursor.txt', 'w+')
    jj = open('data1.json', 'r')
    content = jj.read()
    if len(str(content)) == 0:
        content = []
    else:
        content = json.load(jj)
    jj.close()
    json_file = open('data1.json', 'w')

    while j < pages + 1:
        print(j)
        #добавь обратно "" в url
        url = f"https://api.openalex.org/works?filter=from_publication_date:{date},cited-by-count:>{cites},has_abstract:true&per-page=200&select=display_name,id,authorships,abstract_inverted_index&cursor={cursor}"
        response = requests.get(url)
        json_responce = response.json()
        if not 'results' in json_responce:
            if json_responce['error'] == 'Pagination error.':
                json.dump(content, json_file)
                json_file.close()
                exit()
            else:
                print(json_responce)
                time.sleep(1.0)
        else:
            cursor = json_responce['meta']['next_cursor']
            print(cursor)
            answer_list = json_responce['results']
            for i in range(len(answer_list)):
                authors = []
                for x in range(len(answer_list[i]['authorships'])):
                    try:
                        authors.append([answer_list[i]['authorships'][x]['author']['id'], answer_list[i]['authorships'][x]['author']['display_name']])
                    except KeyError:
                        pass
                text = LoadText(answer_list[i]['abstract_inverted_index'])

                content.append({'display-name': answer_list[i]['display_name'], 'id': answer_list[i]['id'], 'authorships': authors, 'abstract': text})
            cur.write(f'{cursor}\n')
            j += 1

    json.dump(content, json_file)
    json_file.close()

LoadAuthor('2020-01-01', 999999999999999999)
#LoadText({"Abstract": [0], "This": [1], "article": [2], "provides": [3], "an": [4, 31, 73, 103], "update": [5], "on": [6, 28], "the": [7, 12, 23, 67, 96, 238], "global": [8, 178, 255], "cancer": [9, 17, 36, 48, 61, 65, 94, 100, 179, 241, 247, 256], "burden": [10, 180], "using": [11], "GLOBOCAN": [13], "2020": [14], "estimates": [15], "of": [16, 99, 240, 246], "incidence": [18, 123], "and": [19, 44, 89, 117, 144, 153, 170, 227, 244], "mortality": [20, 139], "produced": [21], "by": [22, 81, 110, 220], "International": [24], "Agency": [25], "for": [26, 135, 142, 146, 150, 237, 254], "Research": [27], "Cancer.": [29], "Worldwide,": [30], "estimated": [32, 74, 104], "19.3": [33], "million": [34, 39, 47, 51, 76, 106, 186], "new": [35, 77], "cases": [37, 78, 187], "(18.1": [38], "excluding": [40, 52], "nonmelanoma": [41, 53], "skin": [42, 54], "cancer)": [43, 55], "almost": [45], "10.0": [46], "deaths": [49, 107], "(9.9": [50], "occurred": [56], "in": [57, 130, 160, 188, 199, 249], "2020.": [58], "Female": [59], "breast": [60, 119, 152], "has": [62], "surpassed": [63], "lung": [64, 82], "as": [66], "most": [68], "commonly": [69], "diagnosed": [70], "cancer,": [71], "with": [72, 102, 195, 225], "2.3": [75], "(11.7%),": [79], "followed": [80, 109], "(11.4%),": [83], "colorectal": [84, 111], "(10.0": [85], "%),": [86], "prostate": [87], "(7.3%),": [88], "stomach": [90, 115], "(5.6%)": [91], "cancers.": [92, 121], "Lung": [93], "remained": [95], "leading": [97], "cause": [98], "death,": [101], "1.8": [105], "(18%),": [108], "(9.4%),": [112], "liver": [113], "(8.3%),": [114], "(7.7%),": [116], "female": [118, 151], "(6.9%)": [120], "Overall": [122], "was": [124], "from": [125, 193], "2\u2010fold": [126], "to": [127, 183, 202, 207, 211, 232], "3\u2010fold": [128], "higher": [129, 159], "transitioned": [131, 163, 205], "versus": [132, 162, 204], "transitioning": [133, 161, 200, 250], "countries": [134, 164, 209, 251], "both": [136], "sexes,": [137], "whereas": [138], "varied": [140], "&lt;2\u2010fold": [141], "men": [143], "little": [145], "women.": [147], "Death": [148], "rates": [149], "cervical": [154], "cancers,": [155], "however,": [156], "were": [157], "considerably": [158], "(15.0": [165], "vs": [166, 172], "12.8": [167], "per": [168, 174], "100,000": [169], "12.4": [171], "5.2": [173], "100,000,": [175], "respectively).": [176], "The": [177], "is": [181, 252], "expected": [182], "be": [184, 217], "28.4": [185], "2040,": [189], "a": [190, 196, 228, 234], "47%": [191], "rise": [192], "2020,": [194], "larger": [197], "increase": [198], "(64%": [201], "95%)": [203], "(32%": [206], "56%)": [208], "due": [210], "demographic": [212], "changes,": [213], "although": [214], "this": [215], "may": [216], "further": [218], "exacerbated": [219], "increasing": [221], "risk": [222], "factors": [223], "associated": [224], "globalization": [226], "growing": [229], "economy.": [230], "Efforts": [231], "build": [233], "sustainable": [235], "infrastructure": [236], "dissemination": [239], "prevention": [242], "measures": [243], "provision": [245], "care": [248], "critical": [253], "control.": [257]})
#print(AuthorEncounters(data))