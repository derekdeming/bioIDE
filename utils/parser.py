import json

def process_paper_data(paper_json):
    paper_data = {}

    paper_data['doi'] = paper_json['doi']
    paper_data['title'] = paper_json['title']
    paper_data['authors'] = paper_json['authors'].split('; ')
    paper_data['date'] = paper_json['date']
    paper_data['category'] = paper_json['category']
    paper_data['abstract'] = paper_json['abstract']

    # convert the dictionary to a JSON string
    json_data = json.dumps(paper_data)
    
    return json_data





# def preprocess_text(text):

#     text = text.lower()
#     text = re.sub(r'[^\w\s]', '', text)
#     tokens = word_tokenize(text)
#     # remove stopwords from tokens 
#     tokens = [token for token in tokens if token not in stopwords.words('english')]

#     # lemmatize tokens -- this is so that
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(token) for token in tokens]

#     return ' '.join(tokens)