from flask import Flask, request, jsonify
from flask_cors import CORS
import utils
import database

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins":"*"
    }
})

@app.route('/get_column_info', methods=['GET'])
def get_column_info():
    return utils.get_col_info()

@app.route('/predict_rating', methods=['GET', 'POST'])
def predict_rating():
    """Request information is transferred into a 2D array, which is then preprocessed by an
    initialized pipeline. Pipeline output is fed into the model, where a prediction result is
    finally sent into a json as a response"""
    data_columns = utils.get_data_columns()

    form_dict = utils.add_len_sentiment(request.form.to_dict())

    answers = []
    for col in data_columns:
        # Create an array of feature values in order of data_columns
        entry = form_dict[col]

        # Invalid entries have an "" value for their key
        if (entry == ""):
            # Return the index of the data column with invalid entry, which is handled by
            # on_clicked_rating_pred() in app.js
            response = jsonify({
                'rating': col
            })

            # No prediction; return immediately for error handling
            return response
        else:
            if col == "source":
                # All feature values are floats except for 'source', which is a str
                answers.append(entry)
            else:
                answers.append(float(entry))
    
    # Make prediction, return response
    rating = utils.make_prediction(utils.get_pipeline(), [answers]
    response = jsonify({
        'rating': rating
    })

    # Add entry to database
    database.insert_pred("database/mal_regression.db", form_dict)

    return response

@app.route('/get_db_row', methods=['GET', 'POST'])
def get_db_row():
    """Fetches the top nth scoring row in the mal_regression.db database"""

    form_dict = request.form.to_dict()
    return database.fetch_top_n("database/mal_regression.db", form_dict['n'], form_dict['rows'])

if __name__ == "__main__":
    print("Starting Python Flask Server for MyAnimeList Rating Prediction")
    utils.set_col_info('data_columns.json')
    utils.set_pipeline('gboost_pipe.pickle')
    app.run()