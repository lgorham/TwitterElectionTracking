# We the People
We the People is a web application by [Lydia Gorham](https://www.linkedin.com/in/lydia-gorham) that provides a glimpse at public sentiment regarding the 2016 presidential election by collecting, analyzing and visualizing over one million tweets related to the presidential candidates.

![demo_gif](http://g.recordit.co/ae91d23X1u.gif)

## Contents
- [Technologies Used](#technologiesused)
- [Data Collection](#datacollection)
- [Sentiment Analysis](#sentimentanalysis)
- [Data Visualizations](#datavisualizations)

## <a name="technologiesused"></a>Technologies Used
- [AJAX/JSON](https://jquery.com/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Bootstrap](http://getbootstrap.com/)
- [Chart.js](http://www.chartjs.org/)
- [Flask](http://flask.pocoo.org/)
- [Google Maps API](https://developers.google.com/maps/)
- [PostGreSQL](https://www.postgresql.org/)
- [Python](https://www.python.org/)
- [Selenium WebDriver](http://docs.seleniumhq.org/docs/03_webdriver.jsp)
- [Scikit-Learn](http://scikit-learn.org/stable/)
- [SQLAlchemy](http://flask.pocoo.org/)

## <a name="datacollection"></a>Data Collection
The data for this project was scraped and parsed from Twitter's live search feed using Selenium WebDriver and Beautiful Soup. Selenium is used to call the GET request for a specific date/keyword search, and then to automate the process of scrolling down the page - prompting Twitter's lazy load to render more tweets. The HTML from the search was then parsed using Beautiful Soup to extract the text, user handle, location, and timestamp of each tweet. This process was chosen over using Twitter's Search API, as the API is rate limited to restrict queries to the past 7 days, preventing a comprehensive look at the full election cycle. By scraping the data, I was able to gather tweets with dates ranging from January through August 2016. However, due to the limitations of the scraping process, this data should not be used for research purposes.

## <a name="sentimentanalysis"></a>Sentiment Analysis
Each tweet is classified as 'negative' or 'positive' by using a Bernoulli Naive Bayes classifier, imported from Scikit-Learn. The classifier is trained on a hand-tagged training corpus of 500 tweets from the main body of tweets, in order to provide the most accurate results for the specific domain of election-related tweets. The trained classifier has a accuracy of 79%.

![naive_bayes](http://i.imgur.com/8knlFX2.png)

Naive Bayes is a probabalistic classifier based upon the underlying assumption that every feature or attribute of an instance is considered independent from all other features. This assumption runs contrary to our knowledge of natural language, as sentences are almost never made up of completely independent words, and this interdependence often helps form [the syntactic and semantic meaning](http://ucrel.lancs.ac.uk/acl/N/N01/N01-1021.pdf) of a sentance. The use of n-grams (sections of words that often appear together) instead of independent words, is a popular way to mitigate the independence assumption by forcing the classifier to examine sections of words. However [current research](http://www.cs.cornell.edu/home/llee/papers/sentiment.pdf) demonstrates that sentiment analysis classification does not gain any benefit from word frequency features, particularly in short documents - such as tweets, and my own experimentation with n-grams did not increase the accuracy of the classifier.

It is worth noting that due to constraints in the current field of Natural Language Processing and sentiment analysis, the classifier is unable to distinguish between a negative sentiment directed towards the referenced candidate, and a text with a generally negative valence that does not necessarily indicate the writer's sentiment about the referenced candidate. As such, this data should not be used as a proxy for voting prefrences, but rather to illustrate general trends in sentiment fluctuations throughout the election cycle.

## <a name="datavisualizations"></a>Data Visualizations
The data visualizations of the analyzed tweets are generated using Chart.js and Google Maps API. The line chart shows the raw number of tweets for each candidate, broken down by valence, on any given day from January through present. The line chart is interactive, and allows users to toggle on/off specific candidates and valences in order to best see the comparisons they are most interested in. The doughnut charts displays what percentage of a given candidate's tweets are positive vs. negative. The bar chart compares the raw aggregate number of tweets about each candidate.


The tweets are also displayed by geographical location of the tweeter's profile location. The profile location of each tweet was extracted from the HTML in the scraping process, and then the number of positive/negative tweets for a given candidate in each location were aggregated. This analysis is then displayed using Google Maps API for visualization, and the Google Maps Geocoder API to convert profile locations into coordinates for geospatial display.





