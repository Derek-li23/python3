# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
import urllib3
from bs4 import BeautifulSoup
import re

###_________settings

re1=re.compile(r'\w{3,5}\-\d{3,5}')
sizeFormatRe= re.compile(r'[Gg][Bb]')
sizeNumberRe= re.compile(r'\d{1,3}\.?\d{0,3}')
threadNum=re.compile('\d{5,9}')


# target_url ="https://sis001.us/forum/forumdisplay.php?fid=58"
# http = urllib3.poolmanager.PoolManager()
# response = http.request("get",target_url)
# response1= response.data.decode('utf-8')
# with open ("response.txt",'w') as fo:
#     fo.write(response1)

# print (response1)

with open("response.txt",'r') as fi:
    source_html = fi.read()

bsobj = BeautifulSoup(source_html,features="html.parser")

summary_table= bsobj.findAll('table',id='forum_58')[-1].findAll('tbody')

resultArray=[]

for item in summary_table:
    title=""
    mark=""
    # print (re1.search(item.find('th').get_text(strip=True)))

    ## find description
    description=item.find('th').get_text(strip=True)

    ##       find title info
    if re1.search(description):
        title = re1.search(description).group()
        print (title)
    else:
        title = description
        mark +="Title Exception"

    ##       find author inf
    author=item.find('td', class_='author').find('cite').get_text(strip=True)

    ##         find Size info
    sizeinfo=item.findAll('td',class_="nums")[1].get_text(strip=True)
    fileSize= ""

    ## find url info
    url= "https://sis001.us/forum/"+item.findAll("a")[2]['href']

    ## find thread id
    id=threadNum.search(url).group()


    if sizeFormatRe.search(sizeinfo):
        fileSize = float(sizeNumberRe.search(sizeinfo).group())
    else:
        fileSize = float(int(sizeNumberRe.search(sizeinfo).group())/1024)

    resultArray.append((id,title,description,author,fileSize,url))

print (resultArray)


