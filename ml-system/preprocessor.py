import tensorflow as tf
AUTOTUNE = tf.data.AUTOTUNE
import datetime
from datetime import date, datetime

import pandas as pd
import numpy as np
from datetime import date

# This class is deprecated and in the future versions will be deleted
class Preprocessor:
    def __init__(self, dataframe):

        # Loading the dataset from path
        self.data_df = dataframe


    def add_time(self):
        dataframe = self.data_df.sort_values(by=['cc_num', 'unix_time'])

        delta_time = []

        previous_row = dataframe.iloc[0]
        delta_time.append(0)

        for row in dataframe[1:].itertuples():

            if row.cc_num == previous_row.cc_num:
                delta_time.append(row.unix_time - previous_row.unix_time)
            else:
                delta_time.append(0)

            previous_row = row


        dataframe['delta_time'] = pd.Series(delta_time)

        self.data_df = dataframe


    def one_hot_category(self, label):
        hot = ['gas_transport', 'grocery_pos', 'home', 'shopping_pos', 'kids_pets', 'shopping_net', 'entertainment',
               'food_dining', 'personal_care', 'health_fitness', 'misc_pos', 'misc_net', 'grocery_net', 'travel']
        
        for category in hot:
            self.data_df[category] = pd.Series([1 if x.category == category else 0 for x in self.data_df.itertuples()])
        
        self.data_df = self.data_df.drop('category', axis = 1)
        # Join the encoded df

    
    def one_hot(self, label):
        if label == 'gender':
            
            self.data_df[label] = pd.Categorical(self.data_df[label], categories=['F', 'M'])
            hot = pd.get_dummies(self.data_df[label], columns = ['F', 'M'])
          
            self.data_df = self.data_df.drop(label,axis = 1)
            # Join the encoded df
            self.data_df = self.data_df.join(hot)


    def target_hot(self, label):
        encodings = self.data_df.groupby('cc_num')[label].agg(['count'])
        #self.data_df = self.data_df.merge(encodings, how='left', on='cc_num')
        #print(self.data_df.columns)
        print(encodings)


    def distance(self):
        lat1 = self.data_df['lat']
        lon1 = self.data_df['longs']
        lat2 = self.data_df['merch_lat']
        lon2 = self.data_df['merch_long']
        return np.arccos(np.sin(lat1) * np.sin(lat2) + np.cos(lat1) * np.cos(lat2) * np.cos(lon1 - lon2)) * 6371


    def add_padding_example(self, example, size=32):
        len(example[0])
        padding_ = [0 for x in example[0]]

        while len(example) < size:
            example.append(padding_)
            
        return example


    def add_padding_label(self, label, size=32):
        padding_ = 2

        while len(label) < size:
            label.append(padding_)
            
        return label


    def divide_to_examples(self, size=32):
        dataset = self.data_df
        
        examples = []
        labels = []

        c_user = 0
        l_users = len(dataset.groupby('cc_num'))

        for user_transactions in dataset.groupby('cc_num'):

            user_df = user_transactions[1]

            counter = 0
            while user_df.iloc[counter: counter + size].shape[0] != 0:
                current_example = user_df.iloc[counter: counter + size].copy().drop(['cc_num', 'is_fraud'], axis=1)

                is_fraud = list(user_df.iloc[counter: counter + size]['is_fraud'])

                array = current_example.to_numpy().tolist()

                self.add_padding_example(array)
                self.add_padding_label(is_fraud)

                labels.append(is_fraud)
                examples.append(array)
            
                counter += 1
            
            c_user += 1

            if c_user % 1000 == 0:
                print('Dataset processed: ', c_user / l_users, '%')


        return np.asarray(examples), np.asarray(labels), 0
    
    def add_padding(self):
        header_ = list(self.data_df.columns)
        print('Header:', header_)
        
        print(self.data_df.shape)
        
        
        while self.data_df.shape[0] < 32:
            self.data_df.loc[len(self.data_df)] = pd.Series([0 for x in header_], index=header_)
            
        print(self.data_df)
    
    
    def prepare_submit(self):
        
        self.data_df['age'] = self.data_df['dob'].apply(lambda x: (date.today() - date.fromisoformat(x)).days // 365)
        self.data_df['distance'] = self.distance()

        self.one_hot_category('category')
        # self.one_hot('merchant')
        self.one_hot('gender')

        self.add_time()

        self.data_df = self.data_df.drop(
            columns=['cc_num',
                'trans_date_trans_time', 
                'street', 
                'state', 
                'city_pop',
                'dob',
                'trans_num',
                'first',
                'last',
                'zip',
                'job',
                'longs',
                'lat',
                'merch_lat',
                'merch_long',
                'city',
                'merchant',
                'unix_time'
                ], 
            axis=1
        )
        
        print(self.data_df)
        
        self.add_padding()
        
        print(self.data_df)
        
        return self.data_df
    

    def preprocess(self):
            # Transforming some fields
            self.data_df['age'] = self.data_df['dob'].apply(lambda x: (date.today() - date.fromisoformat(x)).days // 365)
            self.data_df['distance'] = self.distance()
            eps = 0.001 # 0 => 0.1¢

            self.one_hot_category('category')
            # self.one_hot('merchant')
            self.one_hot('gender')

            self.add_time()

            self.data_df = self.data_df.drop(
                columns=[
                    'trans_date_trans_time', 
                    'street', 
                    'state', 
                    'city_pop',
                    'dob',
                    'trans_num',
                    'first',
                    'last',
                    'zip',
                    'job',
                    'city',
                    'merchant',
                    'unix_time',
                    'lat', 
                    'long',
                    'merch_lat', 
                    'merch_long'
                    ], 
                axis=1
            )
            
            examples, labels, weights = self.divide_to_examples()

            return examples, labels, weights


    def process_examples_labels(self, example, label):
        return {"example": example, "label": label}
    
    
    def prepare_dataset(self, batch_size=64):
        examples, labels = self.preprocess()

        dataset = tf.data.Dataset.from_tensor_slices((examples, labels)).map(
            self.process_examples_labels, num_parallel_calls=AUTOTUNE
        )
        return dataset.batch(batch_size).cache().prefetch(AUTOTUNE)


def preprocess_data(data):
    prep = Preprocessor(data)
    data = prep.prepare_submit()
    index = len(data) - 1
    
    if len(data) > 32:
        index = 31
        data = data.iloc[len(data) - 32:len(data)]
    
    padded = np.expand_dims(np.asarray(data), 0)
    
    
    return tf.convert_to_tensor(padded), index


# The new preprocessor class

class PreprocessorML():
    def __init__(self, normalization=False):
        self.norm = normalization
    

    def one_hot_category(self, dataset):
        hot = ['gas_transport', 'grocery_pos', 'home', 'shopping_pos', 'kids_pets', 'shopping_net', 'entertainment',
               'food_dining', 'personal_care', 'health_fitness', 'misc_pos', 'misc_net', 'grocery_net', 'travel']
        
        for category in hot:
            dataset[category] = pd.Series([1 if x.category == category else 0 for x in dataset.itertuples()],
                                          index=dataset.index)
        
        return dataset


    def add_time(self, dataset):
        dataframe = dataset.sort_values(by=['cc_num', 'unix_time'])

        delta_time = []

        previous_row = dataframe.iloc[0]

        delta_time.append(0)

        for row in dataframe[1:].itertuples():

            if row.cc_num == previous_row.cc_num:
                delta_time.append(row.unix_time - previous_row.unix_time)
            else:
                delta_time.append(0)

            previous_row = row

        dataframe['delta_time'] = pd.Series(delta_time, index=dataframe.index)

        return dataframe


    def parse_time(self, string):
        return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


    def add_workhour_category(self, dataset):
        dataset['work_hours'] = dataset['trans_date_trans_time'].apply(
            lambda x: 
                int(self.parse_time(x).hour >= 6 and self.parse_time(x).hour <= 18))
        return dataset


    def add_weekend_category(self, dataset):
        dataset['weekend'] = dataset['trans_date_trans_time'].apply(
            lambda x: 
                int(self.parse_time(x).weekday() >= 5 and self.parse_time(x).weekday() <= 6))
        return dataset

    
    def add_age(self, dataset):
        dataset['age'] = dataset['dob'].apply(lambda x: (date.today() - date.fromisoformat(x)).days // 365)
        return dataset


    def add_distance(self, dataset):
        lat1 = dataset['lat']
        lon1 = dataset['longs']
        lat2 = dataset['merch_lat']
        lon2 = dataset['merch_long']
        dataset['distance'] = np.arccos(np.sin(lat1) * np.sin(lat2) + np.cos(lat1) * np.cos(lat2) * np.cos(lon1 - lon2)) * 6371
        return dataset

    
    def add_gender(self, dataset):
        dataset['gender'] = pd.Categorical(dataset['gender'], categories=['F', 'M'])
        hot = pd.get_dummies(dataset['gender'], columns = ['F', 'M'])
        
        return dataset.join(hot)


    def add_weekday(self, dataset):
        dataset['weekday'] = dataset['trans_date_trans_time'].apply(
            lambda x: int(self.parse_time(x).weekday()))
        
        return dataset
    
    def add_hour(self, dataset):
        dataset['hour'] = dataset['trans_date_trans_time'].apply(
            lambda x: int(self.parse_time(x).hour))
        
        return dataset


    def preprocess(self, dataset, columns_to_delete=['cc_num', 
                      'city', 
                      'dob', 
                      'job', 
                      'first', 
                      'last',
                      'trans_date_trans_time',
                      'category',
                      'trans_num',
                      'lat',
                      'longs',
                      'merch_lat',
                      'merch_long',
                      'unix_time',
                      'street',
                      'merchant',
                      'state',
                      'gender']):
        dataset = self.add_age(dataset)
        dataset = self.add_distance(dataset)
        dataset = self.one_hot_category(dataset)
        dataset = self.add_time(dataset)
        dataset = self.add_workhour_category(dataset)
        dataset = self.add_weekend_category(dataset)
        dataset = self.add_gender(dataset)
        print(type(dataset))
        dataset = self.add_hour(dataset)
        print(type(dataset))
        dataset = self.add_weekday(dataset)
        print(type(dataset))

        dataset = dataset.drop(columns_to_delete, axis = 1)

        return dataset
    
    
    def preprocess_submit(self, data):
        return self.preprocess(data)
        