import praw
from datetime import datetime
import configparser
import logging as log

now = datetime.now()
timestamp = datetime.timestamp(now)
timeMinusOneDay = timestamp-(24*60*60)



LOG_FILENAME = "/home/pi/crosspostbot/log_crossbot.txt"


___debug___ = True
___runprod___= False

if ___debug___ == True:
	log.basicConfig(filename=LOG_FILENAME,level=log.INFO,format='%(asctime)s : %(levelname)s : %(message)s')


def work():
	log.info("Lastrun of the script")
	
	config = configparser.ConfigParser()
	config.read('/home/pi/crosspostbot/config.ini')
	
	_reddituser = config['DEFAULT']['_reddituser']
	_subtocrosspost = config['DEFAULT']['_subtocrosspost']
	_triggerwords =config['DEFAULT']['_triggerwords']
	
	try:
		_UA = 'crossbot by /u/['+_reddituser+']'
		reddit = praw.Reddit("bot1",user_agent=_UA)
		reddit.validate_on_submit=True	
		
		result= reddit.redditor(_reddituser).comments.new(limit=None)
		
		for comment in result:
			log.info("comment found id: {}".format(comment.id))
		
			if comment.created_utc >= timeMinusOneDay:
				if comment.body.strip().lower() in _triggerwords:
					log.info("Trigger found: {}".format(str(comment.body.split("\n", 1)[0][:79])))
					log.info("parent_id: {} comment_id: {}".format(comment.parent_id,comment))
					
					
					if ___runprod___ == True:
						submission = reddit.submission(id=comment.parent_id.replace('t3_',''))
						cross_post = submission.crosspost(subreddit=_subtocrosspost,send_replies=False)
						
						edited_body = comment.body + "."
						comment.edit(edited_body)
						log.info("run IN Production")
					else:
						log.info("run NOT IN Production")
			else:
				log.info("exit script")
				exit()
	except Exception as err:
		log.info("Error: {}".format(str(err)))

	
work()



	
	

	
	
	
	