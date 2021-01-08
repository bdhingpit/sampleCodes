from keras.layers import Dense, LSTM
from keras.models import Sequential
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def OHE_My_Sequence(list_of_sequences):
    amino_acids = 'ACDEFGHIKLMNPQRSTVWY'
    
    #One hot encoding of the amino acid sequence
    final_ohe_seq = []
    for sequence in list_of_sequences:
        ohe_sequence = [[1 if amino_acid == char else 0 
                         for amino_acid in amino_acids] 
                         for char in sequence.strip('\n')]
        
        final_ohe_seq.append(ohe_sequence)
    
    #Determine the amino acid sequence with max length
    len_lists = [len(seq_lists) for seq_lists in final_ohe_seq]
    max_len = max(len_lists)
    
    #Append zeros to the one-hot-encoded form until the length matches the max length
    for seq_num, sequence in enumerate(final_ohe_seq):
        for i in range(max_len - len(sequence)):
            sequence = np.append(sequence, np.array([np.zeros(20)]), axis=0)
        
        final_ohe_seq[seq_num] = sequence
    
    return np.array(final_ohe_seq, dtype=int)
    
    
sequences = open('data/Data/Seq_With_Target/Sequence/all_seq.txt', 'r')
targets = open('data/Data/Seq_With_Target/Target/all_targ.txt', 'r')

array_ohe_seqs = OHE_My_Sequence(sequences)
array_targets = np.array([value.strip('\n') for value in targets])

#Split the data to training and test set (80:20)
x_train, x_test, y_train, y_test = train_test_split(array_ohe_seqs, 
                                                    array_targets, 
                                                    test_size=0.2, 
                                                    random_state=5)

#Create the architecture of the neural network
model = Sequential()

model.add(LSTM(128, activation='sigmoid', input_shape=(None, 20), return_sequences=True))
model.add(LSTM(128, activation='sigmoid', return_sequences=False))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

model.summary()

#Run the learning algorithm
history = model.fit(x_train, y_train, epochs=10, batch_size=1, validation_data=(x_test, y_test))

#Predict the result of the test set
result = model.predict(x_test)

#Plot the Results
plt.scatter(range(1226), result, c='g')
plt.scatter(range(1226), y_test, c='r')

plt.show()


#Create the architecture of the neural network; architecture is smaller this time
model2 = Sequential()

model2.add(LSTM(64, activation='sigmoid', input_shape=(None, 20), return_sequences=True))
model2.add(LSTM(64, activation='sigmoid', return_sequences=False))
model2.add(Dense(1, activation='sigmoid'))

model2.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

model2.summary()

#Run the second learning algorithm
history2 = model2.fit(x_train, y_train, epochs=10, batch_size=1, validation_data=(x_test, y_test))

#Plot the loss and accuracy values of the training and test set
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax1.plot(history2.history['loss'], c='r')
ax1.plot(history2.history['val_loss'], c='g')
ax2.plot(history2.history['accuracy'], c='r')
ax2.plot(history2.history['val_accuracy'], c='g')

plt.show()

#Predict the results with the calculated parameters
result2 = model2.predict(x_test)

#Plot the prediction result
plt.scatter(range(1226), result2, c='g')
plt.scatter(range(1226), y_test, c='r')

plt.show()

#Show how many of the result of model1 are predicted to be alpha helix or not
#>= 0.51 -> alpha helix, <=0.49 -> not alpha helix
print(len(np.where(result <= 0.49)[0]))
print(len(np.where(result >= 0.51)[0]))

#Show how many in the actual test set are alpha helix (1) or not (0)
y_test_reshaped = np.array(y_test, dtype=int).reshape(1226, 1)
print(len(np.where(y_test_reshaped == 0)[0]))
print(len(np.where(y_test_reshaped == 1)[0]))

#Compare the prediction with the test set
#Show how many true negatives were predicted
lower_bound = 0
for seq_num in np.where(result <= 0.49)[0]:
    if int(y_test[seq_num]) == 0:
        lower_bound += 1

print(lower_bound)

#Compare prediction with test set
#Show how many true positives were predicted
upper_bound = 0
for seq_num in np.where(result >= 0.51)[0]:
    if int(y_test[seq_num]) == 1:
        upper_bound += 1

print(upper_bound)

#Attempt to predict any random sequence
test1_data = ['AGTVYYP']
test1_data_processed = OHE_My_Sequence(test1_data)
test1_result = model.predict(test1_data_processed)
test1_result