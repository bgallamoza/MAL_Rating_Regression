from flask import Flask, request, jsonify
from flask_cors import CORS
import utils

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
def predict_crkcoc_usage():
    """Request information is transferred into a 2D array, which is then preprocessed by an
    initialized pipeline. Pipeline output is fed into the model, where a prediction result is
    finally sent into a json as a response"""
    data_columns = utils.get_data_columns()

    answers = []
    for col in data_columns:
        # Create an array of feature values in order of data_columns
        entry = request.form[col]

        # Invalid entries have an "Error" value for their key
        if (entry == "Error"):
            # Return the index of the data column with invalid entry, which is handled by
            # on_clicked_rating_pred() in app.js
            response = jsonify({
                'rating': str(data_columns.index(col))
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
    response = jsonify({
        'rating': utils.make_prediction(utils.get_pipeline(), [answers])
    })

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server for MyAnimeList Rating Prediction")
    utils.set_col_info('data_columns.json')
    utils.set_pipeline('gboost_pipe.pickle')
    app.run()