# coding=UTF-8
import xml.dom.minidom
import svg.path
from numpy import interp # only for interpolation, you can remove this dependency pretty easily
import math

counter = 500

class DrillSpot:
	letter = ''

	def __init__(self, location=(), number=0):
		global counter
		if number == 0:
			number = counter
		counter += 1 # using a counter ensures that if a spot has no number, it still has a unique identifier so we can manually fix it later
		self.location = location
		self.number = number

	def getFieldCoords(self):
		# first tuple value is steps to the RIGHT of the 50 from the director's viewpoint
		# a negative value means you're on the left side of the field, or side 1
		# second tuple value is steps UP from the front sideline
		# all values are rounded to three decimals
		
		# left is x = 29. right is x = 764.
		# interpolate 29->764 to -80->80
		x = interp(self.location[0], [29, 764], [-80, 80])

		# top is y = 56. bottom is y = 442
		y = interp(self.location[1], [56, 442], [84, 0])

		return (round(x, 3), round(y, 3))



class GuardSpot(DrillSpot):
	letter = 'G'

class ClarinetSpot(DrillSpot):
	letter = 'C'

class FluteSpot(DrillSpot):
	letter = 'F'

class TromboneSpot(DrillSpot):
	letter = 'R'

class AltoSpot(DrillSpot):
	letter = 'A'

class BaritoneSpot(DrillSpot):
	letter = 'B'

class TrumpetSpot(DrillSpot):
	letter = 'T'

class TenorSaxSpot(DrillSpot):
	letter = 'E'

class TubaSpot(DrillSpot):
	letter = 'U'

class SnareSpot(DrillSpot): 
	letter = 'S'

class TenorDrumSpot(DrillSpot):
	letter = 'Q'

class BassDrumSpot(DrillSpot):
	letter = 'D'

class Bass1Spot(BassDrumSpot):
	def __init__(self, location=()):
		BassDrumSpot.__init__(self, location, 1)

class Bass2Spot(BassDrumSpot):
	def __init__(self, location=()):
		BassDrumSpot.__init__(self, location, 2)

class Bass3Spot(BassDrumSpot):
	def __init__(self, location=()):
		BassDrumSpot.__init__(self, location, 3)

class Bass4Spot(BassDrumSpot):
	def __init__(self, location=()):
		BassDrumSpot.__init__(self, location, 4)

class Bass5Spot(BassDrumSpot):
	def __init__(self, location=()):
		BassDrumSpot.__init__(self, location, 5)


instruments = {
	57.521: [GuardSpot, 4.128906-1.621094j],
	48.241: [ClarinetSpot, 3.070312-3.710938j],
	41.664: [FluteSpot, -3.101562-4.621094j],
	56.517: [TromboneSpot, 0.480469-0.238281j],
	46.353: [AltoSpot, 1.730469+0.980469j],
	68.85: [BaritoneSpot, 0.101562-0.589844j],
	34.57: [TrumpetSpot, 4.011719-4.621094j],
	54.742: [TenorSaxSpot, -3.328125-4.589844j],
	47.539: [TubaSpot, -2.210938-4.570312j],

	50.11: [SnareSpot, -2.21875+1.710938j],
	56.707: [TenorDrumSpot, 4.328125+4.199219j],
	75.601: [Bass1Spot, -4+0.148438j],
	87.723: [Bass2Spot, -4.449219+0.148438j],
	86.793: [Bass3Spot, -4.019531+0.148438j],
	87.105: [Bass4Spot, -4.449219+0.148438j],
	87.979: [Bass5Spot, -4+0.148438j],
}

numbers = {
	10.952: [1, 5.050781+7.5j],
	18.43: [2, 5.769531+7.039062j],
	18.404: [3, 3.230469+6.460938j],
	17.289: [4, 4.78125+7.5j],
	19.671: [5, 3.230469+6.46875j],
	20.925: [6, 5.730469+4.519531j],
	13.43: [7, 3.261719+4.078125j],
	21.154: [8, 3.96875+5.371094j],
	20.952: [9, 3.300781+6.589844j],
	29.669: [10, 3.550781+7.5j],
	21.9: [11, 3.550781+7.5j],
	29.364: [12, 3.550781+7.5j],
	29.34: [13, 3.550781+7.5j],
	28.241: [14, 3.550781+7.5j],
	30.635: [15, 3.550781+7.5j],
	31.908: [16, 3.550781+7.5j],
	24.393: [17, 3.550781+7.5j],
	32.09: [18, 3.550781+7.5j],
	31.886: [19, 3.550781+7.5j],
	37.147: [20, 4.269531+7.039062j],
	29.377: [21, 4.269531+7.039062j],
	36.842: [22, 4.269531+7.039062j]
}

def getDrillSpots(filename):
	drillSpots = []

	dom = xml.dom.minidom.parse(filename)
	paths = dom.getElementsByTagName('path')

	for pathElement in paths:
		try:
			if pathElement.attributes['style'].value != " stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;":
				continue
		except KeyError:
			continue
		path = svg.path.parse_path(pathElement.attributes['d'].value)
		length = round(path.length(error=1e-4), 3)

		try:
			instrument = instruments[length]
			complexCoordinate = path[0].start - instrument[1]
			coordinate = (round(complexCoordinate.real, 3), round(complexCoordinate.imag, 3))

			drillSpots.append(instrument[0](location=coordinate))
		except KeyError:
			continue

	orphanNumbers = []

	for pathElement in paths:
		try:
			if pathElement.attributes['style'].value != " stroke:none;fill-rule:nonzero;fill:rgb(0%,0%,0%);fill-opacity:1;":
				continue
		except KeyError:
			continue
		path = svg.path.parse_path(pathElement.attributes['d'].value)
		length = round(path.length(error=1e-4), 3)

		try:
			number = numbers[length]
			complexCoordinate = path[0].start - number[1]
			coordinate = (complexCoordinate.real, complexCoordinate.imag)

			objSet = [x for x in drillSpots if x.location == coordinate]
			objSet[0].number = number[0]
		except KeyError:
			continue
		except IndexError:
			orphanNumbers.append([number, path])

	for numberPath in orphanNumbers:
		number = numberPath[0]
		path = numberPath[1]

		# print number[0], coordinate
		# numbers don't always line up in the same spot; instead we look for the closest letter to this number
		# naïve implementation is acceptable, no need to create a tree or deal with more dependencies
		closestDistance = 100
		closest = None
		for d in [d for d in drillSpots if d.number > 500]:	 # loop through the unassigned drill spots
			dx = d.location[0] - path[0].start.real
			dy = d.location[1] - path[0].start.imag
			distance = math.sqrt(dx ** 2 + dy ** 2)
			if distance < closestDistance:
				closestDistance = distance
				closest = d

		if closest is None:
			print 'large problem'
		elif number[0] not in [d.number for d in drillSpots if d.letter == closest.letter]:	# no duplicates
			closest.number = number[0]

	for d in drillSpots:
		if d.number > 500:
			print "problem"	# we assume that if a number was misassigned, there will be some letter without a number.
							# this isn't necessarily true, but with this dataset I think it's a safe assumption.
							# we can manually fix these pages when we see that there was an error output during generation.

	return drillSpots