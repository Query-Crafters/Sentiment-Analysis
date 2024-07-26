from preprocessing import preprocess_data
from models import vader
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from analysis import analyze_reviews
from flask import request
import pandas as pd
import json
import os
import re


app = Flask(__name__)
CORS(app)

    

@app.route('/reviews', methods=['POST'])
def reviews():
    data = pd.DataFrame(json.loads(request.data))
    data = preprocess_data(data)
    results = analyze_reviews(data)
    return jsonify(results)

@app.route('/add_review', methods=['POST'])
def add_review():
    global df
    try:
        new_review = request.json
        new_df = pd.DataFrame([new_review])
        new_df['review_text'] = new_df['review_text'].astype(str).str.lower()  # Convert to lowercase
        new_df['review_rating'] = new_df['review_rating'].apply(
            lambda x: int(re.search(r'\d+', x).group()))  # Extract and convert ratings to integers
        df = pd.concat([df, new_df], ignore_index=True)
        return jsonify({'message': 'Review added successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/lsa_plot', methods=['GET'])
def lsa_plot():
    if os.path.exists('lsa_plot.png'):
        return send_file('lsa_plot.png', mimetype='image/png')
    else:
        return "Plot not found", 404


@app.route('/confusion_matrix', methods=['GET'])
def confusion_matrix_route():
    if os.path.exists('confusion_matrix.png'):
        return send_file('confusion_matrix.png', mimetype='image/png')
    else:
        return "Plot not found", 404

if __name__ == '__main__':
    app.run(debug=True)