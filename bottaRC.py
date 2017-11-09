# -*- coding: utf-8 -*-
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from telegraphapi import Telegraph
import telegram
import json
import re


telegraph = Telegraph()
telegraph.createAccount("PythonTelegraphAPI")
TOKEN_TELEGRAM = '473217650:AAHZdhxYfDDpbQr7X7qth9d3vXO73w7YHmM' #RcalcolatoBot
MY_CHAT_ID_TELEGRAM = 31923577
bot = telegram.Bot(TOKEN_TELEGRAM)

url = 'https://www.rischiocalcolato.it/2017/11/non-esiste-un-partito-dellastensione-la-gente-non-bisogno-organizzarsi-mandarli-affanculo.html'

req = urllib.request.Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
f = urllib.request.urlopen(req)
wholeHTML = str(f.read())
bsObjCOMMENTS_TEXT = BeautifulSoup( wholeHTML, "html.parser").findAll("div", {"class" : "dsq-comment-message"})
bsObjCOMMENTS_AUTHOR = BeautifulSoup( wholeHTML, "html.parser").findAll("cite")
i = 0
textCOMMENTS = ""

for comment in bsObjCOMMENTS_AUTHOR:
	author = comment.text
	#print(author)
	commentText = bsObjCOMMENTS_TEXT[i].text
	textCOMMENTS = textCOMMENTS + "<b>{}</b><code>{}</code>\n\n".format(author, commentText)
	i = i+1
numComments = len(bsObjCOMMENTS_TEXT)
textCOMMENTS = "Ci sono {} commenti.\n\n".format( numComments ) + textCOMMENTS
string = r'''<p><strong>Sono Mauro Bottarelli, Seguimi su Twitter!</strong> <a href="https://twitter.com/maurobottarelli" class="extlink" data-show-count="false" data-size="large" data-wpel-link="external" rel="external noopener noreferrer">Follow @maurobottarelli</a>'''
html = wholeHTML.split(string)[0]
title = BeautifulSoup(html, "html.parser").findAll("div", {"class":"post-container"})[0].findAll("h1")[0].text 
#print(title)
bsObj = BeautifulSoup(html, "html.parser").findAll("div", {"class":"post-container"})[0].findAll("p")

text = ""
author = "Mauro Bottarelli"
text = str( bsObj[0] )
def prettify(text):
	text = text.replace("\\n","\n")
	text = text.replace("\\xc3\\xa8","è")
	text = text.replace("\\xc3\\xa9","è")
	text = text.replace("\\xc3\\xa0","à")
	text = text.replace("\\xc3\\xb9","ù")
	text = text.replace("\\xc3\\xb2","ò")
	text = text.replace("\\xc3\\xac","ì")
	text = text.replace("<br />","\n")
	return text

text = prettify(text)
title = prettify(title)
textCOMMENTS = prettify(textCOMMENTS)
#print(text)

i = 0
bsObjNOSCRIPT = BeautifulSoup(text, "html.parser").findAll("noscript")
for noscript in bsObjNOSCRIPT:
	urlMEDIA = noscript.a['href']
	#print(urlMEDIA)
	if "https://youtu" in urlMEDIA:
		urlYT = urlMEDIA.split("/")[-1]
	STR = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" frameborder="0" allowfullscreen></iframe>'.format(urlYT)
	text = text.replace( str(bsObjNOSCRIPT[i]), STR )
	i = i+1

print()


i = 0
'''
bsObjDIV = BeautifulSoup(text, "html.parser").findAll("div")
for div in bsObjDIV:
	text = text.replace( str(div), '' )
	i = i+1
'''

i = 0
bsObjMETA = BeautifulSoup(text, "html.parser").findAll("meta")
for meta in bsObjMETA:
	text = text.replace( str(meta), '' )
	i = i+1

i = 0
bsObjIFRAME = BeautifulSoup(text, "html.parser").findAll("iframe")
for iframe in bsObjIFRAME:
	urlMEDIA = iframe['src']
	if "facebook.com" in urlMEDIA: 
		reqFB = urllib.request.Request(urlMEDIA, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
		f_FB = urllib.request.urlopen(reqFB)
		wholeHTMLFB = str(f_FB.read())
		FBimg = BeautifulSoup( wholeHTMLFB, "html.parser").findAll("img")[0]["src"]
		FIGCAPTION = '<center><p><a href="{}">Guarda il video</a></p></center>'.format(urlMEDIA)
		STR = '''<figure>
		          <a href="{}"> <img src="{}" /> </a>
		          <figcaption>{}</figcaption>
		          </figure>'''.format(urlMEDIA, FBimg, FIGCAPTION) + "\n" + FIGCAPTION
	else:
		STR = '<a href="{}">[LINK]</a>'.format(urlMEDIA)
	text = text.replace( str(bsObjIFRAME[i]), STR )
	i = i+1
	
i = 0
bsObjIMG = BeautifulSoup(text, "html.parser").findAll("img")
listIMG = [ i['src'] for i in bsObjIMG ]
for IMG in listIMG:
	STR = '<a href="{}"> <img src="{}" />  </a>'.format(IMG,IMG)
	text = text.replace( str(bsObjIMG[i]), STR )
	i = i+1

text = text.replace("Watch this video on YouTube","")
text = text.replace("</div>","")
text = text.replace("&gt;","")

text = text + '\n<b>Sono Mauro Bottarelli, Seguimi su Twitter! <a href="{}">Follow @maurobottarelli</a></b>\n\n'.format("https://twitter.com/maurobottarelli")

from html_telegraph_poster import upload_to_telegraph

url2sendCOMMENTS = upload_to_telegraph(title="COMMENTI A " + title, author='Disqus', text=textCOMMENTS)["url"]
#print(url2send)
text = text +  '<br />\n\n<p>Leggi tutti i {} <a href="{}">commenti</a> su Disqus.</p>'.format(numComments, url2sendCOMMENTS)
url2send = upload_to_telegraph(title=title, author='Mauro Bottarelli', text=text)["url"]
text2send = '<a href="{}">{}</a>\n{}'.format(url2send,title,  u"\u2063")
bot.sendMessage(parse_mode = "Html", text = text2send, chat_id=MY_CHAT_ID_TELEGRAM)



f = open("text","w")
f.write(text)
f.close()