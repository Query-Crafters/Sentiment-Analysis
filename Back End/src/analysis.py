import pandas as pd
from models import vader
from sklearn.metrics import confusion_matrix

def get_stopwords():
    stopwords = []
    with open('data/stopwords.txt') as f:
        [stopwords.append(line.strip()) for line in f.readlines()]
    return stopwords

def parse_confusion_matrix(test, pred):
    sklearn_matrix = confusion_matrix(test, pred)
    parsed_matrix = []
    for ls in sklearn_matrix:
        new_ls = []
        for elem in ls:
            new_ls.append(int(elem))
        parsed_matrix.append(new_ls)
    return parsed_matrix


def get_most_frequent_terms(df):
    term_frequencies = {'positive': dict(), 'negative': dict(), 'neutral': dict()}
    stopwords = get_stopwords()
    i = 0
    for row in df.iterrows():
        i += 1
        print(i)
        row_info = row[1]
        row_terms = row_info['review_text'].split(" ")
        sentiment = row_info['vader_sentiment']
        for term in row_terms:
            if term.lower() in stopwords:
                continue
            if term.lower() in term_frequencies.get(sentiment):
                term_frequencies.get(sentiment).get(term.lower())['count'] += 1
            else:
                term_frequencies.get(sentiment)[term.lower()] = {'label': term.lower(), 'count': 1}
    top_positive = sorted(term_frequencies.get('positive').values(), key= lambda x: x.get('count'), reverse=True)[:20]
    top_neutral = sorted(term_frequencies.get('neutral').values(), key= lambda x: x.get('count'), reverse=True)[:20]
    top_negative = sorted(term_frequencies.get('negative').values(), key= lambda x: x.get('count'), reverse=True)[:20]
    return {'positive': top_positive, 'neutral': top_neutral, 'negative': top_negative}



def analyze_reviews(df):
    sentiments = []
    try:
        for row in df.iterrows():
            review = row[1]
            vs = vader(review['review_text'])
            if vs['compound'] >= 0.05:
                sentiments.append("positive")
            elif vs['compound'] <= -0.05:
                sentiments.append("negative")
            else:
                sentiments.append("neutral")
        df['vader_sentiment'] = sentiments
        sentiment_counts = df['vader_sentiment'].value_counts()
        sentiment_count_list =[]
        for i, x in enumerate(sentiment_counts):
            sentiment_count_list.append({"value": x, "label": sentiment_counts.index[i]})
        df_dict = df[['review_text', 'review_rating', 'rating_sentiment', 'vader_sentiment']].to_dict(orient='records')
        matrix = parse_confusion_matrix(df['rating_sentiment'], df['vader_sentiment'])
        most_frequent_terms = get_most_frequent_terms(df)
        return {"dataframe": df_dict, "confusion_matrix": matrix, "vader_sentiment_counts": sentiment_count_list, 'most_frequent_terms': most_frequent_terms}
    except Exception as e:
        print(f"Error loading or processing data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error