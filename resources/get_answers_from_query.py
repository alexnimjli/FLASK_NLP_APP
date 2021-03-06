from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
import nltk
from nltk import sent_tokenize
from utilities.url_text_extractor import check_for_url

def get_answers_from_query(request):
    """
    Uses infromational retrieval methods to get answers from user query about the inputed text. These queries are answered using the BERT NLP transformer.
    Input
    ----------
    request variable: Flask request variable containing the text for the article
    Returns
    ----------
    The answers to the query.
    """
    text = request.form['text']
    text = check_for_url(text)

    sentences = nltk.sent_tokenize(text)
    sentences = [s for s in sentences if s[-1] != "?"]
    query = request.form['query']

    '''
    This uses a Cross Encoder variant of a transformer.
    It is designed to return the most likely response given an input.
    i.e - its designed for question answering
    '''
    model = CrossEncoder('sentence-transformers/ce-ms-marco-TinyBERT-L-2')

    model_inputs = [[query, passage] for passage in sentences]
    print(model_inputs)
    scores = model.predict(model_inputs)

    #Sort the scores in decreasing order
    results = [{'input': inp, 'score': score} for inp, score in zip(model_inputs, scores)]
    results = sorted(results, key=lambda x: x['score'], reverse=True)

    answers = []
    print("Query:", query)
    for hit in results[0:3]:
        print("Score: {:.2f}".format(hit['score']), "\t", hit['input'][1],'\n')
        if hit['score'] > 0.0:
            answers.append(hit['input'][1])
    return answers
