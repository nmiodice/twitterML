#!/bin/bash

# path parameters
data="data"
sep="/"

# python file names
py="python3"
get_tweets="tw_get.py"
get_clusters="tw_cluster.py"
get_sentiment="tw_sentiment.py"
get_json="tw_geojson.py"

# output/input file names
tweets=$data$sep"tweet.txt"
tweet_clusters=$data$sep"tweet_cluster.txt"
tweet_sentiment=$data$sep"tweet_sentiment.txt"
tweet_json=$data$sep"sentiment.json"

# parameters
n_tweets=80000
bbox="-122 36 -69 48"

# generate output files
#$py $get_tweets    $n_tweets $bbox  >> $tweets
$py $get_sentiment $tweets          > $tweet_sentiment
$py $get_clusters  $tweet_sentiment > $tweet_clusters
$py $get_json      $tweet_clusters  > $tweet_json
