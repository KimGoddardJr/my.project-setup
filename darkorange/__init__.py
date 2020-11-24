import darkorange
from PyQt5 import QtCore

def getStyleSheet():
	stream = QtCore.QFile(':/darkorange.qss')
	if stream.open(QtCore.QFile.ReadOnly):
		st = str(stream.readAll())
		stream.close()
	else:
		print(stream.errorString())
		
	return st