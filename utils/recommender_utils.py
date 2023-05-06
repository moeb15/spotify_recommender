import pandas as pd
import numpy as np


def recommend_artists(genre_lst,model,encoder,data,rec_count):
    
    genre_df = pd.DataFrame({'Subgenre':[genre_lst]})
    genre_df['Subgenre'] = genre_df['Subgenre'].astype('string')
    genre_enc = encoder.transform(genre_df['Subgenre'])

    user_cluster = model.predict(genre_enc)
    user_recommendations = data[model.labels_ == user_cluster]['Artist'].to_numpy()
    idx = np.random.randint(0,len(user_recommendations),rec_count)
    return user_recommendations[idx]