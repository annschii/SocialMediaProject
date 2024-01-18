from flask import Flask, request, jsonify
from transformers import pipeline
sentimentanalyzer = pipeline("sentiment-analysis")

app = Flask(__name__)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get('text', '')

    # Perform sentiment analysis (provisional implementation)
    sentiment = sentimentanalyzer(text)[0]

    return jsonify({'sentiment': sentiment['label']})

def provisional_sentiment_analysis(text):
    # Placeholder for provisional sentiment analysis
    # You can replace this with a more sophisticated model later
    return 'positive'  # Placeholder sentiment result



if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port=5000, debug=True) #otherwise it does not work for me

