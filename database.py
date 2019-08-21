from datetime import datetime
import urllib3

class BD_FireBase(object):

	def __init__(self):
		firebaseConfig = {
			"apiKey": "",
			"authDomain": "",
			"databaseURL": "",
			"projectId": "",
			"storageBucket": "",
			"messagingSenderId": "",
			"appId": ""
		  }
		self.firebase = pyrebase.initialize_app(firebaseConfig)
		self.banco = self.firebase.database()
