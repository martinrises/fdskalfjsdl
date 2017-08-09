import json
import urllib.request

page = 1
url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=SHSZHSSUM&st=0&sr=1&p={}&ps=50&js=var%20RQLTVKNf={pages:(pc),data:[(x)]}&rt=50073233'
dataStr = urllib.request.urlopen(url.format(page))

print(dataStr.read())