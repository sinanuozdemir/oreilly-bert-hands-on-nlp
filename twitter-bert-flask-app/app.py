from flask import Flask
from transformers import pipeline
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

print("Loading tokenzier + model")

pipe = pipeline(
    "text-classification", '../notebooks/clf/results', tokenizer='distilbert-base-uncased',
    return_all_scores=True
)

print("Loaded tokenzier + model!")

# Helper function to use our fine-tuned model

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/classify')
def classify():
    tweet = request.args.get('tweet')
    results = pipe(clean_tweet(tweet))[0]
    print(results)

    return jsonify(dict(tweet=tweet, scores={result['label']: result['score'] for result in results}))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
