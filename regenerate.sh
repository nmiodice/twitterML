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
clus_to_file="tw_cluster_to_files.py"

# output/input file names
tweets=$data$sep"tweet.txt"
tweet_backup=$data$sep"tweet_backup.txt"
tweet_clusters=$data$sep"tweet_cluster.txt"
tweet_sentiment=$data$sep"tweet_sentiment.txt"
tweet_json=$data$sep"sentiment.json"

# parameters
n_tweets=100
bbox="-122 36 -69 48"

# generate output files
$py $get_tweets    $n_tweets $bbox  >> $tweets; cp $tweets $tweet_backup
$py $get_clusters  $tweets          > $tweet_clusters
$py $get_sentiment $tweet_clusters  > $tweet_sentiment
$py $clus_to_file  $tweet_clusters $data
$py $get_json      $tweet_sentiment > $tweet_json

