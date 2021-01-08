import numpy as np

#Separate Sequence and Target; Sequences that are 25 <= x <= 100 are only considered (168)
def separateSeqAndLabel(seq_and_label_file):
	seq_only = open('data/seqOnly.txt', 'w')
	label_only = open('data/labelOnly.txt', 'w')

	#Split the sequence and label then create separate files to contain them
	for line in seq_and_label_file:
		line_split = line.split(' ')

		if len(line_split[0]) >= 25 and len(line_split[0]) <= 100:
			seq_only.write(line_split[0]+'\n')
			label_only.write(line_split[1])

	seq_only.close()
	label_only.close()

	label_only = open('data/labelOnly.txt', 'r')
	label_only_upd = open('data/labelOnlyUpd.txt', 'w')

	#Append 'X' to the labels until it reaches a length of 100
	for line_count, line in enumerate(label_only):
		line_copy = line.strip('\n')

		if len(line.strip('\n')) != 100:
			add_X = 100 - len(line.strip('\n'))

			for i in range(add_X):
				line_copy += 'X'

		label_only_upd.write(line_copy+'\n')

	label_only_upd.close()

	seq_only = open('data/seqOnly.txt', 'r')
	label_only_upd = open('data/labelOnlyUpd.txt', 'r')

	return seq_only, label_only_upd

#One-hot encode and pad the sequence
def OHEAndPadSequence(seq_file):
	amino_acids = 'ACDEFGHIKLMNPQRSTVWY'

	#Generate an array with zeros to fit all data; Pads the data as well
	#Size of array is not generalized
	seq_array = np.zeros((1628, 100, 20))

	#Replace the zeros with 1 if array coordinate is matched
	for line_num, line in enumerate(seq_file):
		for char_num, char in enumerate(line.strip('\n')):
			for aa_num, aa in enumerate(amino_acids):
				if char == aa:
					seq_array[line_num, char_num, aa_num] = 1

	return seq_array

#One-hot encode and pad the target
def OHEAndPadTarget(label_file):
	# BSTGHNE *N = None
	labels = 'BSTGHENX'

	#Generate an array of zeros
	#Size of array is not generalized
	label_array = np.zeros((1628, 100, 8))

	#Replace the zeros with 1 if array coordinate is matched
	for line_num, line in enumerate(label_file):
		for char_num, char in enumerate(line.strip('\n')):
			for label_num, label in enumerate(labels):
				if char == label:
					label_array[line_num, char_num, label_num] = 1

	return label_array