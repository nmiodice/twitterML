import select
import sys
import tw_file_ops as fo
import constants
import json
from scipy.spatial import ConvexHull
import numpy as np
import random as rand
import statistics as stats

"""
A small helper utility to hold information about a sentiments and coordinates
"""
class geojson_cluster:
	def __init__(self, clus_id):
		self.mId = int(clus_id)
		self.mCoords = []
		self.mPolarity = []
		self.mSubjectivity = []
		self.mAvgSubjectivity = None
		self.mAvgPolarity = None

	"""
	Adds coordinate data to the object. Note, a small perturbation is added to
	the points. This fixes an error where getting the convex hull fails because
	of points which lie on the exact same x or y axis
	"""
	def add_coord(self, lat, long, polarity, subjectivity):
		lat = lat + rand.random()*.00000001
		long = long + rand.random()*.00000001

		self.mCoords.append([long, lat])
		self.mPolarity.append(polarity)
		self.mSubjectivity.append(subjectivity)

	def get_bouding_coords(self):
		coords = []
		hull = ConvexHull(self.mCoords)
		for i in range(len(hull.vertices)):
			coords.append(self.mCoords[hull.vertices[i]])
		coords.append(self.mCoords[hull.vertices[0]])
		return coords

	def get_avg_polarity(self):
		if self.mAvgPolarity == None:
			self.mAvgPolarity = sum(self.mPolarity)/len(self.mPolarity)
		return self.mAvgPolarity

	def get_avg_subjectivity(self):
		if self.mAvgSubjectivity == None:
			self.mAvgSubjectivity = sum(self.mSubjectivity)/len(self.mSubjectivity)
		return self.mAvgSubjectivity
		
	def get_cluster_id(self):
	    return self.mId


"""
Creates a JSON object corresponding to clustered 
"""
def create_geojson(js_data, file = sys.stdout):
	feature_array= []
	geojson = {'type' : 'FeatureCollection'}

	for js in js_data:
		jsdict = {}
		jsdict['type'] = 'Feature'
		jsdict['properties'] = {}
		jsdict['properties']['cluster_id'] = js.get_cluster_id()
		jsdict['properties']['polarity'] = js.get_avg_polarity()
		jsdict['properties']['subjectivity'] = js.get_avg_subjectivity()
		jsdict['geometry'] = {}
		jsdict['geometry']['type'] = 'Polygon'
		jsdict['geometry']['coordinates'] = []
		jsdict['geometry']['coordinates'].append(js.get_bouding_coords())
		feature_array.append(jsdict)
	geojson['features'] = feature_array
	
	json_str = json.dumps(geojson, indent = 4, separators = (',', ': '))
	return json_str

"""
Converts a data matrix X into a list of GEOJSON_CLUSTER objects. X is assumed
to be a N x 5 matrix. The columns are assumed to be in the following format:
	col 0 = cluster ID
	col 1 = latitude
	col 2 = longitude
	col 3 = polarity
	col 4 = subjectivity
"""
def aggregate_matrix_data(x):
	aggregate = []

	n_clus = int(max(x[:, 0].A1))
	for i in range(n_clus + 1):
		idxs = x[:, 0].A1 == i
		d = x[idxs, :]
		if len(d) == 0:
			continue
		json_data = geojson_cluster(i)
		for row in d:
			row = row.A1
			json_data.add_coord(row[1], row[2], row[3], row[4])
		aggregate.append(json_data)

	return aggregate

"""
Converts polarity and subjectivity measures for each json object in js_data
to a 0 - 1 scale
"""
def normalize_geojson(js_data):
	pols = []
	subs = []
	for js in js_data:
		pols.append(js.get_avg_polarity())
		subs.append(js.get_avg_subjectivity())
		
	max_pol = max(pols)
	min_pol = min(pols)
	max_sub = max(subs)
	min_sub = min(subs)
	old_range_pol = (max_pol - min_pol)
	old_range_sub = (max_sub - min_sub)

	for js in js_data:
		sub = (js.mAvgSubjectivity - min_sub) / old_range_sub
		sub -= .5
		sub *= 1.25
		sub += stats.pstdev(subs)/2
		sub += .5
		sub = max(0, sub)
		sub = min(1, sub)
		js.mAvgSubjectivity = sub

		pol = (js.mAvgPolarity - min_pol) / old_range_pol
		pol -= .5
		pol *= 1.25
		pol += stats.pstdev(pols)/2
		pol += .5
		pol = max(0, pol)
		pol = min(1, pol)
		js.mAvgPolarity = pol
	return js_data

"""
Converts a file with N rows and 5 delimited columns into a geoJSON object,
represented as a string. The file columns are assumed to be in the following
format:
	<cluster ID> <latitude> <longitude> <polarity> <subjectivity>
"""
def geojason_from_file(file, delim):
	x = fo.file_to_matrix(file, delim).astype(float)
	js_data = aggregate_matrix_data(x)
	js_data = normalize_geojson(js_data)
	js_string = create_geojson(js_data)
	return js_string

"""
Converts a data file or stdin to a geoJSON object, and prints it to STDOUT.
The file columns are assumed to be in the following format:
	<cluster ID> <latitude> <longitude> <polarity> <subjectivity>
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
	
	geo_json = geojason_from_file(file, constants.delim)
	print(geo_json)
