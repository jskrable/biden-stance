from bs4 import BeautifulSoup
import requests
import random


response = requests.get('https://www.ontheissues.org/joe_biden.htm')

soup = BeautifulSoup(response.content)

lists = soup.find_all('ul')


def get_quotes(issue):

    topic = issue.parent.find('a').text.strip().split(' ')[-1].lower()
    quotes = [q.text.strip() for q in issue.find_all('li')]
    return topic, quotes


def get_random_stance(stances):

    all_topics = stances.keys()
    topic = list(topics)[random.randint(0, len(topics))]
    quotes = stances[topic]
    rand_quote = quotes[random.randint(0, len(quotes))]
    return topic, rand_quote


def format_tweet(stance):
    topic, quote = stance
    return 'Joe Biden on ' + topic + ':\n' + quote


## MAIN
#########################################################


stance_gen = (get_quotes(issue) for issue in lists)
stances = {issue: quote for issue, quote in stance_gen}
tweet = format_tweet(get_random_stance(stances))

