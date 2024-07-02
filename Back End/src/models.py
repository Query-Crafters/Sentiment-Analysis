from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def vader(review):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(review)
    return sentiment_dict

def roberta(review):
    # TODO
    return None