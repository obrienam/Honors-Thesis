import os.path
from pathlib2 import Path
def gatherinfo():
	type = raw_input("Please enter a type of feed (type \"e\" for examples): ")
	if(type == "e"):
		print("Currently supported feed types are:\nWeather\nNews")
		type = raw_input("Please enter one of the above: ")
	if(type == "News"):
		feed = raw_input("Please enter a feed url (type \"e\" for examples): ")
		if(feed == "e"):
			print("Examples of news feeds are:\n" +
			       "Apple News Room: https://www.apple.com/newsroom/rss-feed.rss\n"+
			       "r/news on Reddit: https://www.reddit.com/r/news/.rss\n"+
			       "The New York Times Home Page: http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml\n"+
			       "Top Stories on CNN: http://rss.cnn.com/rss/cnn_topstories.rss")
			feed = raw_input("Please enter a feed url: ")
		num = raw_input("Please enter the number of desired articles: ")
		pref = raw_input("Please enter any headline keywords(Each separated by a space): ")
		prefs = pref.split(" ")
		return type,feed,num,prefs
	if(type == "Weather"):
		feed = raw_input("Please enter a feed url (type \"e\" for examples): ")
		if(feed == "e"):
			print("Examples of weather feed are:\n"+
			      "Boone, NC weather from rssweather: https://www.rssweather.com/zipcode/28607/rss.php")
			feed = raw_input("Please enter a feed url: ")
		days = raw_input("Please enter the number of days for the forecast: ")
		pref = raw_input("Please enter any weather preferences (Each separated by a space): ")
		prefs = pref.split(" ")
		return type,feed,days,prefs
def parsefile(type,feed,num,prefs):
	infile = Path("preferences.txt")
	if infile.exists():
		f = open("preferences.txt", "a")
	else:
		f = open("preferences.txt", "w+")
	f.write("Feed Type:\n%s\n" % type)
	f.write("URL:\n%s\n" % feed)
	f.write("Number of entries:\n%s\n" % num)
	f.write("Content Preferences:\n")
	for pref in prefs:
		f.write("%s " % pref)
	f.write("\n")
	f.close()	
	
def run():
	i = 0
	while (i<4):
		type,feed,num,prefs = gatherinfo()
		parsefile(type,feed,num,prefs)	
		i+=1
run()	
