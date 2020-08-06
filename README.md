# crosspostbot
crosspost submission when user `_reddituser` comment some trigger words `_triggerwords`.
The script runs every 15mins (crontab) and collect the comments of the last 24h.
When a trigger word is found, the submission will be crossposted to another sub `_subtocrosspost`.

<pre>
[DEFAULT]
_reddituser = REDDIT_USERNAME
_subtocrosspost = REDDIT_SUBNAME
_triggerwords = ['awesome!','trigger2!','trigger3!','wow!']
</pre>


won't work with videos https://www.reddit.com/r/help/comments/bnjkxr/this_community_does_not_allow_for_crossposting_of/

* why trigger words and not upvotes?
  *	Because not every upvote classifies as content for crosspost
