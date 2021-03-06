#!/usr/bin/python
import sys
import praw
import pandas as pd
import datetime

# read the authorisation info

auth = open('cred.txt')
lines_r = auth.readlines()
lines = [line.rstrip('\n') for line in lines_r]

reddit = praw.Reddit(client_id=lines[0], \
                     client_secret=lines[1], \
                     user_agent=lines[2], \
                     username=lines[3], \
                     password=lines[4])

# get subreddits for the topic
top = sys.argv[1]


def save_top_subreddits(topic = top):
    subreddit = reddit.subreddit(topic)
    top_subreddit = subreddit.top('year')

    #print a sample of submissions
    for submission in subreddit.top(limit=1):
        print(submission.title, submission.id)

    # Quite a few other attributes -- distinguished, edited, id, parent_id, replies,
    # stickied, subreddit, etc. comments could be extracted too

    # set up dictionary for data
    topics_dict = { "title":[], \
                    "score":[], \
                    "id":[], "url":[], \
                    "comms_num": [], \
                    "created": [], \
                    "body":[]}

    for submission in top_subreddit:
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)

    #format in pandas dataframe
    topics_data = pd.DataFrame(topics_dict)
    topics_data['created'] = pd.to_datetime(topics_data['created'], unit='s')

    # save to csv file after some date-time formatting
    time_now  = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    topics_data.to_csv('data/'+topic+'-' + time_now + '.csv', index = False)
    return


save_top_subreddits(top)


