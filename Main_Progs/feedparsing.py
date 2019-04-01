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
from threading import Thread, Lock

#newstest() function takes in three parameters and loops through
#the specified number of headlines. After a certain time interval,
#an email is sent containing the currently found article headlines
#and links.
#parameters:
#feed: the feed to be parsed.
#prefs: the preferences for healines.
#num: the number of desired articles.
#stime: the time when the feed email should be sent (if desired).
#sendTo: the address to send the feed email to (if desired).
#press: the number of times this button has been pressed.
def newsParse(feed, prefs, num, stime, sendTo, press,mutex):
	#clear the console
	clear = lambda: os.system('clear');
	clear();
	#initialize feed components
	d = feedparser.parse(feed)
	hlines = [];
	hlinks = [];
	ohlines = [" "]*num;
	#print feed title
	print("Feed title: " + d['feed']['title'])
	#loop forever, parsing the current feed content
	while True:
		if(mutex.locked()==False):
			hlines = []
			hlinks = []	
			#get the headlines and links,
			#using the specified filters
			#(if there are any).
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
			#print out any headlines
			#that were not part of the
			#previous iteration (print all 
			#if it is the first iteration).
			if hlines != ohlines:
				difflines = diff(hlines,ohlines)
				for word in reversed(difflines):
					print(word)
				ohlines = hlines
			#wait 5 seconds
			time.sleep(5)
			#check the current time. if 
			#it matches the time parameter,
			#and this is the first time
			#this button has been pressed,
			#send an email with the feed
			#information
			ntime = datetime.datetime.now()
			hour = ntime.hour
			if(ntime.hour > 12):
					hour = hour - 12
			if(stime[0] ==  hour and stime[1] == ntime.minute and press == 1):
				press = 10
				email(hlinks,hlines,sendTo)
			#update the feed dictionary
			#for the next iteration
			d = feedparser.parse(feed)


#email() function takes in 3 parameters and
#sends an email containing the appropriate 
#headline and link content.
#parameters:
#hlinks: the list of article links.
#hlines: the list of article titles.
#sendTo: the address to send the 
#email to.
def email(hlinks,hlines,sendTo):
	#initialize gmail smtp server.
	smtp_server = "smtp.gmail.com"
	use_ssl=True
	port = 465
	sender_email = "jakeperlalta99@gmail.com"
	password = "YgKbEoGH325"
	#assemble the email message
	#with the appropriate subject
	#and body.
	message = MIMEMultipart()
	message['Subject'] = "Feed Articles"
	body = ""
	for word1,word2 in zip(hlines,hlinks):
		body += word1.replace(u"\u2019","'") + "\n" + word2 + "\n\n"
	text = MIMEText(body)
	message.attach(text) 
	#send the message
	server = smtplib.SMTP_SSL(smtp_server, port)
	server.login(sender_email, password)
	server.sendmail(sender_email, sendTo, message.as_string())
	server.close()

#compares two lists of headlines
#and returns any headlines
#that are in hlines but not ohlines
#parameters:
#hlines: the new list of article headlines
#ohlines: the old list of article headlines
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
#searches a headline for a 
#specific preference keyword.
#returns the line if the word
#is present, None if it is not
#found.
#parameters:
#prefs: the list of preferences
#line: the line to search through
def newssearch(prefs, line):
	for p in prefs:
		for j, word in enumerate(line):
			if p in word:
				return line
	return "None"

#parses the RSS feed specified by 
#feed, taking into account the 
#words in prefs and the number 
#in days
#parameters:
#feed: the feed url to parse the forecast from
#prefs: the forecast filters specified
#by the user
#days: the number of days to include in the 
#forecast
def weatherParse(feed, prefs,days,mutex):
	#clear the console
	clear = lambda: os.system('clear');
	clear();
	#initialize the feed components
	d = feedparser.parse(feed)
	fcast = []
	ofcast = [] * 2*days
	#loop forever, parsing the 
	#current weather data.
	while True:
		mutex.acquire()
		#Clear list of data from
		#previous iteration.
		fcast = []
		#Append the current weather
		fcast.append("Current weather:")
		fcast.append((d['entries'][0]['description']))
		#loop through the appropriate number of days
		for i in range(0,2*days):
			fcast.append((d['entries'][i+1]['title']))
			forecast = d['entries'][i+1]['description']
			#if there are no preferences, append the forecast.
			#if there are, only append the relevant parts of the 
			#forecast.
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
		
		#if the forecast of this iteration
		#is different than the last, print
		#out the new forecast
		if fcast != ofcast:
			for word in (fcast):
				print(word) + "\n"
			ofcast = fcast
		#sleep five seconds, update feed dictionary
		time.sleep(5)
		d = feedparser.parse(feed)
	
#search through the forecast(line)
#for the words specified in prefs. 
#return the parts of the sentence
#that contain the preference.
#parameters:
#prefs: the list of preferences
#line: the string of the forecast. 
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

#scan through the preferences text file
#starting at line i. based on the feed 
#type, call the appropriate parsing 
#function. 
#parameters:
#i: starting line number.
#press: the number of times the button 
#has been pressed.
def readf(i,press,mutex):
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
					newsParse(feed,prefs,num,time,sendTo,press,mutex)
				if(types == "Weather"):
					weatherParse(feed,prefs,num,mutex)	

#global variables for the number of times 
#each button has been pressed
Apress = 0
Bpress = 0
Cpress = 0
Dpress = 0

mutex1 = Lock();
mutex2 = Lock();
mutex3 = Lock();
mutex4 = Lock();
#function to detect when button a is pressed.
#increment the button variable and then call
#readf function with the appropriate starting 
#line number and button variable value.
#parameters
#button:the button that was pressed.
#pressed:the action that was preformed on the button.
@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
	global Apress
	Apress += 1
	mutex1.acquire(False)
	mutex1.release()
	mutex2.acquire(False)
	mutex3.acquire(False)
	mutex4.acquire(False)
	readf(0,Apress,mutex1)

#function to detect when button a is pressed.
#increment the button variable and then call
#readf function with the appropriate starting 
#line number and button variable value.
#parameters
#button:the button that was pressed.
#pressed:the action that was preformed on the button.
@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
	print("blah")
	global Bpress
	Bpress += 1
	mutex1.acquire(False)
	mutex2.acquire(False)
	mutex2.release()
	mutex3.acquire(False)
	mutex4.acquire(False)
	readf(12,Bpress,mutex2)

#function to detect when button a is pressed.
#increment the button variable and then call
#readf function with the appropriate starting 
#line number and button variable value.
#parameters
#button:the button that was pressed.
#pressed:the action that was preformed on the button.
@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
	global Cpress
	Cpress += 1
	mutex3.acquire(False)
	mutex3.release()
	mutex2 = Lock()
	mutex1 = Lock()
	mutex4 = Lock()
	readf(24,Cpress,mutex3)

#function to detect when button a is pressed.
#increment the button variable and then call
#readf function with the appropriate starting 
#line number and button variable value.
#parameters
#button:the button that was pressed.
#pressed:the action that was preformed on the button.
@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
	global Dpress
	Dpress += 1
	mutex4.acquire(False)
	mutex4.release()
	mutex1 = Lock()
	mutex2 = Lock()
	mutex3 = Lock()
	readf(36,Dpress,mutex4)

#wait initially for the first button to be pressed
signal.pause()
		
