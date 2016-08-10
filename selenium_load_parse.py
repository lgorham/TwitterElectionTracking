import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib
import sys
import json

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


def beatiful_soup_parse(webpage):
    """Takes in a url and parses the html webpage"""
    
    soup = BeautifulSoup(webpage, 'html.parser')

    parent_tweets = soup.findAll("div", {"class" : "content"})

    tweet_info = {}

    #While it would be more concise to seed directly into my database in this step
    #instead of parsing, saving as json and then iterating over the json while seeding
    #given the time constraints of the project, the cost of having to repeat the download/parse
    #process if I needed to drop my tables at any point was too high to make it a worthwhile tradeoff

    for tweet in parent_tweets:
        handles = tweet.findAll("span", {"class" : "username js-action-profile-name"})

        for handle in handles:
            handle = handle.text
            if handle not in tweet_info:
                tweet_info[handle] = []
            tweet_contents = tweet.findAll("p", {"class" : "TweetTextSize js-tweet-text tweet-text"})
            timestamps = tweet.findAll("a", {"class" : "tweet-timestamp js-permalink js-nav js-tooltip"})

        for content in tweet_contents:
            # tweet_info[handle]["tweet_body"] = content.text
            content_for_storage = content.text

        for timestamp in timestamps:
            # tweet_info[handle]["timestamp"] = timestamp['title']
            timestamp_for_storage = timestamp['title']

        tweet_storage = (content_for_storage, timestamp_for_storage)
        tweet_info[handle].append(tweet_storage)

    return tweet_info



def load_page_and_parse():
    """
    Instantiates a selenium webdriver, prompts selenium to scroll to bottom of page,
    and call function that parses returned html with BeautifulSoup
    """

    driver = webdriver.Firefox()

    #advanced search url - looking for tweets containing Trump OR Clinton
    # driver.get("https://twitter.com/search?q=Trump%20OR%20Clinton%20lang%3Aen&src=typd")
    driver.get("https://twitter.com/search?q=Trump%20OR%20Clinton%20lang%3Aen%20since%3A2016-08-08%20until%3A2016-08-09&src=typd&lang=en")


    times_to_scroll = 20

    while times_to_scroll:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        times_to_scroll -= 1

    html = driver.page_source
    processed_tweets = beatiful_soup_parse(html)

    json_data = json.dump(processed_tweets, open('data.txt', 'w'))

    #close the browser instance
    # driver.quit()

    return processed_tweets



if __name__ == '__main__':

    load_page_and_parse()
