import createScreensaverImage, getMostFreqChars

freqFile = "resources/CharFreq.csv"
screensaverDirectory = "screensaver2000-2500/"

i = 1
chars = getMostFreqChars.getChars(freqFile=freqFile, startNo=2000, endNo=2100)

for line in chars: 
	print i,":",line
	image = createScreensaverImage.drawScreensaverImage(line, debug = False)
	outfile = screensaverDirectory+str(i)+".png"
	image.save(outfile)
	i += 1