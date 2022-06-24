from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))

dfbooks = pickle.load(open('dfbooks.pkl', 'rb'))
xdf_pivot = pickle.load(open('xdf_pivot.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           bookName = list(popular_df['Book-Title'].values),
                           bookAuthor = list(popular_df['Book-Author'].values),
                           bookImages = list(popular_df['Image-URL-M'].values),
                           bookVotes = list(popular_df['num_ratings'].values),
                           bookRatins = list(popular_df['avg_rating'].values)
                           )

@app.route('/recommender')
def gui_recommend():
    return render_template('recommendation.html')

@app.route('/recommend_books', methods=['POST'])
def recommender():
    user_input = request.form.get('user_input')
    # fetch Book Index
    indx = np.where(xdf_pivot.index == user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity_score[indx])), key=lambda x: x[1], reverse=True)[1:11]
    data = []
    for i in similar_books:
        item = []
        temp_df = dfbooks[dfbooks['Book-Title'] == xdf_pivot.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return render_template('recommendation.html', data=data)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
