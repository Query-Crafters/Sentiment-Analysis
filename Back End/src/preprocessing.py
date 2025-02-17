import pandas as pd

def get_data():
    try:
        print("Loading Data...")
        df = pd.read_csv('data/apple_iphone_11_reviews.csv')
        df = preprocess_data(df)
        print("Dataframe loaded.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def preprocess_data(df):
    print("Processing Data...")
    df['review_text'] = df['review_text'].astype(str).str.lower()  # Convert to lowercase
    df['review_rating'] = df['review_rating'].str.split(" ", n=1, expand=True).iloc[:,0].astype('float')
    mapped_ratings = []
    for row in df.iterrows():
        row_info = row[1]
        rating = row_info['review_rating']
        if rating > 3.0:
            mapped_ratings.append("positive")
        elif rating < 3.0:
            mapped_ratings.append("negative")
        else:
            mapped_ratings.append("neutral")
    df['rating_sentiment'] = mapped_ratings
    print("Data Loaded With", len(df), "Rows And", df.shape[1], "Columns")
    return df[['review_text', 'review_rating', 'rating_sentiment']]
