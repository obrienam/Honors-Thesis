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
		titles = []
		for i in range(start-1,fin):	
			hline = d['entries'][i]['title']
			hlink = d['entries'][i]['link']
			if prefs[0] == "None":
				hlines.append("Headline: " + hline)
				hlinks.append(hlink)
			else:
				shline = hline.split()
				data = search(prefs, shline)
				if data != "None":
					hlines.append("Headline: " + data)
					hlinks.append(hlink)
		if hlines != ohlines:
			difflines = diff(hlines,ohlines)
			for word in reversed(difflines):
				print(word)
				titles.append(word)	
			ohlines = hlines
		time.sleep(5)
		timeelapsed += 15;
		if timeelapsed == 60:
			email(hlinks)	
		d = feedparser.parse(feed)
def email(hlinks):
	smtp_server = "smtp.gmail.com"
	use_ssl=True
	port = 465
	sender_email = "jakeperlalta99@gmail.com"
	password = "YgKbEoGH325"
	message = MIMEMultipart()
	message['Subject'] = "feed links"
	body = ""
	for word in reversed(hlinks):	
		body += (word + "\n\n")
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
				print(data)
				if (i+1)%2 == 0:
					print("\n")
		time.sleep(5)
		clear = lambda: os.system('clear')
		clear()

def search(prefs, line):	
	for p in prefs:
		for j, word in enumerate(line):
			if ((p == "high") and (word == "high")) or ((p == "low") and (word == "low")):
					return line[j] +  " " + line[j+1] + " " + line[j+2]
			elif p in word:
				return line
	return "None"

def ask():
	type = raw_input("What type of feed do you want to run?: ")
	feed = raw_input("Please enter a feed url: ")
	if(type == "news"):
		num = raw_input("Please enter the range of entries: ")
		nums = num.split(" ")
		pref = raw_input("Please enter any headline preferences: ")
		prefs = pref.split(" ")
		newstest(feed, prefs, nums)
	if(type == "weather"):
		days = raw_input("Please enter the number of days for the forecast: ")
		pref = raw_input("Please enter any data prefences (separated by a space): ")
		prefs = pref.split(" ")
		weathertest(feed, prefs, int(days))
	return

ask()
	
