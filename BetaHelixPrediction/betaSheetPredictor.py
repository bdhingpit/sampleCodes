from keras.layers import LSTM, Dense
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


sequences = open('pdb_study/Data/Seq_With_Target/Sequence/all_seq_(for_B_sheets).txt', 'r')
targets = open('pdb_study/Data/Seq_With_Target/Target/all_targ_(for_B_sheets).txt', 'r')

array_ohe_seqs = OHE_My_Sequence(sequences)
array_targets = np.array([value.strip('\n') for value in targets])

#Split the data to training and test set (80:20)
x_train, x_test, y_train, y_test = train_test_split(array_ohe_seqs, 
                                                    array_targets, 
                                                    test_size=0.2, 
                                                    random_state=5)

#Create the architecture of the neural network
model2 = Sequential()

model2.add(LSTM(128, activation='sigmoid', input_shape=(None, 20), return_sequences=True))
model2.add(LSTM(128, activation='sigmoid', return_sequences=False))
model2.add(Dense(1, activation='sigmoid'))

model2.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

model2.summary()

#Run the learning algorithm
history = model2.fit(x_train, y_train, epochs=10, batch_size=1, validation_data=(x_test, y_test))

#Plot the learning algorithm loss and accuracy
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax1.plot(history.history['loss'], c='g')
ax1.plot(history.history['val_loss'], c='r')

ax2.plot(history.history['accuracy'], c='g')
ax2.plot(history.history['val_accuracy'], c='r')

plt.show()

#Predict the result
result = model2.predict(x_test)

#Plot the predictions and actual labels
plt.scatter(range(len(y_test)), result, c='g')
plt.scatter(range(len(y_test)), y_test, c='r')

plt.show()