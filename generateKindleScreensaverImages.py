import createImage, getMostFreqChars

freqFile = "resources/CharFreq.csv"

i = 1
chars = getMostFreqChars.getChars(freqFile=freqFile, number=100)
for line in chars: 
	print i,":",line
	image = createImage.drawKindleHanzi(line, debug = False)
	outfile = "output/"+str(i)+".png"
	image.save(outfile)
	i += 1