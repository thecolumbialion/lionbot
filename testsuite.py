import unittest as ut
from packages.dining.dining import getDiningEvents
from packages.clubs.clubs import find_clubs


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
        if currently there's no dining events on
        the dining website, result is an empty list
        """
        # ut.TestCase.assertNotEqual(self, getDiningEvents(), [], msg="there are no dining events the result is an empty list")
        ut.TestCase.assertEqual(self, getDiningEvents(), [], msg="there are dining events the result is not an empty list")


class clubTest(ut.TestCase):
    def runTest(self):
        """
        Test find_clubs() function.
        Using "ADI" as an input would get a list of length 2
        as result since ADI and cheerleading team will be
        returned as results
        """

        ut.TestCase.assertEqual(self, len(find_clubs("ADI")), 2, msg="There should be two results when the input is 'ADI' ")


def suite():
    suite = ut.TestSuite()
    suite.addTest(ATest("anyTest"))
    suite.addTest(ATest("moreTest"))
    suite.addTest(BTest("failTest"))
    suite.addTest(BTest())
    suite.addTest(diningTest())
    suite.addTest(clubTest())
    return suite


if __name__ == '__main__':
    runner = ut.TextTestRunner()
    runner.run(suite())
