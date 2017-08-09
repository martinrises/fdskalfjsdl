import urllib.request
import json

saveFilePath = '/data/balance_origin.txt'

def get_first_in_index(list_src, list_target):
	for i in range(len(list_src)):
		if list_src[i] in list_target:
			return i
	return -1



def get_strings(strFrom):
	data = json.loads(strFrom)
	return data['datas']



def saveFile(dataStr):
	if dataStr == None:
		return False

	with open(saveFilePath, 'ar') as targetFile:
		linesToSave = get_strings(dataStr, ',')
		dataInFileStr = targetFile.read()

		linesInFile = targetFile.readlines()

		index = get_first_in_index(linesToSave, linesInFile)
		if index < 0:
			targetFile.writelines(linesToSave)
			return True
		else:
			targetFile.writelines(linesToSave[:index])
			return False




page = 1
url = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=SHSZHSSUM&st=0&sr=1&p={}&ps=50&js=var%20RQLTVKNf={pages:(pc),data:[(x)]}&rt=50073233'
shouleContinue = True
while shouleContinue:
	dataStr = urllib.request.urlopen(url.format(page))
	dataStr = '{\"datas\":' + dataStr[dataStr.index('[') + 1: (len(dataStr))]
	print('subDataStr = {}'.format(dataStr))
	shouldContinue = saveFile(dataStr)
	page+=1