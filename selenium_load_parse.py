import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import urllib
import sys
import json
import datetime

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


def beatiful_soup_parse(html, last_tweet_date):
    """
    Takes in a html from driver and parses for each individual tweet's information,
    and then writes the information to a pipe delimited file for later seeding
    """

    soup = BeautifulSoup(html, 'html.parser')

    parent_tweets = soup.findAll("div", {"class" : "tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable original-tweet js-original-tweet "})

    #While it would be more concise to seed directly into my database in this step
    #given the time constraints of the project, the cost of having to repeat the download/parse
    #process if I needed to drop my tables at any point was too high to make it a worthwhile tradeoff

    data_file = open("data_file.txt", "a")

    for tweet in parent_tweets:
        tweet_id = tweet['data-tweet-id']
        handles = tweet.findAll("span", {"class" : "username"})
        tweet_contents = tweet.findAll("p", {"class" : "TweetTextSize"})
        timestamps = tweet.findAll("span", {"class" : "_timestamp"})
        profile_location = tweet.findAll("span", {"class" : "Tweet-geo"})
        place_id = tweet.findAll("a", {"class": "ProfileTweet-actionButton"})

        handle = handles[0].text
        content = tweet_contents[0].text
        content = content.replace('\n', ' ').replace('|', ' ')


        timestamp = timestamps[0]['data-time']

        #not all twitter users provide geotags or profile location information
        if profile_location:
            profile_location = profile_location[0]['title']
        else:
            profile_location = ""
        if place_id:
            place_id = place_id[0]['data-place-id']
        else:
            place_id = ""

        date_timestamp = datetime.datetime.fromtimestamp(float(timestamp))

        #only write non-repeat tweets to file
        if date_timestamp < last_tweet_date:
            dataline = "|".join([handle, tweet_id, content, timestamp, profile_location, place_id])
            data_file.write("{}\n".format(dataline))


    data_file.close()

    #timestamp is epoch time - converting to datetime object for evaluation

    if date_timestamp.hour <= 17:
        until_date = date_timestamp + datetime.timedelta(days=1)

    else:
        until_date = date_timestamp + datetime.timedelta(days=2)

    return until_date



def load_page_and_parse():
    """
    Instantiates a selenium webdriver, prompts selenium to scroll to bottom of page,
    and call function that parses returned html with BeautifulSoup
    """

    driver = webdriver.Firefox()

    since_date = "2016-01-01"
    # stop_date = datetime.datetime.today() + datetime.timedelta(days=1)
    stop_date = datetime.datetime.strptime("2016-07-28", "%Y-%m-%d") 
    tweets_until = "2016-07-28"
    # tweets_until = stop_date.date()

    date_errors = open("date_errors.txt", "a")
    
    #essentially just an infinite loop
    while since_date == "2016-01-01":

        driver.get("https://twitter.com/search?f=tweets&vertical=news&q=Trump%20OR%20Clinton%20lang%3Aen%20until%3A{}&src=typd&lang=en".format(tweets_until))
        scroll_until = 400
        while scroll_until:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            scroll_until -= 1
            time.sleep(2)
            print "Time: {}: Scroll: {}".format(datetime.datetime.now(), scroll_until)
        html = driver.page_source
        stop_date = beatiful_soup_parse(html, stop_date)
        if stop_date.date() == tweets_until:
            repeats = "|".join([str(stop_date.date())])
            date_errors.write("{}\n".format(repeats))
            tweets_until = stop_date - datetime.timedelta(days=1)
            tweets_until = tweets_until.date()
        else:
            tweets_until = stop_date.date()
        print "tweets until: {}".format(tweets_until)
        
    driver.quit()

    return stop_date

if __name__ == '__main__':

    load_page_and_parse()
