# -*- coding: utf-8 -*-

import csv, codecs
from cjklib.reading import ReadingFactory



def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def getChars(freqFile,startNo,endNo):
	chars = []
	reader=unicode_csv_reader(codecs.open(freqFile, 'rb',"utf-8"), dialect='excel-tab')
	
	frequencyList = [x for x in reader] #read the whole list
	frequencyList = frequencyList[startNo:endNo]
	
	for row in frequencyList:
		templist = list(row[i] for i in [1,4,5])
		pinyin = ReadingFactory()
		readings = templist[1].split('/')
		# print readings
		readingString = ""
		for reading in readings:
			readingString += pinyin.convert(reading, 'Pinyin', 'Pinyin', sourceOptions={'toneMarkType': 'numbers','missingToneMark': 'fifth'}) +" "
		templist[1] = readingString
		
		chars.append(templist)
	
	return chars
	
if __name__ == '__main__':	
	freqFile = "resources/CharFreq.csv"
	chars = getChars(freqFile=freqFile, startNo=1500,endNo=2500)
	
	for line in chars: print line[0],'\t',line[1],'\t',line[2]