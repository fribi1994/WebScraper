import urllib.request
from bs4 import BeautifulSoup
import json

#create array with urls
seed_urls = ['https://inshorts.com/en/read/technology',
             'https://inshorts.com/en/read/sports',
             'https://inshorts.com/en/read/world']

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
extracted_records = []
#starting loop
for url in seed_urls:
    request = urllib.request.Request(url,headers=headers)
    html_page = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html_page,'html.parser')
    news_category = url.split('/')[-1]
#First lets get the HTML of the card stack where all the links are displayed
    main_stack = soup.find("div",attrs={'class':'card-stack'})

#Now we go into main_table and get every a element in it which has a class "title" 
    cards = main_stack.find_all("div", attrs={'class':'news-card z-depth-1'} )

#List to store a dict of the data we extracted 
    for card in cards: 
        main_title = card.find("span", attrs={'itemprop':'headline'}).text
        url = card.find("a", attrs={'class':'clickable'})['href']
        if not url.startswith('http'):
            url = "https://inshorts.com"+url

        #print(main_title)
        author = card.find("span", attrs={'class':'author'}).text
        #print(author)
        date = card.find("span", attrs={'class':'date'}).text
        #print(date)
        time = card.find("span", attrs={'class':'time'}).text
        #print(time)

    #Lets just print it 
        print("%s - %s - %s - %s - %s - %s"%(main_title,url,author,date,time,news_category))
        record = {
            'title':main_title,
            'url':url,
            'author':author,
            'publish date':date,
            'publish time':time,
            'News Category': news_category
        }
        extracted_records.append(record)
#Lets write these to a JSON file for now. 
with open('data2.json', 'w') as outfile:
    json.dump(extracted_records, outfile, indent=4)
