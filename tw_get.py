import sys
import constants as const
import tw_file_ops as fo
import numpy as np
import re
sys.path.append("lib/pytwitter/")
from twitter import *

"""
Cleans a string of all non-alpha only words, special characters, and
links to URLs
"""
def clean(string, pattern):
	# gets rid of random new lines, tabs, etc...
	string = string.lower()
	string = ''.join([c for c in string if is_not_special_char(c)])
	string = pattern.sub('', string)
	string = ' '.join([w for w in string.split() if not 'http' in w])
	return string

"""
Returns true if a character is a lowercase letter OR a space OR
a number
"""
def is_not_special_char(c):
	ascii = ord(c)
	return ((ascii > 96 and ascii < 122) or 
		(ascii > 47 and ascii < 58) or
		ascii == 32)

"""
Returns a matrix with some data about some number of tweets, specified by 
N_TWEETS. The data is returned in an N x P matrix, where N = N_TWEETS. The
tweet features returned are:
	col 0: latitude of tweet
	col 1: longitude of tweet
	col 2: cleaned version of the tweet text
The COORDS parameter is to be a list of length 4 where the properties are:
    coors[0] = southwest corner longitude
    coors[1] = southwest corner latitude
    coors[2] = northeast corner longitude
    coors[3] = northeast corner latitude
"""
def get_tweets(n_tweets, coords):
	tweets = []
	coords = list(map(str, coords))
	query_args = dict()
	query_args['locations'] = ', '.join(coords)#"-80, 40, -69, 48" # New England (ish)

	auth = OAuth(
		consumer_key = const.twitter_consumer_key,
		consumer_secret = const.twitter_consumer_secret,
		token = const.twitter_token,
		token_secret = const.twitter_token_secret
	)
	twitter_stream = TwitterStream(auth = auth)
	iterator = twitter_stream.statuses.filter(**query_args)

	# define a regex pattern for "good quality" words
	pattern = re.compile('\w*\d\w*')
	# get tweets of good quality, until we find the appropriate amount
	cnt = 0
	for tweet in iterator:
		if 'coordinates' in tweet and tweet['coordinates'] is not None:
			if 'text' in tweet and tweet['text'] is not None:
				text = clean(tweet['text'], pattern)
				if text != None and text != '':
					# coords[0] = longitude, coords[1] = latitude
					coords = tweet['coordinates']['coordinates']
					tweets.append([coords[1], coords[0], text])
					cnt = cnt + 1
					if cnt % 1000 == 0:
					    sys.stderr.write("logged " + str(cnt) + " tweets\n")
					    sys.stderr.flush()
					if cnt > n_tweets:
						break

	return np.matrix(tweets)

"""
Prints tweet data to stdout
"""
if __name__ == '__main__':
	if len(sys.argv) != 6:
		print("Usage: " + sys.argv[0] + " <num tweets> <S.W. long> <S.W. lat> <N.E. long> <N.E. lat>")
		exit(-1)
	
	# build the coordinates in the correct order
	for i in range(2, 6):
		sys.argv[i] = int(sys.argv[i])
	coords = []
	coords.append(min(sys.argv[2], sys.argv[4]))
	coords.append(min(sys.argv[3], sys.argv[5]))
	coords.append(max(sys.argv[2], sys.argv[4]))
	coords.append(max(sys.argv[3], sys.argv[5]))

	tweets = get_tweets(int(sys.argv[1]), coords)
	fo.print_matrix(tweets)
