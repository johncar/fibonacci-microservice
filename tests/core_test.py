from src import core
from unittest import TestCase

class core_test(TestCase):
	""" Tests for 'core.py'. """

	def test_fibonacci(self):
		""" Is the fibonacci function runs correctly? """
		result = core.fibonacci(3)
		self.assertEqual(2, result, 'should be equals to {0}'.format(result))

# to run tests in a single module.
# if __name__ == '__main__':
#	 import nose2
#    nose2.main()