# twitterML
A text sentiment analysis visualization tool to see peoples mood visualized on a map. Utilizes the Twitter API and some text processing libraries to see how people are feeling across the US (or, you can modify it to show you data from anywhere, provided people Tweet there...). What does this tell you? Not much -- the text processing libraries aren't very precise, and people don't often type very well on twitter, but its a fun side project that involves some cool machine learning. Perhaps you'd like to contribute and make it more usable!

# Usage #
After modifying the ```ntweets``` variable in ```regenerate.sh``` to have the # of tweets you'd like to query for (large numbers take a while, small numbers don't work due to the nature of the problem at hand -- cluster analysis doesn't work well if you cant cluster!), run:
```
sh regenerate.sh
$python -m SimpleHTTPServer
````

Then point your browser to http://localhost:8000/map.html

You should see some cool clusters, and you can select to see either 'polarity' or 'subjectivity' clusters on the map
