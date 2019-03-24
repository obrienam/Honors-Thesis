#coding: utf-8
import feedparser
import time
import threading
import os
import smtplib, ssl
import email
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from contextlib import contextmanager
import buttonshim
import signal
import datetime
#args:
#feed, the feed to be parsed.
#prefs, the preferences for healines.
#nums, the range of desired articles.
#newstest() function takes in three parameters and loops through
#the specified number of headlines. After a certain time interval,
#an email is sent containing the currently found article headlines
#and links.
def newsParse(feed, prefs, num, stime, sendTo, press):
	clear = lambda: os.system('clear');
	clear();
	d = feedparser.parse(feed)
	hlines = [];
	hlinks = [];
	ohlines = [" "]*num;
	print("Feed title: " + d['feed']['title'])
	while True:
		hlines = []
		hlinks = []	
		for i in range(0,num):	
			hline = d['entries'][i]['title']
			hlink = d['entries'][i]['link']
			if prefs[0] == "None":
				hlines.append(hline)
				hlinks.append(hlink)
			else:
				shline = hline.split()
				data = newssearch(prefs, shline)
				if data != "None":
					hlines.append(hline)
					hlinks.append(hlink)
		if hlines != ohlines:
			difflines = diff(hlines,ohlines)
			for word in reversed(difflines):
				print(word)
			ohlines = hlines
		#print(press)
		time.sleep(5)
		ntime = datetime.datetime.now()
		hour = ntime.hour
		if(ntime.hour > 12):
			hour = hour - 12
		if(stime[0] ==  hour and stime[1] == ntime.minute and press == 1):
			press = 10
			email(hlinks,hlines,sendTo)
		d = feedparser.parse(feed)

#args:
#hlinks, the list of article links.
#hlines, the list of article titles.
#email() function takes in 2 parameters and
#sends an email containing the appropriate 
#headline and link content.
def email(hlinks,hlines,sendTo):
	smtp_server = "smtp.gmail.com"
	use_ssl=True
	port = 465
	sender_email = "jakeperlalta99@gmail.com"
	password = "YgKbEoGH325"
	message = MIMEMultipart()
	message['Subject'] = "Feed Articles"
	body = ""
	for word1,word2 in zip(hlines,hlinks):
		body += word1.replace(u"\u2019","'") + "\n" + word2 + "\n\n"
	text = MIMEText(body)
	message.attach(text) 
	server = smtplib.SMTP_SSL(smtp_server, port)
	server.login(sender_email, password)
	server.sendmail(sender_email, sendTo, message.as_string())
	server.close()

def diff(hlines,ohlines):
	difflines = []
	found = False
	for i in range(0,len(hlines)):
		for j in range(0,len(ohlines)):
			if hlines[i] == ohlines[j]:
				found = True
				break
		if found == False:
			difflines.append(hlines[i]);
	return difflines
	
def newssearch(prefs, line):
	for p in prefs:
		for j, word in enumerate(line):
			if p in word:
				return line
	return "None"

def weatherParse(feed, prefs, days):
	clear = lambda: os.system('clear');
	clear();
	d = feedparser.parse(feed)
	fcast = []
	ofcast = [] * 2*days
	while True:
		fcast = []
		fcast.append("Current weather:")
		fcast.append((d['entries'][0]['description']))
		for i in range(0,2*days):
			fcast.append((d['entries'][i+1]['title']))
			forecast = d['entries'][i+1]['description']
			if(prefs[0] == "None"):
				fcast.append(forecast)
			else:	
				forecasts = forecast.split()
				data = weathersearch(prefs, forecasts)
				if data == "None":
					print("No"),
					for word in prefs[:-1]:
						fcast.append(word + ", ")
					fcast.append(prefs[-1])
				else:
					s = " "
					s = s.join(data)
					fcast.append(s)
		if fcast != ofcast:
			#difflines = diff(fcast, ofcast)
			for word in (fcast):
				print(word) + "\n"
			ofcast = fcast			
		time.sleep(5)
		d = feedparser.parse(feed)
def weathersearch(prefs, line):	
	s = " "
	s = s.join(line)
	sall = []
        for p in prefs:
		for sentence in s.split('.'):
			if p.lower() in sentence or p.capitalize() in sentence:
				sall.append(sentence + ".")
	if len(sall) == 0:
		return "None"
	return sall
		
def readf(i,press):
	types = "init"
	feed = "init"
	prefs = []
	num = 0
	time = [0]*2
	sendTo = "None"
	with open("preferences.txt") as fp:
		for j in range(0,i):
			fp.readline()
		line = "init"
		while line:
			line = fp.readline()
			if(line	== "Feed Type:\n"):
				types = fp.readline().rstrip()
			if(line	== "URL:\n"):
				feed = fp.readline().rstrip()
			if(line	== "Number of entries:\n"):
				num = int(fp.readline().rstrip())
			if(line	== "Content Preferences:\n"):
				prefs = fp.readline().split()
			if(line == "Time:\n"):
				times = fp.readline().split(':')
				if(times[0] != "None\n"):
					time[0] = int(times[0])
					time[1] = int(times[1])
			if(line == "SendTo:\n"):
				sendTo = fp.readline().rstrip()
				if(types == "News"):
					newsParse(feed,prefs,num,time,sendTo,press)
				if(types == "Weather"):
					weatherParse(feed,prefs,num)	

Apress = 0
Bpress = 0
Cpress = 0
Dpress = 0

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
	global Apress
	Apress += 1
	readf(0,Apress)

@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
	global Bpress
	Bpress += 1 
	readf(12,Bpress)

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
	global Cpress
	Cpress += 1
	readf(24,Cpress)

@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
	global Dpress
	Dpress += 1
	readf(36,Dpress)
signal.pause()
		
