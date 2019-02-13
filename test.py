import praw
import pandas as pd

# read the authorisation info

auth = open('secret.txt') 
lines_r = auth.readlines()
lines = [line.rstrip('\n') for line in lines_r]
print lines


reddit = praw.Reddit(client_id=lines[0], \
                     client_secret=lines[1], \
                     user_agent=lines[2], \
                     username=lines[3], \
                     password=lines[4])

subreddit = reddit.subreddit('Nootropics')

top_subreddit = subreddit.top()


for submission in subreddit.top(limit=1):
    print(submission.title, submission.id)
