#!/usr/bin/python3
__author__ = "u/wontfixit"
__license__ = "GPL"
__version__ = "1.0.1"


import praw
import re
from datetime import datetime
import configparser
import logging as log
now = datetime.now()
timestamp = datetime.timestamp(now)


#enable logging
_DEBUG = True
#will write changes to PROD if True
_RUNPROD= False
#days the script will look bakwards in time
_DAYS = 2
#calculate new timestamp
timeMinusDays = timestamp-(24*60*60*_DAYS)
#must be set like cronjob 
#cronjob all 15 mins = 60*15
timeMinusX = timestamp-(60*1)

#add flair id from reddit
_flair_1 = "882c5aa6-c926-11ea-a888-0e38155ddc41"

#########!!!!!!!!!!!!!!!!#####################
#Change your path
_LOCALPATH = "/home/pi/crosspostbot/"

if _RUNPROD == True:
	#path too logfile (if run via crontab, path must be absolut)
	_LOG_FILENAME = _LOCALPATH+"log_crossbot.log"
	#config file path
	_CONFIG_FILE = _LOCALPATH+"config.ini"
else:
	#path too logfile (if run via crontab, path must be absolut)
	_LOG_FILENAME = "log_crossbot.log"
	#config file path
	_CONFIG_FILE = "config.ini"	


if _DEBUG == True:
	log.basicConfig( handlers=[
            log.FileHandler(_LOG_FILENAME),
            log.StreamHandler()],level=log.INFO,format='%(asctime)s ; %(levelname)s ; %(funcName)s() ; %(message)s')




def main():
	log.info("Lastrun of the script")
	try:
		config = configparser.ConfigParser()
		config.read(_CONFIG_FILE)
		
		_reddituser = config['DEFAULT']['_reddituser']
		_subtocrosspost = config['DEFAULT']['_subtocrosspost']
		_subsource = config['DEFAULT']['_subsource']
		_triggerwordscomments =config['DEFAULT']['_triggerwordscomments']
		_triggerwordstitle =config['DEFAULT']['_triggerwordstitle']
		
	except Exception as err:
		log.error("Reading config didn't work {}".format(str(err)))
		exit()
	
	log.info("Script will listen to r/{}".format(_subtocrosspost))	
		
	try:
		_UA = 'crossbot by /u/['+_reddituser+']'
		reddit = praw.Reddit("bot1",user_agent=_UA)
		reddit.validate_on_submit=True	
		
		
	except Exception as err:
		log.error("reddit connection: {}".format(str(err)))
		
	try:	
		#you can fetch mulitple reddits at the same time, just got to the *.ini and write the subreddits name together with + between the names
		#example: mysteryobject+cats+redditdev+requestabot
		submissions = reddit.subreddit(_subsource).top("all",limit=None)
		prettytime = datetime.utcfromtimestamp(timeMinusX).strftime('%Y-%m-%d %H:%M:%S')

		i=0
		j=0
		for submission in submissions:
			tmptitle = submission.title.lower().strip()
			i +=1
			
			if submission.created_utc >= timeMinusX:
				j+=1
				log.info("rSubmission in timerange {}".format(prettytime))
				
				if re.compile('|'.join(_triggerwordstitle),re.IGNORECASE).search(tmptitle):
					log.info("Trigger found {} in {} for id {}\r\n".format(_triggerwordstitle,tmptitle,submission.id))
			
					if _RUNPROD == True:
						try:
							submission = reddit.submission(id=submission.id.replace('t3_',''))
							cross_post = submission.crosspost(subreddit=_subtocrosspost,send_replies=False)
							#add some flair to the submission
							submission.flair.select(_flair_1)
							#make the submission sticky and distinguish as mod
							submission.mod.distinguish(how="yes", sticky=True)
						except Exception as err:
							log.error("Crosspost didn't work for {}, {}".format(submission.id,str(err)))
					else:
						log.info("run NOT IN Production")
		log.info("{} Submissions found and {} in the timerange".format(i,j))	
				
				
				
	except Exception as err:
		log.error("getting comments: {}".format(str(err)))

if __name__ == '__main__':	
	main()

	

	
	
	
	