from kol.request.AccountRequest import AccountRequest
from kol.request.HomepageRequest import HomepageRequest
from kol.request.LoginRequest import LoginRequest
from kol.request.LogoutRequest import LogoutRequest

import cookielib
import hashlib
import urllib2

class Session(object):
	"This class represents a user's session with The Kingdom of Loathing."
	
	def __init__(self):
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
		self.isConnected = False
		self.userId = None
		self.userName = None
		self.userPasswordHash = None
		self.serverURL = None
		self.pwd = None
	
	def login(self, username, password, serverNumber=0):
		"""
		Perform a KoL login given a username and password. A server number may also be specified
		to ensure that the user logs in using that particular server. This can be helpful
		if the user continues to be redirected to a server that is down.
		"""
		
		self.userName = username
		self.userPasswordHash = hashlib.md5(password).hexdigest()
		
		# Grab the KoL homepage.
		homepageRequest = HomepageRequest(self, serverNumber=serverNumber)
		homepageResponse = homepageRequest.doRequest()
		self.serverURL = homepageResponse["serverURL"]
		
		# Perform the login.
		loginRequest = LoginRequest(self, homepageResponse["loginChallenge"])
		loginRequest.doRequest()
		
		# Get pwd, user ID, and the user's name.
		accountRequest = AccountRequest(self)
		accountResponse = accountRequest.doRequest()
		self.pwd = accountResponse['pwd']
		self.userName = accountResponse['userName']
		self.userId = accountResponse['userId']
	
	def logout(self):
		"Performs a logut request, closing the session."
		logoutRequest = LogoutRequest(self)
		logoutRequest.doRequest()
