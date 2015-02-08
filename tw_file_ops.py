import constants
import numpy as np
import sys
"""
A collection of file helper functions for TwitterML
"""

"""
Prints a delimited line with the elements of an iterator
"""
def print_line(iter, delim = constants.delim, file = sys.stdout):
	iter = list(map(str, iter))
	file.write(delim.join(iter))
	file.write('\n')
	file.flush()

"""
Returns an N x P matrix, where N is the number of rows in the file, and P is
the number of delimited columns in each line. DELIM is the delimiter to use
"""
def file_to_matrix(file, delim = constants.delim):
	matrix = []
	for line in file:
		line = line.rstrip('\n')
		matrix.append(line.split(delim))
	return np.matrix(matrix)

"""
Prints a matrix in delimited form
"""
def print_matrix(x, file = sys.stdout, delim = constants.delim):
	x = x.astype(str)
	for row in x:
		# A1 is the flattened 1-D array version of a matrix
		row = row.A1
		line = delim.join(row)
		file.write(line)
		file.write('\n')
	file.flush