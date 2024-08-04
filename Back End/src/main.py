import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request, send_file
import pandas as pd
from preprocessing import get_data, preprocess_data
from analysis import analyze_reviews
from models import vader
import seaborn as sns
import os
app = Flask(__name__)

df = pd.DataFrame()

@app.route('/reviews', methods=['GET'])
def reviews():
    global df
    try:
        sentiment_by_rating, plot_path, topics, conf_matrix, class_report = analyze_reviews(df)
        response = {
            'reviews': df[['review_text', 'review_rating', 'rating_sentiment']].to_dict(orient='records'),
            'sentiment_by_rating': sentiment_by_rating.to_dict(),
            'topics': topics,
            'confusion_matrix': conf_matrix.tolist(),
            'classification_report': class_report
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_review', methods=['POST'])
def add_review():
    global df
    try:
        new_review = request.json
        new_df = pd.DataFrame([new_review])
        new_df = preprocess_data(new_df)
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
def confusion_matrix_plot():
    global df
    try:
        _, _, _, conf_matrix, _ = analyze_reviews(df)
        conf_matrix_path = 'confusion_matrix.png'
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Positive', 'Neutral', 'Negative'],
                    yticklabels=['Positive', 'Neutral', 'Negative'])
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
        plt.savefig(conf_matrix_path)
        plt.close()
        return send_file(conf_matrix_path, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    df = get_data()  # Corrected to use get_data from preprocessing
    app.run(debug=True)
