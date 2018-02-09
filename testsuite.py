import unittest as ut
from packages.dining.dining import getDiningEvents

class ATest(ut.TestCase):
	def anyTest(self):
		print("could be any test code here")

	def moreTest(self):
		print("could be more test code here")

class BTest(ut.TestCase):
	def failTest(self):
		print("test if something fails")

	def runTest(self):
		print("can run a few tests here")

class diningTest(ut.TestCase):
	def runTest(self):
		"""
		   Test getDiningEvents() function: 
		   currently there's no dining events on the dining website, so result is an empty list
		"""
		ut.TestCase.assertNotEqual(self, getDiningEvents(), [], msg="there are dining events the the result is not an empty list")
		#ut.TestCase.assertEqual(self, getDiningEvents(), [], msg="there are dining events the the result is not an empty list")

def suite():
	suite = ut.TestSuite()
	suite.addTest(ATest("anyTest"))
	suite.addTest(ATest("moreTest"))
	suite.addTest(BTest("failTest"))
	suite.addTest(BTest())
	suite.addTest(diningTest())
	return suite 

if __name__ == '__main__':
	runner = ut.TextTestRunner()
	runner.run(suite())