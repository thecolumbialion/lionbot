""" Test for working future dining hall hours """
import unittest
import dining
from dining.future_hall_hours import find_hall_hours
from dining.menu_scraper import get_soup

class test_future_hall_hours(unittest.TestCase):

	#def test_future_hall_hours(self):


	def test_find_hall_hours(self):
		print ("Test Function: Find Hall Hours \n")
		url = 'https://barnard.edu/dining/locations/hewitt-dining-hall'
		#url = 'https://barnard.edu/dining/locations/diana-center-cafe'
		#url = 'https://barnard.edu/dining/locations/lizs-place'
		hours = find_hall_hours(url)
		return hours

		
# run test, print to stdout
if __name__ == '__main__':
	unittest.main();
