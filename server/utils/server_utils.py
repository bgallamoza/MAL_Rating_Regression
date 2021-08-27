import pickle
import gzip
import json
from utils import eda_utils

__col_info = None
__pipeline = None

def set_col_info(file):
    print("Loading data columns...")
    global __col_info

    with open("./artifacts/" + file, 'rb') as f:
        __col_info = json.load(f)

    print("Data columns and information successfully loaded")

def get_col_info():
    return __col_info

def get_data_columns():
    """Extracts the value from the 'data_columns' key in __col_info"""

    return get_col_info()['data_columns']

def set_pipeline(file):
    """Pipeline is loaded from a gzip file, which is then unpickled and used
    to initialize __model"""

    print("Loading Pipeline...")
    global __pipeline

    with open("./artifacts/" + file, 'rb') as f:
        with gzip.open("./artifacts/" + file, 'rb') as f:
            p = pickle.Unpickler(f)
            __pipeline = p.load()

    print("Pipeline successfully loaded")

def get_pipeline():
    return __pipeline

def make_prediction(pipeline, test_matrix):
    """Takes a model, pipeline, and test_matrix. Test matrix is
    transformed by the pipeline and fed into the model. A yes/no string
    is returned according to the prediction"""
    print(test_matrix)
    # test_matrix = pd.DataFrame(test_matrix, columns=get_data_columns())
    prediction = pipeline.predict(test_matrix)
    
    return "{pred: .2f}".format(pred = prediction[0])

def add_len_sentiment(form_dict):
    
    # Length features
    title_len = eda_utils.get_len_text(form_dict['en_title'])
    synopsis_len = eda_utils.get_len_text(form_dict['synopsis'])
    if title_len == 0:
        form_dict['title_len'] = ""
    else:
        form_dict['title_len'] = title_len
    if title_len == 0:
        form_dict['synopsis_len'] = ""
    else:
        form_dict['synopsis_len'] = synopsis_len
    
    # Polarity Sentiment
    form_dict['synop_pol'] = eda_utils.get_polarity(form_dict['en_title'])
    form_dict['title_pol'] = eda_utils.get_polarity(form_dict['synopsis'])

    # Subjectivity Sentiment
    form_dict['synop_subj'] = eda_utils.get_subjectivity(form_dict['en_title'])
    form_dict['title_subj'] = eda_utils.get_subjectivity(form_dict['synopsis'])

    return form_dict

# Main function to test utils functionality
if __name__ == "__main__":
    set_col_info('data_columns.json')
    set_pipeline('gboost_pipe.pickle')

    test_sample = [[1500, 22, 30, 802, 0.06857142857142856, 0.0, 0.38619047619047614,
       0.0, 2, 4.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
       1.0, 0.0, 0, 1.0, 0.0, 0.0, 0.0, 1, 'manga']]

    print(make_prediction(get_pipeline(), test_sample))

    test_dict = {"en_title": "Dogman Ultra",
    "synopsis": "Dogman is a man who must try to defeat the evil Catguy from destroying the world! Can he do it? Who knows."}

    print(add_len_sentiment(test_dict))