# analysis.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessing import get_data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

def load_stopwords(filepath):
    """Loads stopwords from a given file."""
    with open(filepath, 'r') as file:
        stopwords = file.read().splitlines()
    return stopwords

def analyze_reviews(dataframe):
    # Ensure proper sentiment processing
    sentiment_by_rating = dataframe.groupby('review_rating')['rating_sentiment'].value_counts(normalize=True).unstack().fillna(0)

def get_lsa_matrix(dataframe):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(dataframe['review_text'])
    svd = TruncatedSVD(n_components=2)
    lsa_matrix = svd.fit_transform(tfidf_matrix)
    x = lsa_matrix[:, 0]
    y = lsa_matrix[:, 1]
    c = list(dataframe['vader_sentiment'].apply(lambda x: 1 if x >= 0.05 else (-1 if x <= -0.05 else 0)))
    pos = {"label": "Positive", "data": []}
    neu = {"label": "Neutral", "data": []}
    neg = {"label": "Negative", "data": []}
    for i in range(len(x)):
        datapoint = {"x": x[i], "y": y[i], "id": i}
        if c[i] == 1:
            pos["data"].append(datapoint)
        if c[i] == 0:
            neu["data"].append(datapoint)
        if c[i] == -1:
            neg["data"].append(datapoint)
    result = [pos, neu, neg]
    return result


def get_most_frequent_terms(df):
    term_frequencies = {'positive': dict(), 'negative': dict(), 'neutral': dict(), 'one_two_three': dict(), 'four': dict(), 'five': dict()}
    stopwords = get_stopwords()
    i = 0
    for row in df.iterrows():
        i += 1
        print(i)
        
        row_info = row[1]
        row_terms = row_info['review_text'].split(" ")
        sentiment = row_info['vader_sentiment_label']
        rating = row_info['review_rating']
        for term in row_terms:
            if term.lower() in stopwords:
                continue
            if rating <= 3:
                rating_key = 'one_two_three'
            if rating == 4:
                rating_key = "four"
            if rating == 5:
                rating_key = "five"
            if term.lower() in term_frequencies.get(sentiment):
                term_frequencies.get(sentiment).get(term.lower())['count'] += 1
            else:
                term_frequencies.get(sentiment)[term.lower()] = {'label': term.lower(), 'count': 1}
            if term.lower() in term_frequencies.get(rating_key):
                term_frequencies.get(rating_key).get(term.lower())['count'] += 1
            else:
                term_frequencies.get(rating_key)[term.lower()] = {'label': term.lower(), 'count': 1}
    top_positive = sorted(term_frequencies.get('positive').values(), key= lambda x: x.get('count'), reverse=True)[:20]
    top_neutral = sorted(term_frequencies.get('neutral').values(), key= lambda x: x.get('count'), reverse=True)[:20]
    top_negative = sorted(term_frequencies.get('negative').values(), key= lambda x: x.get('count'), reverse=True)[:20]
    top_one_two_three = sorted(term_frequencies.get('one_two_three').values(), key= lambda x: x.get('count'), reverse=True)[:20]
    top_four = sorted(term_frequencies.get('four').values(), key= lambda x: x.get('count'), reverse=True)[:20]
    top_five = sorted(term_frequencies.get('five').values(), key= lambda x: x.get('count'), reverse=True)[:20]
    return {'positive': top_positive, 
            'neutral': top_neutral, 
            'negative': top_negative, 
            'one_two_three':  top_one_two_three, 
            'four': top_four, 
            'five': top_five}
    # Load stop words
    stopwords = load_stopwords('data/stopwords.txt')

    # TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords, max_features=1000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(dataframe['review_text'])

    # Train Naive Bayes Classifier
    X_train, X_test, y_train, y_test = train_test_split(
        tfidf_matrix, dataframe['rating_sentiment'], test_size=0.25, random_state=42,
        stratify=dataframe['rating_sentiment']
    )
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train, y_train)
    y_pred = nb_classifier.predict(X_test)

    # Evaluation
    conf_matrix = confusion_matrix(y_test, y_pred, labels=['positive', 'neutral', 'negative'])
    class_report = classification_report(y_test, y_pred, target_names=['positive', 'neutral', 'negative'], output_dict=True)

def analyze_reviews(df):
    try:
        df['vader_sentiment'] = df['review_text'].apply(lambda x: vader(x)['compound'])
        df['vader_sentiment_label'] = df['vader_sentiment'].apply(
        lambda x: 'positive' if x >= 0.05 else ('negative' if x <= -0.05 else 'neutral'))
        sentiment_counts = df['vader_sentiment_label'].value_counts()
        sentiment_count_list =[]
        rating_counts = df['review_rating'].value_counts()
        rating_count_list =[]
        for i, x in enumerate(sentiment_counts):
            sentiment_count_list.append({"value": x, "label": sentiment_counts.index[i]})
        
        for i, x in enumerate(rating_counts):
            rating_count_list.append({"value": x, "label": str(rating_counts.index[i])})
        df_dict = df[['review_text', 'review_rating', 'rating_sentiment', 'vader_sentiment']].to_dict(orient='records')
        actual_labels = df['review_rating'].apply(
            lambda x: 'positive' if x >= 4 else ('negative' if x <= 2 else 'neutral'))
        predicted_labels = df['vader_sentiment_label']
        conf_matrix = parse_confusion_matrix(actual_labels, predicted_labels)
        most_frequent_terms = get_most_frequent_terms(df)
        lsa_matrix = get_lsa_matrix(df)
        return {"dataframe": df_dict, 
                "confusion_matrix": conf_matrix, 
                "vader_sentiment_counts": sentiment_count_list, 
                'rating_counts': rating_count_list,
                'most_frequent_terms': most_frequent_terms, 
                'lsa_matrix': lsa_matrix}
    except Exception as e:
        print(f"Error loading or processing data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    # LSA (Latent Semantic Analysis)
    svd = TruncatedSVD(n_components=2)
    lsa_matrix = svd.fit_transform(tfidf_matrix)

    plt.figure(figsize=(12, 8))
    plt.scatter(lsa_matrix[:, 0], lsa_matrix[:, 1],
                c=[0 if sentiment == 'neutral' else (1 if sentiment == 'positive' else -1) for sentiment in dataframe['rating_sentiment']],
                cmap='coolwarm', alpha=0.7)
    plt.title('LSA of Review Texts')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.colorbar(label='Sentiment')
    plot_path = 'lsa_plot.png'
    plt.savefig(plot_path)
    plt.close()

    terms = tfidf_vectorizer.get_feature_names_out()
    topics = []
    for i, comp in enumerate(svd.components_):
        terms_in_topic = [terms[i] for i in comp.argsort()[:-11:-1]]
        topics.append(f"Topic {i}: {' '.join(terms_in_topic)}")

    return sentiment_by_rating, plot_path, topics, conf_matrix, class_report
