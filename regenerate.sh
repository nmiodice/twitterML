#!/bin/bash

# python script file names
get_tweets="tw_get.py"
get_clusters="tw_cluster.py"
get_sentiment="tw_sentiment.py"

# output/input file names
tweets="tweet.txt"
tweet_clusters="tweet_cluster.txt"
tweet_sentiment="tweet_sentiment.txt"

# parameters
n_tweets=10000

# generate output files
python3 $get_tweets $n_tweets > $tweets
python3 $get_sentiment $tweets > $tweet_sentiment
python3 $get_clusters $tweet_sentiment > $tweet_clusters