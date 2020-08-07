# crosspostbot - branch for crosspost triggered by title

crosspost submission when the title contains some trigger words `_triggerwordstitle`.
The script can be setupt to runs every 15mins (crontab) and collect the submissions of the last `timeMinusX` in seconds. 60*5 = last 5 minutes
The crontab time should be the same as `timeMinusX`, because the bot would crosspost already posted stuff again. (Database will come)
When a trigger word is found, the submission will be crossposted to another sub `_subtocrosspost`.
You can fetch mulitple reddits at the same time, just got to the config.ini and write the subreddits name together with + between the names into `_subsource`
example: mysteryobject+cats+redditdev+requestabot

<pre>
[DEFAULT]
_reddituser = REDDIT_USERNAME
_subtocrosspost = REDDIT_SUBNAME
_subsource = REDDIT_SUBNAME_SOURCE+SECOND_REDDIT_SUBNAME_SOURCE+THIRD_REDDIT_SUBNAME_SOURCE
_triggerwordscomments = ['awesome!','so soft!','lovely!','wow!']
_triggerwordstitle = ['TIFU','search','help']
</pre>


won't work with videos https://www.reddit.com/r/help/comments/bnjkxr/this_community_does_not_allow_for_crossposting_of/

* why trigger words and not upvotes or saved submissions?
  *	Because not every upvote classifies as content for crosspost
