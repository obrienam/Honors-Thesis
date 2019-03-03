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

#args:
#feed, the feed to be parsed.
#prefs, the preferences for healines.
#nums, the range of desired articles.
#newstest() function takes in three parameters and loops through
#the specified number of headlines. After a certain time interval,
#an email is sent containing the currently found article headlines
#and links.
def newstest(feed, prefs, nums):
	clear = lambda: os.system('clear');
	clear();
	start = int(nums[0])
	fin = int(nums[1])
	d = feedparser.parse(feed)
	hlines = [];
	hlinks = [];
	ohlines = [" "]*fin;
	print("Feed title: " + d['feed']['title'])
	timeelapsed = 0
	while True:
		hlines = []
		hlinks = []	
		for i in range(start-1,fin):	
			hline = d['entries'][i]['title']
			hlink = d['entries'][i]['link']
			if prefs[0] == "None":
				hlines.append(hline)
				hlinks.append(hlink)
			else:
				shline = hline.split()
				data = search(prefs, shline)
				if data != "None":
					hlines.append(data)
					hlinks.append(hlink)
		if hlines != ohlines:
			difflines = diff(hlines,ohlines)
			for word in reversed(difflines):
				print(word)
			ohlines = hlines
		time.sleep(5)
		timeelapsed += 15;
		#For the sake of the demo, an email is sent
		#after 60 seconds. Could easily be changed.
		if timeelapsed == 60:
			email(hlinks,hlines)	
		d = feedparser.parse(feed)
#args:
#hlinks, the list of article links.
#hlines, the list of article titles.
#email() function takes in 2 parameters and
#sends an email containing the appropriate 
#headline and link content.
def email(hlinks,hlines):
	smtp_server = "smtp.gmail.com"
	use_ssl=True
	port = 465
	sender_email = "jakeperlalta99@gmail.com"
	password = "YgKbEoGH325"
	message = MIMEMultipart()
	message['Subject'] = "feed links"
	body = ""
	for word1,word2 in zip(hlines,hlinks):
		body += word1.replace(u"\u2019","'") + "\n" + word2 + "\n\n"
	text = MIMEText(body)
	message.attach(text) 
	server = smtplib.SMTP_SSL(smtp_server, port)
	server.login(sender_email, password)
	server.sendmail(sender_email, sender_email, message.as_string())
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

def weathertest(feed, prefs, days):
	d = feedparser.parse(feed)
	while True:
		print("Today")
		print(d['entries'][0]['description'])
		for i in range(0,2*days):
			print(d['entries'][i+1]['title'])
			forecast = d['entries'][i+1]['description']
			if(prefs[0] == "None"):
				print(forecast)
			else:	
				forecasts = forecast.split()
				data = search(prefs, forecasts)
				if data == "None":
					print("No"),
					for word in prefs[:-1]:
						print(word + ", "),
					print(prefs[-1])
				else:
					s = " "
					s = s.join(data)
					print(s)
				if (i+1)%2 == 0:
					print("\n")
		time.sleep(5)
		clear = lambda: os.system('clear')
		clear()

def search(prefs, line):	
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
		

def run():
	types = "init"
	feed = "init"
	prefs = "init"
	num = 0
	with open("preferences.txt") as fp:
		line = "init"
		while line:
			line = fp.readline()
			if(line	== "Feed Type:"):
				types = fp.readline()
			if(line	== "URL:"):
				feed = fp.readline()
			if(line	== "Number of entries:"):
				prefs = fp.readline()
			if(line	== "Content Preferences:"):
				num = fp.readline()
	if(types == "News"):
		newstest(feed,prefs,num)
	if(types == "Weather"):
		newstest(feed,prefs,num)

			
run()
	
