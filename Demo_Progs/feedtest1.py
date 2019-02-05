import feedparser
import time
import threading
import os
def newstest(feed, start, fin):
	while True:
		d = feedparser.parse(feed)
		print "Feed title: " + d['feed']['title']
		for i in range(start,fin+1):
			print "Headline " + str(i) + ": " + d['entries'][i]['title']
		time.sleep(5)
		clear = lambda: os.system('clear')
		clear()		

def weathertest(feed, spot):
	d = feedparser.parse(feed)
	print "Feed title: " + d['channel']['title']
def ask():
	type = raw_input("What type of feed do you want to run?: ")
	feed = raw_input("Please enter a feed url: ")
	num = raw_input("Please enter the range of entries: ")
	nums = num.split(" ")
	if(type == "news"):
		newstest(feed, int(nums[0]), int(nums[1]))
	return

ask()
	
