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
