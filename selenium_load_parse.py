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

def parse_tweet(tweet):
    """
    Called on individual tweets identified by BeautifulSoup - parses html
    and returns list of relevant data
    """

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

    if profile_location:
        profile_location = profile_location[0]['title']
    else:
        profile_location = ""
    if place_id:
        place_id = place_id[0]['data-place-id']
    else:
        place_id = ""

    date_timestamp = datetime.datetime.fromtimestamp(float(timestamp))

    return [handle, tweet_id, content, date_timestamp, timestamp, profile_location, place_id]



################################################################################



def beatiful_soup_parse(html, last_tweet_date):
    """
    Takes in a html from driver and parses for each individual tweet's information,
    and then writes the information to a pipe delimited file for later seeding
    """

    soup = BeautifulSoup(html, 'html.parser')

    parent_tweets = soup.findAll("div", {"class" : "tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable original-tweet js-original-tweet "})

    # While it would be more concise to seed directly into my database in this step
    # given the time constraints of the project, the cost of having to repeat the download/parse
    # process if I needed to drop my tables at any point was too high to make it a worthwhile tradeoff

    data_file = open("missing_dates.txt", "a")

    for tweet in parent_tweets:
        handle, tweet_id, content, date_timestamp, str_timestamp, profile_location, place_id = parse_tweet(tweet)

        # Checks to make sure that these are not tweets from the overlapping timeperiod, and only writes new tweets to file.
        if date_timestamp < last_tweet_date:
            dataline = "|".join([handle, tweet_id, content, str_timestamp, profile_location, place_id])
            data_file.write("{}\n".format(dataline))


    data_file.close()



################################################################################



def stop_date_evaluation(stop_date, tweets_until):
    """
    Evaluates whether or not the date returned from parsing is a repeat of the last date,
    and if so, subtracts another day in order to not repeat scraping

        >>> stop_date = datetime.datetime.strptime("2016-06-08", "%Y-%m-%d")
        >>> tweets_until = datetime.datetime.strptime("2016-06-08", "%Y-%m-%d")
        >>> stop_date_evaluation(stop_date, tweets_until)
        2016-06-07

    """
    date_errors = open("missing_date_errors.txt", "a")
    if stop_date.date() == tweets_until:
            repeats = "|".join([str(stop_date.date())])
            date_errors.write("{}\n".format(repeats))
            tweets_until = stop_date - datetime.timedelta(days=1)
            tweets_until = tweets_until.date()

    else:
        tweets_until = stop_date.date()

    return tweets_until



################################################################################



def load_page_and_parse():
    """
    Instantiates a selenium webdriver, prompts selenium to scroll to bottom of page,
    and call function that parses returned html with BeautifulSoup
    """

    driver = webdriver.Firefox()

    stop_date = datetime.datetime.today() + datetime.timedelta(days=1)

    # Could automatically read in the last date from the last set of tweets 

    stop_date = datetime.datetime.strptime("2016-08-10", "%Y-%m-%d") 
    tweets_until = "2016-08-10"
    # tweets_until = stop_date.date()

    
    # An infinite loop - since Twitter's Advanced Search will continue to load past the "end date" you specify.
    while True:

        driver.get("https://twitter.com/search?f=tweets&vertical=news&q=Trump%20OR%20Clinton%20lang%3Aen%20until%3A{}&src=typd&lang=en".format(tweets_until))
        scroll_until = 400

        while scroll_until:

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            scroll_until -= 1
            time.sleep(2)
            print "Time: {}: Scroll: {}".format(datetime.datetime.now(), scroll_until)


        html = driver.page_source
        beatiful_soup_parse(html, stop_date)
        stop_date = stop_date - datetime.timedelta(days=1)

        tweets_until = stop_date_evaluation(stop_date, tweets_until)

        print "tweets until: {}".format(tweets_until)
        
    driver.quit()

    return stop_date

################################################################################



def update_database():
    """
    Check and see if time has based since database was last updated,
    if a week has passed, restart the scraping process
    """




################################################################################


if __name__ == '__main__':

    load_page_and_parse()

    import doctest

    print
    result = doctest.testmod()
    if not result.failed:
        print "ALL TESTS PASSED. GOOD WORK!"
    print

