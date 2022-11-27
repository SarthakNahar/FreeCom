import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import requests
import os

def Rec_engine():
  file_size = os.path.getsize('ratings_Electronics (1).csv')
  print("File Size is :", file_size, "bytes")
  if file_size == 318766497:
    print("No Updation in the dataset, using already compiled results")
  else:
    ratings = pd.read_csv('ratings_Electronics (1).csv')
    ratings_df = ratings.copy()
    # Let's rename the columns 
    ratings_df.columns = ['userId', 'productId', 'Rating', 'timestamp']
    #ratings_df

    total_votes = pd.DataFrame(ratings_df.groupby('productId')['Rating'].count().reset_index())
    total_votes.columns = ['productId', 'vote_count']
    total_votes = total_votes.merge(ratings_df, on = "productId")

    mean_rating = total_votes.groupby('productId')['Rating'].mean().reset_index()
    mean_rating = mean_rating.merge(total_votes, on = "productId")
    mean_rating.columns = ['productId', 'avg rating', 'vote_count', 'userId', 'rating', 'timestamp']

    v = mean_rating['vote_count']
    m = mean_rating['vote_count'].quantile(0.95)
    R = mean_rating['avg rating']
    C = mean_rating['rating'].mean()

    mean_rating = mean_rating[mean_rating['vote_count'] >= m]

    recommended_products = mean_rating.drop(['userId', 'timestamp', 'rating'], axis = 1)
    recommended_products.drop_duplicates(inplace = True)

    def recommendation(x):
        v = x['vote_count']
        R = x['avg rating']
        return (v/(v+m) * R) + (m/(m+v) * C)
    recommended_products['score'] = recommended_products.apply(recommendation, axis = 1)

    recommended_products.sort_values(by ="score", ascending = False, inplace = True)

    # Amazon api
    Asin = pd.DataFrame(recommended_products.head(15))
    Asin=Asin.reset_index().drop('index',axis=1)

    Asin['API']=Asin.productId.apply(lambda x:'https://amazon-scraper.tprojects.workers.dev/product/dp/'+x )

    headers = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
    name=[]
    image=[]
    prod_link=[]
    productId=[]
    count=0
    for link in Asin.API:
      payload = requests.get(link,headers=headers).json()
      if payload['product_detail']== None:
        continue
      productId.append(link[-10:]) # ASIN Number are 10-digits
      name.append(payload['product_detail']['name'])
      image.append(payload['product_detail']['image'])
      prod_link.append(payload['product_detail']['product_link'])
      count=count+1
      #print(count,name[count-1])
      if count==10:
        break

    #print(name,image,prod_link,productId)
    zipped=list(zip(productId,name,prod_link,image))
    temp=pd.DataFrame(zipped,columns=['productId','name','prod_link','image'])

    df_final=temp.merge(Asin,on='productId',how='inner')
    print(df_final.shape)
    print(df_final.columns)
    print(df_final)
    df_final.to_csv('top_10.csv')
    print("Updated the Trending Products")
  '''
  data=pd.read_csv("top_10.csv")
  final_data=data.to_dict()
  print(final_data)
  return final_data
'''