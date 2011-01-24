# -*- coding: utf-8 -*-
import web
import json
import random

urls = (
		r'/',			'index',
		r'/main/',		'main'
)

g = globals()
app = web.application(urls, globals())
render = web.template.render('templates/', globals = g, base = 'base')

class index:
	"""shows all functions link"""
	def GET(self):
		return render.index()

GridN = 8
g['GridN'] = GridN

class main:
	"""shows Chinese character phrase search game"""
	def GET(self):
		charsfile = open('./static/json/characters.json', 'r').read()
		Chars = json.loads(charsfile, 'gbk')
		NumChar = len(Chars)
		
		phrasesfile = open('./static/json/phrases.json', 'r').read()
		Phrases = json.loads(phrasesfile, 'gbk')
		NumPhrase = len(Phrases)
		numShow = 3
		
		chars = [[None] * GridN for i in range(GridN)]
		phrases = [None] * numShow
		used = [False] * NumPhrase
		
		for i in range(numShow):
			selectNum = random.randrange(0, NumPhrase)
			while used[selectNum]:
				selectNum = random.randrange(0, NumPhrase)
			else:
				used[selectNum] = True
				phrases[i] = Phrases[selectNum]
		
		for i in range(GridN):
			for j in range(GridN):
				chars[i][j] = Chars[random.randrange(0, NumChar)]
		
		return render.main(phrases, chars)

if __name__ == '__main__':
	app.run()
