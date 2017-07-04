# Bitcamp2017
Programs scrape three news websites (Washington Post, The Verge, and Bloomberg) 
for articles using Python's urllib, nltk, and BeautifulSoup4 libraries. Once the
websites are scraped, the programs return an array of 3-tuples with the articles'
titles, URLs, and comment count. The arrays are ordered from greatest comment 
count to least. The front end (which my partner took care of) then uses that
information to display the top news articles generating the most conversation at
that moment.
