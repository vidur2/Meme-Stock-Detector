# Meme-Stock-Detector
A meme stock detector. Scrapes stock ticker data from the subreddit r/WallStreetBets and sends it via email to a list of people. Can be used to predict markets to a degree.
In the code, I read in a CSV file as input to check against the stock data being recieved from reddit. The CSV is a list of stock tickers. In order for the code to function properly, you need to first download the CSV, save it to a local folder, and then update the Python code to reflect your local file path.
You can run the .py file to see the code in action
Note that to run this code you need to download all the packages that you dont have currently downloaded
These Include(but are not limited to):
1. NLTK
2. Requests
3. bs4

3/15 Update Reason- The Source code for one of the packages that I use(bs4) changed one of its commands which I use- soup.getText- to soup.get_text(). The code ran, but did not function properly with the previous command, thus making it paramount I add this update. The code does the same thing as before, I simply updated it to work with the new source code which the makers of bs4 pushed to their package.
