from preprocessing import preprocess_data
from models import vader
from flask import Flask, jsonify
from flask_cors import CORS
from analysis import analyze_reviews
from flask import request
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

    

@app.route('/reviews', methods=['POST'])
def reviews():
    data = pd.DataFrame(json.loads(request.data))
    data = preprocess_data(data)
    results = analyze_reviews(data)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)