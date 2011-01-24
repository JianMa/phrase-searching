# -*- coding: utf-8 -*-
import web
import json
import random

urls = (
		r'/',			'index',
		r'/main/',		'main',
		r'/setting/',	'setting'
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


class index:
	"""shows all functions link"""
	def GET(self):
		return render.index()


class main:
	"""shows Chinese character phrase search game"""
	def GET(self):
		charsfile = open('./static/json/characters.json', 'r').read()
		Chars = json.loads(charsfile, 'gbk')
		CountChar = len(Chars)
		
		wordsfile = open('./static/json/phrases.json', 'r').read()
		Words = json.loads(wordsfile, 'gbk')
		CountWord = len(Words)
		CountShow = 3
		
		chargrid = [[None] * GridN for i in range(GridN)]
		words = [None] * CountShow
		used = [False] * CountWord
		
		for i in range(CountShow):
			wordnum = random.randrange(0, CountWord)
			while used[wordnum]:
				wordnum = random.randrange(0, CountWord)
			else:
				used[wordnum] = True
				words[i] = [None] * len(Words[wordnum])
				for j, charval in enumerate(Words[wordnum]):
					charnum = Chars.index(charval)
					words[i][j] = Char(charnum, charval)
		
		for i in range(GridN):
			for j in range(GridN):
				charnum = random.randrange(0, CountChar)
				chargrid[i][j] = Char(charnum, Chars[charnum])
		
		return render.main(words, chargrid)


class setting:
	"""allows user to make settings"""
	def GET(self):
		return render.setting()
	
	def POST(self):
		return render.setting()


if __name__ == '__main__':
	app.run()
