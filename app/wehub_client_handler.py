import os,json,traceback
from ws4py.websocket import WebSocket
from .wehub_client_manager import WeHubClientManager
import logging
from . import const

class WeHubClientHandler(WebSocket):
	def _init(self):
		self.logger = logging.getLogger("ClientHandler")
		self.logger.setLevel(logging.INFO)

	def opened(self):
		self._init()
		WeHubClientManager().add(self,str(self.sock.getpeername()))
		self.logger.info("a client connected = %s,pid = %s"%(self.sock.getpeername(),os.getpid()))

	def closed(self,code,reason = None):
		WeHubClientManager().remove(self,str(self.sock.getpeername()))
		self.logger.info("a client disconnected,code =%d,reason=%s"%(code,reason))

	def received_message(self, message):
		try:
			if message.is_text:
				request_dict = json.loads(str(message),strict=False)
				self.logger.info("received a message =%s"%(request_dict))
				self.process_commond(request_dict)
		except Exception as e:
			self.logger.info("exception occur:", e,traceback.format_exc())
			return
		

	def process_commond(self,request_dict):
		#处理wehub客户端程序发过来的消息
		appid = request_dict.get('appid',None)
		action = request_dict.get('action',None)
		wxid = request_dict.get('wxid',None)
		req_data_dict = request_dict.get('data',{})

		if appid is None or action is None or wxid is None:
			self.logger.info("invalid param")
			return

		error_code, error_reason,ack_data,ack_type = self.main_req_process(wxid,action,req_data_dict)
		ack_dict= {'error_code':error_code,'error_reason':error_reason,'ack_type':str(ack_type),'data':ack_data}
		self.send(json.dumps(ack_dict))

		
	def process_browse_command(self,message):
		#处理浏览器发过来的命令(必须是json能解析的格式)
		try:
			command_data = json.loads(str(message),strict=False)
		except  Exception as e:
			print(e)
			return "json解析失败:(%s)"%e

		self.send(json.dumps(command_data))
		return "消息提交成功: %s"%message

	def main_req_process(self,wxid,action,request_data_dict):
		self.logger.info("action = {0},data = {1}".format(action,request_data_dict))
		ack_type = 'common_ack'
		if action in const.FIX_REQUEST_TYPES:
			ack_type = str(action)+'_ack'

		if wxid is None or action is None:
			return 1,'参数错误',{},ack_type
		if action=='login':
			return 0,"no error",{},ack_type
		if action=='report_friend_add_request':
			task_data = {
				'task_type':const.TASK_TYPE_PASS_FRIEND_VERIFY,
				'task_dict':{
					"v1":request_data_dict.get("v1"),
					"v2":request_data_dict.get("v2"),
				}
			}
			ack_data_dict = {'reply_task_list':[task_data]}
			return 0,'',ack_data_dict,ack_type
		if action=='report_new_msg':		
			msg_unit = request_data_dict.get('msg',{})
			if msg_unit:
				msg_type = msg_unit.get('msg_type',const.MSG_TYPE_INVALID)
				if msg_type in const.UPLOADFILE_MSG_TYPES:
					file_index = msg_unit.get('file_index','')
					if len(file_index)>0:
						task_data = {
							'task_type':const.TASK_TYPE_UPLOAD_FILE,
							'task_dict':{
								'file_index':file_index,
							}
						}
						ack_data_dict = {'reply_task_list':[task_data]}
						return 0,'',ack_data_dict,ack_type
				elif msg_type==4902: #转账
					#这里自动收账
					transferid = msg_unit.get('transferid',"")
					wxid_from = msg_unit.get("wxid_from","")
					wxid_to = msg_unit.get("wxid_to","")
					paysubtype = msg_unit.get("paysubtype",0)
					if paysubtype==1 and wxid_to==wxid:
						task_data ={
							'task_type':const.TASK_TYPE_AUTO_ACCOUNT_RECEIVE,		
							'task_dict':{
								'transferid':transferid,
								'wxid_from':wxid_from
							}
						}
						self.logger.info("begin auto confirm transferid")
						ack_data_dict = {'reply_task_list':[task_data]}
						return 0,'',ack_data_dict,ack_type
				elif msg_type==1:
					msg = msg_unit.get("msg","")
					room_wxid = msg_unit.get("room_wxid","")
					wxid_from = msg_unit.get("wxid_from","")
					self.logger.info("recv chatmsg:{0},from:{1}".format(msg,wxid_from))

					#测试代码
					if wxid_from ==const.TEST_WXID and  msg==str('fqtest'):
						reply_task_list =[]
						if len(room_wxid)>0:
							push_msgunit1 = {
								'msg_type':const.MSG_TYPE_TEXT,
								'msg':"群消息自动回复,test\ue537"
							}

							push_msgunit2 = {
								'msg_type':const.MSG_TYPE_IMAGE,
								'msg':"https://n.sinaimg.cn/mil/transform/500/w300h200/20180917/OBId-hikxxna1858039.jpg"
							}

							push_msgunit3 = {
								'msg_type':const.MSG_TYPE_LINK,
								'link_url':"http://httpd.apache.org/docs/2.4/getting-started.html",
								"link_title":"title",
								"link_desc":"hhhhh_desc",
								"link_img_url":"https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=3346649880,432179104&fm=27&gp=0.jpg"
							}

							
							#自动回复群消息
							test_task1 = {
								'task_type':const.TASK_TYPE_SENDMSG,
								"task_dict":
								{
									'wxid_to':room_wxid,
									'at_list':[wxid_from],
									"msg_list":[push_msgunit1,push_msgunit2,push_msgunit3]
								}
							}
							reply_task_list.append(test_task1)

						test_task2 = {
							"task_type":const.TASK_TYPE_SENDMSG,
							"task_dict":
							{
								"wxid_to":const.TEST_WXID,
								"msg_list":
								[
									{
										'msg_type':const.MSG_TYPE_TEXT,
										'msg':"wehub文本表情测试,一个商标,一个男人:\ue537\uE138"
									},
									{
										'msg_type':const.MSG_TYPE_TEXT,
										'msg':"wehub文本表情测试,一个微笑,一个高尔夫:[微笑]\uE014"
									}
								]
							}
						}
						reply_task_list.append(test_task2)
						ack_data_dict = {'reply_task_list':reply_task_list}
						return 0,'',ack_data_dict,ack_type

		return 0,'no error',{},ack_type