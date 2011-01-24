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

class index:
	"""shows all functions link"""
	def GET(self):
		return render.index()


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
		
		chnum = [[None] * GridN for i in range(GridN)]
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
				chnum[i][j] = random.randrange(0, NumChar)
				chars[i][j] = Chars[chnum[i][j]]
		
		return render.main(phrases, chars, chnum)


class setting:
	"""allows user to make settings"""
	def GET(self):
		return render.setting()
	
	def POST(self):
		return render.setting()


if __name__ == '__main__':
	app.run()
