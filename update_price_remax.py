import urllib.request
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


#Actualizacion de datos

df_houses_actualizado = pd.read_excel(r"C:\Users\Julian\Propiedades\remax_raw_data2.xlsx")
df_houses_actualizado = df_houses_actualizado.drop(columns="Unnamed: 0")
df_houses_actualizado = df_houses_actualizado.set_index("ID")

url_actualizacion_format = "https://www.remax.com.ar/es-ar/propiedades/capital-federal/{}"
#ID2 = "420141010-309"
#url_actualizacion = url_actualizacion.format(ID2)
#print(url_actualizacion)

driver = webdriver.Chrome()

df_houses_actualizado["New price"] = 0

for id in df_houses_actualizado.index:
    url_actualizacion = url_actualizacion_format.format(id)
    #print(url_actualizacion)
    driver.get(url_actualizacion)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html)
    soup_filtered = soup.find_all("span", itemprop = "price")
    #print(type(soup_filtered))
    if soup_filtered != []:        
        price = int(soup_filtered[0].get("content"))
        #print(id)
        #print(price)    
        df_houses_actualizado.loc[id,"New price"] = price

df_houses_actualizado["variacion"] = ((df_houses_actualizado["New price"] / df_houses_actualizado["Price"]) - 1) * 100
df_houses_actualizado_filtered = df_houses_actualizado[df_houses_actualizado["New price"] != 0]
df_houses_actualizado_filtered[df_houses_actualizado_filtered["variacion"] != 0]
print(df_houses_actualizado_filtered)
