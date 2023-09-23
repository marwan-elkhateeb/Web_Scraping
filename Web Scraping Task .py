#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from parsel import Selector
import pandas as pd 
import csv

class Scrap:
    def __init__(self, url):
        self.url = url
        
    def makeRequest(self):
        text = requests.get(self.url).text
        selector = Selector(text=text)
        return selector;
    
    
    def getAllBrands(self,selector):
        brands = selector.xpath('//a[contains(@data-test, "party-link")]/text()').getall()
        return brands;
    
    
    def getAllTitles(self,selector):
        titles = selector.xpath('//a[contains(@data-test, "product-title")]/text()').getall()
        return titles;
    
    def getAllPrices(self,selector):
        prices = selector.xpath('//meta[contains(@itemprop, "price")]/@content').getall()
        return prices;
    
    def getAll_N_reviews(self,selector):
        n_reviews = selector.xpath('//div[contains(@class, "star-rating")]/../@aria-label').getall()
        splited_n_reviews = []
        for review in n_reviews:
            splited_n_reviews.append(review.split('de')[1])
        final_n_reviews = []
        for splited_review in splited_n_reviews:
            final_n_reviews.append(splited_review.strip())
        
        return final_n_reviews;
    
    
    def getAllRatings(self,selector):
        ratings = selector.xpath('//div[contains(@class, "star-rating")]/@title').getall()
        split_ratings = []
        for i in range(0,len(ratings),1):
            split_ratings.append(ratings[i].split(":")[1].split("sur")[0])
        trimed_ratings = []
        for i in range(0,len(split_ratings),1):
            trimed_ratings.append(split_ratings[i].strip())
            
        return trimed_ratings;

        

    def getAllUrls(self,selector):
        url = selector.xpath('//a[contains(@class, "product-title px_list_page_product_click list_page_product_tracking_target")]/@href').getall()
        return url;     


    def getCatgoryName(self,selector):
        category_name = selector.xpath('//h1[contains(@class, "h1 bol_header")]/text()').getall()
        return category_name;

        
    def getProductsId(self,selector):
        product_id = selector.xpath('//li[contains(@class, "product-item--row js_item_root ")]/@data-id').getall()
        return product_id;


        
        
    def exportCsv(self,getProductsId,brands,titles,prices,allUrls,n_reviews,AllRatings,category_name):
        import pandas as pd 
        #data = {"Products Id":getProductsId,"brands":brands,"title":titles,"price":prices,"url":allUrls,"n_reviews":n_reviews, "Ratings": AllRatings,"category_name":category_name}
        data = {"Products Id":getProductsId,"brands":brands,"title":titles,"price":prices,"url":allUrls,"n_reviews":n_reviews, "Ratings": AllRatings,"category_name":category_name}

        df = pd.DataFrame(data)
        df.to_csv('E:\Web Scraping Task/scraping.csv',index=False)

        


# In[2]:


scr = Scrap('https://www.bol.com/be/fr/l/audio-hifi/10714/')
selector = scr.makeRequest()
brands = scr.getAllBrands(selector) 
titles =scr.getAllTitles(selector)
prices = scr.getAllPrices(selector)
n_reviews = scr.getAll_N_reviews(selector)
AllRatings = scr.getAllRatings(selector)
allUrls = scr.getAllUrls(selector)
category_name = scr.getCatgoryName(selector)
getProductsId = scr.getProductsId(selector)

scr.exportCsv(getProductsId,brands,titles,prices,allUrls,n_reviews,AllRatings,category_name*len(AllRatings))


# In[ ]:




