import os
import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from app.wehub_client_handler import WeHubClientHandler
from app.wehub_client_manager import WeHubClientManager
import logging

WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 3456
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('app/templates'))

class Root(object):
	@cherrypy.expose
	def index(self):
		return 'yes,server is running.<a href="admin">进入管理页面</a>'

	@cherrypy.expose
	def admin(self):
		temp = env.get_template("manager.html")
		return temp.render(clients =WeHubClientManager().clients)

	@cherrypy.expose
	def ws(self):
		print("a websocket connnected")
		# you can access the class instance through
		handler = cherrypy.request.ws_handler

	@cherrypy.expose
	def commit_commond(self,clientid = None,message = ""):
		'''
		网页管理界面会通过这个url来发送数据
		'''
		print (cherrypy.request.method,clientid,message)
		if clientid not in WeHubClientManager().clients:
			return "param error!"
		client = WeHubClientManager().clients.get(clientid)
		return client.process_browse_command(message)

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(name)s-[%(levelname)s]:%(message)s ',)

	cherrypy.config.update({
		'server.socket_host': SERVER_HOST,
		'server.socket_port': SERVER_PORT,
		'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
		'log.screen': True
		})

	wehub_cfg ={
		'/ws': {
			'tools.websocket.on': True,
			'tools.websocket.handler_cls': WeHubClientHandler
			},

		'/static':{
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './app/static'
		}
	}
	cherrypy.quickstart(Root(), '/', config= wehub_cfg)