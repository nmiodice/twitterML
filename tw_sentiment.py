import sys
import select
import constants
import tw_file_ops as fo
from textblob import TextBlob

def analyze(x, text_col):
	for row in x:
		row = row.A1
		blob = TextBlob(row[text_col])
		print(blob)
		blob.correct()
		print(blob)
		print('\n\n')
	return x

def analyze_file(file, delim, text_col):
	x = fo.file_to_matrix(file, delim)
	x_sentiment = analyze(x, text_col)

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
	
	analyze_file(file, constants.delim, -1)