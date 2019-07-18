import json
import _thread
from .utils import singleton
import logging

@singleton
class WeHubClientManager(object):
	def __init__(self):
		"""
		singleton
		"""
		self.logger = logging.getLogger("ClientManager")
		self.logger.setLevel(logging.INFO)
		self.clients = {}

	def add(self, client,name):
		"""
		add a client to pool
		"""
		self.clients[name]=client
		self.refresh()
		self.logger.info('add a wehub client, current client count: %s,tid=%d'%(self.count(),_thread.get_ident()))
	
	def remove(self, client,name):
		"""
		remove a client object from pool
		"""
		self.clients.pop(name)
		self.refresh()
		self.logger.info('remove a wehub client, current client count: %s,tid=%d'%(self.count(),_thread.get_ident()))

	def get(self, name):
		return self.clients[name];
		
	def refresh(self):
		pass


	def count(self):
		return len(self.clients)
