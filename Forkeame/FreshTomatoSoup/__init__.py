'''
Created on 17/10/2016

@author: joshbigdaddy
'''
#encoding: utf-8

import urllib2, re
import os.path
from bs4 import BeautifulSoup
import sqlite3
import tkMessageBox
import requests
def extraer_datos():
    url="https://www.rottentomatoes.com/top/bestofrt/?year=2016"
    soup = BeautifulSoup(requests.get(url).content,'html.parser')
    return soup
   

def almacena_peliculas():
    conn = sqlite3.connect('test.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS PELICULAS")   
    conn.execute('''CREATE TABLE PELICULAS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       YEAR            INTEGER    NOT NULL,
       TITULO          TEXT    NOT NULL,
       AVERAGECRITICS          TEXT    NOT NULL,
       AVERAGEUSERS          TEXT    NOT NULL,
       DESCRIPTION        TEXT NOT NULL,
       PERCENTLIKEUSERS        TEXT NOT NULL,
       PERCENTLIKECRITICS        TEXT NOT NULL);''')
   
    l = extraer_datos()
    fa=l.findAll("table", class_="table")
    #fa1=fa.findAll("href",class_="unstyled articleLink")
   
    for p in fa:
        if(p.find("a",class_="unstyled articleLink") is not None):
            link=p.find("a",class_="unstyled articleLink")
            
            if(link is not None):
                fb=link['href']
                url="https://www.rottentomatoes.com"+fb
                data = BeautifulSoup(requests.get(url).content,'html.parser')
                description=data.find("meta",property="og:description")['content']
                title=data.find("h1",class_="title hidden-xs")
                year=title.find("span").getText()
                finaltitle=title.getText()[:-len(year)]
                ratings=data.find("div",class_="score_panel col-sm-17 col-xs-15")

                conn.execute("""INSERT INTO PELICULAS (YEAR,TITULO, AVERAGECRITICS, AVERAGEUSERS, DESCRIPTION, PERCENTLIKEUSERS,PERCENTLIKECRITICS) VALUES (?,?,?,?.?,?)""",(year,finaltitle,avgcritics,avgusers,description,percentusers,percentcritics))
                
    conn.commit()
    conn.close()


if __name__ == "__main__":
    almacena_peliculas()