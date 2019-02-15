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

# get comments for the submission at this url
url = sys.argv[1]

def save_submission(u = url):
    submission = reddit.submission(url = u)

    m_dict = {'post_date':[], \
               'comm_date':[], \
               'subreddit': [], \
               'post_score':[],\
               'author':[], \
               'user':[], \
               'comment_score':[], \
               'comment_hidden':[], \
               'controversiality':[], \
               'comment':[], \
               'post_text':[], \
               'link':[], \
               'domain':[], \
               'URL':[]}

    for co in  submission.comments.list():
        m_dict["post_date"].append(submission.title)
        m_dict["comm_date"].append(co.created)
        m_dict["subreddit"].append(submission.subreddit_id)
        # m_dict["post_score"].append(submission.score)
        # m_dict["author"].append(co.author.name)
        m_dict["comment_score"].append(co.score)
        m_dict["comment_hidden"].append(co.score_hidden)
        m_dict["controversiality"].append(co.controversiality)
        m_dict["comment"].append(co.body)
        m_dict["post_score"].append(submission.score)
        m_dict["link"].append(submission.title)
        m_dict["post_text"].append(submission.title)
        m_dict["domain"].append(submission.title)
        m_dict["URL"].append(submission.title)

    submission_data = pd.DataFrame(m_dict)

    # save to csv file after some date-time formatting
    time_now  = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    id =  submission.id
    subreddit = submission.reddit.display_name
    topics_data.to_csv('data/' + subreddit + '/' + id+'-' + time_now + '.csv', index = False)
    return

save_submission(url)
