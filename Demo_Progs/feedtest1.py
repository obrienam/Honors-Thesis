import feedparser
def newstest(feed, spot):
	d = feedparser.parse(feed)
	print "Feed title: " + d['feed']['title']
	print "Number of articles: " + str(len(d['entries']))
	print "Title one: " + d['entries'][spot]['title']
	body = "Body: " + d['entries'][spot]['description']
	body = "\n".join(body.split("<br />"))
	print body
	return

def ask():
	feed = raw_input("Please enter a feed url: ")
	spot = int(raw_input("Please enter a article number: "))
	newstest(feed, spot-1)
	return

ask()
	
