from preprocessing import get_data
from models import vader
import matplotlib.pyplot as plt

data = get_data()
data.dropna(inplace=True)
vader_sentiments = []
i = 0
for row in data.iterrows():
    i += 1
    row_info = row[1]
    print(i)
    vader_result = vader(row_info['review_text'])
    current_max = 'neg'
    if vader_result['neu'] > vader_result['neg']:
        current_max = 'neu'
    if vader_result['pos'] > vader_result[current_max]:
        current_max = 'pos'
    vader_sentiments.append(current_max)

print("calculated sentiments")
plt.hist(vader_sentiments)
plt.show()
plt.hist(data['rating_sentiment'])
plt.show()
plt.hist(data['review_rating'])
plt.show()