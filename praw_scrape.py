#!/usr/bin/python
import sys
import numpy as np
import praw
from praw.models import MoreComments
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

def save_submission(url):
    submission = reddit.submission(url = url)

    m_dict = {'post_date':[], \
               'comm_date':[], \
               'subreddit': [], \
               'post_score':[],\
               'author':[], \
               'user':[], \
               'comment_score':[], \
               'comment':[], \
               'controversiality':[], \
               'comment':[], \
               'post_text':[], \
               'link':[], \
               'domain':[], \
               'URL':[]}

    [c for c in submission.comments.list()]



def save_top_subreddits(topic, limit = 1):
    subreddit = reddit.subreddit(topic)
    top_subreddit = subreddit.top('year')

    #print a sample of submissions
    # for submission in subreddit.top(limit=1):
        # print(submission.title, submission.id, submission.comments.list())

    # Quite a few other attributes -- distinguished, edited, id, parent_id, replies,
    # stickied, subreddit, etc. comments could be extracted too

    # set up dictionary for data
    topics_dict = { "title":[], \
                    "score":[], \
                    "id":[], "url":[], \
                    "comms_num": [], \
                    "created": [], \
                    "allcomments":[],
                    "body":[]}

    for submission in top_subreddit:
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)
        topics_dict["allcomments"].append(load_comments(submission))

    #format in pandas dataframe
    topics_data = pd.DataFrame(topics_dict)
    topics_data['created'] = pd.to_datetime(topics_data['created'], unit='s')
    topics_data = expand_list(topics_data, 'allcomments', 'comments')

    # save to csv file after some date-time formatting
    time_now  = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    topics_data.to_csv('data/'+topic+'-' + time_now + '.csv', index = False)
    return

def load_comments(submission):
    comments = []
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        comments.append(top_level_comment.body)
    return comments


def expand_list(df, list_column, new_column): 
    lens_of_lists = df[list_column].apply(len)
    origin_rows = range(df.shape[0])
    destination_rows = np.repeat(origin_rows, lens_of_lists)
    non_list_cols = (
      [idx for idx, col in enumerate(df.columns)
       if col != list_column]
    )
    expanded_df = df.iloc[destination_rows, non_list_cols].copy()
    expanded_df[new_column] = (
      [item for items in df[list_column] for item in items]
      )
    expanded_df.reset_index(inplace=True, drop=True)
    return expanded_df


save_top_subreddits(top)
