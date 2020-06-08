import urllib.request
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


listPrice = []
listID = []
listDireccion = []
listLat = []
listLng = []
listAmb = []
listDorm = []
listBan = []
listM2 = []

df_houses = pd.DataFrame()

url = "https://www.remax.com.ar/PublicListingList.aspx#mode=gallery&tt=261&cr=2&mpts=1903&pt=1903&min=100000&max=300000&cur=USD&sb=PriceIncreasing&page=1&sc=42&rl=2528&pm=22372,22373,22379&lsgeo=2528,22372,0,0&sid=bf71c10c-307d-43ba-a4d9-a799cdb5aa7d"

driver = webdriver.Chrome()

driver.get(url)

time.sleep(10)

html = driver.page_source

soup = BeautifulSoup(html)

soup_filtered = soup.find_all("div",class_="gallery-item-container")

soup_filtered_price = soup_filtered[0].find_all("span",class_="gallery-price-main")

numero_casas = soup.find_all("span",class_="num-matches")

numero_casas = int(numero_casas[0].text.split("\xa0",1)[0])

paginas =  numero_casas/24

paginas_round = round(paginas)

if paginas > paginas_round:
    paginas_round = paginas_round + 1

for pagina in range(1,(paginas_round + 1)):
    
    
    url1 = "https://www.remax.com.ar/PublicListingList.aspx#mode=gallery&tt=261&cr=2&mpts=1903&pt=1903&min=100000&max=300000&cur=USD&sb=PriceIncreasing&page=" + str(pagina) + "&sc=42&rl=2528&pm=22372,22373,22379&lsgeo=2528,22372,0,0&sid=bf71c10c-307d-43ba-a4d9-a799cdb5aa7d"
    driver.get(url1)
    print(pagina)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html)
    soup_filtered = soup.find_all("div",class_="gallery-item-container")
        

    for item in soup_filtered:
        soup_filtered_price = item.find_all("span",class_="gallery-price-main")
        soup_filtered_id = item.get("id")
        soup_filtered_dir = item.find_all("a")[1].text
        soup_filtered_lat = item.i.get("data-lat")
        soup_filtered_lng = item.i.get("data-lng")
#         soup_filtered_amb = item.find_all("span",class_="gallery-attr-item-value")[0].text
#         soup_filtered_dorm = item.find_all("span",class_="gallery-attr-item-value")[1].text
#         soup_filtered_ban = item.find_all("span",class_="gallery-attr-item-value")[2].text
#         soup_filtered_m2 = item.find_all("span",class_="gallery-attr-item-value")[3].text
        listDireccion.append(soup_filtered_dir)
        listID.append(soup_filtered_id)    
        listPrice.append(soup_filtered_price[0].text)
        listLat.append(soup_filtered_lat)
        listLng.append(soup_filtered_lng)
        
        ambientes = ""
        dormitorios = ""
        baños = ""
        m2 = ""
        
        for i in range(len(item.find_all("img"))):
            tipo = item.find_all("img")[i].get("src")

            if tipo == "/common/images/2019/total-rooms.svg":
                ambientes = item.find_all("img")[i].get("data-original-title").split("Total de Ambientes: ")[1]
            elif tipo == "/common/images/2019/bedrooms.svg":
                dormitorios = (item.find_all("img")[i].get("data-original-title")).split("Num. de Dormitorios: ")[1]
            elif tipo == "/common/images/2019/bathrooms.svg":
                baños = (item.find_all("img")[i].get("data-original-title")).split("Baños: ")[1]
            elif tipo == "/common/images/2019/Sq-meter.svg":
                m2 = (item.find_all("img")[i].get("data-original-title")).split("Sup. Cubierta (m2)  ")[1]
                
        if ambientes != "":
            listAmb.append(ambientes)        
        elif ambientes == "":
            listAmb.append(0)            
        if dormitorios != "":
            listDorm.append(dormitorios)
        elif dormitorios == "":
            listDorm.append(0)        
        if baños != "":
            listBan.append(baños)
        elif baños == "":
            listBan.append(0)
        if m2 != "":
            listM2.append(m2)
        elif m2 == "":
            listM2.append(0)

df_houses["ID"]= listID
df_houses["Price"] = listPrice
df_houses["Direccion"] = listDireccion
df_houses["Lat"] = listLat
df_houses["Lng"] = listLng
df_houses["Ambientes"] = listAmb
df_houses["Dormitorios"] = listDorm
df_houses["Ban"] = listBan
df_houses["M2 cubiertos"] = listM2

print("Escaneo finalizado")
print(df_houses)
