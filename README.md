这是一个通用的websocket的demo.

运行所需的环境:   
 python3 及部分python库: ws4py, cherrypy, jinja2   (可通过pip 或者easy_install 方式安装)

-----------------------------------------------------------------------------------------------

本demo中websocket服务的ws地址为  ws://127.0.0.1:3456/ws  
服务端只处理json格式的文本数据 

客户端通过 ws://127.0.0.1:3456/ws与服务端进行websocket连接

(可以通过websocket_client_test.html  这个页面发起websocket连接)

可以在浏览器中通过http://127.0.0.1:3456/admin  给ws客户端直接发送数据

若要增加功能请修改 app\templates\manager.html  文件

---

测试方法:
1.开启websocket服务器: 运行python start_server.py  

2.在浏览器中打开测试页面 websocket_client_test.html 
将页面中的websockt地址改为 ws://127.0.0.1:3456/ws,然后点击"连接"
此时服务端会和该网页之间建立一个websocket连接
打开多个浏览器tab,重复上面的操作,则会建立了多个websocket连接   

3.打开 http://127.0.0.1:3456/admin 管理页面,即可在网页中管理这些websocket连接