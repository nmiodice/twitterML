import sys
import select
import constants
import tw_file_ops as fo
import numpy as np
from sklearn.cluster import DBSCAN

"""
Removes rows that have no cluster assignment
"""
def prune_no_cluster_data(x):
	x = x[x[:, 0].A1 != '-1', :]
	return x

"""
Performs clustering on a matrix, X, using features FEATURES. FEATURES
determines which columns will be used to cluster, and these columns will be
treated as numeric values. For example, if FEATURES = [0, 2], then columns
0 and 2 will be used as features to cluster the data on, but the returned 
matrix includes all original features. The cluster value will be inserted
as the first column. Data that was not included in any cluster is given a
cluster ID of -1
"""
def cluster(x, features):
	x_to_clus = x[:, features].astype(float)
	# run DBSCAN clustering algorithm for fast clustering
	db = DBSCAN(eps = .08, min_samples = 30).fit(x_to_clus)
	labels = db.labels_
	labels = labels.reshape(len(labels), 1)
	x_clus = np.append(labels, x, axis = 1)
	return x_clus

"""
Performs a clustering algorithm on the data from a tab-delimited file. Each
line in the file is treated as a separate observation, whereas each column is
treated as a separate feature. FEATURES determines which features are used in
the clustering. FEATURES is an array corresponding to the columns to use for
clustering. For example, FEATURES = [0, 2] will use columns 0 and 2. Each
column being clustered is assumed to have numeric values. DELIM specifies the
text delimiter to use to break the file apart
"""
def cluster_from_file(file, features, delim):
	x = fo.file_to_matrix(file, delim)
	x_clus = cluster(x, features)
	# we only care about data we can cluster
	x_clus = prune_no_cluster_data(x_clus)
	return x_clus

"""
Prints cluster information for the tweet data passed in. Only tweets which
are assigned a cluster in the DBSCAN algorithm are printed. Tweets are
clustered based on latitude and longitude data
"""
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
	
	x_clus = cluster_from_file(file, [0, 1], constants.delim)
	fo.print_matrix(x_clus)
