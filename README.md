这是一个通用的websocket的demo.

运行环境:
 python3
 所需要的库:ws4py,cherrypy,jinja2

-----------------------------------------------------------------------------------------------

本demo 中websocket 服务运行在  ws://127.0.0.1:3456/ws
服务端处理json格式的文本数据.

客户端通过 ws://127.0.0.1:3456/ws与服务端进行websocket连接

(客户端可以是任何能发起websocket连接的程序)

可在浏览器中通过http://127.0.0.1:3456/admin 页面对已连接的客户端进行管理.

测试方法:
1.运行 python start_server.py 开启websocket服务器

2.在浏览器中打开测试页面 websocket_client_test.html 
将页面中的websockt地址改为 ws://127.0.0.1:3456/ws,然后点击"连接"
此时服务端会和该网页之间建立一个websocket连接
打开多个浏览器tab,重复上面的操作,则会建立了多个websocket连接

3.打开 http://127.0.0.1:3456/admin 管理页面,即可在网页中管理这些websocket连接