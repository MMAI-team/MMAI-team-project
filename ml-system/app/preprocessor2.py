import pandas as pd
import numpy as np
import datetime
from datetime import date, datetime
import tensorflow as tf
import json
import math

AUTOTUNE = tf.data.AUTOTUNE
from sklearn import preprocessing


class PreprocessorML:
    def __init__(self, normalization=False):
        self.norm = normalization

    def one_hot_category(self, dataset):
        hot = [
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
        ]

        for category in hot:
            dataset[category] = pd.Series(
                [1 if x.category == category else 0 for x in dataset.itertuples()],
                index=dataset.index,
            )

        return dataset

    def add_time(self, dataset):
        dataframe = dataset.sort_values(by=["cc_num", "unix_time"])

        delta_time = []

        previous_row = dataframe.iloc[0]

        delta_time.append(0)

        for row in dataframe[1:].itertuples():
            if row.cc_num == previous_row.cc_num:
                delta_time.append(row.unix_time - previous_row.unix_time)
            else:
                delta_time.append(0)

            previous_row = row

        dataframe["delta_time"] = pd.Series(delta_time, index=dataframe.index)

        return dataframe

    def parse_time(self, string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

    def add_workhour_category(self, dataset):
        dataset["work_hours"] = dataset["trans_date_trans_time"].apply(
            lambda x: int(
                self.parse_time(x).hour >= 6 and self.parse_time(x).hour <= 18
            )
        )
        return dataset

    def add_weekend_category(self, dataset):
        dataset["weekend"] = dataset["trans_date_trans_time"].apply(
            lambda x: int(
                self.parse_time(x).weekday() >= 5 and self.parse_time(x).weekday() <= 6
            )
        )
        return dataset

    def add_age(self, dataset):
        dataset["age"] = dataset["dob"].apply(
            lambda x: (date.today() - date.fromisoformat(x)).days // 365
        )
        return dataset

    def add_distance(self, dataset):
        lat1 = dataset["lat"]
        lon1 = dataset["long"]
        lat2 = dataset["merch_lat"]
        lon2 = dataset["merch_long"]
        dataset["distance"] = (
            np.arccos(
                np.sin(lat1) * np.sin(lat2)
                + np.cos(lat1) * np.cos(lat2) * np.cos(lon1 - lon2)
            )
            * 6371
        )
        return dataset

    def add_gender(self, dataset):
        dataset["gender"] = pd.Categorical(dataset["gender"], categories=["F", "M"])
        hot = pd.get_dummies(dataset["gender"], columns=["F", "M"])

        return dataset.join(hot)

    def add_weekday(self, dataset):
        dataset["weekday"] = dataset["trans_date_trans_time"].apply(
            lambda x: int(self.parse_time(x).weekday())
        )

        return dataset

    def add_hour(self, dataset):
        dataset["hour"] = dataset["trans_date_trans_time"].apply(
            lambda x: int(self.parse_time(x).hour)
        )

        return dataset

    def preprocess(self, dataset, columns_to_delete):
        dataset = self.add_age(dataset)
        dataset = self.add_time(dataset)
        dataset = self.add_distance(dataset)
        dataset = self.one_hot_category(dataset)
        dataset = self.add_workhour_category(dataset)
        dataset = self.add_weekend_category(dataset)
        dataset = self.add_gender(dataset)
        print(type(dataset))
        dataset = self.add_hour(dataset)
        print(type(dataset))
        dataset = self.add_weekday(dataset)
        print(type(dataset))

        dataset = dataset.drop(columns_to_delete, axis=1)

        return dataset


class DataLoader:
    def __init__(self, batch_size=32, max_transactions=32):
        self.batch_size = batch_size
        self.max_transactions = max_transactions

    def add_padding_example(self, example):
        len(example[0])
        padding_ = [0 for x in example[0]]

        while len(example) < self.max_transactions:
            example.append(padding_)

        return example

    def add_padding_label(self, label):
        padding_ = 2

        while len(label) < self.max_transactions:
            label.append(padding_)

        return label

    def divide_to_examples(self, dataset):
        examples = []
        labels = []

        c_user = 0
        l_users = len(dataset.groupby("cc_num"))

        for user_transactions in dataset.groupby("cc_num"):
            user_df = user_transactions[1]

            counter = 0
            while user_df.iloc[counter : counter + self.max_transactions].shape[0] != 0:
                current_example = (
                    user_df.iloc[counter : counter + self.max_transactions]
                    .copy()
                    .drop(["cc_num", "is_fraud"], axis=1)
                )

                is_fraud = list(
                    user_df.iloc[counter : counter + self.max_transactions]["is_fraud"]
                )

                array = current_example.to_numpy().tolist()

                self.add_padding_example(array)
                self.add_padding_label(is_fraud)

                labels.append(is_fraud)
                examples.append(array)

                counter += 1

            c_user += 1

            if c_user % 1000 == 0:
                print("Dataset processed: ", c_user / l_users, "%")

        return np.asarray(examples), np.asarray(labels)

    def normalize_dataset(self, dataset, columns, norm="euclid"):
        for column in columns:
            if norm == "euclid":
                dataset[column] = preprocessing.normalize([dataset[column]])[0]
            elif norm == "gauss":
                vector = tf.constant([list(dataset[column])], dtype=tf.float32)
                mean = tf.math.reduce_mean(vector, axis=1)
                variance = tf.math.reduce_variance(vector, axis=1)[0]

                dataset[column] = dataset[column].apply(
                    lambda x: (x - float(mean)) / math.sqrt(float(variance))
                )

                file = open("dataset_config.json", "w")
                config_dict = {"mean": float(mean), "variance": float(variance)}
                str_obj = json.dumps(config_dict)
                file.write(str_obj)
                file.flush()
                file.close()

        return dataset

    def process_batch(self, element_x, element_y):
        return {"example": element_x, "label": element_y}

    def load_dataset(
        self,
        path,
        preprocess=False,
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
            "long",
            "merch_lat",
            "merch_long",
            "unix_time",
            "street",
            "merchant",
            "state",
            "gender",
        ],
        to_process="ALL",
        normalization=["delta_time", "distance", "city_pop"],
        example_weights=None,
        divide=True,
    ):
        dataset = pd.read_csv(path, index_col=0)
        if to_process != "ALL":
            dataset = dataset[:to_process]

        # Preprocess dataset if preprocess == True
        if preprocess:
            preprocessor = PreprocessorML()
            dataset = preprocessor.preprocess(dataset, columns_to_delete)

        if normalization:
            dataset = self.normalize_dataset(dataset, normalization, norm="gauss")

        dataset_X, dataset_y = None, None
        if divide:
            dataset_X, dataset_y = self.divide_to_examples(dataset)
        else:
            dataset_X, dataset_y = dataset.drop(
                ["is_fraud", "cc_num"], axis=1
            ).to_numpy().tolist(), list(dataset["is_fraud"])

        dataset = tf.data.Dataset.from_tensor_slices((dataset_X, dataset_y))

        return dataset.batch(self.batch_size).prefetch(AUTOTUNE)
