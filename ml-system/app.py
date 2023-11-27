from flask import Flask, jsonify
import flask
from io import StringIO
from preprocessor import preprocess_data
from model import get_TRANSFORMER
import base64

import tensorflow as tf
import pandas as pd


from flask import Blueprint


app = Flask(__name__, instance_relative_config=True)

model = Blueprint(name="model", import_name=__name__, url_prefix="/api/v1/model")

@model.post('/submit')
def submit():
    
    data = flask.request.data
    
    data = base64.decodebytes(data).decode('utf-8')
    
    csv_io = StringIO(data)
    
    data_df = pd.read_csv(csv_io)
    
    X, index = preprocess_data(data_df)

    print(X)
    preds = model.predict(X)
    print(tf.argmax(preds, axis=2))
    preds = preds[0][index][1]
    print(preds)

    return jsonify({"Model Fraud Score:": float(preds)})


def define_model():
    global model

    model = get_TRANSFORMER()

    # the weights is in the folder 'weights', which is placed in the root of the src
    model.load_weights('trans_2_5.h5')

    return print("model loaded")


if __name__ == '__main__':    
    app.register_blueprint(model)
    define_model()
        
    app.run(host='0.0.0.0', port=80)