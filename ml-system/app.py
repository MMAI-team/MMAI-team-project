from flask import Flask, jsonify
import flask
from io import StringIO
from preprocessor import preprocess_data
from preprocessor import PreprocessorML
from preprocessor import DataLoader
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
    
    X, index_transformer = preprocess_data(data_df)
    
    X_FNN, index_fnn = DataLoader(batch_size = 2048).load_submit(data=data_df,
                                 preprocess=True, divide=False, params_path='dataset_config.json', columns_to_delete = [ 'city', 'dob', 'job',  'first', 'last','trans_date_trans_time','category','trans_num',
                      'lat','longs','merch_lat','merch_long','unix_time','street','merchant','state','zip','gender'], normalization=['amt', 'delta_time', 'distance', 'city_pop', 'age', 'hour', 'weekday'])


    print(X)
    preds_tranformer = transformer.predict(X)
    print(tf.argmax(preds_tranformer, axis=2))
    preds = preds_tranformer[0][index_transformer][1]
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
    print(X_FNN)
    preds_FNN = FNN.predict(X_FNN)
    print(preds_FNN)
    
    return jsonify({"transformer_scoring": float(preds),
                    "xgoost_regressor": abs(float(preds_xgboost[len(data_df) - 1])),
                    "random_forest_regressor": float(preds_random_forest_regressor[len(data_df) - 1]),
                    "FNN":float(preds_FNN)})


def define_model():
    global transformer, randomTree, XGBoost, FNN

    transformer = get_TRANSFORMER()
    randomTree = joblib.load('random_forest_regressor.ml')
    XGBoost = xgb.XGBRegressor(n_jobs=-1, tree_method='gpu_hist')
    XGBoost.load_model('model_xgb_reg_v_1.json')
    FNN = tf.keras.models.load_model('model_md_fnn_v3_0.h5')


    # the weights is in the folder 'weights', which is placed in the root of the src
    transformer.load_weights('trans_2_5.h5')

    return print("model loaded")


if __name__ == '__main__':
    #print(type(model))
    app.register_blueprint(model)
    define_model()
        
    app.run(host='0.0.0.0', port=5571)