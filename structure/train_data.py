import pickle
import numpy as np
from imblearn.over_sampling import *
import matplotlib.pyplot as plt
from collections import Counter
from numpy import where


class Record():
    def __init__(self, 
                 text, 
                 vector,
                 is_fake):
        self.x = vector
        self.y = is_fake
        self.text = text


class StoredData():
    data_all = []
    data_train = []
    data_test = []

    def __init__(self, data, do_smote=False, smote_ratio=1, class_ratio=1, test_ratio=0.7):
        dataset = [[data[0][0], pickle.loads(bytes.fromhex(data[0][1])), data[0][2]]]
        for i in range(1, len(data)):  

            dataset.append([data[i][0], pickle.loads(bytes.fromhex(data[i][1])), data[i][2]])

        fake = []
        not_fake = []

        for i in range(len(dataset)):
            if dataset[i][2] == 1:
                fake.append(dataset[i])
            else:
                not_fake.append(dataset[i])


        # max_abs_value = 1

        fake_len_all = len(fake)
        fake_len_train = round(len(fake) * test_ratio)
        fake_len_test = fake_len_all - fake_len_train

        not_fake_len_data = round(len(fake) * class_ratio)
        # not_fake_len_data = len(not_fake) 
        not_fake_len_all = len(not_fake) 
        not_fake_len_train = round(not_fake_len_data * test_ratio)
        not_fake_len_test = fake_len_test * 9
        
        print("fake_len_all: ", fake_len_all)
        print("fake_len_train: ", fake_len_train)
        print("fake_len_test: ", fake_len_test)
        print("not_fake_len_all: ", not_fake_len_all)
        print("not_fake_len_train: ", not_fake_len_train)
        print("not_fake_len_test: ", not_fake_len_test)

                    
        for i in range(fake_len_all):
            # res_vector = ((fake[i][1] / max_abs_value) + 1) / 2
            res_vector = fake[i][1]

            if i < fake_len_train:
                self.data_train.append(Record(fake[i][0], res_vector, fake[i][2]))
            elif i < fake_len_train + fake_len_test:
                self.data_test.append(Record(fake[i][0], res_vector, fake[i][2]))

            self.data_all.append(Record(fake[i][0], res_vector, fake[i][2]))

        for i in range(not_fake_len_all):
            # res_vector = ((not_fake[i][1] / max_abs_value) + 1) / 2
            res_vector = not_fake[i][1]

            if i < not_fake_len_train:
                self.data_train.append(Record(not_fake[i][0], res_vector, not_fake[i][2]))
            elif i < not_fake_len_train + not_fake_len_test:
                self.data_test.append(Record(not_fake[i][0], res_vector, not_fake[i][2]))

            self.data_all.append(Record(not_fake[i][0], res_vector, not_fake[i][2]))


        if do_smote:
            X = []
            y = []
            for i in range(len(self.data_train)):
                X.append(self.data_train[i].x)
                y.append(self.data_train[i].y)    
            
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            X_t = self.x_train.reshape((len(self.x_train), 768))
            y_t = self.y_train

            print(type(X_t[0]))
            print(type(y_t[0]))

            plt.figure(figsize=(15, 11))
            plt.title('Result before SMOTE')
            plt.scatter(X_t[y_t==0][:, 0], X_t[y_t==0][:, 1], label='norm')
            plt.scatter(X_t[y_t==1][:, 0], X_t[y_t==1][:, 1], label='fake')
            plt.legend()
            plt.grid(False)
            plt.show()

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            smt = SVMSMOTE(sampling_strategy=smote_ratio)
            X_smote, y_smote = smt.fit_resample(X, y)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # X_t = np.array(X_smote).reshape((len(X_smote), 768))
            # y_t = y_smote

            # plt.figure(figsize=(9, 6))
            # plt.title('Result after SMOTE')
            # plt.scatter(X_t[y_t==0][:, 0], X_t[y_t==0][:, 1], label='norm')
            # plt.scatter(X_t[y_t==1][:, 0], X_t[y_t==1][:, 1], label='fake')
            # plt.legend()
            # plt.grid(False)
            # plt.show()

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            self.data_train = []
            for i in range(len(X_smote)):
                self.data_train.append(Record(None, X_smote[i], y_smote[i]))
            


        np.random.shuffle(self.data_train)
        np.random.shuffle(self.data_test)
        np.random.shuffle(self.data_all)




    # x_t = storedData.x_train.reshape((len(storedData.x_train), 24, 32))
    # x_ts = storedData.x_test.reshape((len(storedData.x_test), 24, 32))

    def get_x_train(self):
        _x_train = []
        for i in range(len(self.data_train)):
            _x_train.append(self.data_train[i].x)
        return np.array(_x_train).reshape((len(self.data_train), 24, 32))
    
    def get_y_train(self):
        _y_train = []
        for i in range(len(self.data_train)):
            _y_train.append(self.data_train[i].y)
        return np.array(_y_train, dtype=np.int64)
 
    def get_texts_train(self):
        _texts_train = []
        for i in range(len(self.data_train)):
            _texts_train.append(self.data_train[i].text)
        return _texts_train

    def get_x_test(self):
        _x_test = []
        for i in range(len(self.data_test)):
            _x_test.append(self.data_test[i].x)
        return np.array(_x_test).reshape((len(self.data_test), 24, 32))
    
    def get_y_test(self):
        _y_test = []
        for i in range(len(self.data_test)):
            _y_test.append(self.data_test[i].y)
        return np.array(_y_test, dtype=np.int64)
    
    def get_texts_test(self):
        _texts_test = []
        for i in range(len(self.data_test)):
            _texts_test.append(self.data_test[i].text)
        return np.array(_texts_test)
    
    def get_x_all(self):
        _x_all = []
        for i in range(len(self.data_all)):
            _x_all.append(self.data_all[i].x)
        return np.array(_x_all).reshape((len(self.data_all), 24, 32))
    
    def get_y_all(self):
        _y_all = []
        for i in range(len(self.data_all)):
            _y_all.append(self.data_all[i].y)
        return np.array(_y_all, dtype=np.int64)
    
    def get_texts_all(self):
        _texts_all = []
        for i in range(len(self.data_all)):
            _texts_all.append(self.data_all[i].text)
        return np.array(_texts_all)

    x_train = property(get_x_train) 
    y_train = property(get_y_train)
    texts_train = property(get_texts_train)
    x_test = property(get_x_test)
    y_test = property(get_y_test)
    texts_test = property(get_texts_test)
    x_all = property(get_x_all)
    y_all = property(get_y_all)
    texts_all = property(get_texts_all)
