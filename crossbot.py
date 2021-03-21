#!/usr/bin/python3
__author__ = "u/wontfixit"
__license__ = "GPL"
__version__ = "1.0.2"


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
_RUNPROD= True
#days the script will look bakwards in time
_DAYS = 2
#calculate new timestamp
timeMinusDays = timestamp-(24*60*60*_DAYS)
#must be set like cronjob
#cronjob all 15 mins = 60*15
timeMinusX = timestamp-(60*15)

#########!!!!!!!!!!!!!!!!#####################
#Change your path
#_LOCALPATH = "/home/pi/"

if _RUNPROD == True:
	#path too logfile (if run via crontab, path must be absolut)
	_LOG_FILENAME = "log_crossbot.log"
	#config file path
	_CONFIG_FILE = "config.ini"
else:
	#path too logfile (if run via crontab, path must be absolut)
	_LOG_FILENAME = "log_crossbot.log"
	#config file path
	_CONFIG_FILE = "config.ini"


if _DEBUG == True:
	log.basicConfig( handlers=[
            log.FileHandler(_LOG_FILENAME),
            log.StreamHandler()],level=log.INFO,format='%(asctime)s ; %(levelname)s ; %(funcName)s() ; %(message)s')

def words_in_string(word_list, a_string):
    return set(word_list).intersection(a_string.split())

def  readConfig():
	log.info("Try to read config")
	try:
		config = configparser.ConfigParser()
		config.read(_CONFIG_FILE)

		_reddituser = config['DEFAULT']['_reddituser']
		_subtocrosspost = config['DEFAULT']['_subtocrosspost']
		_subsource = config['DEFAULT']['_subsource']
		_triggerwordscomments =config['DEFAULT']['_triggerwordscomments'].split(',')
		_triggerwordstitle = config['DEFAULT']['_triggerwordstitle'].split(',')
		_flair_1 =config['DEFAULT']['_flair_1']

		_monitorByRedditusername =  config['DEFAULT']['_monitorByRedditusername']
		_monitorBytriggerwordscomments =  config['DEFAULT']['_monitorBytriggerwordscomments']
		_monitorBytriggerwordstitle =  config['DEFAULT']['_monitorBytriggerwordstitle']
		_monitorByflair =  config['DEFAULT']['_monitorByflair']
		log.info("config successfully read")

	except Exception as err:
		log.error("Reading config didn't work {}".format(str(err)))
		exit()


def main():
	log.info("Lastrun of the script")
	########################################### Here! last work
	conf = readConfig()

	log.info("Script will listen to r/{}".format(_subsource))

	try:
		_UA = 'crossbot by /u/['+_reddituser+']'
		reddit = praw.Reddit("bot2",user_agent=_UA)
		reddit.validate_on_submit=True

	except Exception as err:
		log.error("reddit connection: {}".format(str(err)))

	try:
		#you can fetch mulitple reddits at the same time, just got to the *.ini and write the subreddits name together with + between the names
		#example: mysteryobject+cats+redditdev+requestabot
		submissions = reddit.subreddit(_subsource).top("all",limit=None)

		#just make some pretty time out of the delta timestamp
		prettytime = datetime.utcfromtimestamp(timeMinusX).strftime('%Y-%m-%d %H:%M:%S')
		log.info("Submission in timerange {}".format(prettytime))
		log.info("")

		i=0
		j=0
		for submission in submissions:
			tmptitle = submission.title.lower().strip()
			i +=1
			if submission.created_utc >= timeMinusX:
				j+=1
				log.info("Try: \"{}\" in \"{}\" for ID:{}".format(_triggerwordstitle,tmptitle,submission.id))

				if words_in_string(_triggerwordstitle, tmptitle):
					log.info("---Trigger found \"{}\" in \"{}\" for ID:{}".format(_triggerwordstitle,tmptitle,submission.id))

					if _RUNPROD == True:
						try:
							cross_post = submission.crosspost(subreddit=_subtocrosspost)
							#add some flair to the submission
							cross_post.flair.select(_flair_1)
							#make the submission sticky
							cross_post.mod.sticky()
							log.info("Crosspost seems to worked, new ID:{}".format(cross_post))
						except Exception as err:
							log.error("Crosspost didn't work for ID:{}, {}".format(submission.id,str(err)))
					else:
						log.info("running NOT IN production, no changes were made.")
		log.info("")
		log.info("{} submissions found and {} were in the timerange".format(i,j))



	except Exception as err:
		log.error("getting submissions: {}".format(str(err)))

if __name__ == '__main__':
	main()
