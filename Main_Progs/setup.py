import os.path
from pathlib2 import Path
#This function asks the user 
#to input their desired
#feed parameters and saves
#their responses in appropriate
#variables.
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
			       "r/technology on Reddit: https://www.reddit.com/r/technology/.rss\n"+
			       "Sports Headlines on Google News: http://news.google.com/news/rss/"+
			       "headlines/section/topic/SPORTS\n")
			feed = raw_input("Please enter a feed url: ")
		num = raw_input("Please enter the number of article to search through: ")
		pref = raw_input("Please enter any headline keywords(Each separated by a space): ")
		prefs = pref.split(" ")
		ansemail = raw_input("Would you like to have articles sent to your email address? (Type y or n): ")
		time = "None"
		sendTo = "None"
		if(ansemail == "y"):
			time = raw_input("Please enter the time you want to receive the email (HH:MM): ")
			sendTo = raw_input("Please enter your email address: ")
		return type,feed,num,prefs,time,sendTo
	if(type == "Weather"):
		feed = raw_input("Please enter a feed url (type \"e\" for examples): ")
		if(feed == "e"):
			print("Examples of weather feed are:\n"+
			      "Boone, NC weather from rssweather: https://www.rssweather.com/zipcode/28607/rss.php"+
			      "Charlotte, NC weather from rssweather: https://www.rssweather.com/zipcode/28210/rss.php")
			feed = raw_input("Please enter a feed url: ")
		days = raw_input("Please enter the number of days for the forecast: ")
		pref = raw_input("Please enter any weather preferences (Each separated by a space): ")
		prefs = pref.split(" ")
		time = "None"
		sendTo = "None"
		return type,feed,days,prefs,time,sendTo
#This function takes the responses
#from gatherinfo and parses them
#into a test file called preferences.txt
def parsefile(type,feed,num,prefs,time,sendTo):
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
	f.write("Time:\n%s\n" % time)
	f.write("SendTo:\n%s\n" % sendTo)
	f.close()		
#This is the runner function that loops four times
#and calles gatherinfo() and parsefile at
#each iteration, transferring the responses 
#between the function.
def run():
	i = 0
	while (i<4):
		type,feed,num,prefs,time,sendTo = gatherinfo()
		parsefile(type,feed,num,prefs,time,sendTo)	
		i+=1
run()	
