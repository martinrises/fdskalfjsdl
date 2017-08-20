import urllib.request
import json
import os.path

saveFilePath = './data/balance_origin.txt'

def get_first_in_index(list_src, list_target):
	for i in range(len(list_src)):
		_ = list_src[i]
		for j in range(len(list_target)):
			_j = list_target[j]
			_j = _j[:len(_j) - 1]
			if _ == _j:
				return i
	return -1



def get_strings(strFrom):
	data = json.loads(strFrom)
	return data['datas']



def saveFile(dataStr):
	if dataStr == None:
		return 0

	print("file exist >>> {}".format(os.path.isfile(saveFilePath)))
	if not os.path.isfile(saveFilePath):
		f = open(saveFilePath, "a")
		f.close()

	with open(saveFilePath, 'r') as targetFile:
		linesInFile = list(targetFile.readlines())
		print('saveFile >>> len(linesInFile) = {}'.format(len(linesInFile)))

	with open(saveFilePath, 'a+') as targetFile:
		linesToSave = get_strings(dataStr)
		print('saveFile >>> len(lineToSave) = {}'.format(len(linesToSave)))

		index = get_first_in_index(linesToSave, linesInFile)
		print('saveFile >>> index = {}'.format(index))
		if index < 0:
			for i in range(len(linesToSave)):
				targetFile.write(linesToSave[i])
				targetFile.write("\n")
		else:
			targetFile.writelines(linesToSave[:index])
		return index




page = 1
url_seg = 'http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=SHSZHSSUM&st=0&sr=1&p='
url_seg1 = '&ps=50&js=var%20RQLTVKNf={pages:(pc),data:[(x)]}&rt=50073233'
first_in_index = -1;
while first_in_index < 0:
	dataStr = urllib.request.urlopen(url_seg + str(page) + url_seg1).read().decode('utf-8')
	print('dataStr >>> {}' + dataStr)
	dataStr = '{\"datas\":[' + dataStr[dataStr.index('[') + 1: (len(dataStr))]
	print('after processed, dataStr >>> ' + dataStr)
	first_in_index = saveFile(dataStr)
	print('shouldContinue = ' + str(first_in_index < 0))
	page+=1