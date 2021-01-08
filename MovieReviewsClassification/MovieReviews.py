from keras.datasets import imdb
from keras.layers import Dense
from keras.models import Sequential
import matplotlib.pyplot as plt
import numpy as np

#Total number of training data: 25,000
#Parameter: num_words=10000 takes the 10000 most common words used in reviewing the movies
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

#Convert the data to vectors
def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1
        
    return results

#Apply the vectorize_sequences function
x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)
y_train = np.asarray(train_labels).astype('float32')
y_test = np.asarray(test_labels).astype('float32')

#Create the neural network architecture
model = Sequential()

model.add(Dense(16, input_shape=(10000,), activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.summary()

#Separate the x_train and y_train for training set (15,000 samples) and validation set (10,000 samples)
x_val = x_train[:10000]
partial_x_train = x_train[10000:]

y_val = y_train[:10000]
partial_y_train = y_train[10000:]

#Run the learning algorthm
fitting_data = model.fit(partial_x_train,
                         partial_y_train,
                         epochs=20,
                         batch_size=512,
                         validation_data=(x_val, y_val))

#Plot the loss and accuracy of training set and validation set
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax1.plot(fitting_data.history['loss'], c='r')
ax1.plot(fitting_data.history['val_loss'], c='g')

ax2.plot(fitting_data.history['accuracy'], c='r')
ax2.plot(fitting_data.history['val_accuracy'], c='g')

plt.show()

#Predict whether the review was positive or negative
model.predict(x_test)