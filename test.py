import sys
sys.path.append("lib/pytwitter/")
from twitter import *

def print_prefix():
	print("""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Heatmaps</title>
    <style>
      html, body, #map-canvas {
        height: 100%;
        margin: 0px;
        padding: 0px
      }
      #panel {
        position: absolute;
        top: 5px;
        left: 50%;
        margin-left: -180px;
        z-index: 5;
        background-color: #fff;
        padding: 5px;
        border: 1px solid #999;
      }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&signed_in=true&libraries=visualization"></script>
    <script>
var map, pointarray, heatmap;

var taxiData = [""")


def print_postfix():
	print("""];

function initialize() {
  var mapOptions = {
    zoom: 6,
    center: new google.maps.LatLng(43, -71),
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };

  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  var pointArray = new google.maps.MVCArray(taxiData);

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: pointArray
  });

  heatmap.setMap(map);
}

function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
  var gradient = [
    'rgba(0, 255, 255, 0)',
    'rgba(0, 255, 255, 1)',
    'rgba(0, 191, 255, 1)',
    'rgba(0, 127, 255, 1)',
    'rgba(0, 63, 255, 1)',
    'rgba(0, 0, 255, 1)',
    'rgba(0, 0, 223, 1)',
    'rgba(0, 0, 191, 1)',
    'rgba(0, 0, 159, 1)',
    'rgba(0, 0, 127, 1)',
    'rgba(63, 0, 91, 1)',
    'rgba(127, 0, 63, 1)',
    'rgba(191, 0, 31, 1)',
    'rgba(255, 0, 0, 1)'
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 20);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
}

google.maps.event.addDomListener(window, 'load', initialize);

    </script>
  </head>

  <body>
    <div id="panel">
      <button onclick="toggleHeatmap()">Toggle Heatmap</button>
      <button onclick="changeGradient()">Change gradient</button>
      <button onclick="changeRadius()">Change radius</button>
      <button onclick="changeOpacity()">Change opacity</button>
    </div>
    <div id="map-canvas"></div>
  </body>
</html>""")

def main():
	query_args = dict()
	query_args['locations'] = "-80, 40, -69, 48" # New England (ish)

	auth = OAuth(
		consumer_key='BAImA9T485yMmGGYKem00LwNj',
		consumer_secret='2hcpyq2VuTtlBTivz62EuXLSmdaZAjMjoq0QCK15M50zekRZ3a',
		token='175392486-fmyCUCmONdksDCh37xNiJqP18GMFlunaqHctmsyp',
		token_secret='II401W6HPwvh4iooKCpm4sRY8qgZi4XayVa3L1Q25uFUP'
	)
	twitter_stream = TwitterStream(auth = auth)
	iterator = twitter_stream.statuses.filter(**query_args)

	print_prefix()
	cnt = 0
	for tweet in iterator:
		if 'coordinates' in tweet:
			if tweet['coordinates'] is not None:
				# c[0] = longitude, c[1] = latitude
				c = tweet['coordinates']['coordinates']
				print('  new google.maps.LatLng(' + str(c[1]) + ', ' + str(c[0]) + '),')
		cnt = cnt + 1
		if cnt >= 1000:
			break

	print_postfix()

if __name__ == '__main__':
	main()
