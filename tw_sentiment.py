import sys
import select
import numpy as np
import constants
import tw_file_ops as fo
from textblob import TextBlob

"""
Runs each line of text through a sentiment analysis tool, then appends
sentiment and polarity measures as extra features. Specifically, 
if X is N x P, the returned value is N x (P + 2). X[i, P] is a measure of
polarity [-1, 1] for row i, and X[i, P + 1] is a measure of subjectivity [0, 1]
"""
def analyze(x, text_col, include_zero_polarity):
	sent_data = np.zeros((x.shape[0], 2))
	for i in range(x.shape[0]):
		row = x[i, :].A1
		blob = TextBlob(row[text_col])
		sent_data[i, 0] = blob.sentiment[0]
		sent_data[i, 1] = blob.sentiment[1]

	# filter out any data requested, then append the sentiment measures to the
	# right side of the matrix
	if include_zero_polarity:
		x = np.concatenate((x, sent_data), axis = 1)
	else:
		idxs = sent_data[:, 0] != 0
		x = np.concatenate((x[idxs, :], sent_data[idxs, :]), axis = 1)
	return x

"""
Removes the column specified by TEXT_COL
"""
def strip_text(x, txt_col):
	return np.delete(x, txt_col, axis = 1)

"""
A wrapper to the ANALYZE function, but reads the data in from a file
"""
def analyze_file(file, delim, text_col, include_zero_polarity):
	x = fo.file_to_matrix(file, delim)
	x_sentiment = analyze(x, text_col, include_zero_polarity)
	return x_sentiment

if __name__ == '__main__':
	if select.select([sys.stdin,],[],[],0.0)[0]:
	    file = sys.stdin
	else:
		if len(sys.argv) != 2:
			print("Usage: " + sys.argv[0] + " <data file> [OR] <stdin>")
			exit(-1)
		else:
			file = open(sys.argv[1], 'r')
			assert(file != None)
	
	x = analyze_file(file, constants.delim, -1, False)
	x = strip_text(x, -3)
	fo.print_matrix(x)
