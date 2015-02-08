import sys
import constants as const
import tw_file_ops as fo
import numpy as np
import re
sys.path.append("lib/pytwitter/")
from twitter import *

# Returns only numbers, letters and spaces, converted to lowercase
def clean(string, pattern):
	# gets rid of random new lines, tabs, etc...
	string = string.lower()
	string = ''.join([c for c in string if is_not_special_char(c)])
	string = pattern.sub('', string)
	string = ' '.join([w for w in string.split() if not 'http' in w])
	return string


def is_not_special_char(c):
	ascii = ord(c)
	return ((ascii > 96 and ascii < 122) or 
		(ascii > 47 and ascii < 58) or
		ascii == 32)

def get_tweets(n_tweets, delim):
	tweets = []
	query_args = dict()
	query_args['locations'] = "-80, 40, -69, 48" # New England (ish)

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
					if cnt > n_tweets:
						break

	return np.matrix(tweets)


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: " + sys.argv[0] + " <num tweets>")
		exit(-1)
	tweets = get_tweets(int(sys.argv[1]), const.delim)
	fo.print_matrix(tweets)
