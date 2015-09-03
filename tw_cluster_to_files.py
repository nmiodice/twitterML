import sys
import select
import tw_file_ops as fo

def split_matrix_to_files(x, text_col, out_dir):
	n_clus = int(max(x[:, 0].A1))
	for i in range(n_clus + 1):
		idxs = (x[:, 0].A1).astype(int) == i
		d = x[idxs, text_col]

		if out_dir[-1] != '/':
			out_dir += '/'
		file = open(out_dir + "cluster." + str(i), 'w')
		for row in d:
			file.write(row.A1[0])
			file.write("\n")
		file.close()


def split_cluster_file(file, text_col, out_dir):
	x = fo.file_to_matrix(file)
	split_matrix_to_files(x, text_col, out_dir)

if __name__ == '__main__':
	if select.select([sys.stdin,],[],[],0.0)[0]:
	    file = sys.stdin
	else:
		if len(sys.argv) != 3:
			print("Usage: " + sys.argv[0] + " <data file> [OR] <stdin> <outdir>")
			exit(-1)
		else:
			file = open(sys.argv[1], 'r')
			assert(file != None)
	
	split_cluster_file(file, -1, sys.argv[2])
