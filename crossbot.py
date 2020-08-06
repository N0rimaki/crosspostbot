#!/usr/bin/python3
__author__ = "u/wontfixit"
__license__ = "GPL"
__version__ = "1.0.0"


import praw
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
timeMinusOneDay = timestamp-(24*60*60*_DAYS)


if _RUNPROD == True:
	#path too logfile (if run via crontab, path must be absolut)
	_LOG_FILENAME = "/home/pi/crosspostbot/log_crossbot.log"
	#config file path
	_CONFIG_FILE = "/home/pi/crosspostbot/config.ini"
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
		_triggerwordscomments =config['DEFAULT']['_triggerwordscomments']
		
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
		result= reddit.redditor(_reddituser).comments.new(limit=None)
		
		for comment in result:
			parent_id = comment.submission.id
			log.info("comment found Pid: {} Cid:{}, no trigger".format(parent_id,comment.id))
		
			if comment.created_utc >= timeMinusOneDay:
				if comment.body.strip().lower() in _triggerwordscomments:
					log.info("Trigger found: {}".format(str(comment.body.split("\n", 1)[0][:79])))
	
					
					if _RUNPROD == True:
						submission = reddit.submission(id=parent_id.replace('t3_',''))
						cross_post = submission.crosspost(subreddit=_subtocrosspost,send_replies=False)
						
						edited_body = comment.body + "."
						comment.edit(edited_body)
						
					else:
						log.info("run NOT IN Production")
			else:
				log.info("finished and exit script")
				exit()
				
	except Exception as err:
		log.error("getting comments: {}".format(str(err)))

if __name__ == '__main__':	
	main()



	
	

	
	
	
	