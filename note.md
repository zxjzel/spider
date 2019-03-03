## 定义  
**网络爬虫(又被称为网页蜘蛛，网络机器人)就是模拟客户端发送网络请求，接受请求响应，一种按照一定的规则，自动地抓取互联网信息的程序。  
只要浏览器能做的事情，原则上，爬虫都能够做**
## 流程
1. **搜索引擎：**
	- **抓取网页**
	- **数据存储**
	- **预处理**
	- **提供检索服务，网站排名**
2. **聚焦爬虫**
	- **url list**
	- **响应内容，提取url**
	- **提取数据**
	- **入库**
## 发送简单的请求
### response的常用方法
	```python
	response = requests.get(url)
	response.text
	response.content
	response.status_code
	response.request.headers
	response.headers```  
**response.text和response.content的区别**  
- response.text  
	- 类型：str  
	- 解码类型：根据HTTP头部对响应的编码做出有根据的推测，推测的文本解码  
	- 如何修改编码方式：`response.encoding="jbk"`  
- response.content  
	- 类型：bytes  
	- 解码类型：没有指定  
	- 如何修改编码方式：`response.content.decode("utf8")`  
### 发送带header的请求
**为什么请求需要带上header？  
模拟浏览器，欺骗服务器，获取和浏览器一致的内容。**  
- header的形式:字典  
- 用法:requests.get(url,headers=headers)
### Reauests深入
1. 发送POST请求  
**哪些地方我们会用到POST请求：**
	- 登陆注册(POST比GET更安全)
	- 需要传输大文本内容的时候(POST请求对数据长度没有要求)
	- 用法
		- `response = requests.post("http://www.baidu.com",data=data,headers=headers)`
    	- data的形式字典
2. 使用代理
	- 用法
		- `reauests.get("http://www.baidu.com",proxies=proxies)`
    	- proxies的形式：字典
   		- `proxies = {
		"http":"http://12.34.56.79:9527",
       	"https":"https://12.34.56.79:9527"}`
	- 准备一堆的ip地址，组成ip池，随机选择一个ip来使用
	- 如何随机选择代理ip，让使用次数较少的ip地址由更大的可能性被使用到
		- {"ip":ip,"times":0}
    	- [{},{},{},{}]，对这个ip的列表进行排序，按照使用次数进行排序
    	- 选择使用次数较少的几个ip，从中随机选择一个
	- 检擦ip的可用性
		- 可以使用requests添加超时参数，判断ip地址的质量
    	- 在线代理ip质量检测的网站
3. 处理cookies session  
**带上cookie、session的好处：  
能够请求到登陆后的页面  
弊端：  
一套cookie和session往往和一个用户对应，请求太快，请求次数太多，容易被服务器识别为爬虫。  
不需要cookie的时候尽量不去使用cookie  
但是为了获取登陆之后的页面，我们必须发送带有cookies的请求。**
	- requests提供了一个叫做session类，来实现客户端和服务端的会话保持
	- 使用方法：
		- 实例化一个session对象
    	- 让session发送get或者post请求,把cookie保存在session中
    	- 再使用session请求登陆后才能访问的网站，session能够自动的携带登陆成功时保存在其中的cookie，进行请求    `session = requests.session()`
		`response = session.get(url,headers)`
	- 不发送post请求，使用cookie获取登陆后的界面
		- cookie工期很长的网站
    	- 在cookie过期之前能够拿到所有的数据
    	- 配合其他程序一起使用，其他程序专门获取cookie，当前程序专门请求页面
	- 获取登陆后的页面的三种方式
		- session
    	- headers中添加cookie建，值为cookie字符串
    	- 在请求方法中添加cookies参数，接收字典形式的cookie
4. Requests小技巧
	1. `reqeusts.util.dict_from_cookiejar`把cookie对象转化为字典
	2. 请求SSL证书验证`response=requests.get("https://www.12306.cn/mormhweb/",verify=False)`
	3. 设置超时`response=requests.get(url,timeout=10)`
	4. 配合状态码判断是否请求成功`assert response.status_code==200`
	5. retrying模块简单用法：
		- stop_max_attempt_number设置最大重试次数
		- 
		```
		@retry(stop_max_attempt_number=7)
		def stop_after_7_attempts():
    		print "Stopping after 7 attempts"
    		raise
		```
		- retry_on_exception指定异常类型，指定的异常类型会重试，不指定的类型，会直接异常退出，wrap_exception参数设置为True，则其他类型异常，或包裹在RetryError中，会看到RetryError和程序抛的Exception error
		- 
		```
		def retry_if_io_error(exception):  
    		"""Return True if we should retry (in this case when it's an IOError), False otherwise"""  
    		return isinstance(exception, IOError)  
		@retry(retry_on_exception=retry_if_io_error)
		def might_io_error():
			print "Retry forever with no wait if an IOError occurs, raise any other errors"
	    	raise Exception('a')
		@retry(retry_on_exception=retry_if_io_error, wrap_exception=True)
		def only_raise_retry_error_when_not_io_error():
	    	print "Retry forever with no wait if an IOError occurs, raise any other errors wrapped in RetryError"
	    	raise Exception('a')```
## 寻找登陆的post地址  
- 在form表单中存照action对应的url地址
	- post的数据时input标签中name的值作为键，真正的用户名密码作为值的字典，post的url地址就是acction对应的url地址
- 抓包，寻找登陆的url地址
	- 勾选perserv log按钮，防止页面跳转找不到url
	- 寻找post数据，确定参数
		- 参数不会变，直接用，比如密码不是动态加密的时候
		- 参数会变
			- 参数在当前的相应中
			- 通过js生成
## 定位想要的js
- 选择会触发js时间的按钮，点击event listener，找到js的位置
- 通过chrome中的search all file 来搜索url中关键字
- 添加断点的方式来查看js的操作，通过python来进行同样的操作
