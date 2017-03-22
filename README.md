# Canvas-File-Downloader

This is a simple Python based web scraper

I have used Selenium and BeautifulSoup4 to pull the desired files off Canvas. As of now it works with 2 of the 3 different layouts of courses on Canvas. Before using the scraper be sure to make necessary changes to the script.

Canvas relies heavily on Javascript therefore Selenium had to be used instead of conventional tools such as Scrapy. Also with the Authentication Tokens and Cookies being used by the Website, I had to fake being a real user. This can only be achieved by using Selenium. I have used BeautifulSoup4 just to trim down the page source and get the necessary download links.

Usage: 

Step 1: Simply download the Python script, replace the necessary parameters (I have mentioned necessary changes to be made as comments in the script)

Step 2: Run it on iPython or your desired Python Shell

Step 3: Enjoy not having to manually browse and download each and every course file

