# -*- coding: utf-8 -*-
import web
import json
import random

urls = (
		r'/',			'index',
		r'/main/',		'main',
		r'/settings/',	'settings'
)

GridN = 8
g = globals()
g['GridN'] = GridN

app = web.application(urls, globals())
render = web.template.render('templates/', globals = g, base = 'base')


class Char:
	def __init__(self, num, val):
		self.num = num
		self.val = val
		self.word = None

class Word:
	def __init__(self, num, x, y, length):
		self.num = num
		self.x = x
		self.y = y
		self.chars = [None] * length


class index:
	"""shows all functions link"""
	def GET(self):
		return render.index()

def GetAllFromJson():
	charsfile = open('./static/json/characters.json', 'r')
	Chars = json.loads(charsfile.read(), 'gbk')
	
	wordsfile = open('./static/json/phrases.json', 'r')
	Words = json.loads(wordsfile.read(), 'gbk')
	
	settingsfile = open('./static/json/settings.json', 'r')
	settings = json.loads(settingsfile.read())
	
	return Chars, Words, settings

def SetAllToJson(Chars, Words, settings):
	charsfile = open('./static/json/characters.json', 'w')
	charsfile.write(json.dumps(Chars, indent = 4))
	
	wordsfile = open('./static/json/phrases.json', 'w')
	wordsfile.write(json.dumps(Words, indent = 4))
	
	settingsfile = open('./static/json/settings.json', 'w')
	settingsfile.write(json.dumps(settings, indent = 4))


def isempty(x, y, length, chargrid):
	for dy in range(length):
		if chargrid[x][y + dy]:
			return False
	return True

def issame(chars, x, y, chargrid):
	wordlen = len(chars)
	for dy in range(wordlen):
		if chargrid[x][y + dy].num != chars[dy].num:
			return False
	return True

def checkonce(word, chargrid, Chars):
	CharCount = len(Chars)
	
	for i in range(GridN):
		for j in range(GridN - len(word.chars)):
			if (word.x != i or word.y != j) and issame(word.chars, i, j, chargrid):
				while True:
					charnum = random.randrange(0, CharCount)
					if charnum != chargrid[i][j].num:
						break
				chargrid[i][j] = Char(charnum, Chars[charnum])


class main:
	"""shows Chinese character phrase search game"""
	def GET(self):
		Chars, Words, settings = GetAllFromJson()
		
		CharCount = len(Chars)
		WordCount = len(Words)
		ShowCount = settings["showcount"]
		
		chargrid = [[None] * GridN for i in range(GridN)]
		words = [None] * ShowCount
		isnew = [True] * WordCount
		
		for i in range(ShowCount):
			while True:
				wordnum = random.randrange(0, WordCount)
				if isnew[wordnum]:
					break
			
			isnew[wordnum] = False
			# find a place to put word in chargrid
			wordlen = len(Words[wordnum])
			while True:
				x, y = random.randrange(0, GridN), random.randrange(0, GridN - wordlen)
				if isempty(x, y, wordlen, chargrid):
					break
			
			words[i] = Word(wordnum, x, y, wordlen) 
			for j, charval in enumerate(Words[wordnum]):
				charnum = Chars.index(charval)
				words[i].chars[j] = Char(charnum, charval)
				chargrid[x][y + j] = words[i].chars[j]
				words[i].chars[j].word = words[i]
		
		for i in range(GridN):
			for j in range(GridN):
				if not chargrid[i][j]:
					charnum = random.randrange(0, CharCount)
					chargrid[i][j] = Char(charnum, Chars[charnum])
		
		# avoid word to appear twice in chargrid
		for word in words:
			checkonce(word, chargrid, Chars)
		
		return render.main(words, chargrid)


class settings:
	"""allows user to make settings"""
	def GET(self):
		Chars, Words, settings = GetAllFromJson()
		return render.settings(Chars, Words, settings)
	
	def POST(self):
		Chars, Words, settings = GetAllFromJson()
		
		charsStr = web.input(chars = "".join(Chars)).chars
		Chars = list(charsStr)
		
		wordsStr = web.input(words = "\n".join(Words)).words
		Words = wordsStr.split()
		
		# save for settings
		showcountStr = web.input(showcount = settings["showcount"]).showcount
		try:
			showcount = int(showcountStr)
			if 0 < showcount and showcount <= 5:
				settings["showcount"] = showcount
		except:
			pass
		
		# upsidedown is disabled
		# turndown is disabled
		
		SetAllToJson(Chars, Words, settings)
		
		raise web.seeother('/settings/')


if __name__ == '__main__':
	app.run()
