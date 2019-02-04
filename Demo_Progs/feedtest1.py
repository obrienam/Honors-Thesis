import feedparser
import time
def newstest(feed, spot):
	d = feedparser.parse(feed)
	choice = ""
	while choice != "quit":
		print "starting"
		print "Feed title: " + d['feed']['title']
		arts = len(d['entries'])
		for i in range(0,arts):
			print "Article " + str(i+1) + ": " + d['entries'][i]['title']
			time.sleep(5)
		choice = raw_input("Go again?")

def weathertest(feed, spot):
	d = feedparser.parse(feed)
	print "Feed title: " + d['channel']['title']
def ask():
	feed = raw_input("Please enter a feed url: ")
	spot = int(raw_input("Please enter a article number: "))
	newstest(feed, spot-1)
	return

ask()
	
