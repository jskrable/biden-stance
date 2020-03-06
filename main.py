"""
title: main.py
date: 2020-03-05
author: jskrable
description: scrapes data from congressional issue site for Joe Biden, picks a random 
topic, and tweets it out. Run on AWS Lambda.
"""

import json
import random
import requests
import twitter
from bs4 import BeautifulSoup


def get_quotes(issue):

    topic = (' ').join(issue.parent.find('a').text.strip().split(' ')[4:])
    quotes = [q.text.strip() for q in issue.find_all('li')]
    return topic, quotes


def get_random_stance(stances):

    all_topics = stances.keys()
    topic = list(all_topics)[random.randint(0, len(all_topics))]
    quotes = stances[topic]
    rand_quote = quotes[random.randint(0, len(quotes))]
    return topic, rand_quote


def format_tweet(stance):
    topic, quote = stance
    body = 'Joe Biden on ' + topic + ':\n\n' + quote
    hashtags = ' '.join(['#' + x.lower() for x in topic.split(' ') if len(x) > 3])
    return body + '\n\n' + hashtags


def get_creds():
    with open('twitter_creds.json') as f:
        creds = json.load(f)
    return creds


def o_auth(creds):
    api = twitter.Api(consumer_key=creds['consumer_key'],
                      consumer_secret=creds['consumer_secret'],
                      access_token_key=creds['access_token_key'],
                      access_token_secret=creds['access_token_secret'])
    return api


def lambda_handler():
    response = requests.get('https://www.ontheissues.org/joe_biden.htm')
    soup = BeautifulSoup(response.content)
    lists = soup.find_all('ul')
    stance_gen = (get_quotes(issue) for issue in lists)
    stances = {issue: quote for issue, quote in stance_gen}
    tweet = format_tweet(get_random_stance(stances))
    api = o_auth(get_creds())
    status = api.PostUpdate(tweet)


if __name__ == '__main__':
    lambda_handler()