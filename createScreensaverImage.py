# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import unicodedata, textwrap

#setup
kindleWidth = 600 	# Kindle 4. Not DX. Not sure about the others
kindleHeight = 800	# Kindle 4. Not DX. Not sure about the others

startFontSize = 24 	#just to save us a few processor cycles
inset = 50 			# the inset which is used here and there
scaleFactor = 1 	# we'll have to scale the picture up and then down again, or the fonts will look bad for some of the smaller sizes


fontFace = {"hanzi":"resources/华文黑体.ttf", 
			"pinyin":"resources/LinBiolinum_RBah.ttf",
			"translation":"resources/华文黑体.ttf"}
			
boxHeight = {"hanzi":450*scaleFactor, 
			"pinyin":100*scaleFactor,
			"translation":250*scaleFactor}
			
textColour = {"hanzi":(0,0,0), 
			"pinyin":(187,187,187),
			"translation":(85,85,85)}
			
			

def drawCenteredWrappedText(draw, text, font, color, bbox, debug=False):
	"""While we're not processing the last word: 
	"""
	x0, y0, x1, y1 = bbox # note: y1 is ignored
	height = y0
	words = text.split()
	line = ""
	i=0;
	lastWord = False
	while i < len(words):
		if (i==len(words)-1): lastWord=True
		
		linewidth, lineheight = draw.textsize(line, font)
		
		if debug: print "line:",line
		if debug: print "i:",i, "of: ", len(words)
		if debug: print "words[i]:",words[i], (draw.textsize(words[i], font)[0])
		if debug: print 'next line:',line+words[i], (draw.textsize(line+words[i], font)[0]), "<", x1		
		
		
		if (draw.textsize(line+words[i], font)[0] > x1) and line != "":
			if debug: print 'breaking with line: ',line, "lastWord:",lastWord
			draw.text((((kindleWidth * scaleFactor) - linewidth)/2, height), line, font = font, fill = color)
			height += lineheight
			line = words[i]
			
		else:
			line += words[i]
					
		if debug: print "is last word? ",lastWord				
		if lastWord:
			linewidth, lineheight = draw.textsize(line, font)
			draw.text((((kindleWidth * scaleFactor)  - linewidth)/2, height), line, font = font, fill = color)
			break			
			
		i+=1;
		line += " "
		
		if debug: print ""
		



def determineOptimalFontSize(draw, text, font, bbox, debug=False):
	"""Figures out where to draw the words within the bounds of bbox 
	with a given font size. I can't use this function directly because I can't center words, 
	but it provides a beautiful work-around to determine the optimal font size.
	This function was originally from: http://svn.effbot.org/public/stuff/sandbox/pil/textwrap.py"""
	
	x0, y0, x1, y1 = bbox # note: y1 is ignored
	space = draw.textsize("w", font)[0]
	words = text.split()
	x = x0; y = y0; h = 0;
	lineCount = 1
	for word in words:
		# check size of this word
		w, h = draw.textsize(word, font)
		if debug: print word, 'w:',w, 'h:',h, 'x1:',x1, 'x0:',x0, "x:",x
		# figure out where to draw it
		if x > x0:
			x += space
			if x + w > x1:
				# new line
				x = x0
				y += h
				lineCount +=1
		x += w
		
	return y + h, lineCount, x
	



def drawScreensaverImage(characterItems, debug = False):
	"""Draws the hanzi and returns the image"""
	
	global kindleWidth, kindleHeight, startFontSize, inset, scaleFactor
	global fontFace, boxHeight, textColour


	character = {"hanzi":characterItems[0],
				"pinyin":characterItems[1],
				"translation":characterItems[2]}
				
	#set up canvas
	image = Image.new("RGBA", ((kindleWidth * scaleFactor), (kindleHeight * scaleFactor)), "white")
	draw = ImageDraw.Draw(image)




	###############	  HANZI	  ########################
	#determine optimal font size by iterating until the text size is just larger than the criteria
	fontSize = startFontSize
	font = ImageFont.truetype(fontFace["hanzi"], fontSize)
	while font.getsize(character["hanzi"])[0] < ((kindleWidth * scaleFactor)) and font.getsize(character["hanzi"])[1] < (boxHeight["hanzi"]):
		fontSize += 1
		font = ImageFont.truetype(fontFace["hanzi"], fontSize)


	#draw the hanzi
	x = ((kindleWidth * scaleFactor)-font.getsize(character["hanzi"])[0])/2 # center based on character width
	y = 0 #we start at the top
	if debug: draw.rectangle((0,0,(kindleWidth * scaleFactor),boxHeight["hanzi"]),outline="green")
	if debug: draw.rectangle((x,y,(kindleWidth * scaleFactor),boxHeight["hanzi"]),outline="red")
	draw.text((x,y), character["hanzi"], textColour["hanzi"], font=font)
	#------------------------------------------------#
	




	###############	  PINYIN   ########################
	#determine optimal font size by iterating until the text size is just larger than the criteria 
	fontSize = startFontSize
	font = ImageFont.truetype(fontFace["pinyin"], fontSize)
	while font.getsize(character["pinyin"])[0] < ((kindleWidth * scaleFactor)-(inset * scaleFactor)*2) and font.getsize(character["pinyin"])[1] < (boxHeight["pinyin"]):
		fontSize += 1
		font = ImageFont.truetype(fontFace["pinyin"], fontSize)

	#draw the pinyin
	x = ((kindleWidth * scaleFactor) - font.getsize(character["pinyin"])[0])/2 # center based on pinyin width. No need for inset because that was already taken into account for the pinyin width, now we just need to center!
	y = boxHeight["hanzi"]+(inset * scaleFactor)/2 # we start after the character and a little space
	if debug: draw.rectangle((x, y, (kindleWidth * scaleFactor), boxHeight["hanzi"]+boxHeight["pinyin"] ), outline="green") #actual box
	if debug: draw.rectangle(((inset * scaleFactor), y, (kindleWidth * scaleFactor), boxHeight["hanzi"]+boxHeight["pinyin"] ), outline="red")	#theoretical box
	draw.text((x, y), character["pinyin"], textColour["pinyin"], font=font)
	#------------------------------------------------#






	###############	  TRANSLATION	########################
	
	character["translation"] = character["translation"].replace('/','; ')	#looks better with ';' instead of '/'
	
	# the box in which the translation has to fit, including insets
	x0 = 0+(inset*scaleFactor)																		#upper left x
	y0 = (boxHeight["hanzi"]+boxHeight["pinyin"]+(inset*scaleFactor)) 					#upper left y
	x1 = (kindleWidth * scaleFactor)-(inset*scaleFactor)								#lower right x
	y1 = (kindleHeight * scaleFactor)-(inset*scaleFactor)								#lower right y
	translationBox = (x0, y0, x1, y1)

	#I use the function determineOptimalFontSize which writes words next to each other until the box is full to determine the optimal font size
	#Once I have that, I use drawCenteredWrappedText which uses that font size obtained in the prior step to write and center the text line-wise!
	fontSize = startFontSize
	font = ImageFont.truetype(fontFace["translation"], fontSize)
	translationBoxHeight = x = 0
	while translationBoxHeight < y1 and x < x1:	#check if the text in the box isn't getting larger than the box and - in the case of a single word - if the word isn't popping out at the edges!
		translationBoxHeight, linecount, x = determineOptimalFontSize(draw, character["translation"], font, translationBox, debug=debug)
		if debug: print "text size:",fontSize, "tbox height:",translationBoxHeight, "allowed height:", y1
		fontSize += 1
		font = ImageFont.truetype(fontFace["translation"], fontSize)
	# now the know the font size and the line count!
	font = ImageFont.truetype(fontFace["translation"], fontSize-2) #why -2? who knows!

	if debug: draw.rectangle(translationBox,outline="red")
	if debug: draw.rectangle((0,(boxHeight["hanzi"]+boxHeight["pinyin"]),(kindleWidth * scaleFactor),(boxHeight["hanzi"]+boxHeight["pinyin"]+boxHeight["translation"])), outline="green")
	
	# draw the translation into the translation box using the right font size determined in the last step
	drawCenteredWrappedText(draw, character["translation"], font, textColour["translation"], translationBox, debug=debug)
	#------------------------------------------------#




	img_resized = image.resize((kindleWidth, kindleHeight), Image.ANTIALIAS) #scale the image down again with antialiasing. Looks much prettier this way!
	return img_resized





if __name__ == '__main__':	 
	
	characterItems = [u"张",u"zhāng",u"pretty/girl/stretch; spread;	 张; expand; open; tes ttest test test last"]
	# characterItems = [u"学",u"xué",u"Learn Chinese simply by looking at your phone!"]
	characterItems = [u'\u5f53', u'd\u0101ng d\xe0ng ', u'to be/to act as/manage/withstand/when/during/ought/should/match equally/equal/same/obstruct/just at (a time or place)/on the spot/right/just at, at or in the very same.../to pawn/suitable/adequate/fitting/proper/replace/represent']
	characterItems = [u'\u5b55', u'y\xf9n ', u'pregnant']

	image = drawScreensaverImage(characterItems, debug = True)
	
	image.show()
	
	outfile = "output.png"
	# image.save(outfile, "PNG")
	