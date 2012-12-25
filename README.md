# What is this?
This generates beautiful Chinese characters to be used as screensaver on your e-Ink Kindles. Please have a look at [http://px0.de/chinese-kindle-screensaver/](http://px0.de/chinese-kindle-screensaver/) for more information and instructions on how to install the files on your Kindle.

# What's in there and how do I use it?
+ **getMostFreqChars.py** - takes a Chinese character frequency list, extracts a certain subset of it, and performs a couple of assorted operations (such as turning numerated pinyin into pinyin with diacritics). Currently, it is pretty inflexible and insists on using [Jun Da's frequency list](http://lingua.mtsu.edu/chinese-computing/statistics/), but it can be easily adapted if you have something different in mind
+ **createScreensaverImage.py** - actually draws the character in a way that I think is pretty. You're welcome to disagree and fork this!
+ **generateKindleScreensaverImages.py** - the main program, which does little more than call the other two programs and store their output.

Each of these files can run by itself and give you an idea on what to expect.

# Why doesn't it work?
I'm using a font called "华文黑体.ttf" to draw the character and translation. I'm not sure what its copyright is so I am not putting it up here. If you have it, just drop it into the 'resources' folder and everything should run. If you don't, choose another Chinese character font (that also includes roman letters), put into into the 'resources' folder and adapt *createScreensaverImage.py*.

# Attributions
The character frequency list on which this is based is the excellent work of [Jun Da](http://lingua.mtsu.edu/chinese-computing/statistics/). The translations and pinyin are taken from from wonderful [CC-EDICT](http://www.mdbg.net/chindict/chindict.php?page=cedict) and set in the beautiful [Linux Libertine](http://www.linuxlibertine.org/) font.

#Output examples
## Sample output file
![Sample output file](http://px0.de/wp-content/uploads/2012/12/14.png)

## On an actual device
![Output example on actual device](http://px0.de/wp-content/uploads/2012/12/sheng1.png)