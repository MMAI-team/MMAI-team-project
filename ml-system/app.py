from flask import Flask, jsonify
import flask
from io import StringIO
from preprocessor import preprocess_data
from preprocessor import PreprocessorML
from model import get_TRANSFORMER
import base64
import joblib

import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
import sklearn
import tensorflow as tf
import pandas as pd


from flask import Blueprint


app = Flask(__name__, instance_relative_config=True)

model = Blueprint(name="model", import_name=__name__, url_prefix="/api/v1/model")

@model.route('/submit', methods=['POST'])
def submit():
    
    data = flask.request.data
    
    data = base64.decodebytes(data).decode('utf-8')
    
    csv_io = StringIO(data)
    
    data_df = pd.read_csv(csv_io)
    
    X, index = preprocess_data(data_df)

    print(X)
    preds_tranformer = transformer.predict(X)
    print(tf.argmax(preds_tranformer, axis=2))
    preds = preds_tranformer[0][index][1]
    print(preds)
    
    preprocessorML = PreprocessorML()
    data = preprocessorML.preprocess_submit(data_df)
    data = data[['amt', 'zip', 'city_pop', 'age', 'delta_time', 'distance',
                 'gas_transport', 'grocery_pos', 'home', 'shopping_pos', 'kids_pets', 
                 'shopping_net', 'entertainment', 'food_dining', 'personal_care', 
                 'health_fitness', 'misc_pos', 'misc_net', 'grocery_net', 'travel', 
                 'work_hours', 'weekend', 'F', 'M', 'hour', 'weekday']]
    preds_random_forest_regressor = randomTree.predict(data)
    print(preds_random_forest_regressor)
    preds_xgboost = XGBoost.predict(data)
    print(preds_xgboost)
    return jsonify({"transformer_scoring": float(preds),
                    "xgoost_regressor": abs(float(preds_xgboost[len(data_df) - 1])),
                    "random_forest_regressor": float(preds_random_forest_regressor[len(data_df) - 1])})


def define_model():
    global transformer, randomTree, XGBoost

    transformer = get_TRANSFORMER()
    randomTree = joblib.load('random_forest_regressor.ml')
    XGBoost = xgb.XGBRegressor(n_jobs=-1, tree_method='gpu_hist')
    XGBoost.load_model('model_xgb_reg_v_1.json')

    # the weights is in the folder 'weights', which is placed in the root of the src
    transformer.load_weights('trans_2_5.h5')

    return print("model loaded")


if __name__ == '__main__':
    #print(type(model))
    app.register_blueprint(model)
    define_model()
        
    app.run(host='0.0.0.0', port=5571)