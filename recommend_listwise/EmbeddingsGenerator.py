import itertools
import pandas as pd
import numpy as np
import random
import csv
import time

import matplotlib.pyplot as plt

import tensorflow as tf2
tf = tf2.compat.v1
tf.disable_v2_behavior()

import keras.backend as K
from keras import Sequential
from keras.layers import Dense, Dropout

txt_writer = open('write layer outputs',mode='w')
txt_writer2 = open('films outputs',mode='w')
txt_writer3 = open('vectors outputs',mode='w')

class EmbeddingsGenerator:
    def __init__(self, train_users, data):
        self.train_users = train_users

        # preprocess
        self.data = data.sort_values(by=['timestamp'])
        # make them start at 0
        self.data['userId'] = self.data['userId'] - 1
        self.data['itemId'] = self.data['itemId'] - 1
        self.user_count = self.data['userId'].max() + 1
        self.movie_count = self.data['itemId'].max() + 1
        self.user_movies = {}  # list of rated movies by each user
        for userId in range(self.user_count):
            self.user_movies[userId] = self.data[self.data.userId == userId]['itemId'].tolist()
        self.m = self.model()

    def model(self, hidden_layer_size=100):
        m = Sequential()
        m.add(Dense(hidden_layer_size, input_shape=(1, self.movie_count)))
        m.add(Dropout(0.2))
        m.add(Dense(self.movie_count, activation='softmax'))
        m.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return m

    def generate_input(self, user_id):
        '''
        Returns a context and a target for the user_id
        context: user's history with one random movie removed
        target: id of random removed movie
        '''
        user_movies_count = len(self.user_movies[user_id])
        # picking random movie
        random_index = np.random.randint(0, user_movies_count - 1)  # -1 avoids taking the last movie
        # setting target
        target = np.zeros((1, self.movie_count))
        target[0][self.user_movies[user_id][random_index]] = 1
        # setting context
        context = np.zeros((1, self.movie_count))
        context[0][self.user_movies[user_id][:random_index] + self.user_movies[user_id][random_index + 1:]] = 1
        print('context = ',context)
        print('target = ',target)
        return context, target

    def train(self, nb_epochs=300, batch_size=10000):
        '''
        Trains the model from train_users's history
        '''
        # xtrain_writer = open('test_data/xtrain_data')
        # ytrain_writer = open('test_data/ytrain_data')
        for i in range(nb_epochs):
            print('%d/%d' % (i + 1, nb_epochs))
            batch = [self.generate_input(user_id=np.random.choice(self.train_users) - 1) for _ in range(batch_size)]
            X_train = np.array([b[0] for b in batch])
            y_train = np.array([b[1] for b in batch])
            # xtrain_writer.write([b[0] for b in batch])

            np.set_printoptions(threshold=np.inf)
            self.m.fit(X_train, y_train, epochs=1, validation_split=0.5)

    def test(self, test_users, batch_size=100000):
        '''
        Returns [loss, accuracy] on the test set
        '''
        batch_test = [self.generate_input(user_id=np.random.choice(test_users) - 1) for _ in range(batch_size)]
        X_test = np.array([b[0] for b in batch_test])
        y_test = np.array([b[1] for b in batch_test])
        return self.m.evaluate(X_test, y_test)

    def save_embeddings(self, file_name):
        '''
        Generates a csv file containg the vector embedding for each movie.
        '''
        inp = self.m.input  # input placeholder
        outputs = [layer.output for layer in self.m.layers]  # all layer outputs
        functor = K.function([inp, K.learning_phase()], outputs)  # evaluation function

        # append embeddings to vectors
        vectors = []
        # for movie_id in range(self.movie_count):
        for movie_id in range(self.movie_count - 1600):

            movie = np.zeros((1, 1, self.movie_count))
            movie[0][0][movie_id] = 1
            print('movie!!!!!!!!!\n')
            aaa = ' '.join(str(e) for e in movie)
            txt_writer2.write(aaa)
            layer_outs = functor([movie])
            print(layer_outs)
            txt_writer.write('testt')
            txt_writer.write('\n')
            aaa = ' '.join(str(e) for  e in layer_outs)
            txt_writer.write(aaa)
            txt_writer.write('\n')

            vector = [str(v) for v in layer_outs[0][0][0]]
            vector = '|'.join(vector)
            vectors.append([movie_id, vector])
            txt_writer3.write('testt')
            txt_writer3.write('\n')
            aaa = ' '.join(str(e) for  e in vector)
            txt_writer3.write(aaa)
            txt_writer3.write('\n')
        # saves as a csv file
        embeddings = pd.DataFrame(vectors, columns=['item_id', 'vectors']).astype({'item_id': 'int32'})
        embeddings_csv = embeddings.to_csv(file_name, sep=';', index=False)
        # with open('embeddings2.csv', 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile, delimiter=';', quotechar='|')
        #     writer.writerow(['www.biancheng.net'] * 5 + ['how are you'])
        #     writer.writerow(['hello world', 'web site', 'www.biancheng.net'])
        # files.download(file_name)