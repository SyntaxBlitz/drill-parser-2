import glob
import extractor
import json

svgs = glob.glob('../pages/*.svg')

for svg in svgs:
	print svg
	drillSpots = extractor.getDrillSpots(svg)
	f = open(svg.replace('.svg', '.json'), 'w')
	outSpots = {spot.letter + str(spot.number): spot.getFieldCoords() for spot in drillSpots}
	print len(outSpots)
	outJson = {
		'spots': outSpots
	}
	json.dump(outJson, f)
	f.close()