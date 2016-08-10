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

    # parent_tweets = soup.findAll("div", {"class" : "content"})
    parent_tweets = soup.findAll("div", {"class" : "tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable original-tweet js-original-tweet "})


    #While it would be more concise to seed directly into my database in this step
    #instead of parsing, saving as json and then iterating over the json while seeding
    #given the time constraints of the project, the cost of having to repeat the download/parse
    #process if I needed to drop my tables at any point was too high to make it a worthwhile tradeoff

    data_file = open("data_file.txt", "w")

    for tweet in parent_tweets:
        tweet_id = tweet['data-tweet-id']
        handles = tweet.findAll("span", {"class" : "username js-action-profile-name"})
        tweet_contents = tweet.findAll("p", {"class" : "TweetTextSize js-tweet-text tweet-text"})
        timestamps = tweet.findAll("a", {"class" : "tweet-timestamp js-permalink js-nav js-tooltip"})
        profile_location = tweet.findAll("span", {"class" : "Tweet-geo u-floatRight js-tooltip"})
        place_id = tweet.findAll("a", {"class": "ProfileTweet-actionButton u-linkClean js-nav js-geo-pivot-link"})

        handle = handles[0].text
        content = tweet_contents[0].text
        timestamp = timestamps[0]['title']
        if profile_location:
            profile_location = profile_location[0]['title']
        if place_id:
            place_id = place_id[0]['data-place-id']

        data_file.write("{} | {} | {} | {} | {} | {}\n".format(handle, tweet_id, content, timestamp, profile_location, place_id))


    data_file.close()

    return timestamp



def load_page_and_parse():
    """
    Instantiates a selenium webdriver, prompts selenium to scroll to bottom of page,
    and call function that parses returned html with BeautifulSoup
    """

    driver = webdriver.Firefox()

    #advanced search url - looking for tweets containing Trump OR Clinton
    driver.get("https://twitter.com/search?q=Trump%20OR%20Clinton%20lang%3Aen&src=typd")
    # driver.get("https://twitter.com/search?q=Trump%20OR%20Clinton%20lang%3Aen%20since%3A2016-08-08%20until%3A2016-08-09&src=typd&lang=en")


    since = 2016-01-01
    # until = 

    while since == 2016-01-01:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        times_to_scroll -= 1

    html = driver.page_source
    last_date = beatiful_soup_parse(html)


    #close the browser instance
    driver.quit()

    print last_date



if __name__ == '__main__':

    load_page_and_parse()
