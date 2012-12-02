# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import unicodedata, textwrap

scaleFactor = 3

def drawline(draw, text, font, color, bbox, size, inset, simulate=False, debug=False):
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
		if debug: print "i:",i
		if debug: print "words[i]:",words[i]
		if debug: print 'next line:',line+words[i], (draw.textsize(line+words[i], font)[0]), "<", x1		
		
		if (draw.textsize(line+words[i], font)[0] > (x1-inset)):
			if debug: print 'breaking with line: ',line, "lastWord:",lastWord
			draw.text(((600*3 - linewidth)/2, height), line, font = font, fill = color)
			height += lineheight
			line = words[i]
		else:
			line += words[i]
			
		if lastWord:
			linewidth, lineheight = draw.textsize(line, font)
			draw.text(((600*3 - linewidth)/2, height), line, font = font, fill = color)
			break
						
		i+=1;
		line += " "
		if debug: print ""
		
		
		


def drawtext(draw, text, font, color, bbox, size, simulate=False, debug=False):
	"""Figures out where to draw the words within the bounds of bbox 
	with a given font size. Returns the lowermost y position of the last word"""
	x0, y0, x1, y1 = bbox # note: y1 is ignored
	space = draw.textsize(" ", font)[0]
	words = text.split()
	x = x0; y = y0; h = 0;
	lineCount = 1
	for word in words:
		if debug: print word
		# check size of this word
		w, h = draw.textsize(word, font)
		# figure out where to draw it
		if x > x0:
			x += space
			if x + w > x1:
				# new line
				x = x0
				y += h
				lineCount +=1
				
		if not simulate: 
			draw.text((x, y), word, font=font, fill=color)
		x += w
		
	if debug: print "Line count:", lineCount
	return y + h, lineCount
	

def drawKindleHanzi(characterItems, debug = False):
	"""Draws the hanzi and returns the image"""
	
	character = {"hanzi":characterItems[0],
				"pinyin":characterItems[1],
				"translation":characterItems[2]}
	
	#setup
	kindleWidth = 600*3
	kindleHeight = 800*3
	
	startFontSize = 12
	inset = 50*3

	fontFace = {"hanzi":"resources/华文黑体.ttf", 
				"pinyin":"resources/LinBiolinum_RBah.ttf",
				"translation":"resources/华文黑体.ttf"}
				
	boxHeight = {"hanzi":450*3, 
				"pinyin":100*3,
				"translation":250*3}
				
	textColour = {"hanzi":(0,0,0), 
				"pinyin":(187,187,187),
				"translation":(85,85,85)}
				
	#set up canvas
	image = Image.new("RGBA", (kindleWidth, kindleHeight), "white")
	draw = ImageDraw.Draw(image)

	###############	  HANZI	  ########################
	#determine optimal font size by iterating until the text size is just larger than the criteria
	fontSize = startFontSize
	font = ImageFont.truetype(fontFace["hanzi"], fontSize)
	while font.getsize(character["hanzi"])[0] < (kindleWidth) and font.getsize(character["hanzi"])[1] < (boxHeight["hanzi"]):
		fontSize += 1
		font = ImageFont.truetype(fontFace["hanzi"], fontSize)


	#draw the hanzi
	x = (kindleWidth-font.getsize(character["hanzi"])[0])/2 # center based on character width
	y = 0 #we start at the top
	if debug: draw.rectangle((0,0,kindleWidth,boxHeight["hanzi"]),outline="green")
	if debug: draw.rectangle((x,y,kindleWidth,boxHeight["hanzi"]),outline="red")
	draw.text((x,y), character["hanzi"], textColour["hanzi"], font=font)
	#------------------------------------------------#
	

	###############	  PINYIN   ########################
	#determine optimal font size by iterating until the text size is just larger than the criteria
	fontSize = startFontSize
	font = ImageFont.truetype(fontFace["pinyin"], fontSize)
	while font.getsize(character["pinyin"])[0] < (kindleWidth-inset*2) and font.getsize(character["pinyin"])[1] < (boxHeight["pinyin"]):
		fontSize += 1
		font = ImageFont.truetype(fontFace["pinyin"], fontSize)

	#draw the pinyin
	x = (kindleWidth - font.getsize(character["pinyin"])[0])/2 # center based on pinyin width. No need for inset because that was already taken into account for the pinyin width, now we just need to center!
	y = boxHeight["hanzi"]+inset/2 # we start after the character and a little space
	if debug: draw.rectangle((x, y, kindleWidth, boxHeight["hanzi"]+boxHeight["pinyin"] ), outline="green") #actual box
	if debug: draw.rectangle((inset, y, kindleWidth, boxHeight["hanzi"]+boxHeight["pinyin"] ), outline="red")	#theoretical box
	draw.text((x, y), character["pinyin"], textColour["pinyin"], font=font)
	#------------------------------------------------#

	###############	  TRANSLATION	########################
	#determine optimal font size by filling the allocated box until the last word's x1,y1 position doesn't fit into the box any more, wrapping the text as we go
	
	# the box in which the translation has to fit, including insets
	x0 = 0+inset										#upper left x
	y0 = (boxHeight["hanzi"]+boxHeight["pinyin"]+inset) #upper left y
	x1 = kindleWidth-inset								#lower right x
	y1 = kindleHeight-inset								#lower right y
	translationBox = (x0, y0, x1, y1)

	#iterate to find the right font size
	fontSize = startFontSize
	font = ImageFont.truetype(fontFace["translation"], fontSize)
	translationBoxHeight = 0
	character["translation"] = character["translation"].replace('/','; ')
	
	while translationBoxHeight < y1:
		translationBoxHeight, linecount = drawtext(draw, character["translation"], font, "black", translationBox, size=fontSize, simulate=True, debug=debug)
		if debug: print "text size:",fontSize, "tbox height:",translationBoxHeight
		fontSize += 1
		font = ImageFont.truetype(fontFace["translation"], fontSize)
	# now the know the font size and the line count!
	
	font = ImageFont.truetype(fontFace["translation"], fontSize-2) #why -2? who knows!
	
	#### new
	# if debug: print "total length: ",len(character["translation"])
	# if debug: print "number of lines: ",linecount
	# if debug: print "so at most every line should be this many characters long: ",len(character["translation"])/linecount
	# lines = textwrap.wrap(character["translation"], width = len(character["translation"])/(linecount-1))
	# y_text = y0
	# for line in lines:
	# 	width, height = font.getsize(line)
	# 	draw.text(((kindleWidth - width)/2, y_text), line, font = font, fill = textColour["translation"])
	# 	y_text += height

	
	###
	
	
	if debug: draw.rectangle(translationBox,outline="red")
	if debug: draw.rectangle((0,(boxHeight["hanzi"]+boxHeight["pinyin"]),kindleWidth,(boxHeight["hanzi"]+boxHeight["pinyin"]+boxHeight["translation"])), outline="green")
	
	# draw the translation into the translation box using the right font size determined in the last step
	# drawtext(draw, character["translation"], font, textColour["translation"], translationBox, size=fontSize, simulate=False)
	drawline(draw, character["translation"], font, textColour["translation"], translationBox, size=fontSize, inset=inset, simulate=False, debug=debug)
	#------------------------------------------------#
	
	return image


if __name__ == '__main__':	 
	characterItems = [u"张",u"zhāng",u"pretty/girl/stretch; spread;	 张; expand; open; tes ttest test test last"]
	# characterItems = [u"学",u"xué",u"Learn Chinese simply by looking at your phone!"]
	characterItems = [u'\u5f53', u'd\u0101ng d\xe0ng ', u'to be/to act as/manage/withstand/when/during/ought/should/match equally/equal/same/obstruct/just at (a time or place)/on the spot/right/just at, at or in the very same.../to pawn/suitable/adequate/fitting/proper/replace/represent']

	image = drawKindleHanzi(characterItems, debug = True)
	# image.show()
	
	# outfile = "icon.png"
	# image.save(outfile, "PNG")
	
	img_resized = image.resize((600, 800), Image.ANTIALIAS)
	img_resized.show()
	# img_resized = image
	# img_resized.save(outfile, "PNG")
	