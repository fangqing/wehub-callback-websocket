import os,json
from ws4py.websocket import WebSocket
from .wehub_client_manager import WeHubClientManager

class WeHubClientHandler(WebSocket):
	def _init(self):
		pass

	def opened(self):
		print("a client connected = %s,pid = %s"%(self.sock.getpeername(),os.getpid()))
		WeHubClientManager().add(self,str(self.sock.getpeername()))
		self._init()

	def closed(self,code,reason = None):
		print("a client disconnected,code =%d,reason=%s"%(code,reason,))
		WeHubClientManager().remove(self,str(self.sock.getpeername()))

	def received_message(self, command_message):
		print ('ws received a message:', command_message)
		try:
			command_data = json.loads(command_message)
		except  Exception as e:
			print(e)
			return
		process_commond(command_data)

	def process_commond(self,command_data):
		#处理wehub客户端程序发过来的消息
		pass

	def process_browse_command(self,message):
		#处理浏览器发过来的命令(必须是json能解析的格式)
		try:
			command_data = json.loads(message)
		except  Exception as e:
			print(e)
			return "消息解析失败:(%s)"%e

		self.send(json.dumps(command_data))
		return "消息提交成功: %s"%message