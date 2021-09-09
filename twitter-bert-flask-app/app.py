from flask import Flask
from transformers import BertTokenizer, DistilBertForSequenceClassification
from flask import request
from flask import jsonify
import re
from torch.nn import Softmax
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)

######## copy/pasted preprocessing from the classification notebook ########

URL_REGEX = re.compile('http(s)?:\/\/t.co\/\w+')
MENTION_REGEX = re.compile('@\w+')

def clean_tweet(tweet):
    # remove mentions, the pound sign, and replace urls with URL token
    tweet = re.sub(URL_REGEX, 'url', tweet)
    tweet = re.sub(MENTION_REGEX, '', tweet)
    tweet = tweet.replace('#', '')

    return tweet.strip()

######## copy/pasted preprocessing from the classification notebook ########

BERT_MODEL = 'distilbert-base-uncased'

print("Loading tokenzier + model")

bert_tokenizer = BertTokenizer.from_pretrained(BERT_MODEL)

sequence_classification_model = DistilBertForSequenceClassification.from_pretrained(
    'notebooks/clf/results', num_labels=2,
    output_attentions = False, # Whether the model returns attentions weights.
    output_hidden_states = False # Whether the model returns all hidden-states.
)


print("Loaded tokenzier + model!")

# Helper function to use our fine-tuned model

softmax = Softmax(dim=1)

def get_probability_of_disaster(tweet):
    cleaned_tweet = clean_tweet(tweet)
    results = sequence_classification_model(bert_tokenizer.encode(cleaned_tweet, return_tensors='pt'))
    probas = softmax(results.logits)
    return float(probas[0][1])

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/classify')
def classify():
    tweet = request.args.get('tweet')

    return jsonify(dict(tweet=tweet, probability=get_probability_of_disaster(tweet)))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
