'''
Vidur Modgil
Reddit Web Scraper
Tech Fair Submission
'''
#Preprossescor Directives
import requests
from bs4 import BeautifulSoup
import sys, os
import time
import nltk
import smtplib
import random
import csv
# You will also need to change the filepath for the csv file
# You must run this on python 3.4.2 or higher
# Creates function which has the capability to send an email out
def send(message, recipients):
        # Original email which sends out, google password and auth here
	auth = ('senderstonk@gmail.com', 'stonkSender2021')
	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()
	server.login(auth[0], auth[1])
	# Send text message through SMS gateway of destination number
	server.sendmail( auth[0], recipients, message)
# This is the method by which stock tickers are sorted in the code
def stockSorter(webList, key):
    methodList = []
    for stonkPossibleFind in webList:
            # Iterates through the headers on the subreddit
                for stonk in key:
                    # Iterates through the possible stocks
                    iteration = 0
                    # NLTK does not detect stock tickers if the $ is before it, maybe because of the way it is used in those situations, so this is the first condition
                    # Basically the $ means that the way the word is used is as a stock
                    if '$' + stonk in stonkPossibleFind:
                        methodList.append(stonk)
                    # Sorts the possible stocks by nouns, if they are being used as nouns, they are appended to the stocks found list
                    # This minimizes error
                    if stonk in stonkPossibleFind:
                        # Sorts out sentences in comments
                        stonkLI = nltk.tokenize.sent_tokenize(stonkPossibleFind)
                        filteredSentence = []
                        for sentences1 in stonkLI:
                            # Sorts out words in sentences
                            for s,pos in nltk.pos_tag(nltk.word_tokenize(str(stonkLI))):
                                # Only adds word to list of filtered sentence if it is a noun
                                if(pos in ['NN', 'NNP', 'NNS', 'NNPS']):
                                    filteredSentence.append(s)
                        for u in filteredSentence:
                            # Only adds noun from filtered sentence if it matches a stock ticker or if it has a dollar sign before it
                            # This functions as a check if the first check for a dollar sign before a stock ticker fails to pick up on the ticker for any reason
                            # The parenthesis are also a way stock tickers are denotated on r/WallStreetBets
                            if stonk == filteredSentence[iteration] or '$' + stonk == filteredSentence[iteration] or '(' + stonk + ')' == filteredSentence[iteration]:
                                methodList.append(filteredSentence[iteration])
                                iteration = iteration + 1
    return methodList
# Start of the main module
def main():
    try:
        # Gets Stock Tickers from a csv file and stores it in a list
        stonkKeyUnfiltered = []
        # Enter the filepath for the CSV here, with your own, the program will not run
        with open('/Users/vidurmodgil/Desktop/Programming Projects/Reddit Web Scraping/Submission Files/StockTickers.csv') as csvOpened:
            csvReader = csv.reader(csvOpened)
            csvList = list(csvReader) 
        for StockTicker in csvList:
            csvFiltered = StockTicker[0].replace("'", '').replace(' ', '')
            stonkKeyUnfiltered.append(csvFiltered)
        # Gets your user input for who you want to send emails out to
        userEmailNumbers = input('How many people do you want to send the email to (please enter an int): ')
        emailList = []
        for i in range(int(userEmailNumbers)):
            email = input('Who do you want to recieve the email (enter an email address): ')
            emailList.append(email)
        userEmail = input('What is your email (this will revieve the error messages, etc.): ')
        # Downloads the nessescary packages from nltk in order to filter out stopwords and sort tickers by nouns to decrease false pickups
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        stop_words = set(nltk.corpus.stopwords.words('english'))
        # Initializes all of the lists which will be used later in the program
        stonksFound = []
        stonkKey = []
        filteredLinks = []
        counter = 0
        keyList = []
        stonkSearch = []
        commentFound = []
        stockComparison = []
        excessHeaders = []
        excessCommentCollecters = []
        stonkComparison = []
        commentComparison = []
        runner = 0
        running = 0
        # Also a filter for stock tickers, usually on r/WallStreetBets stocks with three letters or more become meme stocks
        # In addition to this most stocks which are 'memed' then dumped on r/WallStreetBets contain three characters or more
        for stonk in stonkKeyUnfiltered:
            if len(stonk) > 2 and stonk not in stop_words:
                stonkKey.append(stonk)
        # Initializes counter variable for the loop
        counter = 0
        while True:
            # These two lists are set to the previous iteration of the while loop's comment and header data and compared to the current iteration
            # This is to make sure that the stock tickers mentioned in a single comment aren't double or tripled counted because not enough new data is coming in to erase it from the list
            if len(stonkSearch) > 0:
                stonkComparison = stonkSearch + excessHeaders
            if len(commentFound) > 0:
                commentComparison = commentFound + excessCommentCollecters
            # Initializes counter variables and lists which will be reset every iteration of the loop
            stonkSearch = []
            commentFound = []
            c = 0
            stonkChecker = stonksFound
            threadSearch = []
            dictDataCollecter = []
            # Used later in the code to sort through the desired urls to get to reddit comment data
            websiteReq1 = 'https'
            websiteReq2 = 'comments'
            # Initializes the variable that will be used to store the count of the stock tickers apearances in the form of a string
            dictString = ''
            # Gets the content from r/WallStreetBets via requests
            page = requests.get('https://www.reddit.com/r/wallstreetbets/new/')
            soup = BeautifulSoup(page.content, 'html.parser')
            # Sorts out all the content between 'h3' tags and stores it in the list
            for title in soup.find_all('h3'):
                stock = title.get_text()
                stonkSearch.append(stock)
            # Makes sure stocks aren't counted 2 or 3 times by comparing the current iteration comments to the last iteration stocks
            # Deletes the comment in the current list if it is identical to one in the previous list
            if len(stonkComparison) > 0:
                stonkSearchDuplicate = stonkSearch
                for stockElement in stonkSearchDuplicate:
                    for stockComparator in stonkComparison:
                        if stockElement == stockComparator and stockElement in stonkSearch:
                            '''
                            Appends comments which are equivalent to the previous iteration to a new list
                            These are counted in the next loop, as they will be removed from the comparison list in the next iteration
                            This is because every iteration the comparison is set equal to the stock searcher list
                            '''
                            excessHeaders.append(stockElement)
                            stonkSearch.remove(stockElement)
            stockHeadersFound = stockSorter(stonkSearch, stonkKey)
            # Gets all of the content contained in <a>, tags or the links
            for link in soup.find_all('a'):
                # The part contained in the href tag is the hyperlink to a comment, which is what we are looking for in this part of the code
                # This allows us to scrape for stock tickers in the comments
                thread = link.get('href')
                threadSearch.append(thread)
            threadLength = len(threadSearch)
            # Some links on r/WallStreetBets are links to reddit itself(the button) or the TOS, so this filters them out
            # Also if there are any 'honeypot traps' on the website, this avoids this trap, allowing the webscraper to continue running
            if len(threadSearch) > 0:
                c = 0
                while c < threadLength:
                    '''
                    Sometimes the list appends with a value of None
                    This can cause an error if iterated through and then treated as a string in an if statement
                    '''
                    if threadSearch[c] == None:
                        pass
                    elif websiteReq1 in threadSearch[c] and websiteReq2 in threadSearch[c]:
                        filteredLinks.append(threadSearch[c])
                    c = c + 1
            # Sorts the comments out by the <p> tag, and gets the text in between them
            for d in range(len(filteredLinks)):
                threadPage = requests.get(filteredLinks[d])
                threadSoup = BeautifulSoup(threadPage.content, 'html.parser')
                for comment in threadSoup.find_all('p'):
                    commentData = comment.get_text()
                    commentFound.append(commentData)
            c = 0
            # Does a similar thing to a previous loop, makes sure that the comments from the previous iteration aren't 'double counted'
            if len(commentComparison) > 0:
                commentFoundDuplicate = commentFound
                for commentElement in commentFoundDuplicate:
                    for commentComparator in commentComparison:
                        if commentComparator == commentElement and commentElement in commentFound:
                            excessCommentCollecters.append(commentElement)
                            commentFound.remove(commentElement)
            # Does the same thing as the previous loop that utilizes nltk, it sorts out the stock tickers we want from the unneeded noise
            # The difference is that this is over the comment list
            stockCommentsFound = stockSorter(commentFound, stonkKey)
            # Prints list to notify user that it is picking up content
            stonksFound = stonksFound + stockCommentsFound + stockHeadersFound
            print(stonksFound)
            # Translates List of repeated elements to a dict with those repeated elements as a count next to unique stock tickers
            stonkDict = {t:stonksFound.count(t) for t in stonksFound}
            keyList = list(stonkDict.keys())
            # The 'in' function picks up on stocks of a shorter length(ex if GME is picked up, then GM will also be counted), this removes those unessescary tickers
            for element in keyList:
                for iterator in range(len(keyList)):
                    if element != keyList[iterator] and element in keyList[iterator]:
                        del stonkDict[element]
                        break
            # Prints dictionary for user confirmation
            print(str(stonkDict))

            # Reformats Dictionary as a string with english words to be sent as an email to those on the list
            for dictElement in stonkDict:
                dictData = "The stock {0} appeared {1} times".format(dictElement, stonkDict[dictElement])
                dictDataCollecter.append(dictData)
            for string in dictDataCollecter:
                dictString += str(string) + '{}'.format('\n')
            dictString = dictString[:-1]
            # Notifies user that content has been found on the page
            if len(stonkSearch) > 0:
                print('Connection Established!')
                '''
                Increases counter if stocks have been found, this is used for debugging
                If one notices that the amount of times a stock is counted is equivalent to the counter
                Then one can be sure that values are being double counted
                '''
                if len(stonksFound) > 0:
                    counter = counter + 1
                print(counter)
                # Sends Email to those on the email list if a stock appears 150 times on the subreddit
                for z in stonkDict:
                    if stonkDict[z] > 150 and z != 'GME' and z != 'APHA' and z != 'AMC' and z != 'NOK':
                        send(dictString + '{}'.format('\n'), emailList)
                        print('Email Sent')
                        stonksFound = []
                        counter = 0
                        time.sleep(7200)
                    # Notifies me if a stock has appeared 50 times on the subreddit
                    elif stonkDict[z] > 50 and stonkDict[z] <= 60 and z != 'GME' and z != 'APHA' and z != 'AMC' and z != 'NOK':
                        send(dictString, userEmail)
                        print('Personal Message Sent')
                # Send an email to me which notifies me that the program has picked up on a stock ticker
                if counter == 1:
                    send('Cycle has started!', userEmail)
                # Delays are random, to make sure that a scraper algorithm cannot detect the scraper
                timeDelays = random.randrange(90, 150)
                time.sleep(timeDelays)
            elif len(stonksFound) == 0:
                print('Searching for Stock Tickers... ')
    except KeyboardInterrupt:
        # Notifies potential customers that program is being updates
        send('Server down for maintainence', userEmail)
    except Exception as e:
        # Sends a message to me if an error has occoured
        send('An Error has occoured\nError: {}'.format(e), userEmail)
if __name__ == '__main__':
    main()
