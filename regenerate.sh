#!/bin/bash

# path parameters
data="data"
sep="/"

# python file names
py="python3"
get_tweets="tw_get.py"
get_clusters="tw_cluster.py"
get_sentiment="tw_sentiment.py"

# output/input file names
tweets=$data$sep"tweet.txt"
tweet_clusters=$data$sep"tweet_cluster.txt"
tweet_sentiment=$data$sep"tweet_sentiment.txt"

# parameters
n_tweets=10000

# generate output files
# $py $get_tweets    $n_tweets        > $tweets
$py $get_sentiment $tweets          > $tweet_sentiment
$py $get_clusters  $tweet_sentiment > $tweet_clusters