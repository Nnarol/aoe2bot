#!/usr/bin/env python3

import praw
import scraping
import re
import praw.exceptions
from prawcore.exceptions import PrawcoreException
import time
import os

reddit = praw.Reddit(
    client_id=os.environ["PRAW_CLIENT_ID"],
    client_secret=os.environ["PRAW_SECRET"],
    user_agent="test",
    username=os.environ["PRAW_USERNAME"],
    password=os.environ["PRAW_PASSWORD"]
)

# The subreddit can also be specified through the environment
# for testing purposes.
subreddit = reddit.subreddit(os.environ.get("PRAW_SUBREDDIT") or "aoe2")
*tech_keys, = scraping.tech_all
with open("log_id.txt", "r") as log:
    prev_id = log.read()
    print(prev_id)
    prev_id = prev_id.split("\n")
    print(prev_id)
log_id = open("log_id.txt", "a+")

log = open("log.txt", "a+")


try:
    for comment in subreddit.stream.comments():
        if hasattr(comment, "body") and comment.id not in prev_id:
            search_word = comment.body.replace("\\", "")
            word = re.findall(r"\[([A-Za-z0-9\s]+)\]", search_word)
            if word is not None and len(word)>0:
                for i in range(0, len(word)):
                    if word[i].lower() in tech_keys:
                        print("Match: ", word[i])
                        comment.reply(word[i] + ": " + scraping.tech_all[word[i]])
                        print(scraping.tech_all[word[i]])
                        log.write("Replied to comment: " + comment.body + "\n")
                        print()
                log_id.write(comment.id + "\n")
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted by Keyboard")
except PrawcoreException as e:
    print("Interrupted by ", e)

log.close()
log_id.close()
