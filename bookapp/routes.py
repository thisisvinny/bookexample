from flask import Flask, render_template
from bookapp import app
import re
from bs4 import BeautifulSoup

@app.route("/")
def index():
	book = open("bookapp/static/data/senseandsensibility.html", "r").read()
	chap_links = get_chap_links(book)
	chapters = []
	for chapter in chap_links:
		chapter = chapter[4:]
		chapters.append(chapter)
	return render_template("home.html", title="Sense and Sensibility", chapters=chapters)

@app.route("/<chap>")
def chapter(chap):
	book = open("bookapp/static/data/senseandsensibility.html", "r").read()
	(chap_links, text) = parse_htmlbook(book)
	chapters = []
	for chapter in chap_links:
		chapter = chapter[4:]
		chapters.append(chapter)

	section = text["chap"+chap]["plist"]
	return render_template("section.html", title="Chapter "+chap, chapters=chapters, thisChap=chap, text=section)

def parse_htmlbook(page):
	links = get_chap_links(page)
	sections = {}
	for ind in range(len(links)):
		section = {}
		start = links[ind]
		if ind < len(links)-1:
			end = links[ind+1]
			patt = ('<A NAME="' + start + '"></A>(?P<sectionbody>.*)<A NAME="' + end + '">')
			match = re.search(patt, page, re.MULTILINE|re.DOTALL)
			if match == None:
				raise Exception('patt: '+patt+'\n\n')
		else:
			patt = ('<A NAME="' + start + '"></A>(?P<sectionbody>.*)<pre>')
			match = re.search(patt, page, re.MULTILINE|re.DOTALL)
		if match:
			soup = BeautifulSoup(match.group("sectionbody"), 'html.parser')
			plist = [p.contents[0] for p in soup.find_all('p')]
			section['title'] = (soup.find('h3').contents)[0]
			section['plist'] = plist
			sections[start] = section
	return links, sections

def get_chap_links(page):
	soup = BeautifulSoup(page, 'html.parser')
	links = [str(link.get('href'))[1:] 
				for link in soup.find_all('a') if link.get('href')]
	return links