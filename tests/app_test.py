from flask import Response
from app import app
from unittest import TestCase
import json

class app_test(TestCase):

	def test_getTasks(self):
		""" Is the tasks route working correctly? """

		client = self.getTestClient()
		tasksCall = client.get('/tasks')
		
		myType = type(tasksCall)
		jsonResult = json.loads(tasksCall.data)

		self.assertEqual(myType, Response, "Should be equals to {0}".format(myType))
		self.assertEqual({}, jsonResult['tasks'], "Should exists and should be an empty object")

	def getTestClient(self):
		return app.app.test_client()

# to run tests in a single module.
# if __name__ == '__main__':
#	 import nose2
#    nose2.main()