import praw
from datetime import datetime
import configparser
import logging as log

now = datetime.now()
timestamp = datetime.timestamp(now)
timeMinusOneDay = timestamp-(24*60*60)



LOG_FILENAME = "./log_crossbot.txt"


___debug___ = True

if ___debug___ == True:
	log.basicConfig(filename=LOG_FILENAME,level=log.INFO,format='%(message)s')


def work():
	log.info("{} Lastrun".format(now))
	
	config = configparser.ConfigParser()
	config.read('config.ini')
	
	_reddituser = config['DEFAULT']['_reddituser']
	_subtocrosspost = config['DEFAULT']['_subtocrosspost']
	_triggerwords =config['DEFAULT']['_triggerwords']
	
	_UA = 'crossbot by /u/['+_reddituser+']'
	reddit = praw.Reddit("bot1",user_agent=_UA)
	reddit.validate_on_submit=True	

	for comment in reddit.redditor(_reddituser).comments.new(limit=None):

	
		if comment.created_utc >= timeMinusOneDay:
			if comment.body.strip().lower() in _triggerwords:
				log.info("{} Trigger found: {}".format(now,str(comment.body.split("\n", 1)[0][:79])))
				log.info("{} parent_id: {}".format(now,comment.parent_id))
				
				
				
				submission = reddit.submission(id=comment.parent_id.replace('t3_',''))
				
				cross_post = submission.crosspost(subreddit=_subtocrosspost,send_replies=False)
				

				edited_body = comment.body + "."
				comment.edit(edited_body)
		else:
			
			exit()

	
work()



	
	

	
	
	
	