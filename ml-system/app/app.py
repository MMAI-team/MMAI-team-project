from flask import Flask, jsonify
import flask
from flask import Blueprint
from io import StringIO
from preprocessor import preprocess_data
from preprocessor import PreprocessorML
from preprocessor import DataLoader
from model import get_TRANSFORMER
import base64
import joblib

import xgboost as xgb
import tensorflow as tf
import pandas as pd


def get_predictions_transformer(data) -> "transformer":
    X, index = preprocess_data(data.copy())
    predictions = transformer.predict(X)  # Get prediction on all of the
    # transactions, but we need only the specific

    return float(predictions[0][index][1])


def get_predictions_fnn(data) -> "fnn":
    X, _ = DataLoader(batch_size=2048).load_submit(
        data=data.iloc[len(data) - 1 :],
        preprocess=True,
        divide=False,
        params_path="dataset_config.json",
        columns_to_delete=[
            "city",
            "dob",
            "job",
            "first",
            "last",
            "trans_date_trans_time",
            "category",
            "trans_num",
            "lat",
            "longs",
            "merch_lat",
            "merch_long",
            "unix_time",
            "street",
            "merchant",
            "state",
            "zip",
            "gender",
        ],
        normalization=[
            "amt",
            "delta_time",
            "distance",
            "city_pop",
            "age",
            "hour",
            "weekday",
        ],
    )

    prediction = FNN.predict(X)
    return float(prediction)


def get_predictions_random_forest(data) -> "random_forest":
    preprocessor = PreprocessorML()
    data = preprocessor.preprocess_submit(data)
    data = data[
        [
            "amt",
            "zip",
            "city_pop",
            "age",
            "delta_time",
            "distance",
            "gas_transport",
            "grocery_pos",
            "home",
            "shopping_pos",
            "kids_pets",
            "shopping_net",
            "entertainment",
            "food_dining",
            "personal_care",
            "health_fitness",
            "misc_pos",
            "misc_net",
            "grocery_net",
            "travel",
            "work_hours",
            "weekend",
            "F",
            "M",
            "hour",
            "weekday",
        ]
    ]
    predictions = randomTree.predict(data)
    return float(predictions[len(data) - 1])


def get_predictions_xgboost(data) -> "xgboost":
    preprocessor = PreprocessorML()
    data = preprocessor.preprocess_submit(data)
    data = data[
        [
            "amt",
            "zip",
            "city_pop",
            "age",
            "delta_time",
            "distance",
            "gas_transport",
            "grocery_pos",
            "home",
            "shopping_pos",
            "kids_pets",
            "shopping_net",
            "entertainment",
            "food_dining",
            "personal_care",
            "health_fitness",
            "misc_pos",
            "misc_net",
            "grocery_net",
            "travel",
            "work_hours",
            "weekend",
            "F",
            "M",
            "hour",
            "weekday",
        ]
    ]
    predictions = XGBoost.predict(data)
    return float(predictions[len(data) - 1])


def get_predictions(data):
    l_models = [
        get_predictions_fnn,
        get_predictions_transformer,
        get_predictions_random_forest,
        get_predictions_xgboost,
    ]

    dict_predictions = {}

    for model in l_models:
        dict_predictions[model.__annotations__["return"]] = model(data)

    return dict_predictions


def convert_data_to_df(data):
    data = base64.decodebytes(data).decode("utf-8")
    csv_io = StringIO(data)
    return pd.read_csv(csv_io)


def define_models():
    global transformer, randomTree, XGBoost, FNN

    transformer = get_TRANSFORMER()
    randomTree = joblib.load("random_forest_regressor.ml")
    XGBoost = xgb.XGBRegressor(n_jobs=-1, tree_method="gpu_hist")
    XGBoost.load_model("model_xgb_reg_v_1.json")
    FNN = tf.keras.models.load_model("model_md_fnn_v3_0.h5")

    # the weights is in the folder 'weights', which is placed in the root of the src
    transformer.load_weights("trans_2_5.h5")

    return print("model loaded")


app = Flask(__name__, instance_relative_config=True)
model = Blueprint(name="model", import_name=__name__, url_prefix="/api/v1/model")


@model.route("/submit", methods=["POST"])
def submit():
    # Receives data from the server (transaction to process + 29 historical
    # transactions)
    data = flask.request.data
    data_df = convert_data_to_df(data=data)
    # At this step data converted into a dataframe

    predictions = get_predictions(data_df)

    return jsonify(predictions)


if __name__ == "__main__":
    # print(type(model))
    app.register_blueprint(model)
    define_models()

    app.run(host="0.0.0.0", port=5571)
