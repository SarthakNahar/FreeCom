# import required files and modules

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from scrapy.selector import Selector


def detail(p1,p2):
  # set the headers and user string
  headers = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
  }


  def link_gen(x_prod):
      #For Qr code Comparision
      if x_prod.startswith('http'):
       response = requests.get(x_prod,headers=headers)
       soup = BeautifulSoup(response.content, 'lxml')
       f=soup.find('span',attrs={'class':'B_NuCI'})
       x_prod=f.text
       response.close()
      while True:
        response = requests.get('https://www.flipkart.com/search?q='+x_prod, headers=headers)
        #print(response)
        soup2 = BeautifulSoup(response.content, 'html.parser')
        t=soup2.find('a',attrs={'class':'_1fQZEK'})
        try:
          link=t.get('href')
        except:
          pass
        if link!=None:
          response.close
          break
      temp=link
      api="https://flipkart.dvishal485.workers.dev/product/min"+link
      link='https://www.flipkart.com'+link
      return link,api

  def product(url,api_link):
      # send a request to fetch HTML of the page
      my_links = [url, api_link]
      my_responses = []
      for link in my_links:
          payload = requests.get(link,headers=headers)
          if payload.status_code != 200:
            print('Sorry cannot fetch data for this product right now!!')
            exit()
          print('got response from {}'.format(link))
          my_responses.append(payload)
          #print(payload)
      #response = requests.get(url, headers=headers)
      
      #print(response)
      # create the soup object
      soup = BeautifulSoup(my_responses[0].content, 'lxml')

      # change the encoding to utf-8
      soup.encode('utf-8')
      try:
        dat=my_responses[1].json()
        image=dat['thumbnails'][0]
        print(image)
      except:
        # Selenimum
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=options)
        browser.get(url)
        page = browser.page_source
        image_data = Selector(text=page)
        image = image_data.xpath('//div[@class="CXW8mj _3nMexc"]/img/@src').get()
        browser.quit()
        print(image)

      title = soup.find('span',attrs={'class': 'B_NuCI'}).get_text()
      price = soup.find('div',attrs={'class': '_30jeq3 _16Jk6d'}).get_text()

      th=[]
      th.append('Image')
      th.append('Title')
      th.append('Price')
      for td in soup.find_all('td',attrs={'class':'_1hKmbr col col-3-12'},text=True):
          th.append(td.get_text())

      td=[]
      td.append(image)
      td.append(title)
      td.append(price)
      for t in soup.find_all('li',attrs={'class':'_21lJbe'},text=True):
          td.append(t.get_text())
      
      
      if len(th)==2:
        for i in soup.find_all('div',attrs={'class':'col col-3-12 _2H87wv'},text=True):
          th.append(i.get_text())

        for t in soup.find_all('div',attrs={'class':'col col-9-12 _2vZqPX'},text=True):
          td.append(t.get_text())

      if len(th)>len(td):
        th.pop(2)
      else:
        if len(th)<len(td):
          td.pop(2)

      
      data={"Features": th,
        "Details": td
        }

      df=pd.DataFrame(data=data)
      
      return df

  #n=int(input("Enter number of prod: "))

  list_of_df=[]

  #for i in range(0,n):
  x_prod1=p1
  url1,api_link1=link_gen(x_prod1)
  print(api_link1)
  list_of_df.append(product(url1,api_link1))

  x_prod2=p2
  url2,api_link2=link_gen(x_prod2)
  print(api_link2)
  list_of_df.append(product(url2,api_link2))

  feature={ }
  final={}

  list_of_feature=[]

  for df in list_of_df :
    for index,rows in df.iterrows():
      if rows["Features"] in feature:
        h=1
      else :
        list_of_feature.append(rows["Features"])
        feature[rows["Features"]]=1

  final["Features"]=list_of_feature
  heading='Details of Product '
  for i in range(0,2):
    final[heading+str(i+1)]=[]


  for f in list_of_feature:
    i=0
    for df in list_of_df :
      flag=0 
      for index,rows in df.iterrows():
        if rows["Features"]==f:
          flag=1
          final[heading+str(i+1)].append(rows["Details"])
      if flag==0:
        final[heading+str(i+1)].append('NA')
      i+=1

  final_df=pd.DataFrame(data=final)
  #final_df.to_excel("data.xls",index=False)
  print(final_df.columns)
  x=final_df.to_dict('records')
  #print(x)
  return x